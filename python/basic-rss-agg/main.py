import click
from contextlib import contextmanager
from flask import Flask, render_template, request, redirect, url_for, g
import feedparser
import sqlite3
import urllib.parse as urlp


DATABASE = "feed.db"
app = Flask(__name__)


@contextmanager
def ignore_table_exists(msg):
    """Silence the exception thrown when a table already exists"""
    try:
        print(msg)
        yield
    except sqlite3.OperationalError:
        print("  - already exists")


@contextmanager
def ignore_row_exists():
    """Silence the exception thrown when a row already exists"""
    try:
        yield
    except sqlite3.IntegrityError:
        print("Row already exists")


def get_db():
    """Get a handle on the database"""
    db = getattr(g, "_database", None)

    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    db.row_factory = sqlite3.Row

    return db


def query_db(query, args=(), one=False):
    """Return the result of a query as a dict"""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()

    cur.close()

    return (rv[0] if rv else None) if one else rv


def add_feed_items_to_db(feed_url, cur):
    """Get the latest items from a RSS feed and add them to the database
       Silently ignores duplicates (even if the item was read before)"""
    feed_content = feedparser.parse(feed_url)
    site = feed_content.feed.title

    for item in feed_content.entries:
        with ignore_row_exists():
            cur.execute(
                "INSERT INTO feed_items VALUES (?,?,?,?,?)",
                (site, urlp.quote(item.link), item.title, item.description, 0),
            )

    return site


@app.teardown_appcontext
def close_connection(exception):
    """Close the connection to the database at the end of each request"""
    db = getattr(g, "_database", None)

    if db is not None:
        db.close()


@app.route("/")
def index():
    """Render the index page with all the unread items"""
    for feed in query_db(""):
        add_feed_items_to_db(feed["link"], get_db().cursor())

    return render_template(
        "index.html", feed_items=query_db("SELECT * FROM feed_items WHERE read=0")
    )


@app.route("/rss")
def rss():
    """Add a (potentially) new RSS feed and all its items to the database"""
    feed_url = request.args.get("feed_url")

    db = get_db()
    cur = db.cursor()

    site = add_feed_items_to_db(feed_url, cur)

    with ignore_row_exists():
        cur.execute("INSERT INTO feeds VALUES (?,?)", (site, urlp.quote(feed_url)))

    db.commit()

    return redirect(url_for("index"))


@app.route("/read")
def read():
    """Mark an item as read and redirect to its url"""
    link = request.args.get("link")
    db = get_db()
    cur = db.cursor()

    cur.execute("UPDATE feed_items SET read=1 WHERE link=?", (urlp.quote(link),))
    db.commit()

    return redirect(link)


@app.cli.command()
def initdb():
    """Create the database"""
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    with ignore_table_exists("Create table feed_items"):
        cur.execute(
            """CREATE TABLE feed_items
                       (site text, link text UNIQUE, title text,
                        description text, read integer)"""
        )

    with ignore_table_exists("Create table feeds"):
        cur.execute("""CREATE TABLE feeds (site text, link text UNIQUE)""")

    conn.commit()
    conn.close()


@app.cli.command()
def run():
    app.run()


if __name__ == "__main__":
    app.run()

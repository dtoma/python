#!/usr/bin/env python3


from cgi import parse_header, parse_multipart
from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from subprocess import PIPE, Popen
from urllib.parse import parse_qs

INDEX_HTML = """<html>
<head><title>CppFormatter</title></head>
<body>
<textarea name="code" form="form" rows="25" cols="90">int main() {}</textarea><br/>
<form action="/" method="post" id="form">
Style:
<input type="radio" name="style" value="LLVM" checked> LLVM |
<input type="radio" name="style" value="Google"> Google |
<input type="radio" name="style" value="Chromium"> Chromium |
<input type="radio" name="style" value="Mozilla"> Mozilla |
<input type="radio" name="style" value="WebKit"> WebKit <br/>
<input type="submit" value="Submit">
</form>
</body>
</html>
"""

RESPONSE_HTML = """<html>
<head><title>CppFormatter</title></head>
<body>
<a href="/">Home</a><br/><pre>{}</pre>
</body>
</html>
"""


class CppFormatter(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(INDEX_HTML, "utf8"))
        return

    def do_POST(self):
        # Get the POST variables
        ctype, pdict = parse_header(self.headers["content-type"])
        if ctype == "multipart/form-data":
            post_vars = parse_multipart(self.rfile, pdict)
        elif ctype == "application/x-www-form-urlencoded":
            length = int(self.headers["content-length"])
            post_vars = parse_qs(self.rfile.read(length), keep_blank_values=1)

        # Run clang-format on the input, with the selected style
        code = post_vars[b"code"][0].decode("utf-8")
        style = post_vars[b"style"][0].decode("utf-8")
        command = 'echo "{}" | clang-format -style={}'.format(
            code.replace('"', '\\"'), style
        )
        p = Popen(command, shell=True, stdout=PIPE)
        formatted = p.communicate()[0].decode("utf-8")

        # Send the result back to the client
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        resp = RESPONSE_HTML.format(escape(formatted))
        self.wfile.write(bytes(resp, "utf8"))
        return


def run():
    httpd = HTTPServer(("0.0.0.0", 4242), CppFormatter)
    httpd.serve_forever()


if __name__ == "__main__":
    run()

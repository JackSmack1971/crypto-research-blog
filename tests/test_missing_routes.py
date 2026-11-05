"""Exercise custom error responses without changing the requested nested URL."""
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from html.parser import HTMLParser
from urllib.error import HTTPError
from urllib.parse import urljoin
from urllib.request import urlopen

import build


class Links(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.hrefs = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('a', 'link') and 'href' in attrs:
            self.hrefs.append(attrs['href'])


class MissingRoutesTest(unittest.TestCase):
    def test_nested_missing_routes_at_root_and_pages_project(self):
        for prefix in ('', '/crypto-research-blog'):
            with self.subTest(prefix=prefix):
                site = dict(build.load_site())

                class Host(BaseHTTPRequestHandler):
                    def do_GET(self):
                        relative = self.path.removeprefix(prefix + '/')
                        files = {
                            '': ('text/html', b'<main>All notes</main>'),
                            'design-system.css': ('text/css', build.DESIGN_SYSTEM.read_bytes()),
                            'favicon.svg': ('image/svg+xml', build.FAVICON.read_bytes()),
                            'feed.xml': ('application/rss+xml', b'<rss/>'),
                        }
                        status = 200
                        if self.path.startswith(prefix + '/') and relative in files:
                            mime, payload = files[relative]
                        else:
                            status = 404
                            mime, payload = 'text/html', build.render_404(site).encode()
                        self.send_response(status)
                        self.send_header('Content-Type', mime)
                        self.end_headers()
                        self.wfile.write(payload)

                    def log_message(self, *args):
                        pass

                server = ThreadingHTTPServer(('127.0.0.1', 0), Host)
                site['url'] = f'http://127.0.0.1:{server.server_port}{prefix}'
                thread = threading.Thread(target=server.serve_forever, daemon=True)
                thread.start()
                try:
                    missing = site['url'] + '/definitely-missing-audit/nested/'
                    with self.assertRaises(HTTPError) as caught:
                        urlopen(missing)
                    response = caught.exception
                    self.assertEqual(response.code, 404)
                    self.assertEqual(response.url, missing)
                    html = response.read().decode()
                    links = [urljoin(missing, href) for href in Links(html).hrefs
                             if not href.startswith('#')]
                    for name in ('design-system.css', 'favicon.svg', 'feed.xml', ''):
                        target = site['url'] + '/' + name
                        self.assertIn(target, links)
                        with urlopen(target) as resource:
                            self.assertEqual(resource.status, 200)
                            if name == 'design-system.css':
                                self.assertEqual(resource.headers.get_content_type(), 'text/css')
                    self.assertNotIn('/nested/design-system.css', html)
                finally:
                    server.shutdown()
                    server.server_close()
                    thread.join()

    def test_404_uses_configured_https_origin_and_project_prefix(self):
        for origin in ('https://independent-market-notes.netlify.app',
                       'https://jacksmack1971.github.io/crypto-research-blog'):
            html = build.render_404(dict(build.load_site(), url=origin))
            for path in ('', 'design-system.css', 'favicon.svg', 'feed.xml'):
                self.assertIn(origin + '/' + path, Links(html).hrefs)

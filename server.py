from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 获取 POST 请求中的数据
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(post_data)
        print(params)

        # 对请求进行处理
        # ...

        # 返回响应
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('处理成功！'.encode('utf-8'))

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), RequestHandler)
    print('开始监听 8000 端口...')
    server.serve_forever()
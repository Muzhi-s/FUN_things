from http.server import BaseHTTPRequestHandler
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        # 这里可以调用你原有的工具逻辑
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response_text = f"Serverless 函数运行成功！\n当前云端服务器时间是：{now}"
        self.wfile.write(response_text.encode())
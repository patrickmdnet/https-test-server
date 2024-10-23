import http.server
import ssl
import socket
import urllib.parse
import sys
from datetime import datetime

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    
    def handle_request(self):
        """
        Processes requests to server. Generates and sends the response.
        """
        # Construct a string representation of the request
        print(f"in handle_request: {self}")
        request_line = f"{self.requestline}\r\n"
        headers = ''.join(f"{k}: {v}\r\n" for k, v in self.headers.items())
        full_request = request_line + headers

        # Send the full request back as the response
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(f"<html><body><pre><h1><b>\r\n\r\nSource: {self.client_address[0]}\r\n\r\n{full_request}\r\n</b></h1></pre></body></html>".encode('utf-8'))

    def log_message(self, format, *args):
        """
        Logs the server output to stdout. 
        """
        # Construct and log the custom message
        current_time = datetime.now().strftime('[%d/%b/%Y %H:%M:%S]')
        client_ip = self.client_address[0]
        requested_host = self.headers['Host']
        parsed_path = urllib.parse.urlparse(self.path)
        full_url = f"https://{requested_host}{parsed_path.path}"
        if parsed_path.query:
            full_url += f"?{parsed_path.query}"
        user_agent = self.headers.get('User-Agent', '-')
        headers = ''.join(f"{k}: {v}\r\n" for k, v in self.headers.items())

        print(f"{current_time} - {client_ip} - {full_url}\r\n{self.requestline}\r\n{headers}")

    def do_GET(self):
        """
        Handles GET requests, becuase do_ALL doesn't handle them for some reason.
        """
        self.handle_request()

    def do_ALL(self):
        """
        Handles all requests for HTTP Methods other than GET
        """
        self.handle_request()

    def __getattr__(self, name):
        """
        Redirects mehods that start with do_ to do_ALL to handle all HTTP methods dynamically. 
        """
        if name.startswith('do_'):
            return self.do_ALL
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

# If a port is provided as a command-line argument, use it. Otherwise, default to 4443.
port = int(sys.argv[1]) if len(sys.argv) > 1 else 4443

hostname = socket.gethostname()
hostname = f"{hostname}.mskcc.org"
httpd = http.server.HTTPServer((hostname, port), CustomHandler)
context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
context.verify_mode = ssl.CERT_NONE
context.check_hostname = False
context.load_cert_chain(keyfile="server-key.pem", certfile="server-cert.pem")
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print(f"Server started at https://{hostname}:{port}")
while True:
    try:
        httpd.handle_request()
    except Exception as e:
        pass
        #print(f"An exception occurred: {e}")
        
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    # with context.wrap_socket(sock, server_side=True) as ssock:
        # ssock.bind(('127.0.0.1', 8443))
        # ssock.listen(0)

        # while True:
            # conn, addr = ssock.accept()
            # print(f"conn = {conn}; addr = {addr}")
            # while True:
                # data = conn.recv(1024)
                # if not data:
                    # break
                # print(f"Received: {data.decode('utf-8')}")        

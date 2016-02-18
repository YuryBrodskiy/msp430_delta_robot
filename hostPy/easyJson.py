import BaseHTTPServer
import SimpleHTTPServer

PORT = 8080
class TestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """The test example handler."""
#    def do_GET(self):
#        print "Get handle"
    def do_POST(self):
        """Handle a post request by returning the square of the number."""
        length = int(self.headers.getheader('content-length'))
        print self.headers   
        data_string = self.rfile.read(length)
        print data_string
        try:
            result = int(data_string) ** 2
        except:
            result = 'error'
        print result
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(result)

def start_server():
    """Start the server."""
    server_address = ("localhost", PORT)
    server = BaseHTTPServer.HTTPServer(server_address, TestHandler)
    server.serve_forever()

if __name__ == "__main__":
    print "Hello"
    start_server()
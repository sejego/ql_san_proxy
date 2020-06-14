
#``````````````````````TO DO LIST````````````````````````````
#------ADD IP CONFIG???
#------ADD LOGGING
#------OUTPUT IF WAS ACCESSED/WAS SENT FROM
#------ARGS TO SET IP AND PORT/ELSE DEFAULT
#------DOCKERIZE
#------MAKE CODE LOGICAL AND MORE GENERIC
#````````````````````````````````````````````````````````````

import logging
import http.server as httpsrv
import json
from sanDecode import SAN_response
_PORT_ = 4440

class requestHandler(httpsrv.BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_response()
    
    def do_POST(self):
        contentLen = int(self.headers.get('content-length'))
        response = self.rfile.read(contentLen)
        self._set_response()
        data = json.loads(response)
        SAN_response(data).sendModifiedJson('192.168.0.112', 1026)
        #SAN_response(data).test()

def main():

    server_address = ('192.168.0.112',_PORT_)     # MAKE SURE IT IS NOT LOCALHOST
    server = httpsrv.HTTPServer(server_address,requestHandler)
    print("Serving on port ", _PORT_)
    server.serve_forever()

if __name__ == '__main__':
    main()


#``````````````````````TO DO LIST````````````````````````````
#------ADD LOGGING
#------EXCEPTIONS
#------DOCKERIZE
#------MAKE CODE LOGICAL AND MORE GENERIC?
#------GET LIST OF ENTITIES?
#````````````````````````````````````````````````````````````

import logging
import sys
import http.server as httpsrv
import json
from sanDecode import SAN_response
from serverConfig import serverConfig as sc
from cleanup import cleanup

#GLOBAL VARIABLES DELCARATION

_OCB_IP_ = sc().get_ocb_ip()
_OCB_PORT_ = sc().get_ocb_port()
_PROXY_IP_ = sc().get_proxy_ip()
_PROXY_PORT_ = sc().get_proxy_port()


class requestHandler(httpsrv.BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_response()
    
    def do_POST(self):
        contentLen = int(self.headers.get('content-length'))
        response = self.rfile.read(contentLen).decode('utf-8')
        self._set_response()
        data = json.loads(response)
        SAN_response(data).sendModifiedJson(_OCB_IP_, _OCB_PORT_)
        #SAN_response(data).test()

def main():
    server_address = (_PROXY_IP_, _PROXY_PORT_)     # MAKE SURE IT IS NOT LOCALHOST
    server = httpsrv.HTTPServer(server_address,requestHandler)
    print("Serving on %s:%d" %(_PROXY_IP_,_PROXY_PORT_))
    server.serve_forever()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        cleanup(_OCB_IP_, _OCB_PORT_)
        sys.exit(1)

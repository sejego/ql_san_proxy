import json
import requests
import os

class serverConfig():
    def __init__(self):
        self.dicts = {}
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'config.json')
        with open(filename) as file:
            data = json.loads(file.read())
            for a in data:
                for b in data[a]:
                    self.dicts.update({b:data[a][b]})

    def get_ocb_ip(self):
        return self.dicts['ocb_ip']
    def get_ocb_port(self):
        return self.dicts['ocb_port']
    def get_proxy_ip(self):
        return self.dicts['proxy_ip']
    def get_proxy_port(self):
        return self.dicts['proxy_port']
    
    def test(self):
        print(self.dicts)

if __name__ == "__main__":
    serverConfig().test()

import json
import requests
from cleanup import addEntity

headers = {'Content-Type':'application/json'}

class SAN_response():
    def __init__(self, response):
        self.response = response
        self.dictOfElements = {}
    def entityModifier(self):
        for element in self.response:
            self.dictOfElements[element] = self.response[element]
        
        for elem in self.dictOfElements:
            if isinstance(self.dictOfElements[elem],list):
                for attr in self.dictOfElements[elem][0]:
                    if isinstance(self.dictOfElements[elem][0][attr], str):
                        self.dictOfElements[elem][0][attr] = self.dictOfElements[elem][0][attr] + "_ql"
                        if(str(attr) == 'id'):
                            self.modEntityId = self.dictOfElements[elem][0][attr]
                            addEntity(self.modEntityId)
                    else:
                        if self.dictOfElements[elem][0][attr]['type'] == 'string':
                            self.dictOfElements[elem][0][attr]['type'] = 'Text'
                        if self.dictOfElements[elem][0][attr]['type'] == 'array':
                            if self.dictOfElements[elem][0][attr]['value'][0]['value']['reading']['value'] is True:
                                self.dictOfElements[elem][0][attr]['value'] = 1
                            elif self.dictOfElements[elem][0][attr]['value'][0]['value']['reading']['value'] is False:
                                self.dictOfElements[elem][0][attr]['value'] = 0
                            self.dictOfElements[elem][0][attr]['type'] = 'Number'
                        else:
                            self.dictOfElements[elem][0][attr]['type'] = 'Text'
            else:
                pass

        self.jsonStripped = self.dictOfElements['data'][0]
        jsonStrippedString = json.dumps(self.jsonStripped, indent=4)
        return jsonStrippedString
    
    def entitySeparator(self):
        modEntity = self.jsonStripped
        self.dictOfAttrs = {}
        for attr in modEntity:
            if isinstance(modEntity[attr], str):
                pass
            else:
                self.dictOfAttrs.update({attr: modEntity[attr]})
        
        jsonModifiedAttr = json.dumps(self.dictOfAttrs, indent=4)
        return jsonModifiedAttr


    def sendModifiedJson(self, IP_ADDRESS, PORT):
        jsonModified = self.entityModifier()
        jsonModifiedAttr = self.entitySeparator()
        r_get = requests.get("http://"+str(IP_ADDRESS)+":"+str(PORT)+"/v2/entities/"+str(self.modEntityId))
        if r_get.status_code == 200:
            try:
                r_patch = requests.patch("http://"+str(IP_ADDRESS)+":"+str(PORT)+"/v2/entities/"
                                        +str(self.modEntityId)+'/attrs',data = jsonModifiedAttr,
                                        headers = headers)
                print('PATCH method response {}'.format(r_patch.status_code))
            except requests.exceptions.RequestException as e:
                print('FAILED WITH ERROR: '+e)
        elif r_get.status_code == 404:
            try:
                r_post = requests.post("http://"+str(IP_ADDRESS)+":"+str(PORT)+"/v2/entities/",
                                      data = jsonModified,headers = headers)
                print('POST method response {}'.format(r_post.status_code))
            except requests.exceptions.RequestException as e:
                print('FAILED WITH ERROR '+e)
        else:
            print('Different response code {}'.format(r_get.status_code))


    def test(self):
        print(self.entityModifier())
        print('--------------------------------------------------')
        print(self.entitySeparator())
        print('--------------------------------------------------')
import json
import requests
from cleanup import add_entity

headers = {'Content-Type':'application/json'}

class SAN_response():
    def __init__(self, response):
        self.response = response
        self.dictOfElements = {}

    def modify_entity(self):
        for element in self.response:
            self.dictOfElements[element] = self.response[element]

        for elem in self.dictOfElements:
            if isinstance(self.dictOfElements[elem],list):
                for attr in self.dictOfElements[elem][0]:

                    # Add postfix _ql to entity id, name

                    if isinstance(self.dictOfElements[elem][0][attr], str):
                        self.dictOfElements[elem][0][attr] = self.dictOfElements[elem][0][attr] + "_ql"

                        # add entity id to cleanup later from Orion CB    
                        
                        if(str(attr) == 'id'):
                            self.modified_entity_id = self.dictOfElements[elem][0][attr]
                            add_entity(self.modified_entity_id)
                    else:

                        # convert field types into QuantumLeap-supported ones

                        if self.dictOfElements[elem][0][attr]['type'] == 'string':
                            self.dictOfElements[elem][0][attr]['type'] = 'Text'
                        if self.dictOfElements[elem][0][attr]['type'] == 'array':
                            if self.dictOfElements[elem][0][attr]['value'][0]['value']['reading']['value'] is True:
                                self.dictOfElements[elem][0][attr]['value'] = 1
                            elif self.dictOfElements[elem][0][attr]['value'][0]['value']['reading']['value'] is False:
                                self.dictOfElements[elem][0][attr]['value'] = 0
                            else:
                                self.dictOfElements[elem][0][attr]['value'] = float(self.dictOfElements[elem][0][attr]['value'][0]['value']['reading']['value'])
                            self.dictOfElements[elem][0][attr]['type'] = 'Number'
                        else:
                            self.dictOfElements[elem][0][attr]['type'] = 'Text'
            else:
                pass

        self.jsonStripped = self.dictOfElements['data'][0]
        jsonStrippedString = json.dumps(self.jsonStripped, indent=4)
        return jsonStrippedString
    
    def separate_entity(self):
        modified_entity = self.jsonStripped
        self.dictOfAttrs = {}
        for attr in modified_entity:
            if isinstance(modified_entity[attr], str):
                pass
            else:
                self.dictOfAttrs.update({attr: modified_entity[attr]})
        
        jsonModifiedAttr = json.dumps(self.dictOfAttrs, indent=4)
        return jsonModifiedAttr


    def send_modified_json(self, IP_ADDRESS, PORT):
        jsonModified = self.modify_entity()
        jsonModifiedAttr = self.separate_entity()
        r_get = requests.get("http://"+str(IP_ADDRESS)+":"+str(PORT)+"/v2/entities/"+str(self.modified_entity_id))

        # The proxy will first check if the entity exists by querying it
        # if it exists, it will update it, otherwise it will try to
        # create it.

        if r_get.status_code == 200:
            try:
                r_patch = requests.patch("http://"+str(IP_ADDRESS)+":"+str(PORT)+"/v2/entities/"
                                        +str(self.modified_entity_id)+'/attrs',data = jsonModifiedAttr,
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
        print(self.modify_entity())
        print('--------------------------------------------------')
        print(self.separate_entity())
        print('--------------------------------------------------')
import requests 

entitiesList = []

def add_entity(entity):
    if entity not in entitiesList:
        entitiesList.append(entity)
def cleanup(ocb_ip, ocb_port):
    print('Starting cleanup')
    for entity in entitiesList:
        r_delete = requests.delete("http://"+str(ocb_ip)+":"+str(ocb_port)+"/v2/entities/"+str(entity))
        print('response code: %d' %r_delete.status_code)
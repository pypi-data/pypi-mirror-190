import os
from dotenv import load_dotenv
from nutsFetchGet import nutsFetchGet

load_dotenv()


internal_node_ip = os.environ.get("INTERNAL_NODE_IP")
internal_node_port = os.environ.get("INTERNAL_NODE_PORT")


class VendorMethods:

    def __init__(self, did):
        self.did = did


    def processTrusted(self, did):

        getData = nutsFetchGet(f'http://{internal_node_ip}:{internal_node_port}/internal/vdr/v1/did/{did}')
        resultGETdata = getData.initGetNuts()
        arr = []
        for service in resultGETdata['document']['service']:
            if service['type'] == "node-contact-info":
                arr.append(service['serviceEndpoint']['name'])

        if len(arr) > 0:
            return arr[0]


    def procesNutsComm(self, did):

        getData = nutsFetchGet(f'http://{internal_node_ip}:{internal_node_port}/internal/vdr/v1/did/{did}')
        resultGETdata = getData.initGetNuts()
        for service in resultGETdata['document']['service']:
            if service['type'] != "NutsComm":
                continue
            else:
                return service['serviceEndpoint']

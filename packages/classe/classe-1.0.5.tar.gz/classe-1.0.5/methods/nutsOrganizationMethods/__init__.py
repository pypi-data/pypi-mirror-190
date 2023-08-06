import os
from dotenv import load_dotenv
from nutsFetchGet import nutsFetchGet

load_dotenv()


internal_node_ip = os.environ.get("INTERNAL_NODE_IP")
internal_node_port = os.environ.get("INTERNAL_NODE_PORT")

class OrganizationMethods:

    def __init__(self, did):
        self.did = did



    def getVendor(self, did):

        getDIDdoc = nutsFetchGet(f'http://myhealthconnect-nuts-node-web/internal/vdr/v1/did/{did}')
        resultGETDoc = getDIDdoc.initGetNuts()
        if 'service' in resultGETDoc["document"]:
            for service in resultGETDoc['document']['service']:
                if service['type'] == "node-contact-info":
                    return service["serviceEndpoint"]["name"]

    def getTrusted(self, did):
        parsedDID = did
        getTrustedOrganizations = nutsFetchGet(
            f'http://myhealthconnect-nuts-node-web/internal/vcr/v2/verifier/NutsOrganizationCredential/trusted')
        initGetTrustedOrganizations = getTrustedOrganizations.initGetNuts()
        for care_org in initGetTrustedOrganizations:
            if care_org != parsedDID:
                continue
            else:
                return True

    def getNutsCommService(self, did):
        getServiceForVendor = nutsFetchGet(f'http://myhealthconnect-nuts-node-web/internal/vdr/v1/did/{did}')
        resultGETservice = getServiceForVendor.initGetNuts()
        if 'service' in resultGETservice["document"]:
            for service in resultGETservice['document']['service']:
                if service['type'] == "NutsComm":
                    return service["serviceEndpoint"]


    def eOverdracht_Type(self, did):
        GETeOverdrachtReceiver = nutsFetchGet(f'http://myhealthconnect-nuts-node-web/internal/vdr/v1/did/{did}')
        resultGET = GETeOverdrachtReceiver.initGetNuts()
        arrService = []
        if "service" in resultGET["document"]:
            for service in resultGET["document"]['service']:
                if service['type'] == "eOverdracht-sender" or service['type'] == "eOverdracht-receiver":
                    arrService.append(service['type'])
                else:
                    continue
        return arrService

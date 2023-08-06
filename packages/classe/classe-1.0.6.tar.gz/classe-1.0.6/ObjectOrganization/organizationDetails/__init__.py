
class Organization:

    def __init__(self, did, organizationName, organizationCity, vendor, vendorDID, NutsComm, CompoundService):
        self.did = did
        self.organizationName = organizationName
        self.organizationCity = organizationCity
        self.vendor = vendor
        self.vendorDID = vendorDID
        self.NutsComm = NutsComm
        self.CompoundService = CompoundService

    def castOrganization(self):

        OrganizationObject = {
            "did": self.did,
            "OrganizationName": self.organizationName,
            "OrganizatonCity": self.organizationCity,
            "vendorDID": self.vendorDID,
            "VendorName": self.vendor,
            "NutsComm": self.NutsComm,
            "CompoundService": self.CompoundService

        }

        return OrganizationObject

class Vendor:

    def __init__(self, VendorDID, VednorName, Trusted, NutsComm):
        self.VednorDiD = VendorDID
        self.VednorName = VednorName
        self.Trusted = Trusted
        self.NutsComm = NutsComm

    def castVendor(self):

        vendorDetails = {

            "VendorDID": self.VednorDiD,
            "VendorName": self.VednorName,
            "Trusted": self.Trusted,
            "NutsComm": self.NutsComm

        }

        return vendorDetails

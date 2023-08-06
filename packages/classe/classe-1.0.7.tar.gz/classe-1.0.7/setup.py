from setuptools import setup, find_packages

setup(
    name="classe",
    version="1.0.7",
    author="Bogdan Marcu",
    author_email="bogdan.marcu@tss-yonder.com",
    description="Classes for scripts",
    packages=["Fetch", "nutsFetchGet", "nutsPUTupdate", "nutsSendPost", "nutsOrganizationMethods", "nutsVendorMethods", "contact_info", "organizationDetails", "vendorDetails"],
    package_dir={
        "": ".",
        "Fetch": "./HttpReq/Fetch",
        "nutsFetchGet": "./HttpReq/nutsFetchGet",
        "nutsPUTupdate": "./HttpReq/nutsPUTupdate",
        "nutsSendPost": "./HttpReq/nutsSendPost",
        "nutsOrganizationMethods": "./methods/nutsOrganizationMethods",
        "nutsVendorMethods": "./methods/nutsVendorMethods",
        "contact_info": "./ObjectOrganization/contact_info",
        "organizationDetails": "./ObjectOrganization/organizationDetails",
        "vendorDetails": "./ObjectOrganization/vendorDetails"
    }
)

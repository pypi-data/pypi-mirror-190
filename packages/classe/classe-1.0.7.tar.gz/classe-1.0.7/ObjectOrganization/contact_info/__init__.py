class ContactInfo:

    def __init__(self, name, phone, email, website):

        self.name = name
        self.phone = phone
        self.email = email
        self.website = website

    def castContactInfo(self):

        contactInfoObject = {

            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "website": self.website

        }

        return contactInfoObject

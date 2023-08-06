from Fetch import Fetch

class nutsSendPost(Fetch):

    def __init__(self, path, body):
        super()
        self.path = path
        self.body = body

    def initPostNuts(self):
        return Fetch.sendDataPost(self, self.path, self.body)

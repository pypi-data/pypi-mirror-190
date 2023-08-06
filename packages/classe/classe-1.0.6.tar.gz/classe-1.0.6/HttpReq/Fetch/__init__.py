import requests
import json

class Fetch:

    def fetchDataGet(self, path):
        response = requests.get(path)
        data = response.json()
        return data

    def sendDataPost(self, path,  body):
        response = requests.post(path, json.dumps(body, separators=(',', ':')), headers={
            "Content-Type": "application/json;charset=UTF-8"
        })
        if len(response.content) > 0:
            data = response.json()
            return data
        else:
            return "204 Succes No content"

    def updateDataPut(self, path, data):
        response = requests.put(path, data)
        data = response.json()
        return data

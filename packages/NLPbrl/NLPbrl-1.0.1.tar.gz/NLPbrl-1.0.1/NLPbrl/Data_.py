import requests
import configparser
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
class Data():
    def __init__(self):
        file = 'NLPbrl/config.ini'
        con = configparser.ConfigParser(allow_no_value=True)
        con_file = con.read(file, encoding='utf-8')
        sections = con.sections()
        self.headers = {
            "content-type": "application/json",
            "X-RosetteAPI-Key": con.items(sections[0])[0][0],
            "X-RapidAPI-Key":
            con.items(sections[1])[0][0],
            "X-RapidAPI-Host": con.items(sections[2])[0][0]
        }
        self.payload = {}

    def get_token(self, text):
        self.payload = {}
        url = "https://rosetteapi-rosette-v1.p.rapidapi.com/tokens"
        self.payload['content'] = text
        response = requests.request("POST",
                                    url,
                                    json=self.payload,
                                    headers=self.headers)
        return eval(response.text)['tokens']

    def get_lang(self, text):
        self.payload = {}
        url = "https://api.rosette.com/rest/v1/language"
        self.payload['content'] = text
        response = requests.request("POST",
                                    url,
                                    json=self.payload,
                                    headers=self.headers)
        return eval(response.text)["languageDetections"][0]['language']

    def get_vec(self, text):
        self.payload = {}
        url = "https://api.rosette.com/rest/v1/semantics/vector"
        self.payload['content'] = text
        self.payload['options'] = {"perToken": True}
        response = requests.request("POST",
                                    url,
                                    json=self.payload,
                                    headers=self.headers)
        return {
            'documentEmbedding': eval(response.text)['documentEmbedding'],
            'tokenEmbeddings': eval(response.text)['tokenEmbeddings']
        }

    def get_posTag(self, text):
        self.payload = {}
        null = ''
        url = "https://rosetteapi-rosette-v1.p.rapidapi.com/morphology/complete"
        self.payload['content'] = text
        response = requests.request("POST",
                                    url,
                                    json=self.payload,
                                    headers=self.headers)

        return {
            "tokens": eval(response.text)["tokens"],
            "posTags": eval(response.text)["posTags"]
        }

    def get_senTag(self, text):
        self.payload = {}
        url = "https://api.rosette.com/rest/v1/sentences"
        self.payload['content'] = text
        response = requests.request("POST",
                                    url,
                                    json=self.payload,
                                    headers=self.headers)
        return eval(response.text)['sentences']
    
    def get_relation(self, text):
        self.payload = {}
        url = "https://api.rosette.com/rest/v1/relationships"
        self.payload['content'] = text
        response = requests.request("POST",
                                    url,
                                    json=self.payload,
                                    headers=self.headers)
        return eval(response.text)['relationships']

    def get_classification(self, text):
        self.payload = {}
        url = "https://api.rosette.com/rest/v1/categories"
        self.payload['content'] = text
        response = requests.request("POST",
                                    url,
                                    json=self.payload,
                                    headers=self.headers)
        return eval(response.text)["categories"]
from bs4 import BeautifulSoup
import requests

class test:
    def __init__(self):
        URL = 'https://www.verywellfamily.com/top-1000-baby-boy-names-2757618'
        content = requests.get(URL)

        soup = BeautifulSoup(content.text, 'html.parser')

        list_of_names = soup.find("ol").find_all("li")

        for name in list_of_names:
            print(name.text)

class groupRoom:
    def __init__(self):
        self.session = requests.Session()

    def login(self, username, password):

        payload = {
            "UserName": str(username) + "@net.chalmers.se",
            "Password": str(password),
            "AuthMethod": "FormsAuthentication"
        }

        response = self.session.post("https://idp.chalmers.se/adfs/ls/?SAMLRequest=fZLLTsMwEEX3%2FQrL%2B8RpRAFZTVFphCjiEdHwEBtkkim1cOzgmfD4e5xApUpI9dIezz0%2B4%2BnJV2PYB3jUzmZ8HCecga1cre1rxu%2FKs%2BiYs5PZaIqqMa2cd7Sxt%2FDeARILNy3K4SDjnbfSKdQorWoAJVVyNb%2B6lGmcyNY7cpUznC2xUIj6AzK%2BVgaBszx00lbREL8halEKoes2rjbKNIErRhCqXqMwKDi735KmPWnx1%2FhU21%2FgfRQvv0Uoz8uyiIqbVRl48ow%2Fv5ZHvm7emnHe5e1k8fiwefxcX%2BDF6nbVE2MHS4ukLIXUJE2icRKlh%2BX4UB6kMp08cXbmfAWDmu2zZiMW1iBNDh38jq39mMEP%2BF4Hn211IMSkG4BaU2yBxFZNhG1Ewd9U7ATtRLfyOrRf5oUzuvruMRtF%2B9P7HV1H66FUklcWNVjibG6M%2B1x4UBRmR74LoxPhW4j%2F%2F2I2%2BgE%3D&RelayState=", data=payload)
        print(response.status_code)

    def get_rooms(self, search=""):
        
        rooms_page = self.session.get("https://cloud.timeedit.net/chalmers_test/web/b1/objects.json?max=100&fr=f&part=t&partajax=t&im=f&step=1&sid=1004&l=sv_SE&types=186&subtypes=186&search_text=")

        result = []

        for room in rooms_page.json()["objects"]:
            result.append({
                "id": room["id"],
                "name": room["fields"]["Lokalsignatur"],
                "idAndType": room["idAndType"] 
            })

        return result

account = groupRoom()
account.login("kanjom", "*****")
account.get_rooms()





import requests, time, sys, pickle, json
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class GroupRoomBooker:

    def __init__(self):
        self.session = requests.Session()

        self.rooms = []

        self.session.headers.update({
            "User-Agent":
                "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36",
        })

    def getRoomID(self, name):
        if len(self.rooms) == 0:
            self.get_rooms()

        for room in self.rooms:
            if room["name"] == name:
                return room
        return None


    def load(self, file):
        with open(file, 'rb') as f:
            self.session.cookies.update(pickle.load(f))

    def save(self, file):
        with open(file, 'wb') as f:
            pickle.dump(self.session.cookies, f)

    def login(self, username, password):

        main = self.session.get("https://cloud.timeedit.net/chalmers_test/web/b1/")
        soup = BeautifulSoup(main.text, features="html.parser")
        login = soup.find(id="logincontrol").find("a")

        login_page = self.session.get(login['href'])
        loginSoup = BeautifulSoup(login_page.text, features="html.parser")
        form = loginSoup.find(id="loginForm")

        login_url = "https://" + urlparse(login_page.url).netloc + form["action"]
        login = self.session.post(
            login_url,
            data={
                "UserName": username + "@net.chalmers.se",
                "Password": password,
                "AuthMethod": "FormsAuthentication"
            },
            allow_redirects=True
        )

        resultSoup = BeautifulSoup(login.text, features="html.parser")

        try:
            return True, resultSoup.find(id="errorText").text

            sys.exit(1)
        except Exception as e:
            print("OK")
        print (login.status_code)

        #booking = session.get("https://cloud.timeedit.net/chalmers_test/web/b1/my.html?i=105659575006QQ50ZW606005y0")


        action_url = resultSoup.find("form", {"name": "hiddenform"})["action"]

        SAMLResponse = resultSoup.find("input", {"name": "SAMLResponse"})["value"]

        saml_req = self.session.post(action_url, data={"SAMLResponse": SAMLResponse})

        print(saml_req.status_code)

    def get_booking_page(self):
        page = self.session.get("https://cloud.timeedit.net/chalmers_test/web/b1/")
        soup = BeautifulSoup(page.text, features="html.parser")
        next_url = soup.find("div", {"class": "leftlistcolumn"}).find("a")["href"]

        next_fullurl = "https://" + urlparse(page.url).netloc + next_url

        res = self.session.get(next_fullurl)
        open("output.html","w+").write(res.text)

    def my_bookings(self):
        page = self.session.get("https://cloud.timeedit.net/chalmers_test/web/b1/my.html?so=0&p=0.d,0.d&max=5&part=t")
        soup = BeautifulSoup(page.text, features="html.parser")

        rooms = []

        for item in soup.find_all("tr")[2:]:
            rawdate = item.find_all("td")[1].text
            date, time = rawdate.split(" \xa0 ")

            name = item.find_all("td")[2].text.split(",")[0]
            rooms.append({
                "name": name,
                "date": date,
                "time": time
            })
        return rooms
    def get_rooms(self, search=""):
        page = self.session.get("https://cloud.timeedit.net/chalmers_test/web/b1/objects.json?max=100&fr=f&part=t&partajax=t&im=f&step=1&sid=1004&l=sv_SE&types=186&subtypes=186&search_text=" + search)

        output = []
        for item in page.json()["objects"]:
            output.append({
                "id": item["id"],
                "name": item["fields"]["Lokalsignatur"],
                "idAndType": item["idAndType"]
            })
        self.rooms = output
        return output
    
    def book(self, date, roomID, startTime, endTime):
        page = self.session.post(
            
            #"https://httpbin.org/post",
            "https://cloud.timeedit.net/chalmers_test/web/b1/ri1Q5008.html",
            data={
                "kind": "reserve",
                "nocache": "4",
                "l": "sv_SE",
                "o": [roomID, "203460.192"],
                "aos": "",
                "dates": date,
                "starttime": startTime,
                "endtime": endTime,
                "url": "https://cloud.timeedit.net/chalmers_test/web/b1/ri1Q5008.html",
                "fe2": "",
                "fe8": ""
            },
            allow_redirects=True
        )
        return page.text

#open("output.html","w+").write(saml_req.text)


password = "open("chalmers.password").read()"


booker = GroupRoomBooker()
booker.login("albinfal", password)

booker.load("albinfal.cookie")


print(booker.get_rooms())

room = booker.getRoomID("M1205")

print(booker.book("20201101", room["idAndType"], "15:00", "16:00"))

for booking in booker.my_bookings():
    print(booking)

#data = booker.get_booking_page()
#
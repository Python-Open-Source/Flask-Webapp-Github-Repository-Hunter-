__Author__ = "Soumil Nitn Shah"
__Version__ = '0.0.1'
__Email__ = "shahsoumil519@gmail.com"
__Website__ ="https://www.soumilshah.herokuapp.com"



try:
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
except Exception as e:
    print("Some Modules are Missing {}".format(e))


class Request(object):

    def __init__(self, url = 'https://github.com/soumilshah1995?tab=repositories'):
        self.url = url
        self.headers = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'http://www.wikipedia.org/',
            'Connection': 'keep-alive',
        }


    def get(self):
        """

        :return: Response
        """
        try:

            r = requests.get(url=self.url, headers = self.headers)
            return r

        except Exception as e:

            print("Failed to make response ")


class HashMap(object):

    def __init__(self):
        self.data = {
            'RepoName':[],
            'url':[],
            'No':[]
        }


class GithubHunter(object):

    def __init__(self, username= '', pages=5):

        self.username = username
        self.url = "https://github.com/"+self.username+"?tab=repositories"
        self.resp = Request(self.url)
        self.soup = self.createSoup()
        self.datastructure = HashMap()
        self.pages = pages

    def createSoup(self):
        soup = BeautifulSoup(self.resp.get().text, 'html.parser')
        return soup

    def getToken(self, soup):
        """
        Gets the Next Page Token
        :return: Url
        """
        token = soup.findAll('div', class_='BtnGroup')
        for x in token:
            for y in x.findAll('a', class_="btn btn-outline BtnGroup-item"):
                return y["href"]


    def getData(self, soup):

        li = soup.findAll('div', class_='d-inline-block mb-1')

        base_url = "https://github.com/"

        # Page 1 Scrapper
        for _, i in enumerate(li):
            for a in i.findAll('a'):
                newUrl = base_url + a["href"]

            self.datastructure.data["No"].append(_)
            self.datastructure.data["RepoName"].append(i.text.strip())
            self.datastructure.data["url"].append(newUrl)

    def run(self):

        # Get the Token for Next page
        token = self.getToken(self.soup)

        # scrape Page 1
        self.getData(self.soup)

        tem = ''
        for i in range(1,self.pages):
            try:
                if i==1:
                    r = requests.get(url=token)
                    data = r.text
                    soup = BeautifulSoup(data, 'html.parser')
                    token = self.getToken(soup)
                    self.getData(soup)
                    tem = token

                else:
                    r = requests.get(url=tem)
                    data = r.text
                    soup = BeautifulSoup(data, 'html.parser')
                    token = self.getToken(soup)
                    self.getData(soup)
                    tem = token

            except Exception as e:
                pass

        data = list(zip(self.datastructure.data["RepoName"],
                        self.datastructure.data["url"]))
        df = pd.DataFrame(data=data, columns=["Repo Name", "url"])

        print("Hunt Complete ....... ")
        return df


    def createCSV(self):

        data = list(zip(self.datastructure.data["RepoName"],
                        self.datastructure.data["url"]))
        df = pd.DataFrame(data=data, columns=["Repo Name", "url"])
        print(df)
        df.to_csv("Repo.csv")

    def saveExcel(self):

        data = list(zip(self.datastructure.data["RepoName"],
                        self.datastructure.data["url"]))
        df = pd.DataFrame(data=data, columns=["Repo Name", "url"])
        print(df)
        df.to_excel("Repo.xls")

    def saveJson(self):

        data = list(zip(self.datastructure.data["RepoName"],
                        self.datastructure.data["url"]))
        df = pd.DataFrame(data=data, columns=["Repo Name", "url"])
        print(df)
        df.to_json("Repo.json")


# if __name__ == "__main__":
#     hunter = GithubHunter(username = "dathu", pages=2)
#     df = hunter.run()
#     print(df)


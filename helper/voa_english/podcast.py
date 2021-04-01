from bs4 import BeautifulSoup
import json
import requests
import urllib.request
import os


class ParseData:
    dirName = ""
    allData = {}
    tempData = {}
    errorData = {}
    currentIter = 0
    totalIter = 0
    mainIter = 0

    """


    """

    def read_link_data(self):
        self.errorData['error'] = []
        with open('links.json', 'r') as outfile:
            data = json.load(outfile)
        datas = data["data_link"]
        for i in range(len(datas)):
            self.mainIter = i + 1
            print(i+1, "."+" Started ")
            self.dirName = str(i+1)
            if not os.path.exists(self.dirName):
                os.mkdir(self.dirName)

            self.main_parse_site(datas[i]["link"], i+1)

    """
    
    """

    def main_parse_site(self, site_link, level):

        r = requests.get(site_link)
        soup = BeautifulSoup(r.text, 'html.parser')
        results = soup.find_all(
            'li', attrs={'class': 'col-xs-12 col-sm-6 col-md-6 col-lg-6'})
        self.allData["learnenglish"] = []
        for i in range(len(results)):
            try:
                temp = "https://learningenglish.voanews.com" + \
                    results[i].find('a')['href']
                self.currentIter = i + 1
                self.tempData[self.currentIter] = []
                data = self.child_parse_site(temp)
                self.create_json_file(data, "data/podcast_voa-2.json")
                self.printProgressBar(self.currentIter, len(results), prefix=str(
                    self.mainIter)+". Unit ", suffix='Complete', length=50)
            except Exception as exx:
                self.errorData['error'].append({"errorCode": str(exx)})
                print("HATA "+str(exx))
               # self.createJSONFile(self.errorData,"data/error_data.json")

    def child_parse_site(self, site_link):

        link = ""
        title = ""
        dialog = ""

        r = requests.get(site_link)
        soup = BeautifulSoup(r.content, 'html5lib')
        mp3_links = soup.find_all('div', attrs={'class': 'c-mmp__player'})
        pg_title = soup.find('div', attrs={'class': 'pg-title'})

        title = pg_title.text.strip()
        dialog = self.get_conv(soup)

        for i in range(len(mp3_links)):
            temp_found_link = mp3_links[i].find('audio')
            if temp_found_link != None:
                link = temp_found_link['src']
        self.tempData[self.currentIter].append({
            "title": title,
            "link": link,
            "dialog": dialog
        })

        return self.tempData

    def get_conv(self, soup):
        span = soup.find('div', attrs={'class': 'wsw__embed'})
        span.extract()
        span = soup.find('div', attrs={'class': 'wsw__embed'})
        span.extract()

        sonuc = soup.find_all('div', attrs={'class': 'wsw'})

        for i in range(13):
            if sonuc[0].find('h2', attrs={'class': 'wsw__h2'}) != None:
                span = sonuc[0].find('h2', attrs={'class': 'wsw__h2'})
                span.extract()

        #f=open("dene3.html", "a+")
        #f.write(''.join(str(e.text) for e in sonuc))

        #sonuc = sonuc.find_all('div',attrs={'class':'wsw'})

        return sonuc[0].text

    def getConversation(self, soup):
        main_div = soup.find(
            'div', attrs={'class': 'content-floated-wrap fb-quotable'}).findChildren('div')
        child_tag = main_div[0].findChildren()
        extract = False
        _conv = []
        for j in range(len(child_tag)):
            if child_tag[j].name == "span":
                if child_tag[j].text == "Pop-out player":
                    extract = True

            elif child_tag[j].name == "h2":
                if child_tag[j].text == "Writing":
                    extract = False
            if extract:
                if child_tag[j].text.strip() != "" and child_tag[j].text.strip() != None:
                    print(child_tag[j].text.strip())
                    _conv.append(child_tag[j].text.strip())
        return _conv

    """
    
    """

    def download(self, url, file_name):
        print("indirmeye basladi")
        with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
            data = response.read()  # a `bytes` object
            out_file.write(data)
        print("indirmeye bitti")

    def create_json_file(self, data, temp_dirName):
        with open(temp_dirName, 'w') as outfile:
            json.dump(data, outfile, indent=4)

    def printProgressBar(self, iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                         (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' %
              (prefix, bar, percent, suffix), end=printEnd)
        # Print New Line on Complete
        if iteration == total:
            print()

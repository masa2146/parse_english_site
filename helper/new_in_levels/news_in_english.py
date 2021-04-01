from bs4 import BeautifulSoup
import json
import requests
import urllib.request
import os

class ParseData:
    """
    This aim of class is parse web page content adress by url
    @author: 
        Fatih Bulut
    """
    temp_data   = {}
    data        = {}
    startIndexProgress = 0
    total_iteration = 1
    tempErrorData   = {}
    errorData       = {}
    cache_download  = {}
    all_download  = {}
    pg_number = 122

    def read_link_data(self):
        """
        This function read links.json file where in the same folder 
        After, extract link which it will be parse content
        """
        self.data['news']        = []
        self.errorData["errors"] = []
        self.cache_download["last_download"] = []
        self.all_download["all_downloads"] = []
        with open('links.json', 'r') as outfile:
            data = json.load(outfile)
        datas = data["data_link"]
        print("--- Started ---")

        PAGE_NUMBERS =300
        self.startIndexProgress = 0
        self.total_iteration = len(datas) * (PAGE_NUMBERS)

        for page_number in range(PAGE_NUMBERS):
            self.pg_number+=1
            for i in range(len(datas)):
                self.main_parse_site(datas[i]["link"].replace('PAGE_NUMBER',str(page_number+1)))

    def main_parse_site(self,site_link):
        """
        Parse to main page of site and extract news links.
        """
        r = requests.get(site_link)
        soup = BeautifulSoup(r.text,'html.parser')
        main_links = soup.find_all('div',attrs={'class':'fancy-buttons'})
       

        for i in range(len(main_links)):
            a_hrefs = main_links[i].find_all('a')
            tempFirstIter = len(a_hrefs) * len(main_links) * self.total_iteration

            for a_index in range(len(a_hrefs)):
                new_link = a_hrefs[a_index]['href']
                self.printProgressBar(self.startIndexProgress + 1, tempFirstIter, prefix = 'Progress:', suffix = 'Complete', length = 50)
                self.parse_news(new_link,a_index+1,site_link)
                self.startIndexProgress+=1
               
            self.data["news"].append(self.temp_data)
            self.temp_data = {}
            if bool(self.tempErrorData) == True:
                self.errorData["errors"].append(self.tempErrorData)
                self.tempErrorData = {}
            
            

        self.createJSONFile(self.data,"data/newsData.json")
        if bool(self.errorData) == True:
            self.createJSONFile(self.errorData,"data/error_data.json")


   
    def parse_news(self,news_link,index,site_link):
        """
        Parse news link by content text, video url, content image and content title \r\n
        @params: 
            news_link - Required : News url adress (Str)
            index     - Required :  Declare of level chapter (Int)
        """
        try:
            self.temp_data["level_"+str(index)] = []
            r    = requests.get(news_link)
            soup = BeautifulSoup(r.text,'html.parser')

            content_title = soup.find('div',attrs={'class':'article-title'}).get_text()
            content       = soup.find('div',attrs={'id':'nContent'}).get_text()
            content_image = soup.find('div',attrs={'class':'upper-content'}).find('div',attrs={'class':'img-wrap'}).find('a')['href']
            content_video = "https:"+soup.find('div',attrs={'class':'article-lower'}).find('iframe')['src']

            self.temp_data["level_"+str(index)].append({
                "title"      :content_title,
                "content"    :content,
                "video_link" :content_video,
                "video_image":content_image
                })
            self.cache_download["last_download"] = {"last_pageNumber":self.pg_number,
                                                    "last_url":news_link,
                                                    "last_level":index
                                                    
                                                    }
            self.all_download["all_downloads"].append({
                                                    "downloaded_pageNumber":self.pg_number,
                                                    "downloaded_url":news_link,
                                                    "downloaded_content_title":content_title,
                                                    "downloaded_level":index
            })
            self.createJSONFile(self.all_download,"data/all_download.json")
            self.createJSONFile(self.cache_download,"data/cache.json")
                            
        except Exception as ex:
            self.tempErrorData["error_"+str(self.startIndexProgress)] = []
            self.tempErrorData["error_"+str(self.startIndexProgress)].append({
                "link"         :news_link,
                "error_detail" :str(ex).replace('"',"'")
            })

    def createJSONFile(self, data,temp_dirName):
        """
        This method creates the json file based on the data and file name \r\n
        @params:
            data         - Required : This variable is contain json data (dict)
            temp_dirName - Required : This variable is json file name (Str)
        """
        with open(temp_dirName, 'w') as outfile:
            json.dump(data, outfile, indent=4)

    def printProgressBar (self,iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
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
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
        # Print New Line on Complete
        if iteration == total: 
            print()

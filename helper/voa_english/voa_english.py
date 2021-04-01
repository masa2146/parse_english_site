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
from prettytable import PrettyTable
import json
from argparse import ArgumentParser, SUPPRESS
import requests
from bs4 import BeautifulSoup as bs 
import os
from prettytable import PrettyTable
from collections import OrderedDict


class Clr:
    RESET = '\033[39m'
    Green = '\033[32m'
    Yellow = '\033[33m'
    RED = '\033[31m'
    White = '\033[37m'



try :
    import requests
except ImportError :
    print("Please Download The requierments : pip install -r oussama_requires.txt")

def analyze(url):
        
    atatos_SH = "https://securityheaders.com/?q={0}"

    data = {}
    api_url = atatos_SH.format(url)
    rep = requests.get(api_url).text
    soup = bs(rep,"html.parser")
    host_name = soup.find_all("th", class_ = "tableLabel", string="Site:")[0].find_next_sibling("td").text.strip()
    host_ip = soup.find_all("th", class_ = "tableLabel", string="IP Address:")[0].find_next_sibling("td").text.strip()
    security_grade =  soup.find_all("th", class_ = "tableLabel", string="Warning:")[0].find_next_sibling("td").text.strip()
    data["Host Name"],data["Host IP"] = host_name,host_ip
    data["Grade"] = security_grade[16]

    headers = OrderedDict()
    for header, value in get_report("Raw Headers",soup) :
        headers[header] = {
                "rating" : "info",
                "value" : value
            }
        

    raw_headers = soup.find_all("th",class_ = "tableLabel", string="Headers:")[0].find_next_sibling("td").find_all("li")
    for h in raw_headers :
        rating = 'good' if 'green' in h['class'] else 'bad'
        if h.text not in headers :
            headers[h.text] = {}
        headers[h.text]["rating"] = rating
        
    for header, value in get_report("Missing Header",soup):
        headers[header]["description"] = value
    
    for header, value in get_report("Additional Information", soup):
        headers[header]["description"] = value

    data['headers'] = headers

    return data




def get_report(title,soup):
    try : 
        report_body = soup.find_all("div",class_ = "reportTitle",string = title)[0].find_next_sibling("div")
    except IndexError :
        return []
    else :
        report_th = (x.text for x in report_body.select("table tbody tr th"))
        report_td = (x.text for x in report_body.select("table tbody tr td"))
        return zip(report_th,report_td)




        

        


        

            





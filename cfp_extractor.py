# -*- coding: utf-8 -*-
"""cfp_extractor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DQtNx7Vso5dHCAEc6EbI6f0bOhGP3U86
"""

import requests
import time, json 
from bs4 import BeautifulSoup
import nltk 
import os

nltk.download("punkt")
nltk.download('averaged_perceptron_tagger')

from nltk import pos_tag, word_tokenize,sent_tokenize

def cfp_extract(entry_url): #entry url is "/CFP/26108", "/CFP/26129", etc. 
    rawText = ""
    
    cfp_entry_dict = {}

    entry_html = "https://www.cfplist.com{}".format(entry_url)
    entry_response = requests.get(entry_html)

    entry_soup = BeautifulSoup(entry_response.content, "html.parser")
    content = entry_soup.find("div", {"class" : "entry"})

    #Title 
    title_block = content.find_all("a", {"class" : "titleLink"})
    title = title_block[0].text

    cfp_entry_dict['title'] = title

    #Location 
    location_block = content.find_all("h5", {"class" : "text-muted"})

    if len(location_block) == 0: #Tag not found, none 
        location = "NA"
    else:
        location = (location_block[0].text)
    
    cfp_entry_dict['location'] = location

    #Organization, contains info about location as well 

    organization_block = content.find_all("h6", {"class" : "text-muted"})

    if len(organization_block) == 0: #Tag not found, none 
        organization = "NA"
    else:
        organization = (organization_block[0].text)

    cfp_entry_dict['organization'] = organization

    #Conference Date 

    conference_date_block = content.find_all("span", {"class" : "badge badge-primary eventBox"})

    if len(conference_date_block) == 0: #Tag not found, none 
        conference_date = "NA"
    else:
        conference_date = (conference_date_block[0].text.strip())

    cfp_entry_dict['conference_date'] = conference_date
    #Submission Deadline 

    submission_date_block = content.find_all("span", {"class" : "badge badge-primary deadlineBox"})

    if len(submission_date_block) == 0: #Tag not found, none 
        submission_date = "NA"
    else:
        submission_date = (submission_date_block[0].text.strip())

    cfp_entry_dict['submission_date'] = submission_date

    #Description info
    description = ""

    description_block = content.find_all("p")

    for text in description_block[1:-1]:
        description += text.text + "\n"

    cfp_entry_dict['description'] = description

    #Append every info 
    rawText += title + "\n" + location + "\n" + organization + "\n" + conference_date + "\n" + submission_date + "\n" + description + "\n"

    #Add cfp_dict to cfp_json
    cfp_json.append(cfp_entry_dict)

    return rawText

cfp_data = []
cfp_json = []

for x in range(1,20):
    url = "https://www.cfplist.com/_CFPList?category=&page={}&query=&sortBy=CID#".format(x)
    print(url)
    response = requests.get(url)
    #print(response)
    soup = BeautifulSoup(response.content, "html.parser")

    entry_hrefs = soup.find_all("a", {"class" : "titleLink"})

    #print(entry_hrefs)
    for entry in entry_hrefs:
        href = entry['href']
        #print(href)
        rawText = cfp_extract(href)
    
        cfp_data.append(rawText)

print(len(cfp_data))
print(len(cfp_json))

cfp_json_obj = json.dumps(cfp_json)
with open("cfp_events.json", "w") as outfile: 
    outfile.write(cfp_json_obj)


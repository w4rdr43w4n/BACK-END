import requests
import json
import csv
import os
from urllib.parse import urlparse, ParseResult
from bs4 import BeautifulSoup

springer_api_key = "2498a3119bec21389fd480eb1610d3ae"


class Springer_Article:
    def __init__(self, records={}):
        self.records = records
        if "creators" in records:
            self.creators = records["creators"]
        else:
            self.creators = "N/A"
        self.title = records["title"]
        self.journal = records["publicationName"]
        self.date = records["publicationDate"]
        self.citesnumber = "N/A"
        if "p" in records["abstract"]:
            self.abstract = records["abstract"]["p"]
        else:
            self.abstract = "N/A"
        self.full_text = None

    def author(self):
        name_lst = []
        if self.creators == "N/A":
            combine_name = "N/A"
        else:
            for i in self.creators:
                name_lst.append(i["creator"])
            combine_name = ", ".join(name_lst)
        return combine_name

    def significant(self):
        # sentences_lst = self.abstract.split('.')
        for s in self.abstract:
            if "significan" in s or "associat" in s:
                return s
        return "None"

    def conclusion(self):
        # sentences_lst = self.abstract.split('.')
        for s in self.abstract:
            if "conclu" in s:
                return s
        return "None"

    def suggest(self):
        # sentences_lst = self.abstract.split('.')
        for s in self.abstract:
            if "suggest" in s:
                return s
        return "None"

    def get_doi(self):
        if "doi" in self.records:
            return self.records["doi"]
        else:
            return None

    def get_full_text(self):
        conts = {}
        doi = self.get_doi()
        if doi:
            url = f"http://api.springernature.com/openaccess/json?q=doi:{doi}&api_key={springer_api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
            if "records" in data and len(data["records"]) > 0:
                record = data["records"][0]
                if "url" in record:
                    for url_info in record["url"]:
                        pdf_url = url_info["value"]
                        conts["PDF URL"] = pdf_url
                        conts["contentType"] = record["contentType"]
            return conts


base_url_springer = "http://api.springernature.com/openaccess/json"
url_params_springer = {}
url_params_springer["api_key"] = springer_api_key
url_params_springer["p"] = 200
url_params_springer["q"] = "title: Robotics"
url_params_springer["date-facet-mode"] = "between"
url_params_springer["date"] = "2017-01-01 TO 2019-12-31"
url_params_springer["facet"] = "language"
url_params_springer["facet-language"] = "nl"
url_params_springer["facet"] = "content-type"
url_params_springer["facet-content-type"] = "Article" # Adjusted to only retrieve articles
d_springer = requests.get(base_url_springer, params=url_params_springer)
json_content = d_springer.json()

with open("springer_abstract.txt", "w") as fr_springer:
    json.dump(json_content, fr_springer)
# try:
article_insts2 = [Springer_Article(records) for records in json_content["records"]]
# except:
# for i in json_content['records']:
# print(i)
print(len(article_insts2))

titlelst2 = [i.title for i in article_insts2]
authorlst2 = [i.author() for i in article_insts2]
journallst2 = [i.journal for i in article_insts2]
datelst2 = [i.date for i in article_insts2]
citeslst2 = [i.citesnumber for i in article_insts2]
abstractlst2 = [i.abstract for i in article_insts2]
significantlst2 = [i.significant() for i in article_insts2]
conclusionlst2 = [i.conclusion() for i in article_insts2]
suggestlst2 = [i.suggest() for i in article_insts2]
# full_textlst2 = [i.full_text for i in article_insts2]
headers = {
    'x-api-key': 'ask_091df11bd8bb8d924465b10e464ffffe'
}
prompts = []

for article in article_insts2:
    s = article.get_full_text()
    w = s["PDF URL"]
    try:
      response = requests.get(w)
    except:
        continue
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        #file_nam = article.title[:3] + ".txt"

            # Write the full text to the text file
        #with open(file_nam, "wb") as fil:
                     #fil.write(response.content)
        try:
            html_url = soup.find("meta", {"name": "citation_fulltext_html_url"})[
                "content"
            ]
            try:
                pdf_file_path = (
                   soup.find("body")
                  .find("div", class_=lambda x: x and x.startswith("c-pdf-download"))
                .find("a", href=True)["href"]
                            )
             # pdf_file_path = (
                # soup.find("body")
                 #.find("div", class_="c-pdf-download u-clear-both u-mb-16")
                 #.find("a", href=True)["href"]
           #  )
              
            except:
                  file_nam = article.title[:3] + ".txt"

            # Write the full text to the text file
                  with open(file_nam, "wb") as fil:
                               fil.write(response.content)
                #try:
                     #pdf_file_path = (
                     #soup.find("body")
                      #.find("div", class_="c-pdf-download u-clear-both")
                       #.find("a", href=True)["href"]
                            #)
                     
                #except:
                      #pdf_file_path = (
                    # soup.find("body")
                      #.find("div", class_="c-pdf-download u-clear-both js-pdf-download")
                       #.find("a", href=True)["href"]
                            #)
                      #file_nam = article.title[:3] + ".txt"

            # Write the full text to the text file
                      #with open(file_nam, "wb") as fil:
                               #fil.write(response.content)
            parsed_html_url: ParseResult = urlparse(html_url)
            # ParseResult(
            #     scheme="https",
            #     netloc="link.springer.com",
            #     path="/article/10.1007/s40329-014-0062-0",
            #     params="",
            #     query="",
            #     fragment="",
            # )

            print(parsed_html_url.geturl())
            print(pdf_file_path)
            full_pdf_url = (
                f"{parsed_html_url.scheme}://{parsed_html_url.netloc}{pdf_file_path}"
            )
            print(full_pdf_url)
        except Exception as e:
            print(e)
            continue
        response = requests.get('https://api.askyourpdf.com/v1/api/download_pdf', 
        headers=headers, 
        params={'url': full_pdf_url})

        if response.status_code == 201:
            id = response.json()
            print(id)
            prompt = {} # Create a new dictionary for each element
            prompt['authors'] = article.author()
            prompt['docId'] = id['docId']
            prompts.append(prompt)
        else:
            print('Error:', response.status_code)
    

       
    else:
       continue
    if (len(prompts)>2):
         break
print(prompts)
headers = {
    'Content-Type': 'application/json',
    'x-api-key': 'ask_091df11bd8bb8d924465b10e464ffffe'
}
api_url = 'https://api.openai.com/v1/chat/completions'
    # Set your OpenAI API key
api_key = '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'
lR  = []
for prompt in prompts:
    a = prompt['authors']
    """
    a = a[0]
    if (len(a)>2):
       a = a[0] + 'et al'
    else:
       a = a[0]
       """
    id = prompt['docId']
    data = [
    {
        "sender": "User",
        "message": f"complete the following statement in a paragraph format to match the summary of the document:\n ' The study found' "
    }
   ]
    response = requests.post(
       f'https://api.askyourpdf.com/v1/chat/{id}?model_name=GPT3', 
           headers=headers, data=json.dumps(data))

    if response.status_code == 200:
              print(response.json())
              t = response.json()
              headers1 = {
             'Content-Type': 'application/json',
             'Authorization': f'Bearer {api_key}'
            }   
              payload = {
               'model': 'gpt-4',
                           'messages': [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content':f'Rephrase the following paragraph:\n{t} to be include the authors names:\n {a}'}
    ]
    }
    # Make the API request
              response = requests.post(api_url, headers=headers1, json=payload)

    # Parse the 
              if response.status_code == 200:
                     data = response.json()
                     message = data['choices'][0]['message']['content']  
                     print(message)  
                     lR.append(message) 
              else:  
                   print('Error:', response.status_code)
    else:
              print('Error:', response.status_code)
m = '\n'.join(lR)
print(m)
payload = {
               'model': 'gpt-3.5-turbo',
                           'messages': [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content':f'rephrase the following pharagraphs to be structured as a literature review:\n{m}'}
    ]
    }
    # Make the API request
response = requests.post(api_url, headers=headers1, json=payload)

    # Parse the response
data = response.json()
message = data['choices'][0]['message']['content']  
print(message)     
with open("springer_abstract.csv", "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(
        [
            "title",
            "authors",
            "journal",
            "date",
            "cites number",
            "abstract",
            "significant relationship",
            "conclusion",
            "suggestion",
        ]
    )
    writer.writerows(
        zip(
            titlelst2,
            authorlst2,
            journallst2,
            datelst2,
            citeslst2,
            abstractlst2,
            significantlst2,
            conclusionlst2,
            suggestlst2,
        )
    )

import requests
import json
from  info import *
from literature_review_class import Literature_Review, Research

paper_data_params = {'fields': 'title,year,abstract,authors.name,'}

def search_in_semantic(topic:str, max_results=50) -> list[Research]:
  query_params = {
      'query': f'{topic}',
      'limit': max_results
  }
  # Make the GET request with the URL and query parameters
  resp = requests.get(SEMANTIC_URL,params=query_params)
  if resp.ok:
    res = []
    data = json.loads(resp.text)['data']
    for p in data:
      paperId = p["paperId"]
      det_url = 'https://api.semanticscholar.org/v1/paper/' + paperId
      det = requests.get(det_url,params=paper_data_params)
      if det.ok:
        data = json.loads(det.text)
        url = data['url']
        print(f'\n{url}\n')
        if not 'arxivId' in data.keys():
          print(f'\n{data.keys()}\n')
        authors = [data['authors'][i]['name'] for i in range(0,len(data['authors']))]
        year = data['year']
        title = data['title']
        r= Research(title,authors,url,year)
        res.append(r)
      else:
        print(f"Error:{det.status_code}")
        break
    return res
  else:
    print(f'Error:{resp.status_code}')
    exit(1)
'''
def get_full_text(doi:str):
  conts = {}
  if doi:
      url = f"http://api.springernature.com/openaccess/json?q=doi:{doi}
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
'''

if __name__ == "__main__":
  search_in_semantic("quantom computing")
  
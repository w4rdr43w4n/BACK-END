import requests
import json
from urllib.parse import ParseResult
from bs4 import BeautifulSoup
from info import SCHOLAR_API_KEY


class Author:
   def __init__(self, name, id, link):
       self.name = name
       self.id = id
       self.link = link

class Citation:
   def __init__(self, title,snippet):
       self.title = title
       self.snippet = snippet
class SearchResult:
   def __init__(self, position, title,link, publication,data_cid, snippet,authors, resource, cluster_id,cites_id):
       self.position = position
       self.title = title
       self.data_cid = data_cid
       self.link = link
       self.publication = publication
       self.snippet = snippet
       self.resource = resource
       self.authors = authors # This is now a list of Author objects
       self.cluster_id = cluster_id
       self.cites_id = cites_id
def fetch_and_parse(url, params):
   response = requests.get(url, params=params)
   data = json.loads(response.text)
   return data
def generate_citation(data_cid,title):
   url = "https://www.searchapi.io/api/v1/search"
   params = {
   "engine": "google_scholar_cite",
   "data_cid":  data_cid,
   "api_key": SCHOLAR_API_KEY
   }
   data = fetch_and_parse(url, params)
   cite = 'NULL'
   
   for citation in data['citations']:
              if (citation['title']==title):
                  cite =  citation['snippet']
                  break
              else:
                 continue
   return cite
   
def create_search_results(data):
   results = []
   for result in data['organic_results']:
         position = result['position']
         title = result['title']
         link = result['link']
         publication = result['publication']
         data_cid = result['data_cid']
         snippet = result['snippet']
         try:
                authors = [Author(author['name'], author['id'], author['link']) for author in result['authors']]
         except:
             authors = 'No one'
         try:
             resource = result['resource']
         except:
             resource = 'No one'
         try:
            cluster_id = result['inline_links']['versions']['cluster_id']
         except:
             cluster_id = 0
         try:
            cites_id = result['inline_links']['cited_by']['cites_id']
         except:
              cites_id = 0
         serachresult = SearchResult(position,title,link,publication,data_cid,snippet,authors,resource,cluster_id, cites_id)
         results.append(serachresult)
   return results
   #results.append(search_result)
def get_citation(title:str,type='APA'):
   """type can be 'MLA' or 'APA' or 'Chicago' or 'Harvard' or 'Vancouver'
     title indicates paper title"""
   
   url = "https://www.searchapi.io/api/v1/search"
   params = {
     "engine": "google_scholar",
     "q": title,
     "api_key": SCHOLAR_API_KEY,
      }
   data = fetch_and_parse(url, params)
   search_results = create_search_results(data)
   if (len(data['organic_results'])==1):
       data_cid = search_results[0].data_cid
       cite = generate_citation(data_cid,type)
       return cite
   else:
        for s in search_results:
             if (s.title == title):
                 data_cid = s.data_cid
                 cite = generate_citation(data_cid,type)
                 return cite
             else:
                 continue
        return 'citation not found'
if __name__ == '__main__':
    pdfs = []
    title = 'electronic circuits'
    type = 'APA'
    url = "https://www.searchapi.io/api/v1/search"
    params = {
        "engine": "google_scholar",
        "q": title,
        "api_key": SCHOLAR_API_KEY,
        }
    data = fetch_and_parse(url, params)
    search_results = create_search_results(data)

    for cite in search_results:
        print(get_citation(cite.title,"APA"))
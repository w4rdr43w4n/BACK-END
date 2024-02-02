# https://lukasschwab.me/arxiv.py/arxiv.html
# https://poe.com/chat/2t4f2epll96yl0li4gn

import requests
import json
import arxiv
from scholar import get_citation, fetch_and_parse, create_search_results
from info import *


# Dependency functions

def parse_year(d) -> int:
  d = str(d)
  return d.split()[0][0:4]

def search_in_arxiv(query: str, max_results: int = 10):
    client = arxiv.Client(page_size=100, delay_seconds=1.0, num_retries=3)
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
        sort_order=arxiv.SortOrder.Descending,
    )

    all_results = list(client.results(search))
    return all_results

# Classes

class Research:
   def __init__(self, title:str,authors:list, pdfUrl:str,publish_year:str):
       self.title = title
       self.author_name = self.parse_author_name(authors)
       self.pdfUrl = pdfUrl 
       self.publish_year = parse_year(publish_year)
   def parse_author_name(self,authors:list):
     
     if len(authors) == 1:
              author = str(authors[0]).split()[-1]
     else:
          au = str(authors[0]).split()[-1] 
          author = au + ' et al'
     return author
       


class Literature_Review:
  def __init__(self,Researches:list[Research]):
    self.research_count = len(Researches)
    self.authors = [obj.author_name for obj in Researches]
    self.publish_years = [obj.publish_year for obj in Researches]
    self.pdf_urls = [obj.pdfUrl for obj in Researches]
    self.titles = [obj.title for obj in Researches]
    self.docIds = self.get_docId()
    self.raw_literature_reviews = self.generate_literature_review()
    self.full_literature_review = self.merge_and_rephrase()
    self.references = []
    self.isCited = False

  def get_docId(self) -> list:
    Ids = []
    for url in self.pdf_urls:
      response = requests.get('https://api.askyourpdf.com/v1/api/download_pdf',
      headers=headers1,
      params={'url': url})
      if response.status_code == 201:
          id = response.json()
          Id = id['docId']
          Ids.append(Id)
      else:
          print(f'Error:{response.status_code}')
          break
    return Ids
  
  def list_researches(self) -> None:
    print(f"Researches Count:{self.research_count} \n")
    for i in range(0,self.research_count):
      r = f'[{i+1}] Title:{self.titles[i]}\n Authors:{self.authors[i]}\nURLs:{self.pdf_urls[i]}\nDocId:{self.docIds[i]}\nPublish Year:{self.publish_years[i]}\n'
      print(r)

  def generate_literature_review(self) -> list:
    lR  = []
    for i in range(0,self.research_count):
      a = self.authors[i] 
      id = self.docIds[i]
      data = [
      {
          "sender": "User",
          "message": f"complete the following statement in a paragraph format to match the summary of the document:\n 'The study found' or 'The research discovers'  "
      }
      ]
      # AskYourPdf Request
      response = requests.post(
        f'https://api.askyourpdf.com/v1/chat/{id}?model_name=GPT3', 
            headers=headers2, data=json.dumps(data))

      if response.status_code == 200:
        t = response.json()
        payload = {
        'model': 'gpt-4',
        'messages': [
              {'role': 'system', 'content': 'You are a helpful assistant.'},
              {'role': 'user', 'content':f'Rephrase the following paragraph:\n{t} to include the author name:{a}'}
            ]
        }
        # First GPT-4 Request
        response = requests.post(api_url, headers=headers3, json=payload)
        # Parse the response
        data = response.json()
        message = data['choices'][0]['message']['content']  
        #print(message)  
        lR.append(message)   
      else:
          return [f'Error: {response.status_code}']
    return lR


  def merge_and_rephrase(self) -> str:
    m = '\n'.join(self.raw_literature_reviews)
    payload = {
              'model': 'gpt-4',
              'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content':f'merge and rephrase the following pharagraphs together as a literature review:\n{m} , and also remember to use linking words "While", "However" and "Whereas", between each paragraph'}
        ]
        }
      # Second GPT-4 request 
    response = requests.post(api_url, headers=headers3, json=payload)
    # Parse the response
    data = response.json()
    message = data['choices'][0]['message']['content']  
    return message

  def add_citations(self,citation_type:str):
    # Adding citations to the literature review
    full_lr = self.full_literature_review
    if not self.isCited:
      self.isCited = True
      for i in range(0,self.research_count):
          year = self.publish_years[i] # year of publish
          auth_name = self.authors[i] # author name case
          alt_auth_name = auth_name + '\'s ' # author name case with 's
          # Getting author name position in the lr
          pos = self.full_literature_review.find(auth_name) 
          pos = self.full_literature_review.find(alt_auth_name) + len(alt_auth_name) if pos == -1 else pos + len(auth_name)
          # Preparing citations
          match citation_type:
              case 'MLA':
                  citation = f'({auth_name})'
              case 'IEEE':
                  citation = f'[{i+1}]'
              case _:
                  citation = f'({auth_name}, {year})'
          
          full_lr = '{}{}{}'.format(full_lr[:pos],citation,full_lr[pos+1:])
      self.full_literature_review = full_lr
      return full_lr
    else:
      return "This literature review is already cited!"
    
  def add_references(self,type:str):
    ref_index = 1
    if len(self.references) == 0:
      lr = self.full_literature_review
      lr = f'{lr}\nReferences:'
      # Creating references
      url = "https://www.searchapi.io/api/v1/search"
      for i in range(0,self.research_count):
        params = {
            "engine": "google_scholar",
            "q": self.titles[i],
            "api_key": SCHOLAR_API_KEY
            }
        data = fetch_and_parse(url, params)
        search_results = create_search_results(data)
        self.references.append(get_citation(search_results[0].title,type))
      # Adding refs to the bottom of the lr
      for ref in self.references:
          lr = f'{lr}\n[{ref_index}] {ref}\n'
          ref_index  = ref_index + 1
      self.full_literature_review = lr
      return lr
    else:
      return "References are already loaded!"



if __name__ == "__main__":
  rl = [] # Initializing a list to handle Research objects
  for r in search_in_arxiv("Neural networks"):
    r1 = Research(r.title,r.authors,r.pdf_url,r.published)
    rl.append(r1)
  lr = Literature_Review(rl) # Defining a Literaure Review object
  # Simple Doc:
  lr.list_researches() # list the loaded researches
  lr.raw_literature_reviews # list all literature review     paragraphs before merging
  lr.full_literature_review # returns the whole literature review with author names only
  lr.add_citations(citation_type="APA") #add citation
  print(lr.add_references(type="APA")) # add referrences
  
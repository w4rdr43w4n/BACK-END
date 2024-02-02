# https://lukasschwab.me/arxiv.py/arxiv.html
# https://poe.com/chat/2t4f2epll96yl0li4gn

import arxiv
import requests
import json
from scholar import get_citation, fetch_and_parse, create_search_results

# the Arxiv search function
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


if __name__ == "__main__":
    
    # Sending pdf urls to AskYourPdf API
    
     prompts = [] # requests to gpt-4
     headers = {
    'x-api-key': 'ask_091df11bd8bb8d924465b10e464ffffe'
     }
     for article in search_in_arxiv("Neural networks"):
        response = requests.get('https://api.askyourpdf.com/v1/api/download_pdf', 
        headers=headers, 
        params={'url': article.pdf_url})
        if response.status_code == 201:
            id = response.json()
            prompt = {} 
            year = str(article.published).split()[0][0:4]
            prompt['year'] = year
            prompt['title'] = article.title
            # Parsing Author names
            if len(article.authors) == 1:
                prompt['authors'] = str(article.authors[0]).split()[-1]
            else:
                au = str(article.authors[0]).split()[-1] 
                prompt['authors'] = au + ' et al'
            
            prompt['docId'] = id['docId']
            prompts.append(prompt)
        else:
            print('Error:', response.status_code)
        #Take just 3 articles
        if (len(prompts)>4):
             break
# Sending resualts to GPT-4 for rephrasing
headers = {
    'Content-Type': 'application/json',
    'x-api-key': 'ask_091df11bd8bb8d924465b10e464ffffe'
}
api_url = 'https://api.openai.com/v1/chat/completions'
    # Set your OpenAI API key
api_key = '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'
lR  = []
IEEE_index = 1
for prompt in prompts:
    a = prompt['authors']
    #print(f'\n {a} \n')
    
    
    id = prompt['docId']
    
    data = [
    {
        "sender": "User",
        "message": f"complete the following statement in a paragraph format to match the summary of the document:\n 'The study found' or 'The research discovers'  "
    }
   ]
    # AskYourPdf Request
    response = requests.post(
       f'https://api.askyourpdf.com/v1/chat/{id}?model_name=GPT3', 
           headers=headers, data=json.dumps(data))

    if response.status_code == 200:
              #print(response.json())
              t = response.json()
              headers1 = {
             'Content-Type': 'application/json',
             'Authorization': f'Bearer {api_key}'
            }   
              payload = {
               'model': 'gpt-4',
                           'messages': [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content':f'Rephrase the following paragraph:\n{t} to include the author name:{a}'}
    ]
    }
     # First GPT-4 Request
              response = requests.post(api_url, headers=headers1, json=payload)

    # Parse the response
              data = response.json()
              message = data['choices'][0]['message']['content']  
              #print(message)  
              lR.append(message)   
    else:
              print('Error:', response.status_code)

m = '\n'.join(lR)

payload = {
               'model': 'gpt-4',
                           'messages': [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content':f'merge and rephrase the following pharagraphs together as a literature review:\n{m} , and also remember to use linking words "While", "However" and "Whereas", between each paragraph'}
    ]
    }
# Second GPT-4 request 
response = requests.post(api_url, headers=headers1, json=payload)

# Parse the response
data = response.json()
message = data['choices'][0]['message']['content']  
refs = []

# Adding citations to the literature review
for prompt in prompts:
    year = prompt['year']
    citation_type = 'APA'
    auth_name = prompt['authors']
    alt_auth_name = prompt['authors'] + '\'s '
    pos = message.find(auth_name)
    pos = message.find(alt_auth_name) + len(alt_auth_name) if pos == -1 else pos + len(auth_name)
    # Preparing citations
    match citation_type:
        case 'MLA':
            citation = f'({auth_name})'
        case 'IEEE':
            citation = f'[{IEEE_index}]'
            IEEE_index = IEEE_index + 1
        case _:
            citation = f'({auth_name}, {year})'
    message = '{}{}{}'.format(message[:pos],citation,message[pos+1:])
    # Creating refrences
    type = 'APA'
    url = "https://www.searchapi.io/api/v1/search"
    
    params = {
        "engine": "google_scholar",
        "q": prompt['title'],
        "api_key": "74tprW6GKdTpz1VoTxfw3vkC"
        }
    data = fetch_and_parse(url, params)
    search_results = create_search_results(data)
    refs.append(get_citation(search_results[0].title,type))

ref_index = 1    
message = f'{message}\n References:'
for ref in refs:
    message = f'{message }\n [{ref_index}] {ref}\n'
    ref_index  = ref_index + 1
 

print(message)
   
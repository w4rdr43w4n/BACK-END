'''
import requests

def get_pdf_url(arxiv_id):
# Arxiv API base URL
  base_url = "http://export.arxiv.org/api/query?id_list="

  # Send a GET request to the Arxiv API
  response = requests.get(base_url + arxiv_id)

  if response.status_code == 200:
  # Extract the PDF URL from the response
  paper_xml = response.text
  pdf_url_start = paper_xml.find("<arxiv:pdf>")
  pdf_url_end = paper_xml.find("</arxiv:pdf>")
  if pdf_url_start != -1 and pdf_url_end != -1:
  pdf_url = paper_xml[pdf_url_start + len("<arxiv:pdf>"):pdf_url_end]
  return pdf_url
  else:
  return "PDF URL not found in the response"
  else:
  return "Failed to retrieve data from the Arxiv API"

# Example usage
arxiv_id = "Replace_with_your_arxiv_id"
pdf_url = get_pdf_url(arxiv_id)
print("PDF URL:", pdf_url)
'''

import requests

paper_id = "your_paper_id_here" # Replace with the actual paper ID

url = f'https://api.semanticscholar.org/{paper_id}'

response = requests.get(url)

if response.status_code == 200:
  data = response.json()
  pdf_url = data.get('pdfUrls', {}).get('download')
  if pdf_url:
   print(f'PDF URL for paper {paper_id}: {pdf_url}')
  else:
    print(f'PDF URL not found for paper {paper_id}')
  else:
  print(f'Failed to fetch data for paper {paper_id} from Semantic Scholar API')
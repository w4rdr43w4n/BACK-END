from literature_review_class import Literature_Review,Research
from internetarchive import *



def search_in_archive(topic:str) -> list[Research]:
  q = f"{topic} AND collection:(journals) AND format:(Text PDF) AND mediatype:(texts)"
  arch_res = search_items(query=q)
  res = []  
  for r in arch_res:
    Id = r['identifier']
    item = get_item(Id)
    title = item.item_metadata['metadata']['title']
    try:
      author = item.item_metadata['metadata']['creator']
    except KeyError:
      author = item.item_metadata['metadata']['uploader']
    try:
      year = item.item_metadata['metadata']['date']
    except KeyError:
      year = item.item_metadata['metadata']['publicdate']
    
    url = f"https://archive.org/details/{Id}"
    rs = Research(title,[author],url,year)
    res.append(rs)
    if len(res) > 4:
      break
  return res


if __name__=='__main__':
  lr = Literature_Review(search_in_archive("Hotel Paradox"))
  lr.list_researches()
  print(lr.full_literature_review)
  lr.add_citations("APA")
  lr.add_references("APA")
  print(lr.full_literature_review)
  
  
    
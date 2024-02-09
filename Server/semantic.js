const axios = require('axios')
const cfg = require('./config')
const { parse_author_name, parse_year, get_pdf_url_from_arxiv, get_pdf_url_from_doi, asyncRetryHandler } = require('./dep');




async function searchInSemantic(query, maxResults = 5) {
  try{
    const response = await axios.get(cfg.SEMANTIC_CONFIG.api_url, {
      params: {
        'query': `${query}`,
        'limit': maxResults
      }
    });
    const Ids = response.data.data
    let i = 0
    var r = []
    for (let id of Ids) {
      let details = await getSemanticItemDetails(id.paperId);
      i++;
      if (details) {
        r.push(details)
      } else {
        continue
      }
    }
    return r
  } catch(err){
    if(err.response && err.response.status == 429){
      throw err
    } else {
      console.log(`ERROR: ${err}`)
    }
  }
}

async function getSemanticItemDetails(identifier) {
  // Getting PDF URLs
  pdf_link = ''
  try {
    const url = `https://api.semanticscholar.org/v1/paper/${identifier}`;
    const response = await axios.get(url);
    const Metadata = response.data
    if (Metadata.arxivId == null) {
      if(Metadata.doi == null){
        pdf_link = ''
      }
      else{
        pdf_link = await get_pdf_url_from_doi(Metadata.doi)
        pdf_link = (pdf_link == null)? '':pdf_link
      }
    } else {
      pdf_link = get_pdf_url_from_arxiv(Metadata.arxivId)
    }
  // Getting author names
    var authors = []
    Metadata.authors.forEach((a) =>{
      authors.push(a.name)
    } )
    const author = parse_author_name(authors)
    const title = Metadata.title
    const year = parse_year(Metadata.year)
    var details = {"title":title,"author":author,"publish_year":year,'pdfLink':pdf_link}
    return details
  } catch (err) {
    return null
  }
}
/*
let query = 'Canada'
let i = 0
let res = asyncRetryHandler(searchInSemantic,query).then((sre)=>{
  console.log(sre)
})
*/
module.exports = {searchInSemantic}
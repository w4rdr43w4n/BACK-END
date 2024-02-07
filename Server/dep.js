const axios = require('axios');
const cheerio = require('cheerio');

function parse_year(year) {
  let y = year.toString()
  return y.slice(0, 4)
}

function parse_author_name(author_name) {
  var author = author_name[0].toString()
  let comma = author.match(/\s*,/)
  if(comma){
    author = author.substring(comma.index - author.length,comma.index)
    var pos = author.lastIndexOf(' ')
    author = author.substring(pos + 1)
    return ` ${author} et al ` 
  } 
  else{
    var pos = author.lastIndexOf(' ')
  author = author.substring(pos + 1)
  if (author_name.length == 1) {
    return author
  }
  else {
    return ` ${author} et al `
  }
  }
}

function get_pdf_url_from_arxiv(arxivId) {
  return `http://arxiv.org/pdf/${arxivId}.pdf`
}
// Function to resolve relative URLs
function resolveUrl(base, relative) {
  const url = new URL(relative, base);
  return url.href;
}

// Function to scrape the website and retrieve PDF URLs
async function get_pdf_url_from_doi(doi) {
  try {
    const url = `http://dx.doi.org/${doi}`
    const response = await axios.get(url);
    const $ = cheerio.load(response.data);

    // Replace 'selector' with the appropriate CSS selector for your PDF element
    const pdfElement = $('a');

    // Retrieve the relative URL
    for (let link of pdfElement) {
      const href = link.attribs.href
      console.log(`link[dep]:${href}`)
      if (typeof href == null) {
        console.log(`link[dep] is null`)
        continue
      }
      else {
        console.log(`link is not null[dep]:${href}`)
        if (href.includes('.pdf')) {
          const completePdfUrl = resolveUrl(url, href);
          return completePdfUrl
        }
      }

    }
    return null
  } catch (error) {
    console.error('Error[dep]:', error.message);
  }
}

module.exports = { get_pdf_url_from_arxiv, get_pdf_url_from_doi, parse_author_name, parse_year }
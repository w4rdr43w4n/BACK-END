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


async function get_pdf_url_from_doi(doi) {
  const url = `https://doi.org/${doi}`;
  try {
    const response = await axios.get(url, {
      headers: {
        'Accept': 'text/html',
      },
    });

    const $ = cheerio.load(response.data);
    const pdfUrl = $('meta[name="citation_pdf_url"]').attr('content');

    if (pdfUrl) {
      return pdfUrl
    } else {
      
      return null
    }
  } catch (error) {
    //console.error(`Error fetching data for DOI ${doi}: ${error.message}`);
    return null
  }
}

const asyncRetryHandler = async (func,value,maxRetries=30, retryDelay=1000) => {
  let retries = 0;
  const retry = async () => {
    try {
      const result = await func(value);
      return result; // Resolve the promise with the result
    } catch (error) {
      if (retries < maxRetries) {
        retries++;
        await new Promise(resolve => setTimeout(resolve, retryDelay));
        return retry(); // Retry after the delay
      } else {
        throw error; // Reject the promise after maxRetries
      }
    }
  };
  return retry();
};

module.exports = { get_pdf_url_from_arxiv, get_pdf_url_from_doi, parse_author_name, parse_year,asyncRetryHandler}

const axios = require('axios')
const xml = require('xml2js');
const { parse_author_name, parse_year } = require('./dep');


async function searchInArxiv(query, maxResults = 10) {
 const baseUrl = 'http://export.arxiv.org/api/query?';
 const params = `search_query=${encodeURIComponent(query)}&max_results=${maxResults}`;
 const url = `${baseUrl}${params}`;
 const response = await axios.get(url);
 const parser = new xml.Parser();
 const result = await parser.parseStringPromise(response.data);

 // Extract entries from the parsed XML
 const entries = result.feed.entry;

 // Convert entries to a simpler format
 const simplifiedEntries = entries.map((entry) => ({
    id: entry.id[0],
    title: entry.title[0],
    summary: entry.summary[0],
    updated: entry.updated[0],
    author: entry.author[0].name[0],
    category: entry['arxiv:primary_category'][0]['$'].term,
    pdfLink: entry.link[1]['$'].href + '.pdf',
 }));
 let res = [];
 let i = 0;
 simplifiedEntries.forEach(e => {
  let author = (typeof e.author == 'string')? [e.author]:e.author
   let r = {'title':e.title,'author':parse_author_name(author),'pdfLink':e.pdfLink,'publish_year':parse_year(e.updated)}
   res.push(r);
 });
 return res
}
// Define the query and maximum results
let query = 'quantum mechanics';
let maxResults = 5;


// Call the function with the defined parameters


 module.exports = {searchInArxiv}


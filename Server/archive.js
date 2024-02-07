const axios = require('axios')
const { parse_author_name, parse_year } = require('./dep');


async function searchInArchive(query,maxResults=10) {
    const response = await axios.get("https://archive.org/advancedsearch.php", {
      params: {
        q: `"${query}" AND collection:(journals) AND format:(Text PDF) AND mediatype:(texts)`,
        fl: ["identifier"],
        rows: maxResults,
        output: "json",
      }
    });
    const res = [];
    
    for (let e of response.data.response.docs) {
      let details = await getInternetArchiveItemDetails(e.identifier);
      let r = {'title':details.title,'author':parse_author_name([details.author]),'pdfLink':details.pdfUrl,'publish_year':parse_year(details.publish_year)}
      res.push(r);
    }
  return res;
}

async function getInternetArchiveItemDetails(identifier) {
  const filesMetadataUrl = `https://archive.org/metadata/${identifier}`;
  const response = await axios.get(filesMetadataUrl);
  // adjusting author name
  const MetaData = response.data.metadata
  if('creator' in MetaData){
    var author =  MetaData.creator
  }
  else if('journaltitle' in MetaData){
    var author = MetaData.journaltitle;
  }
  else if('contributor' in MetaData){
    var author = MetaData.contributor;
  }
  else{
    var author = 'Unknown'
  }
  const year = MetaData.publicdate
  const title = MetaData.title
  var details = {"title":title,"author":author,"publish_year":year}
  const filesMetaData = response.data['files'];
  for (let fileData of filesMetaData) {
    if (fileData.format === "Text PDF") {
      const pdfdownloadUrl = `https://archive.org/download/${identifier}/${fileData.name}`;
      details['pdfUrl'] = pdfdownloadUrl;
    }
  }
  return details
}


module.exports = {searchInArchive}
// APIs Credintals

// GPT API
const GPT_api_key = '******************'
const GPT_CONFIG = {
  api_url: 'https://api.openai.com/v1/chat/completions',
  api_key:GPT_api_key,
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${GPT_api_key}`
              }
}

// AskYourPdf API
const ASK_CONFIG = {
  headers1:{
    'x-api-key': '***************************'
  },
  headers2:{
    'Content-Type': 'application/json',
    'x-api-key': '*******************************'
  }
}

// Scholar API
const SCHOLAR_CONFIG = {
  api_key:"**************************"
}


// Semantic Scholar API
const SEM_api_key = '***************************************'
const SEMANTIC_CONFIG = {
  api_url:'https://api.semanticscholar.org/graph/v1/paper/search',
  api_key:SEM_api_key,
  headers:{
    'x-api-key': SEM_api_key
  }
}
module.exports = {GPT_CONFIG, ASK_CONFIG, SCHOLAR_CONFIG , SEMANTIC_CONFIG}

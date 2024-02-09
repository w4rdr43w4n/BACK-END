const express = require('express')
const bodyParser = require('body-parser')
const app = express()

// Local libs

const {searchInArxiv} = require('./arxiv')
const {searchInArchive} = require('./archive')
const {searchInSemantic} = require('./semantic')
const {asyncRetryHandler} = require('./dep')
// Server Configuration
const PORT = 3000
app.set('view engine', 'ejs');
app.set('views', __dirname + '/views');
app.use(bodyParser.urlencoded({ extended: true }));

// URLs
app.get('/', (req, res) => {
  res.render('home', { output: '' })
});

app.post('/search', (req, res) => {
  const buttonClicked = req.body.button;
  let output = ''
  let query = req.body.inputText;
  console.log(`Searching for ${query}....`)
  console.log(`BUTTON: ${buttonClicked} is clicked!`)
  var outputHTML = ''
  switch (buttonClicked) {
    case 'arxiv':
      search(query,'arxiv').then((sre) => {
          res.render('home',{output:sre})
        }).catch((err) => {
          console.log(`Error :${err}`)
        })
            break;
        case 'archive':
          search(query,'archive').then((sre) => {
            res.render('home',{output:sre})
          }).catch((err) => {
            console.log(`Error :${err}`)
          })
            break;
        case 'semantic':
          asyncRetryHandler(deliverSemanticResults,query).then((sre) => {
            res.render('home',{output:sre})
          })
            break;
        default:
          res.render('home',{output:'<p>Something went wrong...try again later</p>'})
  }
})

//Initializing the server
app.listen(PORT, () => {
  console.log(`Server is listening at http://localhost:${PORT}`)
});

async function search(query,engine) {
  switch(engine){
    case 'arxiv':
    var res = await searchInArxiv(`${query}`)
    break;
    case 'archive':
    var res = await searchInArchive(`${query}`)
    break;
    default:
    var res = await searchInArxiv(`${query}`)
  }
  let i = 0;
  var htmlRes = ''
  for (let r of res) {
    var item = `<div class='item'><h4>Title:${r.title}</h4><h4>Author:${r.author}</h4><h4>Published:${r.publish_year}</h4><h4>PDF:<a href='${r.pdfLink}'>Download</a></h4></div>`
    htmlRes += item
  }
  return htmlRes
}
async function deliverSemanticResults(query) {
  let res = await searchInSemantic(query)
  let i = 0;
  var htmlRes = ''
  for (let r of res) {
    var item = `<div class='item'><h4>Title:${r.title}</h4><h4>Author:${r.author}</h4><h4>Published:${r.publish_year}</h4><h4>`
    item = (r.pdfLink == '')? item + '</div>' :item + `PDF:<a href='${r.pdfLink}'>Download</a></h4></div>`
    htmlRes += item
  }
  return htmlRes
}




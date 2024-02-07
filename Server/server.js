const express = require('express')
const bodyParser = require('body-parser')
const app = express()

// Local libs

const arxiv = require('./arxiv')
const archive = require("./archive")
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
        parse_res_arxiv(query).then((sre) => {
          res.render('home',{output:sre})
        }).catch((err) => {
          console.log(`Error :${err}`)
        })
            break;
        case 'archive':
          parse_res_archive(query).then((sre) => {
            res.render('home',{output:sre})
          }).catch((err) => {
            console.log(`Error :${err}`)
          })
            break;
        case 'button3':
            outputHTML = '<em>Output for Button 3</em>';
            break;
        default:
            outputHTML = '<p>Invalid button click</p>';
  }
})

//Initializing the server
app.listen(PORT, () => {
  console.log(`Server is listening at http://localhost:${PORT}`)
});

async function parse_res_arxiv(query) {
  let res = await arxiv.searchInArxiv(`${query}`)
  let i = 0;
  var htmlRes = ''
  for (let r of res) {
    var item = `<div class='item'><h4>Title:${r.title}</h4><h4>Author:${r.author}</h4><h4>Published:${r.publish_year}</h4><h4>PDF:<a href='${r.pdfLink}'>Download</a></h4></div>`
    htmlRes += item
  }
  return htmlRes
}
async function parse_res_archive(query) {
  let res = await archive.searchInArchive(`${query}`)
  let i = 0;
  var htmlRes = ''
  for (let r of res) {
    var item = `<div class='item'><h4>Title:${r.title}</h4><h4>Author:${r.author}</h4><h4>Published:${r.publish_year}</h4><h4>PDF:<a href='${r.pdfLink}'>Download</a></h4></div>`
    htmlRes += item
  }
  return htmlRes
}

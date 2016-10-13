var connect = require("connect");
var logger = require("morgan");
var http = require("http");
var ejs = require('ejs');
var bodyparse = require('body-parser');
var serve_static = require("serve-static");
var ex_session = require('express-session');


var app = connect()
    .use (logger('dev'))
    .use (bodyparse())
    .use (serve_static(__dirname + '/public'))
    .use (serve);

http.createServer(app).listen(3000);

function serve (req, res) {
  var email = req.body.email;
  var message = req.body.message;
  if(email && message){
    console.log(req.body.email);
    console.log(req.body.message);
  }
  render(res, req.url);
}

function render (res, view, model){
  ejs.renderFile("templates/" + view + ".ejs",
    function(err, result){
      if(!err)
        res.end(result);
      else {
        res.end("ERROR 404")
      }
    });
}

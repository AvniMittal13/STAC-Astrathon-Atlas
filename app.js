const express=require("express");
const bodyParser = require("body-parser");
// const date = require (__dirname+"/date.js");

const app=express();

app.set('view engine', 'ejs');

app.use(bodyParser.urlencoded({extended:true}));
app.use(express.static("public"));

key = '3X32YF-VDRZFK-35RFJS-4TFW'

app.get("/",function(req,res){

    res.render("index")

});

app.post("/",function(req,res){

     
})

app.listen(3000,function(){

    console.log("Server is up and running");
    
});
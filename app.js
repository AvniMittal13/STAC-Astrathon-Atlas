const express=require("express");
const https = require("https");
const bodyParser = require("body-parser");
const { urlencoded } = require("body-parser");
// const date = require (__dirname+"/date.js");
const PythonShell = require('python-shell').PythonShell;
const spawn = require("child_process").spawn;


const app=express();

app.set('view engine', 'ejs');

app.use(bodyParser.urlencoded({extended:true}));
app.use(express.static("public"));

const ny2o_key = '3X32YF-VDRZFK-35RFJS-4TFW'
const nasa_key='4EhtxrAK41OTThAXAB5mDZe1fiYAPh7cjS8Ra6qb'
const base = 'https://tle.ivanstanojevic.me/api/tle/'

var satName = ''
var satDate = ''
var satL1 = ''
var satL2= ''



app.get("/",function(req,res){

    res.render("index")

});

app.post("/",function(req,res){

    sat_code = req.body.satellite_code;
    // sat_name = req.body.satellite_name;

    // console.log(req.body)

    // if(sat_code==''){

    //     https.get(url+'?search='+sat_name)
    // } else if (sat_name!='' && sat_code=='') {
    // const url = base+sat_code+"?search="+sat_name;

    const url = base+sat_code;
    https.get(url,function(response){
        // console.log(response.statusCode);

        response.on("data",function(data){
            sat_data=JSON.parse(data)
            
            satId= sat_data.satelliteId
            satName = sat_data.name
            satDate = sat_data.date
            satL1 = sat_data.line1
            satL2= sat_data.line2
            // console.log(sat_data)
            // console.log('hello')

            res.redirect("/simulation")
            // PythonShell.run('orbit_calculation.py', null, function (err) {
            //     if (err) throw err;
            //     console.log('finished');
            //   });
        })

    } )
    // }

})


app.get("/simulation",function(req,res){

    
    // const pythonProcess = spawn('python',["orbit_calculation.py",satName, satL1, satL2]);

    
    // pythonProcess.stdout.on('data', function(data){
    //     // Do something with the data returned from python script
    //     console.log(data)
    // });

    var options = {
        mode: 'text',
        // pythonPath: 'path/to/python',
        // pythonOptions: ['-u'],
        // scriptPath: 'path/to/my/scripts',
        args: [satName, satL1, satL2]
      };
      
      PythonShell.run('orbit_calculation.py', options, function (err, results) {
        if (err) 
          throw err;
          python_data=JSON.parse(results)
        // Results is an array consisting of messages collected during execution
        console.log('results: %j', results);
        console.log(python_data)
      });


    // console.log(satL1)
    // console.log(satL2)
    res.render("simulation",{sat_name:satName,l1:satL1,l2:satL2})

});

app.listen(3000,function(){

    console.log("Server is up and running");
    
});
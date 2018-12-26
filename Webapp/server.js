var express = require('express');
var app = express();
var bodyParser=require('body-parser');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true} ) );

app.get('/', function(req, res){
   res.sendFile('/home/ubuntu/query_app/index.html');
});

app.post('/form', function(req, res){
   console.log(req.body["user_message"]);
   var func=async function(str){
      const {BigQuery} = require('@google-cloud/bigquery');
      const bigquery = new BigQuery();

var query = str
var options = {
  query: query,
  // Location must match that of the dataset(s) referenced in the query.
  location: 'US',
};

// Runs the query as a job
var [job] = await bigquery.createQueryJob(options);
console.log(`Job ${job.id} started.`);

// Waits for the query to finish
var [rows] = await job.getQueryResults();

// Prints the results
res.send("recieved your request!");
res.send('Rows:');
rows.forEach(row => res.send(row));
   }
func(req.body["user_message"]);


   
});
app.listen(8080);
const { checkIfLinkExists } = require('./modules/creatingLink');
require('dotenv').config();
const express = require('express');
const fs = require('node:fs');
const mysql = require('mysql2');
const app = express();
const PORT = 8080;

app.use(express.json());
app.use(function (req, res, next) {
  // Website you wish to allow to connect
  res.setHeader('Access-Control-Allow-Origin', 'http://127.0.0.1:5500');

  // Request methods you wish to allow
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');

  // Request headers you wish to allow
  res.setHeader('Access-Control-Allow-Headers', 'content-type');

  // Set to true if you need the website to include cookies in the requests sent
  // to the API (e.g. in case you use sessions)
  res.setHeader('Access-Control-Allow-Credentials', true);

  // Pass to next layer of middleware
  next();
});

const { HOST, USER, PASSWORD, DATABASE } = process.env;

const connection = mysql.createConnection({
  host: HOST,
  user: USER,
  password: PASSWORD,
  database: DATABASE,
  port: 3306,
  ssl: { ca: fs.readFileSync('./DigiCertGlobalRootCA.crt.pem') },
});
connection.connect((err) => {
  if (err) {
    console.error(`Error connecting: ` + err.stack);
  }
});

app.post('/create/:url', async (req, res) => {
  const { url } = req.params;
  const sql = `insert into urls_info (original_url) values (?)`;

  checkIfLinkExists(connection, url, (err, record) => {
    if (!record) {
      connection.execute(sql, [url], (err) => {
        if (err) {
          res.status(500).send({
            message: 'could not update database',
          });
        }
        res.status(200).send({
          message: 'shortened url added',
        });
      });
    } else {
      res.status(200).send({
        message: 'record already exists',
        info: record,
      });
    }
  });
});

app.listen(PORT, () => console.log(`Listening on port ${PORT}`));

import routes from './src/routes/nmmRoutes';
import bodyParser from 'body-parser';

const express = require('express');
var app = express();
const MongoClient = require('mongodb').MongoClient;
const PORT = 6660;
require('dotenv').config();

// set the mongoClient
let db,
    dbConnectionStr = 'mongodb://127.0.0.1:27017',
    dbName = 'test';

MongoClient.connect(dbConnectionStr, { useUnifiedTopology: true })
    .then((client) => {
        console.log(`${dbName} connection succeeded: [mongoclient]`);
        db = client.db(dbName); //connection to database
    })
    .catch((err) => {
        console.error(err);
        console.log('error in DB connection : ' + err);
    });

// set the server
app.set('view engine', 'ejs');
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// bodyparser setup
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json()); 
routes(app);

// serving static files on public folder such as png's
app.use(express.static('public'));

// mongoose connection for rest
import mongoose from 'mongoose';
mongoose.Promise = global.Promise;
mongoose.connect(dbConnectionStr, {
    useNewUrlParser: true,
    useUnifiedTopology: true
}, (err) => {
    if (!err) {
        console.log(`${dbName} connection succeeded: [mongoose]`);
    } else {
        console.log('error in DB connection : ' + err);
    }
});



// begin of new code
//todos = datas
//todo = status

//route - /get @home
app.get('/', async (req, res) => {
    const todoItems = await db.collection('datas').find().toArray();
    const itemsLeft = await db
      .collection('datas')
      .countDocuments({ completed: false });
    res.render('index.ejs', { info: todoItems, left: itemsLeft });
});
  
//start the server
app.listen(process.env.PORT || PORT, () => {
    console.log(`NMMpp server is running on: [127.0.0.1:${PORT}]`);
});

// home page
app.get('/dashboard', (req, res) => {
    res.sendFile(__dirname + '/public/dashboard.html');
});

// chat rooms page
app.get('/crooms', (req, res) => {
    res.sendFile(__dirname + '/public/crooms.html');
});

// chat room 1
app.get('/developers', (req, res) => {
    res.sendFile(__dirname + '/public/developers.html');
});

// chat room 2
app.get('/endusers', (req, res) => {
    res.sendFile(__dirname + '/public/endusers.html');
});

// network discovery page
app.get('/discovery', (req, res) => {
    res.sendFile(__dirname + '/public/discovery.html');
});

// manage nodes page
app.get('/nodes', (req, res) => {
    res.sendFile(__dirname + '/public/nodes.html');
});

// integrations page
app.get('/config', (req, res) => {
    res.sendFile(__dirname + '/public/config.html');
});
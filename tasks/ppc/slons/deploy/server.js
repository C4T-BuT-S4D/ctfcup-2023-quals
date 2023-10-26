const express = require('express');
const session = require('express-session');
const NodeRSA = require('node-rsa');
const cookieParser = require('cookie-parser');
const app = express();

app.use(cookieParser()); 

app.use(session({
    secret: process.env.KEY,
    resave: false,
    saveUninitialized: true
}));

app.use(express.static('public'));

function generateTaskVariant(key) {
    const text = `I placed ${Math.floor(Math.random() * 2000) - 1000} slons or no`;
    const encrypted = key.encrypt(text, 'base64');
    return {
        n: key.exportKey('components-public')['n'].toString('hex'),
        e: key.exportKey('components-public')['e'],
        c: encrypted
    };
}

function checkTask(task, input, key) {
    return `I placed ${input} slons or no` == key.decrypt(task.c,'utf-8');
}

app.use(express.json());

app.get('/generate-task', (req, res) => {
    const key = new NodeRSA({b: 512});
    const task = generateTaskVariant(key);
    const keyExport = key.exportKey('pkcs8-private')
    req.session.key = keyExport
    req.session.task = task;
    res.json({ task });
});

app.post('/check-task', (req, res) => {
    const input = req.body.input;
    const task = req.session.task;
    const key = new NodeRSA();
    key.importKey(req.session.key,'pkcs8-private')
    const result = checkTask(task, input, key);

    if (result) {
        req.session.correctAnswers = (req.session.correctAnswers || 0) + 1;

        if (req.session.correctAnswers === 100) {
                return res.json({ flag: process.env.FLAG });
        }
    }
    const newKey = new NodeRSA({b: 512});
    const newTask = generateTaskVariant(newKey);
    const keyExport = newKey.exportKey('pkcs8-private');
    req.session.key = keyExport;
    req.session.task = newTask;
    res.json({ task: newTask, answered: req.session.correctAnswers, success: result });
});

const PORT = 80;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

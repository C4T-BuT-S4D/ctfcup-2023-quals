const express = require('express');
const path = require('path');

const app = express();

app.use(express.static(path.join(__dirname, './static')));

app.listen(3000, () => {
    console.log('Static server is running on https://static-mistakes-4a27e2504ec596fe.ctfcup.ru');
});

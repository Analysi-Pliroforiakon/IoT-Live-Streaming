const express = require('express');
const bodyParser = require('body-parser');

const hbase = require('hbase');






const app = express();

app.use(bodyParser.json());

app.get('/:table/', async (req, res) => {
    try {
    const client = hbase({ host: 'localhost', port: 8080 });
    const table = req.params.table;
    console.log('GET request received', table);
    let result =[];
//   get all rows from table
    await new Promise(async (resolve, reject) => {
        client.table(table).scan({}, (err, rows) => {
            if (err) {
                console.log('Error', err);
            }
            if (!rows || rows.length === 0) {
                console.log('No rows found');
                return;
            }
            console.log('Rows found', rows.length);
            let groupedRows = {};
            rows.forEach(row => {
                // parse rows
                const key = row.key;
                const column = row.column.split(":")[1];
                const value = row.$;
                // grou by key
                if (!groupedRows[key]) {
                    groupedRows[key] = {};
                }
                if (column === 'sensor'){
                    groupedRows[key].sensor = value;
                } else if (column === 'value'){
                    groupedRows[key].value = value;
                } else if (column === 'datetime'){
                    groupedRows[key].datetime = value;
                }

                // append to result
                result.push(groupedRows[key]);
            });
            resolve();
        });
    });
    console.log('Result', result.length);
    // send it to read by grafana
        res.send(JSON.stringify(result));
    } catch (err) {
        console.log('Error', err);
        res.send(err);
    }
});


module.exports = app;
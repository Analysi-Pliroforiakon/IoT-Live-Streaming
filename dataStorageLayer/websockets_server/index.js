const express = require('express');
const app = express();
const server = require('http').createServer(app);
const WebSocket = require('ws');
const hbase = require('hbase');
const client = hbase({ host: '127.0.0.1', port: 8080 });

var tables = {
    raw: {name: 'raw', startRow: '0000000000'},
    aggregated: {name: 'aggregated', startRow: '0000000000'},
    late: {name: 'late', startRow: '0000000000'}
}

const wss = new WebSocket.Server({ server: server });

wss.on('connection', function connection(ws) {
    console.log('New connection established');

    ws.on('error', function (error) {
        console.error(error);
    });

    // run function periodically.
    setInterval(function () {
        // iterate over tables.
        for (var key in tables) {
            if (tables.hasOwnProperty(key)) {
                console.log('querying: %s with startRow: %s', tables[key].name, tables[key].startRow);
                handle_new_rows(tables[key]);
            }
        }
    }, 1000);
});

app.get('/', (req, res) => res.send('Hello World!'))
server.listen(1234, () => console.log('Listening on port 1234!'));

// function scans table, checks if there are new rows and sends them to the client.
function handle_new_rows (table) {
    const scanner = client
        .table(table.name)
        .scan({
            startRow: table.startRow,
            maxVersions: 1
        });
    const rows = [];
    scanner.on('readable', () => {
        while (chunk = scanner.read())
            rows.push(chunk)
    });
    scanner.on('error', (err) => {
        throw err
    });
    scanner.on('end', () => {
        //console.log('scanner ended');
        //console.info(rows)
        // check if there are new rows.
        if (rows.length != 0) {
            console.log('new rows: %s', rows.length);
            console.log(rows[rows.length - 1].key);
            let last_row = rows[rows.length - 1];
            // increment last_row lexicographically by 1.
            console.log('Old start row: %s', table.startRow);
            table.startRow = last_row.key + '0';
            console.log('New start row: %s', table.startRow);

            // group rows by key.
            var grouped_rows = {};
            rows.forEach(function (row) {
                if (grouped_rows[row.key] == undefined) {
                    grouped_rows[row.key] = {measurement: null, value: null, timestamp: null, late_rejected: table == 'late'};
                }
                if (row.column == 'f:measurement') {
                    grouped_rows[row.key].measurement = row.$;
                } else if (row.column == 'f:value') {
                    grouped_rows[row.key].value = row.$;
                } else if (row.column == 'f:timestamp') {
                    grouped_rows[row.key].timestamp = row.$;
                } else {
                    console.error('Unknown column: %s', row.column);
                }
            });

            console.log('grouped_rows: %s', JSON.stringify(grouped_rows));
            
            // send data in the format: {measurement: 'measurement1', value: 1, timestamp: 123456789}
            for (var key in grouped_rows) {
                if (grouped_rows.hasOwnProperty(key)) {
                    console.log('key: %s, sending value: %s', key, JSON.stringify(grouped_rows[key]));
                    //console.log('sending: %s', JSON.stringify(grouped_rows[key])));
                    wss.clients.forEach(function each(client) {
                        if (client.readyState === WebSocket.OPEN) {
                            // send data to client to custom webpath: /data
                            client.send(JSON.stringify(grouped_rows[key]));
                        }
                    });
                }
            }

        } else {
            console.log('no new rows')
        }
    });
}

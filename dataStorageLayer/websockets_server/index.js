const express = require('express');
const app = express();
const server = require('http').createServer(app);
const WebSocket = require('ws');
const hbase = require('hbase');
const client = hbase({ host: '127.0.0.1', port: 8080 });

var tables = {
    '/raw/temperature': {name: 'rawData', startRow: '0000000000'},
    '/raw/energy/HVAC': {name: 'rawData', startRow: '0000000000'},
    '/raw/energy/MiAC': {name: 'rawData', startRow: '0000000000'},
    '/raw/water': {name: 'rawData', startRow: '0000000000'},
    '/agg': {name: 'aggregatedData', startRow: '0000000000'},
    '/late': {name: 'lateData', startRow: '0000000000'},
    '/raw/daily': {name: 'rawData', startRow: '0000000000'}
}

const wss = new WebSocket.Server({ server: server });
const clients = {};

wss.on('connection', (ws, req) => {
    console.log('New connection established');
    const path = req.url;

    if (tables.hasOwnProperty(path)) {
        if (!clients[path]) {
            clients[path] = new Set();
        }
    } else {
        console.log('req path invalid: %s', req.url);
        ws.close();
        return;
    }

    clients[path].add(ws);

    ws.on('error', function (error) {
        console.error(error);
    });

    // run function periodically.
    setInterval(function () {
        // iterate over tables.
        //for (var key in tables) {
        if (tables.hasOwnProperty(path)) {
            console.log('querying: %s with startRow: %s', tables[path].name, tables[path].startRow);
            handle_new_rows(tables[path], path);
        }
        //}
    }, 1000);
});

app.get('/', (req, res) => res.send('Hello World!'))
server.listen(1234, () => console.log('Listening on port 1234!'));

// function scans table, checks if there are new rows and sends them to the client.
function handle_new_rows (table, path) {
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
            if (! (table.startRow == '0000000000')) {
            // group rows by key.
            var grouped_rows = {};
            rows.forEach(function (row) {
                if (grouped_rows[row.key] == undefined) {
                    //check if row.key contains TH1 or TH2, and path is /raw/TH1.
                    conditions = (
                        (path == '/raw/temperature' && (row.key.includes('TH1') || row.key.includes('TH2'))) ||
                        (path == '/raw/energy/HVAC' && (row.key.includes('HVAC1') || row.key.includes('HVAC2'))) ||
                        (path == '/raw/energy/MiAC' && (row.key.includes('MiAC1') || row.key.includes('MiAC2'))) ||
                        (path == '/raw/daily' && (row.key.includes('Etot') || row.key.includes('Wtot'))) ||
                        (path == '/raw/water' && (row.key.includes('W1'))) ||
                        (path == '/agg') || (path == '/late')
                    );
                    if (!conditions) {
                        return
                    }
                    grouped_rows[row.key] = {measurement: null, value: null, timestamp: null};
                }
                if (row.column == 'cf:sensor') {
                    grouped_rows[row.key].measurement = row.$;
                } else if (row.column == 'cf:value') {
                    grouped_rows[row.key].value = row.$;
                } else if (row.column == 'cf:datetime') {
                    grouped_rows[row.key].timestamp = row.$;
                } else {
                    console.error('Unknown column: %s', row.column);
                }
            });
            
            console.log('grouped_rows: %s', JSON.stringify(grouped_rows));
            }

            console.log('Old start row: %s', table.startRow);
            table.startRow = last_row.key + '0';
            console.log('New start row: %s', table.startRow);

            // send data in the format: {measurement: 'measurement1', value: 1, timestamp: 123456789}
            for (var key in grouped_rows) {
                if (grouped_rows.hasOwnProperty(key)) {
                    console.log('key: %s, sending value: %s', key, JSON.stringify(grouped_rows[key]));
                    //console.log('sending: %s', JSON.stringify(grouped_rows[key])));
                    clients[path].forEach(function each(client) {
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

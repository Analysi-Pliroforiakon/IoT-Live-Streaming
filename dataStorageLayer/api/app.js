const express = require("express");
const bodyParser = require("body-parser");

const hbase = require("hbase");

const app = express();

app.use(bodyParser.json());

app.get("/:table/:sensor", async (req, res) => {
  try {
    const client = hbase({ host: "localhost", port: 8080 });
    const table = req.params.table;
    const sensor = req.params.sensor;
    // handle errors form request
    if (!table || !sensor) {
      res.send("Table or sensor not provided");
      return;
    }
    // else valid request
    console.log("GET request received", table, sensor);
    // create result array
    let result = [];

    // get all rows from table where sensor = sensor
    await new Promise(async (resolve, reject) => {
      client.table(table).scan(
        {

        },
        (err, rows) => {
          if (err) {
            console.log("Error", err);
          }
          if (!rows || rows.length === 0) {
            console.log("No rows found");
            return;
          }
          console.log("Rows found", rows.length);
          let groupedRows = {};
          rows.forEach((row) => {
            
            // parse rows
            const key = row.key;
            const column = row.column.split(":")[1];
            const value = row.$;
            
            // console.log("Row", row);
            // grou by key
            if (!groupedRows[key]) {
              groupedRows[key] = {};
            }
            if (column === "sensor") {
              groupedRows[key].sensor = value;
            } else if (column === "value") {
              groupedRows[key].value = value;
            } else if (column === "datetime") {
              groupedRows[key].datetime = value;
            }
            if (column === "sensor" && value === sensor) {
                // append to result
                result.push(groupedRows[key]);
            }
            
            
          });
          resolve();
        }
      );
    });

    console.log("Result", result.length);
    // send it to read by grafana
    res.send(JSON.stringify(result));
  } catch (err) {
    console.log("Error", err);
    res.send(err);
  }
});

module.exports = app;

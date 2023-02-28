const app = require("./app");

const port = 1235;
app.listen(process.env.port || port, () => {
    console.log(`Server is listening on https://localhost:${port}`);
  });

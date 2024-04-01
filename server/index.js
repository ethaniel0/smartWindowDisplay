const express = require('express')
const app = express()
const port = 3000

app.use(express.static('static'));

// app.get('/', (req, res) => {
//   res.send('Hello World!')
// })

app.listen(port, () => {
  console.log(`Example app listening on port http://localhost:${port}`)
})
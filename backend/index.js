require("dotenv").config()
const express = require("express")
const http = require("http")

const port = process.env.PORT || 3000

const app = express()
app.use(express.json())

const dbConnect = require("./config/database")
dbConnect()

const socketHandler = require("./websockets/socket_handler")
const server = http.createServer(app)
socketHandler(server)

server.listen(port, () => {
    console.log("Server and websocket running at port " + port)
})
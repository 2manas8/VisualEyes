const socketIo = require("socket.io")

const socketHandler = (server) => {
    const io = socketIo(server)

    io.on("connect", (socket) => {
        console.log("New node is connected")
        require("./room_socket")(socket)
        socket.on("diconnect", () => {
            console.log("Node disconnected")
        })
    })
}

module.exports = socketHandler
const Frame = require("../models/frame")

const roomSocket = (socket) => {
    socket.on("joinRoom", (roomId) => {
        socket.join(roomId)
        socket.emit("A node has joined the room " + roomId)
        console.log("A node has joined the room " + roomId)
    })
    socket.on("leaveRoom", (roomId) => {
        socket.emit("A node has left the room " + roomId)
        console.log("A node has left the room " + roomId)
        socket.leave(roomId)
    })
    socket.on("sendFrame", (data) => {
        const roomId = data.roomId
        const frame = data.frame
        const objects = data.objects
        try {
            Frame.create({
                roomId: roomId,
                frame: frame,
                objects: objects
            })
            socket.to(roomId).emit("receiveFrame", {
                frame: frame,
                objects: objects
            })
            console.log("Frame saved")
        } catch(error) {
            console.error("Error saving frame:", error)
        }
    })
    socket.on("sendIp", (data) => {
        const roomId = data.roomId
        const ip = data.ip
        socket.to(roomId).emit("receiveIp", {
            ip: ip
        })
        console.log("IP updated")
    })
}

module.exports = roomSocket
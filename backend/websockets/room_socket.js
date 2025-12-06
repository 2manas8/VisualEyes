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
        let message = "No objects detected"
        if (objects.length > 5) {
            message = "A lot of objects detected"
        } else if (objects.length > 0) {
            const names = [...objects]
            let formattedList = ""
            if (names.length === 1) {
                formattedList = names[0]
            } else {
                const last = names.pop()
                formattedList = names.join(', ') + " and " + last
            }
            message = formattedList.charAt(0).toUpperCase() + formattedList.slice(1) + " detected"
        }
        try {
            Frame.create({
                roomId: roomId,
                frame: frame,
                objects: objects
            })
            socket.to(roomId).emit("receiveFrame", {
                message: message,
                frame: frame
            })
            console.log("Frame saved")
        } catch(error) {
            console.error("Error saving frame:", error)
        }
    })
    // socket.on("sendIp", (data) => {
    //     const roomId = data.roomId
    //     const ip = data.ip
    //     socket.to(roomId).emit("receiveIp", {
    //         ip: ip
    //     })
    //     console.log("IP updated")
    // })
}

module.exports = roomSocket
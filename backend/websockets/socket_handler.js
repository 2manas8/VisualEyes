const socketIo = require("socket.io")
const fs = require("fs")
const path = require("path")

let io

const socketHandler = (server) => {
    io = socketIo(server)

    io.on("connect", (socket) => {
        console.log("New node is connected")
        require("./room_socket")(socket)
        socket.on("diconnect", () => {
            console.log("Node disconnected")
        })
    })
}

const stop = (roomId) => {
    const audioPath = path.join(__dirname, "../../assets/audio")
    const audioPlaylist = ["stop.mp3"]
    
    const audioData = audioPlaylist.map(fileName => {
        try {
            const filePath = path.join(audioPath, fileName);
            const fileBuffer = fs.readFileSync(filePath);
            return fileBuffer.toString('base64');
        } catch (err) {
            console.error(`Error reading audio file ${fileName}:`, err.message);
            return null; 
        }
    }).filter(data => data !== null)
    
    io.to(roomId).emit("stop", {
        roomId: roomId,
        audio: audioData
    })
    console.log("Stop audio signal sent to room " + roomId)
}

const start = (roomId) => {
    io.to(roomId).emit("start", {
        roomId: roomId
    })
    console.log("Start audio signal sent to room " + roomId)
}

module.exports = socketHandler
module.exports.stop = stop
module.exports.start = start
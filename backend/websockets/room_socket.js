const Frame = require("../models/frame")
const fs = require("fs")
const path = require("path")

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
        const direction = data.direction
        const audioPath = path.join(__dirname, "../../assets/audio")
        let message = ""
        if(objects.length === 0) {
            message = "No objects detected"
        }
        if(objects.length > 5) {
            message = "A lot of objects detected"
        } else {
            const names = [...objects]
            let formattedList = ""
            if (names.length === 1) {
                formattedList = names[0]
            } else {
                const lastText = names.pop();
                formattedList = names.join(', ') + " and " + lastText;
            }
            message = formattedList.charAt(0).toUpperCase() + formattedList.slice(1) + " detected"
        }

        const audioFile = direction.toLowerCase().replace(/ /g, '_') + ".mp3"
        const audioData = []
        try {
            const fileBuffer = fs.readFileSync(path.join(audioPath, audioFile))
            audioData.push(fileBuffer.toString('base64'))
        } catch (err) {
            console.error(`Error reading audio file ${audioFile}:`, err.message)
        }
        try {
            Frame.findOneAndUpdate(
                {roomId: roomId},
                {
                    roomId: roomId,
                    frame: frame,
                    objects: objects,
                    enableNavigation: data.enableNavigation
                },
                {upsert: true, new: true, setDefaultsOnInsert: true}
            )
            socket.to(roomId).emit("receiveFrame", {
                message: message,
                frame: frame,
                audio: audioData,
                enableNavigation: data.enableNavigation
            })
            console.log("Frame saved")
        } catch(error) {
            console.error("Error saving frame:", error)
        }
    })
}

const stop = (io, roomId) => {
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

module.exports = roomSocket
module.exports.stop = stop
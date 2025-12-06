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
        const audioPath = path.join(__dirname, "../../assets/audio")
        let message = ""
        let audioPlaylist = []
        if(objects.length === 0) {
            message = "No objects detected"
            audioPlaylist.push("no_objects.mp3")
        }
        if(objects.length > 5) {
            message = "A lot of objects detected"
            audioPlaylist.push("a_lot_of_objects.mp3")
        } else {
            const names = [...objects]
            let formattedList = ""
            const fileNames = objects.map(name => 
                name.toLowerCase().replace(/ /g, '_') + ".mp3"
            )
            if (names.length === 1) {
                formattedList = names[0]
                audioPlaylist.push(fileNames[0])
            } else {
                const lastText = names.pop();
                formattedList = names.join(', ') + " and " + lastText;
                const lastFile = fileNames.pop();
                fileNames.forEach(file => audioPlaylist.push(file));
                audioPlaylist.push("and.mp3");
                audioPlaylist.push(lastFile);
            }
            message = formattedList.charAt(0).toUpperCase() + formattedList.slice(1) + " detected"
            audioPlaylist.push("detected.mp3")
        }
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
        try {
            Frame.create({
                roomId: roomId,
                frame: frame,
                objects: objects
            })
            socket.to(roomId).emit("receiveFrame", {
                message: message,
                frame: frame,
                audio: audioData
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
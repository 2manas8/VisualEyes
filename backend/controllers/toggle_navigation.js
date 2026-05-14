const Frame = require("../models/frame")
const { getIO } = require("../websockets/socket_handler")
const { stop } = require("../websockets/room_socket")

exports.toggleNavigation = async (req, res) => {
    try {
        const roomId = req.body.roomId
        if(!roomId) {
            return res.status(400).json({message: "No room ID provided"})
        }
        const enableNavigation = req.body.enableNavigation
        await Frame.findOneAndUpdate(
            {roomId: roomId},
            {enableNavigation: enableNavigation},
            {new: true, sort: {_id: -1}}
        )
        
        if (!enableNavigation) {
            const io = getIO()
            if (io) {
                stop(io, roomId)
            }
        }
        
        res.status(200).json({message: "Navigation setting updated"})
        console.log("Navigation setting updated for room " + roomId)
    } catch(error) {
        console.log(error)
        res.status(500).json({message: "Internal server error"})
    }
}
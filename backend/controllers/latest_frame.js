const Frame = require("../models/frame")

exports.latestFrame = async (req, res) => {
    try {
        const roomId = req.query.roomId
        if(!roomId) {
            return res.status(400).json({message: "No room ID provided"})
        }
        const frame = await Frame.findOne({roomId: roomId}).sort({timestamp: -1})
        res.status(200).json({
            message: "Frame found",
            frame: frame
        })
    } catch(error) {
        console.log(error)
        res.status(500).json({message: "Internal server error"})
    }
}
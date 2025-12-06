const Frame = require("../models/frame")

exports.latestFrame = async (req, res) => {
    try {
        const roomId = req.query.roomId
        if(!roomId) {
            return res.status(400).json({message: "No room ID provided"})
        }
        const frame = await Frame.findOne({roomId: roomId}).sort({_id: -1})
        if (!frame) {
            return res.status(404).json({message: "No frame found for this room"});
        }
        let message = "No objects detected"
        const objects = frame.objects || []
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
        res.status(200).json({
            message: message,
            frame: frame.frame
        })
    } catch(error) {
        console.log(error)
        res.status(500).json({message: "Internal server error"})
    }
}
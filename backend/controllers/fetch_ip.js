const Ip = require("../models/ip")

exports.fetchIp = async (req, res) => {
    try {
        const roomId = req.query.roomId
        if(!roomId) {
            return res.status(400).json({message: "No room ID provided"})
        }
        const ip = await Ip.findOne({roomId: roomId}).sort({_id: -1})
        if(!ip) {
            return res.status(400).json({message: "No IP for the provided room ID exists"})
        }
        res.status(200).json({
            message: "IP found",
            ip: ip.ip
        })
    } catch(error) {
        console.log(error)
        res.status(500).json({message: "Internal server error"})
    }
}
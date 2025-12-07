const Ip = require("../models/ip")

exports.saveIp = async (req, res) => {
    try {
        const roomId = req.body.roomId
        const ip = req.body.ip
        await Ip.deleteMany({roomId: roomId})
        const newIp = await Ip.create({
            roomId: roomId,
            ip: ip
        })
        res.status(200).json({message: "IP was updated"})
        console.log("IP updated for room " + roomId)
    } catch(error) {
        console.log(error)
        res.status(500).json({message: "Internal server error"})
    }
}
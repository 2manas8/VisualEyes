const mongoose = require("mongoose")

const IpSchema = new mongoose.Schema({
    roomId: String,
    ip: String
})

const Ip = mongoose.model("IpCollections", IpSchema)

module.exports = Ip
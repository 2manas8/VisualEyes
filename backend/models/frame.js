const mongoose = require("mongoose")

const FrameSchema = new mongoose.Schema({
    roomId: String,
    frame: String,
    objects: [String]
})

const Frame = mongoose.model("FrameCollection", FrameSchema)

module.exports = Frame
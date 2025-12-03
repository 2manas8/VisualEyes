const mongoose = require("mongoose")

const FrameSchema = new mongoose.Schema({
    roomId: String,
    frame: String,
    objects: [String],
    timeStamp: {
        type: Date,
        default: Date.now
    }
})

const Frame = mongoose.model("FrameCollection", FrameSchema)

module.exports = Frame
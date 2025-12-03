const router = require("express").Router()

const {latestFrame} = require("../controllers/latest_frame")
router.get("/latest_frame", latestFrame)

module.exports = router
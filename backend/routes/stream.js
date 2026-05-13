const router = require("express").Router()

const {saveIp} = require("../controllers/save_ip")
router.post("/save_ip", saveIp)

const {fetchIp} = require("../controllers/fetch_ip")
router.get("/fetch_ip", fetchIp)

const {toggleNavigation} = require("../controllers/toggle_navigation")
router.post("/navigation", toggleNavigation)

module.exports = router
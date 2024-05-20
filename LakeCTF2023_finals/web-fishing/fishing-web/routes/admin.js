const express = require('express');
const router = express.Router();
const User = require('../models/user');
FLAG = process.env.FLAG || "EPFL{fake_flag}"

// Only administrators from there
router.use(async (req, res, next) => {
    if (!req.session.user || !(await User.findByUsername(req.session.user)) || !((await User.findByUsername(req.session.user)).permissions.includes('administrator'))) {
        return res.status(401).send('Unauthorized');
    }
    next();
});

router.get('/flag', async (req, res) => {
    res.render('flag', {flag: FLAG});
})


module.exports = router;
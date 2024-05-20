const express = require('express');
const User = require('../models/user');

const router = express.Router();

// Only moderators from there
router.use(async (req, res, next) => {
    if (!req.session.user || !(await User.findByUsername(req.session.user)) || !((await User.findByUsername(req.session.user)).permissions.includes('moderator'))) {
        return res.status(401).send('Unauthorized');
    }
    next();
});

router.post('/promote', async (req, res) => {
    const user = req.body.username;
    const permission = req.body.permission;
    if (typeof user !== 'string' || typeof permission !== 'string') {
        return res.status(400).send('{"error":"Bad Request"}');
    }
    if (permission.includes('administrator')) {
        return res.status(500).send('{"error":"Not allowed"}');
    }
    const currentPermissions = JSON.parse((await User.findByUsername(user)).permissions);
    const newPermissions = JSON.stringify([...currentPermissions, permission]);
    User.editPermission(user, newPermissions).then(() => {
        res.status(200).send('{}');
    }).catch(() => {
        res.status(500).send('{"error":"Internal Server Error"}');
    });
});

router.get('/logs', async (req, res) => {
    const logs = "Not implemented yet"
    res.render('logs', logs);
});

module.exports = router;

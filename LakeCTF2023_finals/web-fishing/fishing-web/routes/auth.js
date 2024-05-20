const express = require('express');
const bcrypt = require('bcrypt');
const User = require('../models/user');
const crypto = require('crypto')

const router = express.Router();

router.get('/login', (req, res) => {
    res.render('login');
});

router.post('/login', async (req, res) => {
    const { username, password } = req.body;
    if (typeof username !== 'string' || typeof password !== 'string') {
        return res.status(400).send('{"error":"Bad Request"}');
    }
    try {
        let user = await User.findByUsername(username);
        if (!user) {
            user = {}
            user.permissions = JSON.stringify(["user"])
            user.password = "$2b$10$XeKD8ih3RR3aZUA7iHhZfe.MiOKRfkf7ViY0qr2h2lv/AD9OU2msK" // error out but keep the bcrypt check to avoid side channel, this hash is not brute-foceable
        }
        user.permissions = JSON.parse(user.permissions)
        const match = await bcrypt.compare(password, user.password);
        if (match && user.ip == req.socket.remoteAddress.replace(/^.*:/, '')) {
            req.session.user = user.username;
            return res.status(200).send("{}");
        } else {
            return res.status(401).send('{"error":"Invalid username or password or ip"}');
        }
    } catch (error) {
        console.error(error);
        res.status(500).send('{"error":"Internal Server Error"}');
    }
});

router.get('/register', (req, res) => {
    res.render('register');
});

router.post('/register', async (req, res) => {
    const { username } = req.body;
    if (typeof username !== 'string') {
        return res.status(400).send('{"error":"Bad Request"}');
    }
    const password = crypto.randomBytes(16).toString('hex');
    try {
        //check if user exists
        const user = await User.findByUsername(username);
        if (user) {
            return res.status(400).send('{"error":"User already exists"}');
        }
        const hashedPassword = await bcrypt.hash(password, 10);
        permissions = JSON.stringify(["user"])
        await User.create(username, hashedPassword, permissions, req.socket.remoteAddress.replace(/^.*:/, ''));
        res.status(200).send('{"password":"' + password + '"}');
    } catch (error) {
        console.error(error);
        res.status(500).send('{"error":"Internal Server Error"}');
    }
});

module.exports = router;

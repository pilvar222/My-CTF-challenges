const express = require('express');
const Post = require('../models/post');
const User = require('../models/user');
const { parse } = require('tldts');
const { JSDOM } = require('jsdom');

const router = express.Router();

// create new post page
router.get('/', async (req, res) => {
    res.render('new-post');
});

// Get a specific post
router.get('/:postId', async (req, res) => {
    const postId = req.params.postId;
    const isAuth = req.session.user && (await User.findByUsername(req.session.user)) && (await User.findByUsername(req.session.user)).permissions.includes('user')
    const isMod = req.session.user && (await User.findByUsername(req.session.user)) && (await User.findByUsername(req.session.user)).permissions.includes('moderator')
    try {
        const post = await Post.getById(postId);
        if (!post) {
            return res.status(404).send('Post not found');
        }

        const dom = new JSDOM("<p id=content>"+post.content+"</p>");
        const content = dom.window.document.getElementById('content');
        content.querySelectorAll('a').forEach(a => {
            try {
                if (parse(a.href).hostname !== parse(req.headers.host).hostname && !isAuth) {
                    a.text = "[Login to view this content]"
                    a.href = "/login";
                }
            } catch (e) {
                a.innerText = "[Login to view this content]"
                a.href = "/login";
            }
        });

        res.render('post', { post, content: content.innerHTML, isMod });
    } catch (error) {
        console.error(error);
        return res.status(500).send('Internal Server Error');
    }
});

// Only auth user from there
router.use(async (req, res, next) => {
    if (!req.session.user || !(await User.findByUsername(req.session.user)) || !((await User.findByUsername(req.session.user)).permissions.includes('user'))) {
        return res.status(401).send('Unauthorized');
    }
    next();
});

// Create a new post
router.post('/', async (req, res) => {
    const { title, content } = req.body;
    if (typeof title !== 'string' || typeof content !== 'string') {
        return res.status(400).send('{"error":"Bad Request"}');
    }
    const author = req.session.user;
    try {
        const postId = await Post.create(title, author, content, req.socket.remoteAddress.replace(/^.*:/, ''));
        return res.status(200).send(`{"postId":"${postId}"}`);
    } catch (error) {
        console.error(error);
        return res.status(500).send('{"error":"Internal Server Error"}');
    }
});

// Only moderators from there
router.use(async (req, res, next) => {
    if (!req.session.user || !(await User.findByUsername(req.session.user)) || !((await User.findByUsername(req.session.user)).permissions.includes('moderator'))) {
        return res.status(401).send('Unauthorized');
    }
    next();
});

// Approve an existing post
router.post('/:postId', async (req, res) => {
    const postId = req.params.postId;
    const { not_a_csrf } = req.body;
    if (typeof postId !== 'string' || not_a_csrf !== true) {
        return res.status(400).send('{"error":"Bad Request"}');
    }
    try {
        const result = await Post.approve(postId);
        if (result === 0) {
            return res.status(404).send('{"error":"Post not found"}');
        }
        return res.status(200).send("{}");
    } catch (error) {
        console.error(error);
        return res.status(500).send('{"error":"Internal Server Error"}');
    }
});

module.exports = router;

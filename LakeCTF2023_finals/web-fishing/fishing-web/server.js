const express = require('express');
const session = require('express-session');
const FileStore = require('session-file-store')(session);
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

app.use(session({
    store: new FileStore(),
    secret: process.env.SECRET || 'your_secret_key',
    resave: false,
    saveUninitialized: true,
    cookie: { sameSite: "strict", httpOnly: true}
}));

app.use((req, res, next) => {
    const session = req.session;
    if (session.ip) {
        if (session.ip !== req.socket.remoteAddress.replace(/^.*:/, '')) {
            return res.status(403).send('Unauthorized');
        }
    } else {
        req.session.ip = req.socket.remoteAddress.replace(/^.*:/, '');
    }
    next();
})

app.use('/', require('./routes/auth'));
app.use('/posts', require('./routes/posts'));
app.use('/moderator', require('./routes/moderator'));
app.use('/admin', require('./routes/admin'));
const router = express.Router();

router.get('/', async (req, res) => {
    res.render('index', { user: req.session.user });
});


app.use(router)

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

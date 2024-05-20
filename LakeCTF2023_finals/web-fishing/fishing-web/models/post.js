const sqlite3 = require('sqlite3').verbose();
const crypto = require('crypto')
const db = new sqlite3.Database('./db.sqlite');
const createDOMPurify = require('dompurify');
const { JSDOM } = require('jsdom');


const createPostTable = () => {
    const createPostTableQuery = `
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT NOT NULL PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            content TEXT NOT NULL,
            approved BOOLEAN DEFAULT 0
        )
    `;
    db.run(createPostTableQuery);
};

const Post = {
    create: (title, author, content) => {
        id = crypto.randomBytes(16).toString('hex')
        const insertPostQuery = `
            INSERT INTO posts (id, title, author, content, approved) VALUES (?, ?, ?, ?, ?)
        `;
        const window = new JSDOM('').window;
        const DOMPurify = createDOMPurify(window);
        const sanitizedContent = DOMPurify.sanitize(content, {ALLOWED_TAGS: ['a'], ALLOWED_ATTR: ['href']});
        return new Promise((resolve, reject) => {
            db.run(insertPostQuery, [id, title, author, sanitizedContent, false], function (err) {
                if (err) {
                    reject(err);
                } else {
                    resolve(id);
                }
            });
        });
    },
    getById: (postId) => {
        const getPostByIdQuery = `
            SELECT * FROM posts WHERE id = ?
        `;
        return new Promise((resolve, reject) => {
            db.get(getPostByIdQuery, [postId], (err, row) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(row);
                }
            });
        });
    },
    approve: (postId) => {
        const updatePostQuery = `
            UPDATE posts SET approved = ? WHERE id = ?
        `;
        return new Promise((resolve, reject) => {
            db.run(updatePostQuery, [true, postId], function (err) {
                if (err) {
                    reject(err);
                } else {
                    resolve(this.changes);
                }
            });
        });
    }
};

createPostTable();

module.exports = Post;

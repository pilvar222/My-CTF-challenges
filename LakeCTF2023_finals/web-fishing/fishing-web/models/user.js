const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const bcrypt = require('bcrypt');

const db = new sqlite3.Database('db.sqlite');

MODERATOR_USERNAME = process.env.MODERATOR_USERNAME || "moderator"
MODERATOR_PASSWORD_HASH = process.env.MODERATOR_PASSWORD_HASH || "$2b$10$U/qyLkYx0mZVciZQJmz31e14cYIy8opAhAi/yJxVW0AvnJpkKYsFW" // await bcrypt.hash("password", 10)
MODERATOR_IP = process.env.MODERATOR_IP || "172.16.238.10"

const createUserTable = async () => {
    const createUserTableQuery = `
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            permissions TEXT NOT NULL,
            ip TEXT NOT NULL
        );
    `;
    db.run(createUserTableQuery);
    await new Promise(resolve => setTimeout(resolve, 1000));
    User.findByUsername(MODERATOR_USERNAME).then(user => {
    if (!user) {
      db.run(`INSERT INTO users (username, password, permissions, ip) VALUES ('${MODERATOR_USERNAME}', '${MODERATOR_PASSWORD_HASH}', '["user", "moderator"]', '${MODERATOR_IP}');`)
        }
    });
};

const User = {
    create: (username, password, permissions, ip) => {
        const insertUserQuery = `
            INSERT INTO users (username, password, permissions, ip) VALUES (?, ?, ?, ?)
        `;
        return new Promise((resolve, reject) => {
            db.run(insertUserQuery, [username, password, permissions, ip], function (err) {
                if (err) {
                    reject(err);
                } else {
                    resolve(this.lastID);
                }
            });
        });
    },
    findByUsername: (username) => {
        const findUserQuery = `
            SELECT * FROM users WHERE username = ?
        `;
        return new Promise((resolve, reject) => {
            db.get(findUserQuery, [username], (err, row) => {
                if (err) {
                    reject(err);
                } else {
                    if (row === undefined) {
                        resolve(undefined)
                    } else {
                        resolve(row);
                    }
                }
            });
        });
    },
    editPermission: (username, permissions) => {
        const addPermissionQuery = `
            UPDATE users SET permissions = ? WHERE username = ?
        `;
        return new Promise((resolve, reject) => {
            db.run(addPermissionQuery, [permissions, username], function (err) {
                if (err) {
                    reject(err);
                } else {
                    resolve(this.changes);
                }
            });
        });
    },
};

createUserTable();

module.exports = User;

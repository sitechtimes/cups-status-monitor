DROP TABLE IF EXISTS admin;

CREATE TABLE admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email_encrypted BLOB NOT NULL,
    email_hash TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
)

CREATE INDEX idx_users_email_hash ON users(email_hash);
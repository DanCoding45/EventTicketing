-- DROP TABLE IF EXISTS users;
-- DROP TABLE IF EXISTS event_hosts;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS event_hosts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    primary_host TEXT NOT NULL,
    host_email TEXT NOT NULL,
    organization_name TEXT UNIQUE NOT NULL,
    organization_address TEXT NOT NULL,
    organization_email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);


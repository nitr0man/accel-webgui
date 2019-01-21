CREATE TABLE user (
    id INTEGER PRIMARY KEY NOT NULL,
    login CHAR(32) NOT NULL,
    password TEXT NOT NULL,
    superuser boolean NOT NULL DEFAULT 0,
    created TIMESTAMP,
    updated TIMESTAMP,
    UNIQUE (login)
    );

CREATE TRIGGER insert_user_created
AFTER INSERT ON user

BEGIN
    UPDATE user
    SET created = DATETIME ('now')
    WHERE id = new.id;
END;

CREATE TRIGGER update_user_modifies
AFTER UPDATE ON user

BEGIN
    UPDATE user
    SET updated = DATETIME ('now')
    WHERE id = new.id;
END;


CREATE TABLE options (
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    PRIMARY KEY (key),
    UNIQUE (key)
    );

INSERT INTO options (
    key,
    value
    )
VALUES (
    'hostname',
    'Accel-PPP NAS'
    ),
    (
    'accel_host',
    '127.0.0.1'
    ),
    (
    'accel_port',
    '2001'
    ),
    (
    'accel_password',
    ''
    ),
    (
    'db_version',
    '1'
    );

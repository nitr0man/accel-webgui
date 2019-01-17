CREATE TABLE user (
    id INT auto_increment,
    LOGIN CHAR(32) NOT NULL,
    password TEXT NOT NULL,
    superuser boolean NOT NULL DEFAULT 0,
    created DATE,
    updated DATE,
    PRIMARY KEY (id),
    UNIQUE (LOGIN)
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
    id INT auto_increment,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    PRIMARY KEY (id),
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
    'accel_port',
    '2000'
    ),
    (
    'db_version',
    '1'
    );

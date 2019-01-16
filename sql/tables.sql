CREATE TABLE user (
    id int auto_increment,
    login char(32) not null,
    password text not null,
    created date,
    primary key(id),
    unique (login)
);

CREATE TRIGGER insert_user_created after insert on user
begin
update user set created = datetime('now')
where id = new.id;
end;

CREATE TABLE options (
    id int auto_increment,
    key text not null,
    value text not null,
    primary key(id),
    unique (key)
);

INSERT INTO options (key, value) VALUES
    ('hostname', 'Accel-PPP NAS'),
    ('accel_port', '2000');
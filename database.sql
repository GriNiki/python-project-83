DROP TABLE IF EXISTS urls;
DROP TABLE IF EXISTS url_checks;

CREATE TABLE urls (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR UNIQUE,
    created_at TIMESTAMP NOT NULL
    );

CREATE TABLE url_checks (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id bigint,
    status_code integer,
    h1 varchar(255),
    title varchar(255),
    description text,
    created_at timestamp
);
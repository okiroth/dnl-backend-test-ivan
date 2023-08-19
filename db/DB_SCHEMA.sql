DROP TABLE IF EXISTS model_parts;
DROP TABLE IF EXISTS models;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS brands;

CREATE TABLE brands (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    url VARCHAR(255)
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    brand_id INT REFERENCES brands(id),
    name VARCHAR(255),
    url VARCHAR(255)
);

CREATE TABLE models (
    id SERIAL PRIMARY KEY,
    category_id INT REFERENCES categories(id),
    name VARCHAR(255),
    url VARCHAR(255)
);

CREATE TABLE model_parts (
    id SERIAL PRIMARY KEY,
    model_id INT REFERENCES models(id),
    code VARCHAR(255),
    name VARCHAR(255),
    url VARCHAR(255)
);

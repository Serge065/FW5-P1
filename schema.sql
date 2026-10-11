CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    CONSTRAINT authors_name_not_empty CHECK (length(trim(name)) > 0),
    CONSTRAINT authors_lastname_not_empty CHECK (length(trim(lastname)) > 0)
);

CREATE INDEX idx_authors_name_trgm ON authors USING gin (name gin_trgm_ops);
CREATE INDEX idx_authors_lastname_trgm ON authors USING gin (lastname gin_trgm_ops);

CREATE TABLE collections (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL UNIQUE,
    description TEXT NOT NULL DEFAULT '',
    CONSTRAINT collections_name_not_empty CHECK (length(trim(name)) > 0)
);

CREATE TABLE conditions (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50)  NOT NULL UNIQUE,
    label VARCHAR(100) NOT NULL,
    needs_restoration BOOLEAN NOT NULL DEFAULT FALSE,
    needs_check BOOLEAN NOT NULL DEFAULT FALSE
);

INSERT INTO conditions (id, code, label, needs_restoration, needs_check) VALUES
    (1, 'отличное', 'Отличное', FALSE, FALSE),
    (2, 'хорошее', 'Хорошее', FALSE, FALSE),
    (3, 'удовлетворительное', 'Удовлетворительное', FALSE, TRUE),
    (4, 'плохое', 'Плохое', TRUE,  FALSE);

SELECT setval('conditions_id_seq', (SELECT MAX(id) FROM conditions));

CREATE TABLE exhibits (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    author_id INT NOT NULL REFERENCES authors(id)     ON DELETE RESTRICT,
    collection_id INT NOT NULL REFERENCES collections(id) ON DELETE RESTRICT,
    condition_id INT NOT NULL REFERENCES conditions(id)  ON DELETE RESTRICT,
    year INT NOT NULL CHECK (year BETWEEN 0 AND 2100),
    price NUMERIC(14, 2) NOT NULL CHECK (price >= 0),
    is_available  BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT exhibits_name_not_empty CHECK (length(trim(name)) > 0)
);

CREATE INDEX idx_exhibits_author ON exhibits(author_id);
CREATE INDEX idx_exhibits_collection ON exhibits(collection_id);
CREATE INDEX idx_exhibits_condition ON exhibits(condition_id);
CREATE INDEX idx_exhibits_price ON exhibits(price);
CREATE INDEX idx_exhibits_coll_avail ON exhibits(collection_id, is_available);
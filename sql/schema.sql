CREATE TABLE IF NOT EXISTS authors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS collections (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS conditions (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    label VARCHAR(100) NOT NULL,
    needs_restoration BOOLEAN DEFAULT FALSE,
    needs_check BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS exhibits (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    author_id INTEGER REFERENCES authors(id) ON DELETE CASCADE,
    collection_id INTEGER REFERENCES collections(id) ON DELETE CASCADE,
    condition_id INTEGER REFERENCES conditions(id),
    year INTEGER NOT NULL,
    price NUMERIC(12, 2) NOT NULL CHECK (price >= 0),
    is_available BOOLEAN DEFAULT TRUE
);

INSERT INTO conditions (id, code, label, needs_restoration, needs_check) VALUES
(1, 'отличное', 'Отличное', FALSE, FALSE),
(2, 'хорошее', 'Хорошее', FALSE, FALSE),
(3, 'удовлетворительное', 'Удовлетворительное', FALSE, TRUE),
(4, 'плохое', 'Плохое', TRUE, FALSE)
ON CONFLICT (id) DO NOTHING;
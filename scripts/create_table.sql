
DROP TABLE IF EXISTS functions;

CREATE TABLE functions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_en TEXT NOT NULL,
    name_th TEXT,
    description_en TEXT,
    description_th TEXT,
    syntax_en TEXT,
    syntax_th TEXT,
    example_en TEXT,
    example_th TEXT
);

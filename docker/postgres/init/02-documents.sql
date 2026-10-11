CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    path TEXT NOT NULL UNIQUE,
    modality TEXT NOT NULL CHECK (modality IN ('text', 'image', 'audio', 'video')),
    embedding VECTOR(768) NOT NULL
);

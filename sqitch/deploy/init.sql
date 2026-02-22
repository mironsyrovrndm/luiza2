-- Deploy psy:init to pg

BEGIN;

CREATE TABLE IF NOT EXISTS site_content (
    key text PRIMARY KEY,
    payload jsonb NOT NULL,
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS records (
    id text PRIMARY KEY,
    date text NOT NULL,
    name text NOT NULL,
    phone text NOT NULL,
    telegram text NOT NULL DEFAULT '',
    complaint text NOT NULL,
    status text NOT NULL DEFAULT 'Новая',
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS photos (
    id text PRIMARY KEY,
    category text NOT NULL CHECK (category IN ('hero', 'about', 'uploads')),
    filename text NOT NULL,
    mime_type text NOT NULL,
    payload bytea NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS photos_category_created_idx ON photos (category, created_at DESC);

COMMIT;

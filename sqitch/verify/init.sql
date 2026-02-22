-- Verify psy:init on pg

BEGIN;

SELECT key, payload FROM site_content WHERE false;
SELECT id, status FROM records WHERE false;
SELECT id, category, filename, mime_type, payload FROM photos WHERE false;

ROLLBACK;

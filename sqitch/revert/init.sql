-- Revert psy:init from pg

BEGIN;

DROP TABLE IF EXISTS photos;
DROP TABLE IF EXISTS records;
DROP TABLE IF EXISTS site_content;

COMMIT;

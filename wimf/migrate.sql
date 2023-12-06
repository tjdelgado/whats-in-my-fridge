PRAGMA foreign_keys = OFF;
BEGIN EXCLUSIVE TRANSACTION;
DROP TABLE IF EXISTS "recipes";
DROP TABLE IF EXISTS "recipes_ingredients";
DROP TRIGGER IF EXISTS "compute_expiry_date";

PRAGMA user_version = 1;

CREATE TABLE "tags" (
    "id" INTEGER PRIMARY KEY,
    "name" TEXT NOT NULL
);

CREATE TABLE "item_tags" (
    "item_id" INTEGER NOT NULL,
    "tag_id" INTEGER NOT NULL,
    FOREIGN KEY("item_id") REFERENCES "items"("id"),
    FOREIGN KEY("tag_id") REFERENCES "tags"("id")
);
COMMIT;
PRAGMA foreign_keys = ON;

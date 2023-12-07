DROP TABLE IF EXISTS "items";
DROP TABLE IF EXISTS "stored_items";
DROP TABLE IF EXISTS "schema_ver";
DROP TABLE IF EXISTS "tags";
DROP TABLE IF EXISTS "item_tags";

PRAGMA user_version = 1;

CREATE TABLE "items" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "quantity" INTEGER DEFAULT 1,
    "expiry_time" INTEGER NOT NULL DEFAULT 0, -- deprecated column
    "date_added" TEXT NOT NULL DEFAULT CURRENT_DATE,
    "expiry_date" TEXT DEFAULT NULL,
    "archived" INTEGER DEFAULT 0
);


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

-- some initial data for items in the fridge

INSERT INTO "items" ("name", "quantity", "expiry_time", "date_added", "expiry_date")
VALUES ("rotten eggs", 1, -1, date(), date('now', '-1 days')),
       ("milk", 2, 2, date(), date('now', '+2 days')),
       ("bread", 3, 7, date(), date('now', '+7 days'));

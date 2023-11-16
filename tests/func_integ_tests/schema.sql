DROP TABLE IF EXISTS "items";
DROP TABLE IF EXISTS "stored_items";
DROP TABLE IF EXISTS "recipes";
DROP TABLE IF EXISTS "recipes_ingredients";

CREATE TABLE "items" (
    "id" INTEGER,
    "name" TEXT NOT NULL,
    "expiry_time" INTEGER NOT NULL,
    "date_added" TEXT NOT NULL DEFAULT CURRENT_DATE,
    "expiry_date" TEXT DEFAULT NULL,
    PRIMARY KEY("id")
);

CREATE TRIGGER compute_expiry_date
AFTER INSERT ON "items"
FOR EACH ROW
WHEN NEW."expiry_date" IS NULL AND "expiry_time" > 0
BEGIN
    UPDATE "items"
    SET "expiry_date" = date('now', '+' || "expiry_time" || ' days')
    WHERE "id" = NEW."id";
END;

CREATE TABLE "stored_items" (
    "id" INTEGER,
    "name" TEXT NOT NULL,
    "expiry_time" INTEGER NOT NULL,
    PRIMARY KEY("id")
);

CREATE TABLE "recipes" (
    "id" INTEGER,
    "name" TEXT NOT NULL,
    PRIMARY KEY("id")
);

CREATE TABLE "recipes_ingredients" (
    "id" INTEGER,
    "recipe_id" INTEGER NOT NULL,
    "ingr_id" INTEGER NOT NULL,
    "ingr_qty" NUMERIC NOT NULL,
    PRIMARY KEY("id"),
    FOREIGN KEY("recipe_id") REFERENCES "recipes"("id"),
    FOREIGN KEY("ingr_id") REFERENCES "stored_items"("id")
);

-- some initial data for items in the fridge

INSERT INTO "items" ("name",
                     "expiry_time")
    VALUES ("eggs", 14),
           ("milk", 7),
           ("bread", 7);

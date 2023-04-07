CREATE VIEW "powers" ( pk VARCHAR PRIMARY KEY, "personal"."hero" VARCHAR, "personal"."power" VARCHAR, "professional"."name" VARCHAR);
SELECT p1."name" as "Name1", p2."name" as "Name2", p1."power" as "Power"
FROM "powers" AS p1
INNER JOIN "powers" AS p2
       ON p1."power" = p2."power"
WHERE p1."hero" = 'yes' AND p2."hero" = 'yes';

CREATE TABLE houses_info AS SELECT * FROM houses;

DO $$
DECLARE
    district houses_info.district%TYPE;

BEGIN
    district := 'Other ';
    FOR counter IN 1..10
        LOOP
            INSERT INTO houses_info(district, year_built)
            VALUES (district, 2021 + counter);
        END LOOP;
END;
$$

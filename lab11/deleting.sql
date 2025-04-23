CREATE OR REPLACE PROCEDURE deleting(dat VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN 
    DELETE FROM contacts WHERE first_name = dat OR phone_number = dat;
END;
$$;

CREATE OR REPLACE PROCEDURE user_update(p_name VARCHAR(255),p_number VARCHAR(255))
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS(SELECT 1 FROM contacts where first_name = p_name) THEN
        UPDATE contacts SET phone_number = p_number WHERE first_name = p_name ;
    ELSE
        INSERT INTO contacts(first_name,phone_number) VALUES (p_name,p_number);
    END IF;  
END $$;
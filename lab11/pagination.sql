CREATE OR REPLACE FUNCTION pagination(p_limit INT , p_offset INT)
RETURNS TABLE(id INT,first_name VARCHAR ,phone_number VARCHAR)
AS $$ 
BEGIN
    RETURN QUERY
    SELECT * FROM contacts ORDER BY id LIMIT p_limit OFFSET p_offset;
END; $$ LANGUAGE plpgsql;
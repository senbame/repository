CREATE OR REPLACE FUNCTION query_by_pattern(p_pattern VARCHAR(255))
RETURNS TABLE(id INT, first_name VARCHAR(255), phone_number VARCHAR(255)) AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM contacts WHERE contacts.first_name LIKE p_pattern OR contacts.phone_number LIKE p_pattern;
END;
$$ LANGUAGE plpgsql;
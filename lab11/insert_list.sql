CREATE TABLE IF NOT EXISTS invalid_log (
    id SERIAL PRIMARY KEY,
    entry TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE PROCEDURE insert_users_batch(
    IN p_names TEXT[], 
    IN p_phones TEXT[], 
    OUT incorrect_entries TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
    phone_regex TEXT := '^\+?\d+$'; -- только цифры
BEGIN
    incorrect_entries := ARRAY[]::TEXT[];

    IF array_length(p_names, 1) IS DISTINCT FROM array_length(p_phones, 1) THEN
        RAISE EXCEPTION 'Arrays must be of equal length';
    END IF;

    FOR i IN 1..array_length(p_names, 1) LOOP
        IF p_phones[i] ~ phone_regex THEN
            BEGIN
                INSERT INTO contacts(first_name, phone_number)
                VALUES (p_names[i], p_phones[i]);
            EXCEPTION
                WHEN unique_violation THEN
                    -- если уже существует пользователь, обновим номер
                    UPDATE contacts
                    SET phone_number = p_phones[i]
                    WHERE first_name = p_names[i];
            END;
        ELSE
            -- добавим некорректную запись в OUT-массив
            incorrect_entries := array_append(incorrect_entries, p_names[i] || ':' || p_phones[i]);

             INSERT INTO invalid_log(entry) VALUES (p_names[i] || ':' || p_phones[i]);
        END IF;
    END LOOP;
END;
$$;

-- 1. Upsert: if contact exists - update phone, if not - insert
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO phonebook(name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;


-- 2. Bulk insert: insert many contacts, validate phone, return invalid ones
CREATE OR REPLACE PROCEDURE insert_many_contacts(
    p_names  VARCHAR[],
    p_phones VARCHAR[]
)
LANGUAGE plpgsql AS $$
DECLARE
    i       INT;
    v_name  VARCHAR;
    v_phone VARCHAR;
BEGIN
    FOR i IN 1 .. array_length(p_names, 1) LOOP
        v_name  := p_names[i];
        v_phone := p_phones[i];

        -- phone validation: must start with + and be 11-12 digits
        IF v_phone ~ '^\+[0-9]{10,11}$' THEN
            CALL upsert_contact(v_name, v_phone);
        ELSE
            RAISE NOTICE 'Invalid phone for %: %', v_name, v_phone;
        END IF;
    END LOOP;
END;
$$;


-- 3. Delete by name or phone
CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook
    WHERE name ILIKE '%' || p_value || '%'
       OR phone = p_value;
END;
$$;
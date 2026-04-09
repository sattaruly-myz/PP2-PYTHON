-- 1. Search contacts by pattern (name or phone)
CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p text)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
        SELECT c.id, c.name, c.phone
        FROM phonebook c
        WHERE c.name ILIKE '%' || p || '%'
           OR c.phone ILIKE '%' || p || '%';
END;
$$ LANGUAGE plpgsql;


-- 2. Paginated query (returns contacts by page)
CREATE OR REPLACE FUNCTION get_contacts_paginated(page_num INT, page_size INT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
        SELECT c.id, c.name, c.phone
        FROM phonebook c
        ORDER BY c.id
        LIMIT page_size
        OFFSET (page_num - 1) * page_size;
END;
$$ LANGUAGE plpgsql;
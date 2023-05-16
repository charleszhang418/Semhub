DROP FUNCTION IF EXISTS QuantifyImpact;
CREATE FUNCTION QuantifyImpact( impact VARCHAR(255) )
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE res INT;
    IF UPPER(impact) = 'LOW' THEN SET res = 1;
    ELSEIF UPPER(impact) = 'MEDIUM' THEN SET res = 3;
    ELSE SET res = 5;
    END IF;
    RETURN res;
END ;

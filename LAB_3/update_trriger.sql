CREATE OR REPLACE FUNCTION role_update() RETURNS TRIGGER AS 
$$
BEGIN
    IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
	NEW.p7 = (SELECT p7_value FROM station_role WHERE role_id IN (SELECT role FROM stations WHERE station_id=NEW.base_station));
    END IF;
RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER p7_update BEFORE INSERT OR UPDATE ON measurments FOR EACH ROW EXECUTE PROCEDURE role_update();


CREATE OR REPLACE FUNCTION check_station() RETURNS TRIGGER AS
$$
DECLARE
     base_station_value int4;
BEGIN 
     IF TG_OP='UPDATE' THEN
	IF OLD.role != NEW.role AND NEW.station_id IN (SELECT base_station FROM Measurments) THEN
		UPDATE measurments SET p7=(SELECT p7_value FROM station_role WHERE role_id=NEW.role) WHERE base_station=NEW.station_id;
	END IF;
     END IF;
RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_stations AFTER UPDATE ON stations FOR EACH ROW EXECUTE PROCEDURE check_station();



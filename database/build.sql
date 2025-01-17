CREATE TABLE IF NOT EXISTS provinces
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS districts
(
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    province_id INT                 NOT NULL,
    FOREIGN KEY (province_id) REFERENCES provinces (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS communes
(
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    district_id INT                 NOT NULL,
    FOREIGN KEY (district_id) REFERENCES districts (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS cities
(
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    commune_id INT                 NOT NULL,
    FOREIGN KEY (commune_id) REFERENCES communes (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS addresses
(
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(255),
    city_id INT,
    FOREIGN KEY (city_id) REFERENCES cities (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS stations
(
    id           SERIAL PRIMARY KEY,
    station_name VARCHAR(255)     NOT NULL,
    latitude     DOUBLE PRECISION NOT NULL,
    longitude    DOUBLE PRECISION NOT NULL,
    address_id   INT,
    FOREIGN KEY (address_id) REFERENCES addresses (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS params
(
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(255)       NOT NULL,
    formula VARCHAR(50)        NOT NULL,
    code    VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS sensors
(
    id           SERIAL PRIMARY KEY,
    station_id   INT,
    parameter_id INT,
    FOREIGN KEY  (station_id) REFERENCES stations (id) ON DELETE CASCADE,
    FOREIGN KEY  (parameter_id) REFERENCES params (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS measurements
(
    id           SERIAL PRIMARY KEY,
    date         TIMESTAMP        NOT NULL,
    value        DOUBLE PRECISION NOT NULL,
    parameter_id INT,
    sensor_id    INT,
    FOREIGN KEY (parameter_id) REFERENCES params (id) ON DELETE CASCADE,
    FOREIGN KEY (sensor_id) REFERENCES sensors (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS air_quality_levels
(
    id         SERIAL PRIMARY KEY,
    level_name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS air_quality
(
    id                    SERIAL PRIMARY KEY,
    station_id            INT,
    calculate_date        TIMESTAMP,
    air_quality_level_id  INT,
    source_date           TIMESTAMP,
    index_status          BOOLEAN,
    critical_param        VARCHAR(50),
    FOREIGN KEY (station_id) REFERENCES stations (id) ON DELETE CASCADE,
    FOREIGN KEY (air_quality_level_id) REFERENCES air_quality_levels (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS air_quality_pollutants
(
    id                   SERIAL PRIMARY KEY,
    air_quality_id       INT NOT NULL,
    parameter_id         INT NOT NULL,
    calculate_date       TIMESTAMP,
    air_quality_level_id INT,
    source_date          TIMESTAMP,
    FOREIGN KEY (air_quality_id) REFERENCES air_quality (id) ON DELETE CASCADE,
    FOREIGN KEY (parameter_id) REFERENCES params (id) ON DELETE CASCADE,
    FOREIGN KEY (air_quality_level_id) REFERENCES air_quality_levels (id) ON DELETE CASCADE
);

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM air_quality_levels LIMIT 1) THEN
        INSERT INTO air_quality_levels (id, level_name)
        VALUES (-1, 'Brak indeksu'),
               (0, 'Bardzo dobry'),
               (1, 'Dobry'),
               (2, 'Umiarkowany'),
               (3, 'Dostateczny'),
               (4, 'Zły'),
               (5, 'Bardzo zły');
    END IF;
END $$;

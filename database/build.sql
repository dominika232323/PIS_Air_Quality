CREATE TABLE provinces
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE districts
(
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) UNIQUE NOT NULL,
    province_id INT                 NOT NULL,
    FOREIGN KEY (province_id) REFERENCES provinces (id) ON DELETE CASCADE
);

CREATE TABLE communes
(
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) UNIQUE NOT NULL,
    district_id INT                 NOT NULL,
    FOREIGN KEY (district_id) REFERENCES districts (id) ON DELETE CASCADE
);

CREATE TABLE cities
(
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(100) UNIQUE NOT NULL,
    commune_id INT                 NOT NULL,
    FOREIGN KEY (commune_id) REFERENCES communes (id) ON DELETE CASCADE
);

CREATE TABLE addresses
(
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(255),
    city_id INT,
    FOREIGN KEY (city_id) REFERENCES cities (id) ON DELETE CASCADE
);

CREATE TABLE stations
(
    id           SERIAL PRIMARY KEY,
    station_name VARCHAR(255)     NOT NULL,
    latitude     DOUBLE PRECISION NOT NULL,
    longitude    DOUBLE PRECISION NOT NULL,
    address_id   INT,
    FOREIGN KEY (address_id) REFERENCES addresses (id) ON DELETE CASCADE
);

CREATE TABLE params
(
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(255)       NOT NULL,
    formula VARCHAR(50)        NOT NULL,
    code    VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE sensors
(
    id         SERIAL PRIMARY KEY,
    station_id INT,
    param_id   INT,
    FOREIGN KEY (station_id) REFERENCES stations (id) ON DELETE CASCADE,
    FOREIGN KEY (param_id) REFERENCES params (id) ON DELETE CASCADE
);

CREATE TABLE measurements
(
    id         SERIAL PRIMARY KEY,
    date       TIMESTAMP        NOT NULL,
    value      DOUBLE PRECISION NOT NULL,
    param_code VARCHAR(50)      NOT NULL,
    sensor_id  INT,
    FOREIGN KEY (param_code) REFERENCES params (code) ON DELETE CASCADE,
    FOREIGN KEY (sensor_id) REFERENCES sensors (id) ON DELETE CASCADE
);

CREATE TABLE air_quality_levels
(
    id         SERIAL PRIMARY KEY,
    level_name VARCHAR(50) NOT NULL
);

CREATE TABLE air_quality
(
    id                  SERIAL PRIMARY KEY,
    station_id          INT,
    calculate_date      TIMESTAMP,
    quality_level       INT,
    source_date         TIMESTAMP,
    so2_calculate_date  TIMESTAMP,
    so2_quality_level   INT,
    so2_source_date     TIMESTAMP,
    no2_calculate_date  TIMESTAMP,
    no2_quality_level   INT,
    no2_source_date     TIMESTAMP,
    pm10_calculate_date TIMESTAMP,
    pm10_quality_level  INT,
    pm10_source_date    TIMESTAMP,
    pm25_calculate_date TIMESTAMP,
    pm25_quality_level  INT,
    pm25_source_date    TIMESTAMP,
    o3_calculate_date   TIMESTAMP,
    o3_quality_level    INT,
    o3_source_date      TIMESTAMP,
    index_status        BOOLEAN,
    critical_param      VARCHAR(50),
    FOREIGN KEY (station_id) REFERENCES stations (id) ON DELETE CASCADE,
    FOREIGN KEY (quality_level) REFERENCES air_quality_levels (id) ON DELETE CASCADE,
    FOREIGN KEY (so2_quality_level) REFERENCES air_quality_levels (id) ON DELETE CASCADE,
    FOREIGN KEY (no2_quality_level) REFERENCES air_quality_levels (id) ON DELETE CASCADE,
    FOREIGN KEY (pm10_quality_level) REFERENCES air_quality_levels (id) ON DELETE CASCADE,
    FOREIGN KEY (pm25_quality_level) REFERENCES air_quality_levels (id) ON DELETE CASCADE,
    FOREIGN KEY (o3_quality_level) REFERENCES air_quality_levels (id) ON DELETE CASCADE
);

INSERT INTO air_quality_levels (id, level_name)
VALUES (-1, 'Brak indeksu'),
       (0, 'Bardzo dobry'),
       (1, 'Dobry'),
       (2, 'Umiarkowany'),
       (3, 'Dostateczny'),
       (4, 'Zły'),
       (5, 'Bardzo zły');

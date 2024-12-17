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
    date       TIMESTAMP,
    value      DOUBLE PRECISION NOT NULL,
    param_code VARCHAR(50)      NOT NULL,
    sensor_id  INT,
    FOREIGN KEY (param_code) REFERENCES params (code) ON DELETE CASCADE,
    FOREIGN KEY (sensor_id) REFERENCES sensors (id) ON DELETE CASCADE
);


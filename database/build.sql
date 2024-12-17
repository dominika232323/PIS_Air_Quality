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
    FOREIGN KEY (province_id) REFERENCES provinces (id)
);

CREATE TABLE communes
(
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) UNIQUE NOT NULL,
    district_id INT                 NOT NULL,
    FOREIGN KEY (district_id) REFERENCES districts (id)
);

CREATE TABLE cities
(
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(100) UNIQUE NOT NULL,
    commune_id INT                 NOT NULL,
    FOREIGN KEY (commune_id) REFERENCES communes (id)
);

CREATE TABLE addresses
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE stations
(
    id           SERIAL PRIMARY KEY,
    station_name VARCHAR(255)     NOT NULL,
    latitude     DOUBLE PRECISION NOT NULL,
    longitude    DOUBLE PRECISION NOT NULL,
    city_id      INT              NOT NULL,
    address_id   INT,
    FOREIGN KEY (city_id) REFERENCES cities (id),
    FOREIGN KEY (address_id) REFERENCES addresses (id)
);
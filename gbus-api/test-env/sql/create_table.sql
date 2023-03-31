CREATE TABLE bus (
  id serial PRIMARY KEY,
  bus_id varchar(64) NOT NULL,
  bus_name varchar(64) NOT NULL,
  plate integer
);

CREATE TABLE station (
  id serial PRIMARY KEY,
  station_id varchar(64) NOT NULL,
  station_name varchar(64) NOT NULL,
  region_name varchar(64)
);

CREATE TABLE bus_stop (
    id SERIAL PRIMARY KEY,
    bus_id varchar(64),
    bus_name varchar(64),
    station_id varchar(64),
    station_name varchar(64),
    stop_order INTEGER
);


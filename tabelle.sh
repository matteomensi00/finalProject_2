#!/usr/bin/bash
USERNAME='dlbd'
DATABASE='master_db'
PATH='\\wsl$\Ubuntu\home\corso\progetto\finalProject_2\taxi_ny.csv'
#Creazione schema e tabella
PGPASSWORD=admin2022 psql --user dlbd -h localhost master_db -c "CREATE SCHEMA IF NOT EXISTS finalproject2; 
																CREATE TABLE IF NOT EXISTS finalproject2.taxi_ny (
																id varchar(20) primary key,
																vendor_id int not null,
																pickup_datetime timestamp not null,
																dropoff_datetime timestamp not null,
																passenger_count int not null,
																pickup_longitude double precision not null,
																pickup_latitude double precision not null,
																dropoff_longitude double precision not null,
																dropoff_latitude double precision not null,
																store_and_fwd_flag varchar not null,
																trip_duration int not null,
																pickup_street varchar not null,
																pickup_suburb varchar not null,
																pickup_city varchar not null,
																dropoff_street varchar not null,
																dropoff_suburb varchar not null,
																dropoff_city varchar not null,
																distance_miles double precision not null,
																trip_price double precision not null);"
#Popolazione database
PGPASSWORD=admin2022 psql --user dlbd -h localhost master_db -c "\copy finalproject2.taxi_ny FROM taxi_ny.csv WITH (FORMAT csv, HEADER true);"
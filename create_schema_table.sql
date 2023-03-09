
DROP SCHEMA finalproject2;
CREATE SCHEMA IF NOT EXISTS finalproject2;
DROP TABLE taxi_ny;
CREATE TABLE IF NOT EXISTS taxi_ny (
id varchar(20) primary key,
vendor_id int(3) not null,
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
total_cost double precision not null
);
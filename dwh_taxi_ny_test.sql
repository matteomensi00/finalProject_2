{{config(
    re_data_monitored=true,
    materialized="table",
    unique_key=["id"],
    tag="dwh"
)}}
with source as (
    select * from {{ source('finalproject2', 'taxi_ny') }}
)
select *
from source
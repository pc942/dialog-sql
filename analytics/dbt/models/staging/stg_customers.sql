
{{ config(materialized='view') }}
select *
from postgres_scan('host=postgres port=5432 dbname=dialog user=dialog password=dialog', 'public', 'customers')

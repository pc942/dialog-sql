
{{ config(materialized='view') }}
select
  o.product_line,
  date_trunc('quarter', o.created_at) as quarter,
  avg(o.amount) as avg_order_value,
  count(*) as orders
from {{ ref('stg_orders') }} o
join {{ ref('stg_customers') }} c
  on c.customer_id = o.customer_id
group by 1,2

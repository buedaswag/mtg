# mtg
mtg card price visualization project

#postgres notes
CREATE DATABASE mtg;

sudo su - postgres 
psql
create database mtg;
\l # list databases, then press q to go back to db console

\q # to exit:

\dt # list tables of the public schema

CREATE TABLE card_listings (
  card_name varchar(100), 
  ts timestamp, 
  list_order int, 
  seller_name varchar(30), 
  seller_sales int, 
  seller_available_items int, 
  item_price int, 
  item_amount int, 
  item_location varchar(30), 
  item_condition char(2), 
  item_language varchar(20),  
  item_is_playset boolean, 
  item_is_foil boolean,
  PRIMARY KEY (card_name, ts, list_order)
);

GRANT ALL PRIVILEGES ON DATABASE mtg to mig;

GRANT CONNECT ON DATABASE mtg TO mig;
GRANT USAGE ON SCHEMA public TO mig;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO mig;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO mig;

GRANT USAGE ON SCHEMA public TO mig;
GRANT SELECT, UPDATE, INSERT, DELETE ON ALL TABLES IN SCHEMA public TO mig;

#cron notes
0/30 * * * * /home/mig/anaconda3/envs/mtg/bin/python ~/mtg/prototype_scraping.py

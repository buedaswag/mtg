# mtg
mtg card price visualization project

#postgres notes
CREATE DATABASE mtg;<br />

sudo su - postgres <br />
psql<br />
create database mtg;<br />
\l # list databases, then press q to go back to db console<br />

\q # to exit:<br />

\dt # list tables of the public schema<br />

CREATE TABLE card_listings (<br />
  card_name varchar(100), <br />
  ts timestamp, <br />
  list_order int, <br />
  seller_name varchar(30), <br />
  seller_sales int, <br />
  seller_available_items int, <br />
  item_price int, <br />
  item_amount int, <br />
  item_location varchar(30), <br />
  item_condition char(2), <br />
  item_language varchar(20),  <br />
  item_is_playset boolean, <br />
  item_is_foil boolean,<br />
  PRIMARY KEY (card_name, ts, list_order)<br />
);<br />

GRANT ALL PRIVILEGES ON DATABASE mtg to mig;<br />

GRANT CONNECT ON DATABASE mtg TO mig;<br />
GRANT USAGE ON SCHEMA public TO mig;<br />
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO mig;<br />
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO mig;<br />

GRANT USAGE ON SCHEMA public TO mig; <br />
GRANT SELECT, UPDATE, INSERT, DELETE ON ALL TABLES IN SCHEMA public TO mig;<br />

#cron notes
0/30 * * * * /home/mig/anaconda3/envs/mtg/bin/python ~/mtg/prototype_scraping.py<br />

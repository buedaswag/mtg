# mtg
mtg card price visualization project

# postgres notes
psql [database_name] [user_name]<br />
https://www.freecodecamp.org/news/how-to-get-started-with-postgresql-9d3bc1dd1b11/<br />

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

create user mig with password 'password';<br />

GRANT ALL PRIVILEGES ON DATABASE mtg to mig;<br />

GRANT CONNECT ON DATABASE mtg TO mig;<br />
GRANT USAGE ON SCHEMA public TO mig;<br />
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO mig;<br />
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO mig;<br />

GRANT USAGE ON SCHEMA public TO mig; <br />
GRANT SELECT, UPDATE, INSERT, DELETE ON ALL TABLES IN SCHEMA public TO mig;<br />

# cron notes

https://askubuntu.com/questions/420981/how-do-i-save-terminal-output-to-a-file<br />

https://askubuntu.com/questions/420981/how-do-i-save-terminal-output-to-a-file<br />

crontab -u mig -e

#regular job
*/30 * * * * export DISPLAY=:0.0 ; /home/mig/anaconda3/envs/mtg/bin/python ~/mtg/prototype_scraping.py | tee -a ~/mtg/logs/regular_log.txt<br />

#experimental job
25 * * * * export DISPLAY=:0.0 ; /home/mig/anaconda3/envs/mtg/bin/python ~/mtg/prototype_scraping.py | tee -a ~/mtg/logs/experimental_log.txt<br />

# access remote server, and running graphics applications (browser windows, for example)
https://askubuntu.com/questions/213678/how-to-install-x11-xorg<br />

https://unix.stackexchange.com/questions/353258/how-to-run-google-chrome-or-chromium-on-a-remote-ssh-session<br />


ssh -X user@hostname<br />
ssh -X mig@192.168.1.8<br />

# timezone notes
SET TIME ZONE 'UTC';

use this setting in pandas as well
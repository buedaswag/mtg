# mtg
mtg card price visualization project

# postgres notes
psql [database_name] [user_name]<br />
psql mtg mig<br />
https://www.freecodecamp.org/news/how-to-get-started-with-postgresql-9d3bc1dd1b11/<br />

CREATE DATABASE mtg;<br />

sudo su - postgres <br />
psql<br />
\c DBNAME<br />
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
  item_price real, <br />
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

# SSH access remote server, and running graphics applications (browser windows, for example)
https://askubuntu.com/questions/213678/how-to-install-x11-xorg<br />

https://unix.stackexchange.com/questions/353258/how-to-run-google-chrome-or-chromium-on-a-remote-ssh-session<br />

do this on mig-pc: <br />
~/.ssh/config<br />
Host mig-server<br />
    HostName mtgdata.ml<br />
    User mig<br />
    Port 49000<br />

do this on mig-server:<br />
https://pt.godaddy.com/help/alterar-a-porta-ssh-para-o-seu-servidor-com-o-linux-7306<br />


ssh -X -p 49000 user@hostname<br />
ssh -X -p 49000 mig@192.168.1.8<br />
ssh -X -p 49000 mig@mtgdata.ml
ssh -X -p 49000 mig@79.168.14.53

check if port is open or closed:
nmap -p 49000 79.168.14.53
nmap -p 49000 mtgdata.ml

allow connections on specific port:
sudo ufw allow 49000

# How do I properly test whether my Port Forwarding works?
https://superuser.com/questions/307820/how-do-i-properly-test-whether-my-port-forwarding-works

# timezone notes

https://serverfault.com/questions/554359/postgresql-timezone-does-not-match-system-timezone<br />
The solution for your case is quite simple, just change the TimeZone setting on postgresql.conf to the value you want:<br />

TimeZone = 'Europe/Vienna'<br />

After that you need to reload the service:<br />

sudo su - postgres -c "psql mtg -c 'SELECT pg_reload_conf()'"

https://stackoverflow.com/questions/3602450/where-are-my-postgres-conf-files<br />
ask your database:<br />
$ psql -U postgres -c 'SHOW config_file'<br />


SET TIME ZONE 'UTC';<br />
select now();<br />
show timezone;<br />

use this setting in pandas as well (UTC)<br />



ALTER TABLE card_listings <br />
ALTER COLUMN item_price TYPE real; <br />
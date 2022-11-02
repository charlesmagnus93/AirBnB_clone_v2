#!/usr/bin/env bash
# Deploy project
if [[ ! -f "/etc/init.d/nginx" ]]; then
	sudo apt install -y nginx
fi
sudo mkdir -p "/data/web_static/shared"
sudo mkdir -p "/data/web_static/releases/test"
echo "Hello World!" | sudo tee "/data/web_static/releases/test/index.html"
sudo ln -sf "/data/web_static/releases/test" "/data/web_static/current"
sudo chown -R ubuntu:ubuntu "/data"
sudo sed -i "s/^.*location \/hbtn_static.*//" /etc/nginx/sites-available/default
sudo sed -i "s/^.*location \/hbnb_static.*//" /etc/nginx/sites-available/default
sudo sed -i \
	"s/^}$/\tlocation \/hbnb_static\/ \{ alias \/data\/web_static\/current\/; \}\n\}/" \
	/etc/nginx/sites-available/default
sudo ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default
sudo service nginx restart

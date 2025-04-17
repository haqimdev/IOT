##db manager beekeeeper studio
#install beekeeper studio
# Install our GPG key
curl -fsSL https://deb.beekeeperstudio.io/beekeeper.key | sudo gpg --dearmor --output /usr/share/keyrings/beekeeper.gpg \
  && sudo chmod go+r /usr/share/keyrings/beekeeper.gpg \
  && echo "deb [signed-by=/usr/share/keyrings/beekeeper.gpg] https://deb.beekeeperstudio.io stable main" \
  | sudo tee /etc/apt/sources.list.d/beekeeper-studio-app.list > /dev/null

# Update apt and install
sudo apt update && sudo apt install beekeeper-studio -y

## Portainer webserver
http://172.20.10.2:9000
## if cant enter web portainer
#find the container ID
docker ps
#stop and restart the portainer using container ID
docker stop CONTAINER_ID  
docker start CONTAINER_ID
#create a user and password
user : admin
psword : Schottraspberrypi

##Mariadb info
MYSQL_ADMIN root
MYSQL_ROOT_PASSWORD 	IOtSt4ckToorMariaDb
MYSQL_USER 	mariadbuser
MYSQL_PASSWORD 	IOtSt4ckmariaDbPw

##node red webserver 
http://172.20.10.2:1880

##Grafana
http://172.20.10.2:3000/login
user : admin
psword : Schottraspberrypi

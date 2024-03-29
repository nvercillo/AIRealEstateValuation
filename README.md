# AI Real Estate Valuation

## Repo Principles

* When checking out a branch, use a branch with your name. I.e. git checkout -b "sathirasBranch"
* Open a PR and then merge into master that way the history of mergers is always maintained well. 
* Help clean any dead or misformatted files and code

## Introduction
The purpose of this project is to predict the current value of unlisted properties in the Toronto region based on a 30+ variable multilayer percepitron. The intention is then to visualize this on a web-application like a Python-Flask with react flask where you would be able to type in an address or postal code, and our pre-trained model would spit out a value.


## Data
The data for this project was retrieved using a Puppeteer webscrapper taking data primarily from zolo.com with over 14,000 properties in data pulled and which will be stored in a MySQL database. The geolocational data was then found by using a latlong.net where the Puppeteer scrapper simulates human behavior to the long, lat data.

### Variables
There were a variety of variables as mentioned taken into consideration for the MLP model:
* location
* type of property
* nearby amenities (i.e. nearest distance to schools, grocery stores etc.)
* Rankings of nearest schools

#### Location
This was a unique variable to take into consideration. Basically what was done here was each individual area code was given a new exponential function for how important close data points or properties are in affecting property value. I.e. in some area codes, houses slightly outside of the neighborhood affect the current property value.
All of these unique exponetial funcitons are calculated using a secondary model.



## Web Scrapper



## Backend 

### Setup 
Requirements: python3 as python, pip3 as pip, virtuenv-python, MySql
```
sudo apt-get install libmysqlclient-dev
sudo apt-get install libssl-dev
pip3 install mysqlclient

pip3 install black 
```

### Formatting

USE BLACK FORMATTER TO AVOID MERGE CONFLICTS AND IMPROVE CODE QUALITY

* On Linux: 
```
cd backend 
python -m venv env (optional)
source env/bin/activate (optional)
pip install -r requirements.txt


sudo -u postgres -i

psql

create database NODE_DATA;

python manage.py db init

python manage.py db migrate

python manage.py db upgrade

ONE TIME ONLY: 
python create_api_key.py (optional, creates api key and adds it to env file. This should be copied in frontend)

python server.py 
```


### Testing 
Requirements: pytest 
```
cd Backend;
pipenv shell;
pytest -s;
```


## Deploy

Requirements: have gcloud installed 

```
gcloud init # then link to current project 
gcloud app deploy
```



# Setup:



## Docker

- Install docker
## Database: 

```
sudo docker pull mysql/mysql-server:latest
sudo docker run --name=mysql-docker -d mysql/mysql-server:latest
```


Pull out password: 
``` sh
sudo docker logs mysql_docker

# [Entrypoint] GENERATED ROOT PASSWORD: <PASSWORD>
```

MySQL config:
``` sh 
sudo docker exec -it mysql-docker bash
mysql -uroot -p
```

Change Password
``` sql
ALTER USER 'root'@'localhost' IDENTIFIED BY '[newpassword]';
```


## Update config:

``` sh 
# create dir
sudo mkdir -p /root/docker/mysql-docker/conf.d

sudo nano /root/docker/[container_name]/conf.d/my-custom.cnf 

## ADD FOLLOWING LINES: 
[mysqld]
max_connections=250


# Then update: 
docker run \
--detach \
--name=mysql-docker \
--env="MYSQL_ROOT_PASSWORD=32darklink" \
--publish 6603:3306 \
--volume=/root/docker/[container_name]/conf.d:/etc/mysql/conf.d \
mysql
```
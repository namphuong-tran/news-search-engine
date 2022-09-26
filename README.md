# Breaking news search engine
![alt text](https://raw.githubusercontent.com/phuongtrannam/news-search-engine/main/SW2022.jpg)
This is the final project in the Software education for Vietnamese students in Korea. We built a search engine for news. Data is collected from five well-known news channels: CNBC, CNN, NBC, Reuters and USAToday. 

## Installation
### Python 
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirement packages.

```bash
pip install -r requirements.txt
```
### Docker desktop
Docker Desktop is an easy-to-install application for your Mac, Linux, or Windows environment that enables you to build and share containerized applications and microservices.

You can follow this [guide](https://docs.docker.com/desktop/install/mac-install/) to install appropriate docker desktop with your operating system. 

## Usage
### Run Flask app
```bash
python3 articles.py
```
### Run Docker containers
Ro run Elastic Stack (ELK) and MySQL: 
```bash
cd news-search-engine/mysql-elk-compose
docker compose up
```
To run individual services: 
```bash
cd news-search-engine/mysql-elk-compose
docker compose up -d service_name 
# example: docker compose up -d mysql
```
To stop Elastic Stack (ELK) and MySQL: 
```bash
cd news-search-engine/mysql-elk-compose
docker compose stop
```
To stop individual services:  
```bash
cd news-search-engine/mysql-elk-compose
docker compose stop service_name
```
To remove containers together with saved states, run
```bash
cd news-search-engine/mysql-elk-compose
docker compose down -v
```
## Basic Configurations

- Specify versions of Elastic Stack (ELK) and MySQL in `.env`
- MySQL: `mysql/config/mysql.cnf`
- Elasticsearch: `elasticsearch/config/elasticsearch.yml`
- Logstash: `logstash/config/logstash.yml`
- Kibana: `kibana/config/kibana.yml`
- Refer to `docker-compose.yml` for configurations like username, password, ports, etc.

## MySQL

- **Database Credentials**
  - Username: _system_
  - Password: _admin123_
- By default, `temp_db`, which is populated with some dummy data, have been created.
- Write SQL scripts and store in `mysql/sql` to initialize database with new tables and populate data into the tables.


## Elasticsearch

- **Login Credentials**
  - Username: _elastic_
  - Password: _changeme_


## Logstash

- **Pipeline**
  - `init_temp_table.conf` is used to load existing data from MySQL to Elasticsearch. It is only run _once_.
  - `sync_temp_table.conf` is used to sync newly inserted/updated data between MySQL and Elasticsearch. It is configured to run every 5 seconds. 
- When adding a new pipeline:
  - Write new config file and store it in `logstash/pipeline/conf`
  - Write new SQL statement and store it in `logstash/pipeline/sql`. Link the `.sql` file path to `statement_filepath` in your config file. 
 



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
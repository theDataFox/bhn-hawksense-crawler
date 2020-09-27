
# HawkSense Web Crawler

Application to serve the main HawkSense application by running spiders to crawl requested sites as HTTP requests from Fast API.

## Features

## Overview and Structure
The application has two major subsections. A front end React interface used by the end user and server side code to
 process all the machine learning and analysis that needs to be done. Some server side code will be real time
  and will be detailed later. 
  
  - Backend Language: Python 3
  - Scraping server: Scrapyd
  - Backend task management: Celery
  - Web framework: FastAPI
  - Database: PostgreSQL
  - Deployment: Multicontainer Docker
  
  
## technology stack

category | name | comment
---------|----------|---------

## Structure
```
|——app/
|  |——api/  
|  |    |—-dependencies/
|  |    |     |—-audit/
|  |    |     |—-backlink/
|  |    |     |—-keyword/
|  |    |     |—-pagespeed/
|  |    |—-errors/
|  |    |—-routes/  
|  |——core/  
|  |    |—-config.py
|  |    |—-event_handlers.py
|  |    |—-logging.py
|  |——data/ 
|  |    |—-raw/
|  |    |—-processed/
|  |——models/
|  |    |—-audit.py
|  |    |—-backlink.py
|  |    |—-keyword.py
|  |    |—-pagespeed.py
|  |——resources/
|  |    |—-messages.py
|  |——services/   
|  |    |—-audit.py
|  |    |—-backlink.py
|  |    |—-keyword.py
|  |    |—-pagespeed.py   
|  |——main.py/ 
|  |——setup.cfg/ 
|——docs/
|——tests/
|  |——test_api/ 
|  |——test_schemas/   
|  |——test_services/
|  |——conftest.py
|  |——testing_helpers.py     
|——.dockerignore
|——.env
|——Dockerfile
|——requirements.txt
|——setup.py
```


## Configuration and Setup

# SagaStartTime Server + Discord Bot

API built in Flask that stores Countries and Locations of Saga Robotics treatments, and then serves the time that treatment can begin

Also contains a script to send data from the API to a Discord webhook at 12PM every day. 

---

Before running the script, you will need to include a webhook URL. You can add this by navigating to the app/ directory, and pasting your webhook URL into the file called 'WEBHOOK_URL'.

Includes a Dockerfile that can be built using the following commands

`docker build -t sagastarttime .`

This should build the Docker image, which can then be ran with

`docker run sagastarttime`


## Documentation

Route  | Description | Requirements | Method 
------------- | ------------- | ------------- | ------------- | 
/api/countries | Lists all countries in database | None | GET
/api/countries | Adds a country given a name | name | POST
/api/locations | Lists all locations in database | None | GET
/api/locations | Adds a location given data | lat, lon, name, country_id | POST
/api/locations/by_name/<country_id> | Lists locations per country_id | country_id (in url) | GET
/api/start_time/<location_id> | Returns start and end times per location_id | location_id (in url) | GET
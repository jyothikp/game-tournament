# game-tournament
This is a sample app for tournament data consumption and searching.
* Tournament data in JSON format is sent to the RabbitMQ using a sample producer.
* The consumer who listens for this information will receive the data and save that information in the DB
* This data can be queried using the Falcon app 

How to set up the docker
``` docker-compose up -d --build ```

This command will start following containers
* A RabbitMQ broker (`http://localhost:15672/#/`)
* A MongoDB with persistent volume (`docker exec -it game-mongo bash`)
* A simple Falcon app (`http://localhost:5000/`)
* A RabbitMQ consumer

Two APIs are available to search the data:
* GET API: Fetches information about a match using an internal match_id. 
Eg. `curl -XGET 
http://localhost:5000/game/v1.0/search/5ec26e52b5f6f62bea2cd969`
* POST API: Fetches all match information along with their team and score data. It accepts a few filters as well:
`curl -XPOST -d '{"query":{"state":1}}' http://localhost:5000/game/v1.0/search/ -H "Content-Type: application/json"`

Other filter samples:
```
{
  "query": {
    "state": 1,
    "tournament": "my_tournament_name",
    "title": "my_title_name",
    "date_start_gte": "2020-01-07 14:30:00",
    "date_start_lte": 2020-01-07 19:30:00",
  }
}
```

The common code used by the API and the consumer is availabe as a python package `game-tournament`:

`pip install -i https://test.pypi.org/simple/ game-tournament==1.0.0`


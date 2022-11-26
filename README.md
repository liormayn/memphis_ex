### How to run:
to run this project, you need to have docker installed on your station.

while in the memphis folder:
run these commands one by one:
```
docker compose build
docker compose up
```

to alter timeouts or intervals - use common/configuration.py

#### disclaimers and assumptions:
1. i'm taking the news articles from the front page - some don't have summary for some reason.
2. the posts keep appearing because bbc's news don't change as fast as 10 seconds :)

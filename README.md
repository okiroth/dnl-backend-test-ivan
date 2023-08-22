# DNL Backend Test Project

### Overview
This project consists of `3` main processes:
- `API`: Queries the DB
- `DB`: The database instance
- `SCRAPPER`: Runs throught the website and stores the data into the DB.

## Run it
```
docker compose up --build
```
This command will run all Docker processes, this means `Scrapping` and `Saving` data.


if you want the `API` only run
```
docker compose --profile no-scrapping up 
```


## scrapper
Currently, it take around `10 minutes`` to scrap the whole website on a local laptop.

## db
The data is saved using `4 Tables`:
- brands
- categories
- models
- parts

Each having the correspodning relationship to it's parent.

## api
`TODO`: implement filtering, currently only returns `Brands` and `Categories`

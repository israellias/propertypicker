The main purpose of the project is to serve as a database to store and analyze real estate properties for sale in the market. 


# How to run 

You need docker and docker compose installed

```bash
$ docker compose up -d --build
```
Copy .env file and fill the correct values. Hint: You can use this [website](https://djecrety.ir/) for development purposes 
```bash
$ cp .env.example .env
```

Run migrations 
```bash
$ docker compose exec web python manage.py migrate
```

Create a superuser
```bash
$ docker compose exec web python manage.py createsuperuser
```

Go to app and start to populate the database: [http://localhost:8000/admin/](http://localhost:8000/admin/)



# How the app works

You can create a new Property with the following data 
* URL: optional
* Reference: this is the verbose name
* Position: this needs to be a LatLong data or a you can fill a Google [PlusCodes](https://maps.google.com/pluscodes/) wich is a very easy way to share locations from mobile
* m2: dimension of the property
* Price: price of the property. Please use nominal prices. If seller is pretending to use different exchange rates you must modify this value to match the official exchange rate
* Phone: optional
* Zone: You can create new zones to group properties by your own criteria
* Condition: notes of the property
* Tags: notes of the property

The next elements are optionals or readonly


You must want to fill first the **Locations** data. In order to have meassured directions to your locations of interest. 



# Queue between a file reader and writer
Two django apps(setter, getter) communicate via a service broker(redis) using the producer-consumer model. The app `setter` set data and the app `getter` comsumes the data.

## Build
Clone the project and change to the root of the project. Then run the command below to build it:
```
docker-compose up
```

## Setter App
* Visit ```http://127.0.0.1:8120/setter/``` in your browser
* Upload a text file



## Getter App
* Visit ```http://127.0.0.1:8000/getter/``` to see your uploaded file




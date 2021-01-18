
# Rental Car administration.

   This project is for building a Car Rental application. It invloves User, Car and Price data intialization, and then allow user to book the car on rent at any given time.

## Steps to run the project:
```
1: Clone the project to the local machine

2: pip install -r requirements.txt

3: python app.py (This will start running the application)

4: While running the above command please note down the host. ex: http://127.0.0.1:5000/
```

## Tech Stacks used in the project:
    Python(3.6), Flask(1.1.2), SQLAlchemy(1.3.19), SQLite

## API Details

1:  API intialising the data for Customers, Cars, Category and price inverntory.
    ```
    Type: Post
    URL: initialize/data.   (http://127.0.0.1:5000/initialize/data)
    Body: Empty
    ```
   Description: The above API will intialize the primary/basic data used for the Application. This API will save the data in Customers, Cars, Car Category and Price table.

2:  Get available cars for rent.
    ```
    Type: Get
    URL: get/rides
    Query Parameters: 
         start_date: Epoc time for starting the Trip.
         end_date: Epoc time for ending the Trip.
    Sample URL: http://127.0.0.1:5000/get/rides?start_date=1611764187&end_date=1612282587
    Response:
          {
             "available_cars": [
                 {
                     "category": 2,
                     "colour": "Red",
                     "current_milage": 20,
                     "location": "Punjab",
                     "model": "2018",
                     "reg_number": "KA-03 JE 1863"
                 },
                 {
                     "category": 3,
                     "colour": "Grey",
                     "current_milage": 12,
                     "location": "Mumbai",
                     "model": "2021",
                     "reg_number": "KA-03 JE 1864"
                 }
             ],
             "success": true
         }
    ```
    Description: The above API will fetch the available cars for the mentioned dates.
    
 3: Book Ride.
     ```
     Type: POST
     URL: /book/ride
     Body Parameters:
         user:        User Id, who is booking the car.
         reg_number:  Car registration number that user wish to book.
         start_time:  Trip start Epoc time.
         end_time:    Trip end Epoc time. 
     Sample URL: http://127.0.0.1:5000/book/ride
     Response:
              {
                "booking_id": 7,
                "msg": "Trip booked.",
                "success": true
             }
     ```
     Descripton: This API will book the ride for the user for the time period mentioned.
     Note: This API is supports future and multiple booking in advance, so this will not start the Trip. This API is only for booking/reserving the car for the mentioned dates.

4: Start Ride.
     ```
     Type: PUT
     URL:  /start/ride
     Body Parameters:
      booking_id: This should be fetch from the last call.(API 3)
      start_km:   Pass the current KM count from the car's dashboard.
     Sample URL: http://127.0.0.1:5000/start/ride
     Response:
      {
       "msg": "Trip started.",
       "success": true
      }
     ```
     Descripton: This API is for starting the already booked trip.
  
5: End Trip.
     ```
     Type: PUT
     URL: /end/ride
     Body Parameters:
      booking_id:     This should be same as the start trip ID.
      end_km:         Pass the current KM count from the car's dashboard.
      current_milage: Pass the current milage count from the car's dashboard.
     Sample URL: http://127.0.0.1:5000/end/ride
     Response:
        {
          "msg": "Trip Completed.",
          "success": true,
          "total_fare": 34225
         }
      
     ```
     Descripton: This API is used for ending the already started Trip. In the backend we also calculate the total fare and return in the response while we also update the current of the car with the exsting milage in the DB.
     

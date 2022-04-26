<h1>Smart Home</h1><br>
This is my first big project in python. The assumption is to make it a REST API 
<h2>Project Description</h2>
The project consists of a client application, a server application and individual devices.<br>
Flask and FlaskRESTfull were used to set up the server.<br>
PostgreSQL was used to set up the database.<br>
The user has flats and rooms in which the devices may be located.
The devices can perform actions such as turning on, turning off, setting the colour etc.
The server checks if there are devices broadcasting on localhost ports and gives the possibility to create devices when it detects one, it asks the user where the device is located in which flat and room and adds it to the database.
The server also reads flats, rooms and devices from the database. It verifies whether a device that is in the database is active or not if it does not display this device to the user.
Flats and rooms are already entered in the database and the user cannot add new flats or rooms.
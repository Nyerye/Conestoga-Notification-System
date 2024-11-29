# Conestoga Notification System Concept
This Python Flask-based web application allows users to select a notification type and a target site, which then triggers the sending of a notification. The application logs the notifications and displays the selected notification type and site on a separate page.

## Features
Notification Types: Users can choose from different types of notifications, such as "Fire Drill", "System Update", or "Emergency Alert".
Site Selection: Users can select from predefined sites like "Head Office" or remote sites.
Logging: The application logs every notification sent with a timestamp into a log file (notifications.log).
Dynamic Display: Once a notification is sent, the user is redirected to a page displaying the notification type and the target site along with associated measures to be taken.

## Technologies Used
Flask: Lightweight web framework for building the web application.
HTML Templates: menu.html for user input and notification.html for displaying the sent notification.
Logging: Tracks and stores information about each notification in notifications.log.
Python 3.13: The backend language for running the server and handling user interactions.

## How does it work?
Home Route (/): Displays a form where users can choose a notification type and site.
Send Notification Route (/send_notification): Handles the form submission, logs the notification details, and redirects the user to a display page.
Display Notification Route (/display_notification): Shows the notification type and site, including a message for actions to take based on the selected notification.

## File Structure
Conestoga_Notification_System.py: Main Python application containing Flask routes, logging configuration, and server startup code.
menu_and_notification_html_code: Includes the code for the two html files we would add to the Flask servers template. 
Flask_Application.py: The code we will use to initiiate the direct call to the Flask server so it only ever runs when asked to. This takes away the need for an HTTP listener through PowerShell (the assumption I have that is the method of delivery of the notifcations used today).

## How to use
- Clone or download the repository.
- Install the required dependencies:
  - Python 3.13
  - Flask
  - pip install flask
### Run the application
- python app.py
- Open a web browser and go to whatever the URL address and port number you decide to use for the Flash server to interact with it. 
- Logging
- All notifications sent through the application are logged with a timestamp in the notifications.log file for auditing and tracking purposes.


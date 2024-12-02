# Conestoga-Notification-System


Conestoga Notification System Concept:
This Python based system is able to ask the user for the type of notification to be sent out as wella s the location that they want to target. The script then takes all possible subnets and breaks down the IP addresses that are possible in the range and tries to establish a connection. If one is successful, the Python script will call the Flask Server and generate a POST request with the site information and the notification type. A webpage template is made taking in te site name and the notification types as parameters. A GET request then issues the paylaod to be send to the device and opens it in a web browser. 

Notification Types: Users can choose from different types of notifications, such as "Fire Drill", "Hold in Place", or "Emergency Alert". This can be modified to the persons needs.
Site Selection: Users can select from predefined sites like "Head Office" or remote sites. The current code has most, if not all, Conestoga College sites entered in. 
Logging: The application logs every notification sent with a timestamp into a log file (notifications.log).
Dynamic Display: Once a notification is sent, the user is redirected to a page displaying the notification type and the target site along with associated measures to be taken.

Technologies Used:
Flask: Lightweight web framework for building the web application.
HTML Templates: menu.html for user input and notification.html for displaying the sent notification.
Logging: Tracks and stores information about each notification in notifications.log.
Python 3.13: The backend language for running the server and handling user interactions.

How does it work?:
Home Route (/): Displays a form where users can choose a notification type and site.
Send Notification Route (/send_notification): Handles the form submission, logs the notification details, and redirects the user to a display page.
Display Notification Route (/display_notification): Shows the notification type and site, including a message for actions to take based on the selected notification.

File Structure:
Conestoga_Notification_System.py: All in one solution that runs the Flask Server locally for testing, incorporates the Tkinter UI and main source code for ForUserOnly.py
menu.html:Includes a menu that takes in the parameters from a POST request and then outputs information into a temlplate and calls a GET request to send payload to a device.
notification.html: Inlcudes a basic HTML template for testing that is the payload called and sent to devices where a connection was established. 
Flask_Application.py: The code we will use to run the server and listen in on a specified port number for incoming requests.
ForUserOnly.py: The script that is for the user to use only. Contains the Tkinter UI and main code that will call the Flask Server and evaluate subnets and addresses. 
requirements.txt: The names of all packages needed to be imprted in order for scripts to function. 

How to use (for end user):
Clone or download the repository from main.
Download Python 3.13 from Pythons website: https://www.python.org/downloads/release/python-3130/?featured_on=pythonbytes
Install the required dependencies from requirements.txt. In a Command Line, enter: **pip install -r requirements.txt**
Whenever a notification needs to be called, run the ForUserOnly.py


How to use (for Flask Server)
Decide what infrastructure you want to use. In my testing, I opted into a virtual machine that allowed incoming and outgoing traffic through port 5000.
Set up the virtual machine with Windows 11. 
Launch the virtual machine.
Once virtual machine is booted up, open Windows Defender Firewall and Security. 
Create rules that allow incoming and outgoing traffic on port xxxx on TCP and UDP.
On the Desktop, create a folder called Flask Server.
Clone or download the repository from the Development branch into the Flask Server folder.
Download Python 3.13 from Pythons website: https://www.python.org/downloads/release/python-3130/?featured_on=pythonbytes
Install the required dependencies from requirements.txt. In a Command Line, enter: **pip install -r requirements.txt**
Run the Conestoga_Notification_System.py
Take note of the IP address for the virtual machine and the port number you chose. If you are not sure, there is a log that allows you to see what IP and port you have.
In a browser, enter: https://enteripadresshere:portnumber
If it is running, you should see a success message on the browser page. 
Stop the Conestoga_Notification_System.py script.
Use only the Flask_Application.py to run the server from now on. 
You can further test this by making a POST key in Postman and then setting up your server and IP address in a POST and GET workspaces to test it. 


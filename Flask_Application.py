#Title                      Flask_Application.py
#Author:                    Nicholas Reilly
#Initial date created:      October 2 2024
#Description:               Main file where we would be hosting the new script in theory. As the script is determining successful connections, 
#                           it will be logging information and errors to a text file which Tier 3 can use to review whether or not modifications are needed. 
#                           If the script establishes a successful connection, it will then call upon a function that takes in the parameters for the type of
#                           notification and the site location, and calls a Flask server to generate an alert with a premade html template that just fills in the blanks.
#Credits to:                Wayne Pielsticker, debugging and test enviornment deployment.

#Imprting all packages required for code and other functions to work. 
from flask import Flask, request, jsonify, render_template, redirect, url_for
import logging
from datetime import datetime
import ipaddress


#Initialize the Flask application.
app = Flask(__name__)

#Configure logging to track activities and errors.
logging.basicConfig(
    filename='notifications.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

#Subnets for each site. Conestoga can adjust these as needed.
site_subnets = {
    "Guelph": [ipaddress.IPv4Network("99.22.56.0/24")],
    "Milton": [ipaddress.IPv4Network("99.22.56.0/24")],
    "Cambridge": [ipaddress.IPv4Network("99.22.56.0/24")],
    "Waterloo": [ipaddress.IPv4Network("99.22.56.0/24")],
    "Brantford": [ipaddress.IPv4Network("99.22.56.0/24")],
    "DTK": [ipaddress.IPv4Network("99.22.56.0/24")],
    "Kitchener": [ipaddress.IPv4Network("99.22.56.0/24")],


    #Developer, enter your subnet here where the address for controlled environment is. 
    "TestDev": [ipaddress.IPv4Network("99.22.56.0/24")],
}


#Function name:     devices_from_site
#Description:       Takes the site name and looks up IP address options. subnet.hosts generates all possible options excpet 0 and 255.  
#Parameters:        site, the data value from the UI that holds the name of the site selected. 
#Returns:           target_ips, the list fo all usable IP addresses that can be targeted. 
def devicesFromSite(site):
    subnets = site_subnets.get(site, [])
    target_ips = []
    for subnet in subnets:
        for ip in subnet.hosts():
            target_ips.append(str(ip))
    return target_ips

@app.route('/')
def menu():
    return render_template('menu.html')

##Function name:    send_notification
#Description:       Handles all POST requests from the UI. Extracts the value for notification.
#                   type and the site to be able to start evaluating IP address within the subnet. If no devices are found
#                   it will log an error message and display a 404 error.   
#Parameters:        notification_type, the type of notification value picked up from the UI and site, the name of the site value
#                   picked up from the UI.
#Returns:           a response value, depending on whether or not connection was achieved. Inputs this into log file and displays on screen.
@app.route('/sendNotification', methods=['POST'])
def sendNotification():
    notif_type = request.form.get('notification_type')
    site = request.form.get('site')

    #Get all valid IPs for the site.
    target_ips = devicesFromSite(site)
    if not target_ips:
        log_message = f"No devices found in {site}."
        logging.warning(log_message)
        return jsonify({"error": log_message}), 404

    #Log the notification action.
    log_message = f"Notification '{notif_type}' sent to devices in {site}: {', '.join(target_ips)}"
    logging.info(log_message)

    redirectR = redirect(url_for('notification', notif_type=notif_type, site=site))
    jsonifyR = jsonify({"message": f"Notification '{notif_type}' sent to {site} successfully!"})

    return redirectR,jsonifyR

@app.route('/notification')
def notification():
    notif_type = request.args.get('notif_type')
    site = request.args.get('site')


    return render_template('notification.html', notif_type=notif_type, site=site) 

#Main entry point for running the Flask server.
if __name__ == '__main__':

    #Allow external access to the server by binding to '0.0.0.0'
    logging.debug("Starting Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
    logging.debug("Flask server started.")

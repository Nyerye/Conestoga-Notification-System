#Title:                     DEVConestoga_Notification.py
#Author:                    Nicholas Reilly
#Initial date created:      October 2 2024
#Description:               A consolidation of the Ui, the main program as well as the Flask Server code for development use only. This runs a local Flask Server on your defined
#                           subnet. This is to ensure that a proper outbound connection can be heard.
#Credits to:                Wayne Pielsticker, debugging and test enviornment deployment. 

import threading
import tkinter as tk
from tkinter import messagebox
import requests
import ipaddress
import logging
from flask import Flask, request

#Flask App Setup. This defines routes for handling UI data inputs.
app = Flask(__name__)

#Lists for types of notifications available to security and list of site locations
notification_types = ['Fire Drill', 'Hold in Place', 'Hazardous Weather']
sites = ['Cambridge', 'Doon', 'DTK', 'Guelph', 'Brantford', 'Waterloo', 'Milton','TestSubnet']

#List of subnet sites. Conestoga will add or modify as many as they need
site_subnets = {
    "Doon": [ipaddress.IPv4Network("192.168.1.0/24")],
    "Cambridge": [ipaddress.IPv4Network("10.0.0.0/24")],
    "Waterloo": [ipaddress.IPv4Network("172.16.0.0/24")],
    "DTK": [ipaddress.IPv4Network("172.20.0.0/24")],
    "Guelph": [ipaddress.IPv4Network("172.24.0.0/24")],
    "Milton": [ipaddress.IPv4Network("172.28.0.0/24")],
    "Brantford": [ipaddress.IPv4Network("172.31.0.0/24")],

    #Developer, enter the IP address of your controlled test environment here.  
    "TestSubnet": [ipaddress.IPv4Network("192.168.50.0/24")]
}

#Formatting for the logging portion of the program.
logging.basicConfig(
    filename='notification_script.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

#Flask Routes. / is the default route for a Flask App.
@app.route('/')
def home():
    return "Flask Server is Running!"


#Function name:     send_notification
#Description:       Handles all POST requests from the UI. Extracts the value for notification 
#                   type and the site to be able to start evaluating IP address within the subnet. If no devices are found
#                   it will log an error message and display a 404 error.   
#Parameters:        notification_type, the type of notification value picked up from the UI and site, the name of the site value
#                   picked up from the UI.
#Returns:           a response value, depending on whether or not connection was achieved. Inputs this into log file and displays on screen.                 
@app.route('/send_notification', methods=['POST'])
def sendNotification():
    notif_type = request.form.get('notification_type')
    site = request.form.get('site')

    #Log and process the notification.
    target_devices = devicesFromSite(site)
    if not target_devices:
        logging.warning(f"No devices found in {site}.")
        return f"No devices found in {site}.", 404

    log_message = f"Notification '{notif_type}' sent to devices in {site}: {', '.join(target_devices)}"

    logging.info(log_message)
    return f"Notification '{notif_type}' sent to {site} successfully!"


#Function name:     run_flask
#Description:       Starts the server locally for connection testing at specified address on port 5000.   
#Parameters:        nothing.
#Returns:           nothing. 
def runFlaskServer():
    app.run(host='127.0.0.1', port=5000, debug=False)

flask_thread = threading.Thread(target=runFlaskServer, daemon=True)
flask_thread.start()


#Function name:     devices_from_site
#Description:       Evaluates all potetnial devices within a subnet. 
#Parameters:        site, the input value from the UI of the name of the site user chose.
#Returns:           target_ips. The list of all potential targets in a subnet.  
def devicesFromSite(site):
    """Generate all valid IP addresses in the site's subnet."""
    subnets = site_subnets.get(site, [])
    target_ips = []

    for subnet in subnets:
        # Generate all valid IPs within the subnet
        for ip in subnet.hosts():  # .hosts() excludes .0 and .255 by default
            target_ips.append(str(ip))

    return target_ips


#Function name:     send_notification_ui
#Description:       sends the values picked up by the UI to the Flask Server for processing and template creation.
#Parameters:        notification_type, the type of notification value picked up from the UI and site, the name of the site value
#                   picked up from the UI.
#Returns:           An error text message only if the user tries to submit without selecting a site and notification type.  
def sendNotificationUI():
    notif_type = notification_var.get()
    site = site_var.get()

    if not notif_type or not site:
        messagebox.showerror("Error", "Please select both a notification type and a site.")
        return

    try:
        response = requests.post("http://127.0.0.1:5000/send_notification", data={
            'notification_type': notif_type,
            'site': site
        })

        if response.status_code == 200:
            messagebox.showinfo("Success", response.text)
        else:
            messagebox.showerror("Error", f"Error: {response.text}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to connect to server: {e}")


#Code for creating and modifying the UI window appearance and function.  
root = tk.Tk()
root.title("Notification System")

tk.Label(root, text="Select Notification Type:").grid(row=0, column=0, padx=10, pady=10)
notification_var = tk.StringVar()
notification_menu = tk.OptionMenu(root, notification_var, *notification_types)
notification_menu.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Select Site:").grid(row=1, column=0, padx=10, pady=10)
site_var = tk.StringVar()
site_menu = tk.OptionMenu(root, site_var, *sites)
site_menu.grid(row=1, column=1, padx=10, pady=10)

send_button = tk.Button(root, text="Send Notification", command=sendNotificationUI)
send_button.grid(row=2, column=0, columnspan=2, pady=20)

root.mainloop()

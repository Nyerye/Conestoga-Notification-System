
#Author:                    Nicholas Reilly
#Initial date created:      October 2 2024
#Description:               Main file where we would be hosting the new script in theory. As the script is determining successful connections, 
#                           it will be logging information and errors to a text file which Tier 3 can use to review whether or not modifications are needed. 
#                           If the script establishes a successful connection, it will then call upon a function that takes in the parameters for the type of
#                           notification and the site location, and calls a Flask server to generate an alert with a premade html template that just fills in the blanks.

#Importing install packages in order to execute the code successfully
import ipaddress
import requests
import logging
import FlashApplication

#Configure the logging logic for the notification script
logging.basicConfig(
    filename=r'C:\Users\nick_\Desktop\notification_script.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

#Define the subnets for each site
site_subnets = {
    "Doon": [ipaddress.IPv4Network("192.168.1.0/24")],
    "Cambridge": [ipaddress.IPv4Network("10.0.0.0/24")],
    "Waterloo": [ipaddress.IPv4Network("172.16.0.0/24")],
    "DTK": [ipaddress.IPv4Network("172.20.0.0/24")],
    "Guelph": [ipaddress.IPv4Network("172.24.0.0/24")],
    "Milton": [ipaddress.IPv4Network("172.28.0.0/24")],
    "Brantford": [ipaddress.IPv4Network("172.31.0.0/24")]
}

#List of devices with IP addresses. In this list, we would need to assume all things within certain ranges
#are added into this list. Everything from 1,254 inclusive that is not already allocated for other reasons. 
#A Tier 3/Network Admin would need to be able to provide the list. This would be designed for devices with static IP addresses.
devices = {
    "Device 1": "192.168.1.10",  
    "Device 2": "10.0.0.5",      
    "Device 3": "172.16.0.2"     
}

# Define notification types
notification_types = {
    1: "Fire Drill Alert",
    2: "Hold in Place",
    3: "Hazardous Weather"
}

# URL of the Flask server's notify endpoint
FLASK_SERVER_URL = "http://127.0.0.1:5000/notify"  # NOTE: This would be updated to the actual URL of the server once set up. 


#
#FUNCTION : flaskNotification
#DESCRIPTION : This function takes the notification site determined by security and the campus location into the Flask server.
#              Using the predefined template, it will use that information to generate the alert html with proper information. 
#PARAMETERS :  notif_type (a list of strings) and site
#RETURNS : nothing. 
def flaskNotification(notif_type, site):
    message = f"A {notif_type} has been triggered at {site}. Please follow safety procedures."
    payload = {
        "type": notif_type,
        "site": site,
        "message": message
    }
    try:
        response = requests.post(FLASK_SERVER_URL, json=payload)
        if response.status_code == 200:
            log_message = f"Notification '{notif_type}' sent to {site}."
            print(log_message)
            logging.info(log_message)
        else:
            log_message = f"Failed to send notification to Flask server. Status Code: {response.status_code}"
            print(log_message)
            logging.error(log_message)
    except requests.exceptions.RequestException as e:
        log_message = f"Error sending notification to Flask server: {e}"
        print(log_message)
        logging.error(log_message)

#
#FUNCTION : flaskNotification
#DESCRIPTION : This function determines the type of choice that the user is trying to select. It actively
#              looks for invalid data types and will prompt user to enter something valid.  A numbered choice is only allowed.
#PARAMETERS :  nothing. 
#RETURNS : notifications_types[choice] an index value in the predefined list earlier of choices that is associated with the string. 
def select_notification_type():
    print("\nSelect the type of notification:")
    for key, value in notification_types.items():
        print(f"{key}. {value}")
    while True:
        try:
            choice = int(input("Enter the number for your choice: "))
            if choice in notification_types:
                return notification_types[choice]
            else:
                print("Invalid choice. Please select a valid option.")
        except ValueError:
            print("Please enter a valid number.")
#
#FUNCTION : selectSite
#DESCRIPTION : This function determines the site choice that the user is trying to select. It actively
#              looks for invalid data types and will prompt user to enter something valid.  A numbered choice is only allowed.
#PARAMETERS :  nothing. 
#RETURNS : site_subnets.keys [choice] which would be the index value number from the list of strings given to the user.
def selectSite():
    print("\nSelect the site to target:")
    for idx, site in enumerate(site_subnets.keys(), 1):
        print(f"{idx}. {site}")
    while True:
        try:
            choice = int(input("Enter the number for your site choice: "))
            if 1 <= choice <= len(site_subnets):
                return list(site_subnets.keys())[choice - 1]
            else:
                print("Invalid choice. Please select a valid option.")
        except ValueError:
            print("Please enter a valid number.")
#
#FUNCTION : selectSite
#DESCRIPTION : This function determines the available IP address to target by looking at the site subnet indicated by the user.
#PARAMETERS :  site, the index number of what was indicated by the user. 
#RETURNS : target_devices, a list that contains all the possible IP addresses to target. 
def devicesFromSite(site):
    subnets = site_subnets.get(site, [])
    target_devices = []
    for device_name, device_ip in devices.items():
        ip = ipaddress.IPv4Address(device_ip)
        for subnet in subnets:
            if ip in subnet:
                target_devices.append((device_name, device_ip))
                break
    return target_devices

#Main function to execute the calling of the other functions and the html file.
def main():
    print("=== Notification System ===")
    
    #Call the notification type selection function for usr to seelct ype of notification.
    notif_type = select_notification_type()
    
    #Call the 
    site = selectSite()
    
    # Step 3: Get target devices
    target_devices = devicesFromSite(site)
    
    if not target_devices:
        print(f"\nNo devices found in {site}.")
        logging.info(f"No devices found in {site}.")
        return
    
    # Step 4: Send notification to Flask server
    flaskNotification(notif_type, site)
    
    # Log which devices were targeted
    device_info = ', '.join([f"{name} ({ip})" for name, ip in target_devices])
    log_message = f"Notification '{notif_type}' sent to devices in {site}: {device_info}"
    logging.info(log_message)
    print(f"\nNotification '{notif_type}' sent to devices in {site}: {device_info}\n")

if __name__ == "__main__":
    main()


  
#Title:                     ForUserOnly.py
#Author:                    Nicholas Reilly
#Initial date created:      October 2 2024
#Description:               This is the main script that would be at the end users station. This holds the code for the UI and for security guard
#                           to be able to call the Flask Server and initiate a deployment of an HTML file on the Flask Server.
#Credits to:                Wayne Pielsticker, debugging and test enviornment deployment. 
import tkinter as tk
from tkinter import messagebox
import requests

#List of notification types and sites (adjust these as needed)
notification_types = ['Fire Drill', 'Hold in Place', 'Hazardous Weather']
sites = ['Cambridge', 'Doon', 'DTK', 'Guelph', 'Brantford', 'Waterloo', 'Milton','TestSubnet']


# Flask server URL. Conestoga can define where it is hosted and port to communicate on. 
FLASK_SERVER_URL = "http://<FLASK_SERVER_IP>:5000/send_notification" 


#Function name:     send_notification_ui
#Description:       sends the values picked up by the UI to the Flask Server for processing and template creation.
#Parameters:        notification_type, the type of notification value picked up from the UI and site, the name of the site value
#                   picked up from the UI.
#Returns:           An error text message only if the user tries to submit without selecting a site and notification type.  
def send_notification_ui():
    notif_type = notification_var.get()
    site = site_var.get()

    if not notif_type or not site:
        messagebox.showerror("Error", "Please select both a notification type and a site.")
        return

    # Send the notification to the Flask server via HTTP POST request
    try:
        response = requests.post(FLASK_SERVER_URL, data={
            'notification_type': notif_type,
            'site': site
        })

        if response.status_code == 200:
            messagebox.showinfo("Success", response.json()['message'])
        else:
            messagebox.showerror("Error", response.json()['error'])
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to connect to the server: {e}")


#Create the Tkinter UI window.
root = tk.Tk()
root.title("Notification System")


#Notification type dropdown menu.
tk.Label(root, text="Select Notification Type:").grid(row=0, column=0, padx=10, pady=10)
notification_var = tk.StringVar()
notification_menu = tk.OptionMenu(root, notification_var, *notification_types)
notification_menu.grid(row=0, column=1, padx=10, pady=10)


#Site dropdown menu.
tk.Label(root, text="Select Site:").grid(row=1, column=0, padx=10, pady=10)
site_var = tk.StringVar()
site_menu = tk.OptionMenu(root, site_var, *sites)
site_menu.grid(row=1, column=1, padx=10, pady=10)


#Send button.
send_button = tk.Button(root, text="Send Notification", command=send_notification_ui)
send_button.grid(row=2, column=0, columnspan=2, pady=20)


#Start the Tkinter UI loop.
root.mainloop()


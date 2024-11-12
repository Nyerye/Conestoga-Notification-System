
from flask import Flask, render_template, request, redirect, url_for
import logging
from datetime import datetime

#Initializes the Flask application to handle incoming requests and direct them to the appropriate routes.
app = Flask(__name__)

#Configure the logging to collect info on Flask server processes
logging.basicConfig(
    filename='notifications.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(message)s'
)

#Sample data: notification types and sites
notification_types = ['Fire Drill', 'System Update', 'Emergency Alert']
sites = ['Head Office', 'Remote Site 1', 'Remote Site 2']

@app.route('/')

#
#FUNCTION : mainTemplate
#DESCRIPTION : This function looks for the main html file template to reference and prepare for modification.
#PARAMETERS : none
#RETURNS : render_template. The modfied version of the base html template with the site name and notification type name populated. 
def mainTemplate():
    """Home route: display menu for selecting notification type and site."""
    return render_template('menu.html', notification_types=notification_types, sites=sites)


#Defines the send_notification route, which processes POST requests sent from the form submission.
@app.route('/send_notification', methods=['POST'])


#
#FUNCTION : sendNotification
#DESCRIPTION :  Retrieves data from the form, logs the notification, and redirects to display the notification.
#PARAMETERS : none
#RETURNS : render_template. Retrieves data from the form, logs the notification, and redirects to display the notification. 
def send_notification():
    #Handles the form submission, logs the notification, and redirects to display it."""
    notif_type = request.form.get('notification_type')
    site = request.form.get('site')

    # Log the notification
    log_message = f"Notification sent: {notif_type} to {site}"
    app.logger.info(log_message)

    # Redirect to display the notification
    return redirect(url_for('display_notification', notif_type=notif_type, site=site))

#Defines the display_notification route to show the notification.
@app.route('/display_notification')

#
#FUNCTION : displayNotification
#DESCRIPTION :  Retrieves the notification type and site from query parameters and renders an HTML page.
#PARAMETERS : none
#RETURNS : render_template. Retrieves data from the form, logs the notification, and redirects to display the notification. 
def displayNotification():
    """Displays the notification based on user selection."""
    notif_type = request.args.get('notif_type', 'Notification')
    site = request.args.get('site', 'Unknown Site')
    return render_template('notification.html', notif_type=notif_type, site=site)

#Line is added so that way this code only runs when directly called. 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

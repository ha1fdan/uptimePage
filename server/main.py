from flask import Flask, render_template
import requests
import time
import json
import threading
from datetime import datetime

app = Flask(__name__)

# Global variables
systems_status = {}
last_checked_times = {}  # Store last checked time for each system
settings = {}

# Load systems from systems.conf
def load_systems():
    systems = []
    with open('config/systems.conf', 'r') as file:
        for line in file.readlines():
            if line.strip() and not line.startswith("#"):
                name, address, port = line.strip().split(',')
                systems.append({"name": name.strip(), "address": address.strip(), "port": port.strip()})
    return systems

# Load settings from settings.conf
def load_settings():
    global settings
    with open('config/settings.conf', 'r') as file:
        for line in file.readlines():
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split('=')
                settings[key.strip()] = value.strip()

    # Convert monitoring_interval to integer
    if "monitoring_interval" in settings:
        settings["monitoring_interval"] = int(settings["monitoring_interval"])

# Send Discord notification
def send_discord_notification(system_name, status_text):
    #print(f"Sending Discord notification for {system_name}...")
    if settings["notification_method"] == "discord":
        webhook_url = settings["discord_webhook_url"]
        username = settings.get("discord_webhook_username", "uptimePage")
        avatar_url = settings.get("discord_webhook_avatar_url", "")
        extra_content = settings.get("discord_webhook_extra_content", "")
        if status_text == "Online":
            data = {
                "username": username,
                #"avatar_url": avatar_url,
                "content": f"✅ **{system_name}** is back online! {extra_content}"
            }
        elif status_text == "Offline":
            data = {
                "username": username,
                #"avatar_url": avatar_url,
                "content": f"⚠️ **{system_name}** is offline! {extra_content}"
            }
        else:
            data = {
                "username": username,
                #"avatar_url": avatar_url,
                "content": f"⚠️ **{system_name}** status is unknown! {extra_content}"
            }
        result=requests.post(webhook_url, json=data)
        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        #else:
            #print(f"Payload delivered successfully, code {result.status_code}.")
    else:
        print(f"Unsupported notification method: {settings['notification_method']}")

# Check system status
def check_system_status(system):
    try:
        url = f'http://{system["address"]}:{system["port"]}'
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return json.loads(response.text)  # Return the actual data from the response
        else:
            return {"statusText": "Offline"}  # Return a dictionary for consistency
    except requests.exceptions.RequestException:
        return {"statusText": "Offline"}  # Return a dictionary for consistency

# Monitor systems in the background
def monitor_systems():
    while True:
        systems = load_systems()
        for system in systems:
            status = check_system_status(system)  # Get detailed status from the agent
            previous_status = systems_status.get(system["name"], {"statusText": "Unknown"})
            
            # Update last checked time for the system
            last_checked_times[system["name"]] = datetime.now().strftime("%d %B, %Y %H:%M:%S")
            
            # Log previous and current status for debugging
            #print(f"System: {system['name']} - Previous: {previous_status['statusText']}, Current: {status['statusText']}")

            # Update the systems_status dictionary with the full status
            systems_status[system["name"]] = status

            # Check for status change and send notification if necessary
            if status['statusText'] == "Offline" and previous_status['statusText'] == "Online":
                send_discord_notification(system["name"], status['statusText'])
            if status['statusText'] == "Online" and previous_status['statusText'] == "Offline":
                send_discord_notification(system["name"], status['statusText'])

        time.sleep(settings.get("monitoring_interval", 300))  # Use the specified interval or default to 300 seconds (5min)


# Route for homepage
@app.route('/')
def index():
    systems = load_systems()
    
    # Only use the cached status data, don't check the systems again
    for system in systems:
        system_name = system["name"]
        status = systems_status.get(system_name, "Unknown")

        if status['statusText'] == "Offline":
            system["online"] = False
            system["status"] = "Offline"
            # Set default values for offline systems
            system['platform'] = "N/A"
            system['upSince'] = "N/A"
            system['diskUsage'] = 0
            system['memoryUsage'] = 0
            system['memoryAvail'] = 0
            system['cpuUsage'] = 0
        else:
            system["online"] = True
            system["status"] = "Online"
            data = status  # This should be a dictionary
            
            # Ensure that you're working with a dictionary
            if isinstance(data, dict):
                system['platform'] = data.get('platform', 'Unknown')
                system['upSince'] = data.get('upSince', 'Unknown')
                system['diskUsage'] = data.get('diskUsage', 0)
                system['memoryUsage'] = data.get('memoryUsage', 0)
                system['memoryAvail'] = data.get('memoryAvail', 0)
                system['cpuUsage'] = data.get('cpuUsage', 0)
            else:
                # Handle unexpected status format
                #print(f"Unexpected status format for system {system_name}: {data}")
                system['platform'] = "Unknown"
                system['upSince'] = "Unknown"
                system['diskUsage'] = 0
                system['memoryUsage'] = 0
                system['memoryAvail'] = 0
                system['cpuUsage'] = 0

        # Add the last checked time to the system data
        system['last_checked'] = last_checked_times.get(system_name, "N/A")

    return render_template('index.html', systems=systems)


if __name__ == '__main__':
    load_settings()  # Load settings on startup
    threading.Thread(target=monitor_systems, daemon=True).start()  # Start monitoring in the background
    webui_port = int(settings.get("webui_port", 8190))
    app.run(host=settings.get("webui_host", "0.0.0.0"), port=int(webui_port), debug=False)

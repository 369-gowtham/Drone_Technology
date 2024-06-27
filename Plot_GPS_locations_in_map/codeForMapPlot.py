import pandas as pd
import schedule
import time
import folium
import webbrowser
import threading

# Initial coordinates
x = float(input('Enter longitude: '))
y = float(input('Enter latitude: '))

# Global variables
map_file_path = "C:\\Users\\gowth\\Downloads\\map.html"
df = pd.read_excel('C:\\Users\\gowth\\Downloads\\waterwatch_clean2.xlsx', sheet_name='Sheet1')
print("Initial data loaded at", time.strftime("%Y-%m-%d %H:%M:%S"))

# Create the initial map
map_osm = folium.Map(location=[x, y], zoom_start=10)

# Function to reload data
def reload_data():
    global df  # Use global to modify the df defined outside the function
    df = pd.read_excel('C:\\Users\\gowth\\Downloads\\waterwatch_clean2.xlsx', sheet_name='Sheet1')
    

# Function to update the map
def update_map():
    global map_osm
    print("Updating map at", time.strftime("%Y-%m-%d %H:%M:%S"))
    
    # Extract latitude and longitude data
    df_location = df[['Latitude', 'Longitude']]
    df_location_list = df_location.values.tolist()
    df_location_list_size = len(df_location_list)

    # Add markers to the map
    for point in range(df_location_list_size):
        folium.Marker(df_location_list[point], popup=df['Suburb'][point]).add_to(map_osm)
    
    # Save the map to an HTML file
    map_osm.save(map_file_path)
    print("Map updated and saved at", time.strftime("%Y-%m-%d %H:%M:%S"))

# Function to get user input to stop the script
def get_input():
    global stop_thread
    while True:
        user_input = input()
        if user_input.strip().lower() == 'q':
            stop_thread = True
            break

# Schedule the data reload and map update
schedule.every(1).seconds.do(reload_data)  # Update data every second
schedule.every(10).seconds.do(update_map)  # Update map every 10 seconds

# Flag to indicate when to stop the loop
stop_thread = False

# Start a thread to get user input
input_thread = threading.Thread(target=get_input)
input_thread.start()

# Open the initial map in the web browser
map_osm.save(map_file_path)
webbrowser.open(f'file://{map_file_path}')
print("Initial map opened in the default web browser")

# Infinite loop to keep the scheduler running
print("Press 'q' and enter to stop the scheduler")

while not stop_thread:
    schedule.run_pending()
    time.sleep(1)

# Wait for the input thread to finish
input_thread.join()
print("Scheduler stopped.")


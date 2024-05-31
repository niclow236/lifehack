# Theme 3: Safeguarding Public Security
# Subtheme 1: Strengthening Domestic Security
## Crime Data Simulation and Analysis

 Our solution will simulate crime data as random 2D coordinates (using latitude and longitude), identify crime hotspots using KMeans clustering, and optimise patrol routes for a given number of patrol units. We dynamically adjusted these routes based on simulated real-time incidents and visualised the results.

### Features

- Simulate crime data as random 2D coordinates
- Identify crime hotspots using KMeans clustering
- Optimize patrol routes based on identified hotspots
- Dynamically adjust patrol routes based on new incidents
- Visualize crime incidents, hotspots, patrol units, and routes

### Prerequisites

- Python 3
- numpy
- matplotlib
- scikit-learn
- dash
- plotly

### Installation

1. **Clone the repository**

   ```
   git clone https://github.com/niclow236/lifehack.git
   cd lifehack
   ```

2. **Install dependencies**

   ```
   pip install numpy matplotlib scikit-learn dash plotly
   ```

### Usage

Run the script to perform the crime data simulation, hotspot identification, patrol route optimization, and visualization:

   ```
   python test.py
   ```

### Main Components

#### 1. Crime Data Generation

The script starts by generating simulated crime data as random 2D coordinates. This represents the locations of crime incidents within a unit square area. Since we do not have access to the crime data about the location and details of crimes, we have decided to randomise the location of crimes for demonstration purposes. If we do have access to crime data, we can calculate the risk factor for each location based on metrics such as frequency and severity of crimes.

   ```
   import numpy as np

   np.random.seed(42)
   num_incidents = 1000
   crime_locations = np.random.rand(num_incidents, 2)
   ```
#### 2. Identify Crime Hotspots

To identify areas with high crime density, the script uses the KMeans clustering algorithm to cluster the crime locations into a specified number of hotspots.

   ```
   from sklearn.cluster import KMeans

   def identify_hotspots(crime_locations, num_hotspots):
      kmeans = KMeans(n_clusters=num_hotspots, random_state=42)
      kmeans.fit(crime_locations)
      hotspot_centers = kmeans.cluster_centers_
      return hotspot_centers

   num_hotspots = 3
   hotspot_centers = identify_hotspots(crime_locations, num_hotspots)
   ```

#### 3. Optimize Patrol Routes

The script then optimizes patrol routes by assigning patrol units to the identified hotspots. Each patrol unit is assigned to the closest hotspot.

   ```
   def optimize_routes(hotspot_centers, num_patrol_units):
      patrol_units = []
      units_per_hotspot = num_patrol_units // len(hotspot_centers)
      for hotspot in hotspot_centers:
         for _ in range(units_per_hotspot):
               patrol_units.append(hotspot)
      return patrol_units

   num_patrol_units = 5
   patrol_units = optimize_routes(hotspot_centers, num_patrol_units)
   ```

#### 4. Dynamic Route Adjustment

Simulate real-time incidents and adjust patrol routes accordingly:

   ```
   def simulate_realtime_incidents():
      return np.random.rand(2)

   num_iterations = 10
   for i in range(num_iterations):
      new_incident_location = simulate_realtime_incidents()
      patrol_units = optimize_routes(np.vstack([hotspot_centers, new_incident_location]), num_patrol_units)
      
      # Visualization
      import matplotlib.pyplot as plt
      plt.figure(figsize=(8, 6))
      plt.scatter(crime_locations[:, 0], crime_locations[:, 1], s=20, color='blue', alpha=0.5, label='Crime Incidents')
      plt.scatter(hotspot_centers[:, 0], hotspot_centers[:, 1], s=200, color='red', marker='x', label='Crime Hotspots')
      plt.scatter(np.array(patrol_units)[:, 0], np.array(patrol_units)[:, 1], s=200, color='green', marker='o', label='Patrol Units')
      plt.scatter(new_incident_location[0], new_incident_location[1], s=300, color='purple', marker='*', label='New Incident')
      
      # Plot optimal routes
      for patrol_unit in patrol_units:
         for hotspot_center in hotspot_centers:
               plt.plot([patrol_unit[0], hotspot_center[0]], [patrol_unit[1], hotspot_center[1]], color='black', linestyle='--')

      plt.title(f"Iteration {i+1}")
      plt.xlabel('Latitude')
      plt.ylabel('Longitude')
      plt.legend()
      plt.show()
   ```



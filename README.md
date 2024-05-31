
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
#### 2. Crime Hotspots Analysis

To identify areas with high crime density, the script uses the KMeans clustering algorithm to cluster the crime locations into a specified number of hotspots.

   ```
   from sklearn.cluster import KMeans

   def identify_hotspots(crime_locations, num_hotspots):
      kmeans = KMeans(n_clusters=num_hotspots, random_state=42)
      kmeans.fit(crime_locations)
      hotspot_centers = kmeans.cluster_centers_
      return hotspot_centers
   ```

#### 3. Optimize Patrol Routes

The script then optimizes patrol routes by assigning patrol units to the identified hotspots. Each patrol unit is assigned to the closest hotspot.

   ```
   def optimize_routes(hotspot_centers, num_patrol_units):
      patrol_units = []
      for i in range(num_patrol_units):
         random_point = np.random.rand(2)
         closest_hotspot = np.argmin(np.linalg.norm(hotspot_centers - random_point, axis=1))
         patrol_units.append(hotspot_centers[closest_hotspot])
      return patrol_units
   ```

#### 4. Dynamic Route Adjustment (Simulated Real-Time Incidents)

Simulating real-time incidents by randomly selecting one of the hotspot locations.

   ```
   def simulate_realtime_incidents(hotspot_centers):
      new_incident = np.random.choice(len(hotspot_centers))
      return hotspot_centers[new_incident]
   ```

#### 5. Initial Hotspot Identification and Patrol Route Optimization

Initialising hotspot identification and patrol route optimization by specifying the number of hotspots and patrol units.

   ```
   num_hotspots = 3
   hotspot_centers = identify_hotspots(crime_locations, num_hotspots)
   num_patrol_units = 5
   patrol_units = optimize_routes(hotspot_centers, num_patrol_units)
   ```

#### 6. Create Dash App

Creating a Dash app for visualizing crime data.

   ```
   import dash
   from dash import dcc, html
   from dash.dependencies import Input, Output
   import plotly.graph_objs as go

   app = dash.Dash(__name__)
   ```

#### 7. Define Layout

Defining the layout of the Dash app, including a title and a graph for displaying the crime map.

   ```
   # Define layout
   app.layout = html.Div([
      html.H1("Crime Data Analysis Dashboard"),
      dcc.Graph(id='crime-map')
   ])
   ```

#### 8. Define Callback to Update Crime Map

Defining a callback to update the crime map graph based on user interactions.

   ```
   @app.callback(
      Output('crime-map', 'figure'),
      Input('crime-map', 'id')
   )
   def update_crime_map(_):
      fig = go.Figure()

      # Plot crime incidents
      fig.add_trace(go.Scatter(
         x=crime_locations[:, 0],
         y=crime_locations[:, 1],
         mode='markers',
         marker=dict(color='blue', size=5),
         name='Crime Incidents'
      ))

      # Plot crime hotspots
      fig.add_trace(go.Scatter(
         x=hotspot_centers[:, 0],
         y=hotspot_centers[:, 1],
         mode='markers',
         marker=dict(color='red', size=20, symbol='x'),
         name='Crime Hotspots'
      ))

      # Plot patrol units
      patrol_units_x = [unit[0] for unit in patrol_units]
      patrol_units_y = [unit[1] for unit in patrol_units]
      fig.add_trace(go.Scatter(
         x=patrol_units_x,
         y=patrol_units_y,
         mode='markers',
         marker=dict(color='green', size=10, symbol='circle'),
         name='Patrol Units'
      ))

      # Plot new incident
      new_incident_location = simulate_realtime_incidents(hotspot_centers)
      fig.add_trace(go.Scatter(
         x=[new_incident_location[0]],
         y=[new_incident_location[1]],
         mode='markers',
         marker=dict(color='purple', size=15, symbol='star'),
         name='New Incident'
      ))

      # Plot optimal routes
      for patrol_unit in patrol_units:
         for hotspot_center in hotspot_centers:
               fig.add_trace(go.Scatter(
                  x=[patrol_unit[0], hotspot_center[0]],
                  y=[patrol_unit[1], hotspot_center[1]],
                  mode='lines',
                  line=dict(color='black', width=1, dash='dash'),
                  showlegend=False
               ))

      fig.update_layout(
         title='Crime Map',
         xaxis_title='Latitude',
         yaxis_title='Longitude'
      )

      return fig
   ```

#### 9. Running the Application

Running the Dash app server to display the crime data analysis dashboard.

   ```
   if __name__ == '__main__':
      app.run_server(debug=True)
   ```


import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from sklearn.cluster import KMeans

# Simulate crime data generation
np.random.seed(42)
num_incidents = 1000
crime_locations = np.random.rand(num_incidents, 2)  # Random 2D coordinates

# Crime Hotspots Analysis
def identify_hotspots(crime_locations, num_hotspots):
    kmeans = KMeans(n_clusters=num_hotspots, random_state=42)
    kmeans.fit(crime_locations)
    hotspot_centers = kmeans.cluster_centers_
    return hotspot_centers

# Patrol Route Optimization
def optimize_routes(hotspot_centers, num_patrol_units):
    patrol_units = []
    for i in range(num_patrol_units):
        random_point = np.random.rand(2)
        closest_hotspot = np.argmin(np.linalg.norm(hotspot_centers - random_point, axis=1))
        patrol_units.append(hotspot_centers[closest_hotspot])
    return patrol_units

# Dynamic Route Adjustment (Simulated Real-Time Incidents)
def simulate_realtime_incidents(hotspot_centers):
    new_incident = np.random.choice(len(hotspot_centers))
    return hotspot_centers[new_incident]

# Initial hotspot identification and patrol route optimization
num_hotspots = 3
hotspot_centers = identify_hotspots(crime_locations, num_hotspots)
num_patrol_units = 5
patrol_units = optimize_routes(hotspot_centers, num_patrol_units)

# Create Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1("Crime Data Analysis Dashboard"),
    dcc.Graph(id='crime-map')
])

# Define callback to update crime map
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
        marker=dict(color='red', size=10, symbol='x'),
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

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
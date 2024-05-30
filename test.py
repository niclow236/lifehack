import numpy as np
import matplotlib.pyplot as plt
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

num_hotspots = 3
hotspot_centers = identify_hotspots(crime_locations, num_hotspots)

# Debug: Print hotspot centers to verify
print("Hotspot centers:\n", hotspot_centers)

# Patrol Route Optimization
def optimize_routes(hotspot_centers, num_patrol_units):
    patrol_units = []
    for i in range(num_patrol_units):
        random_point = np.random.rand(2)
        closest_hotspot = np.argmin(np.linalg.norm(hotspot_centers - random_point, axis=1))
        patrol_units.append(hotspot_centers[closest_hotspot])
    return patrol_units

num_patrol_units = 5
patrol_units = optimize_routes(hotspot_centers, num_patrol_units)

# Dynamic Route Adjustment (Simulated Real-Time Incidents)
def simulate_realtime_incidents(hotspot_centers):
    new_incident = np.random.choice(len(hotspot_centers))
    return hotspot_centers[new_incident]

# Main Simulation Loop
num_iterations = 10
for i in range(num_iterations):
    # Simulate real-time incident
    new_incident_location = simulate_realtime_incidents(hotspot_centers)
    
    # Update patrol routes based on new incident
    patrol_units = optimize_routes(np.vstack([hotspot_centers, new_incident_location]), num_patrol_units)
    
    # Visualization
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

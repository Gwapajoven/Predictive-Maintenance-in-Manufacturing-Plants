import heapq
from collections import defaultdict

# Sensor Metadata Management (Hash Table)
class SensorMetadata:
    def __init__(self):
        self.metadata = {}  # Dictionary to store sensor ID and corresponding metadata

    def add_sensor(self, sensor_id, location, machine_id, threshold):
        """Add metadata for a new sensor."""
        self.metadata[sensor_id] = {
            "location": location,
            "machine_id": machine_id,
            "threshold": threshold
        }

    def get_sensor(self, sensor_id):
        """Retrieve metadata for a given sensor ID."""
        return self.metadata.get(sensor_id, "Sensor not found")

# Time-Series Data Storage (Prefix Tree or Dictionary)
class TimeSeriesData:
    def __init__(self):
        self.data = defaultdict(dict)  # Dictionary to store {sensor_id: {timestamp: value}}

    def add_reading(self, sensor_id, timestamp, value):
        """Store a time-series reading for a specific sensor."""
        self.data[sensor_id][timestamp] = value

    def get_reading(self, sensor_id, timestamp):
        """Retrieve a specific time-series reading for a sensor at a given timestamp."""
        return self.data[sensor_id].get(timestamp, "No data available")

    def get_all_readings(self, sensor_id):
        """Retrieve all readings for a specific sensor."""
        return self.data[sensor_id] if sensor_id in self.data else "No readings available for this sensor"

# Anomaly Detection (Top-K using Min-Heap)
class TopKAnomalies:
    def __init__(self, K):
        self.K = K
        self.heap = []  # Min-Heap to track top-K anomalies

    def add_anomaly(self, sensor_id, timestamp, deviation):
        """Add a new anomaly to the heap. Only keeps the top-K anomalies."""
        heapq.heappush(self.heap, (deviation, sensor_id, timestamp))
        if len(self.heap) > self.K:
            heapq.heappop(self.heap)  # Remove the smallest anomaly to maintain top-K

    def get_top_anomalies(self):
        """Return the top-K anomalies sorted by deviation."""
        return sorted(self.heap, reverse=True)

# Integration: Predictive Maintenance System
class PredictiveMaintenanceSystem:
    def __init__(self, K):
        self.sensor_metadata = SensorMetadata()
        self.time_series_data = TimeSeriesData()
        self.top_k_anomalies = TopKAnomalies(K)

    def add_sensor(self, sensor_id, location, machine_id, threshold):
        """Add a new sensor with metadata."""
        self.sensor_metadata.add_sensor(sensor_id, location, machine_id, threshold)

    def add_sensor_reading(self, sensor_id, timestamp, value):
        """Add a new time-series reading for a sensor and check for anomalies."""
        # Add the reading to time-series storage
        self.time_series_data.add_reading(sensor_id, timestamp, value)

        # Check for anomaly based on predefined threshold
        sensor_info = self.sensor_metadata.get_sensor(sensor_id)
        if sensor_info != "Sensor not found":
            threshold = sensor_info["threshold"]
            deviation = abs(value - threshold)
            if deviation > threshold:
                # Add to anomaly tracker if deviation exceeds the threshold
                self.top_k_anomalies.add_anomaly(sensor_id, timestamp, deviation)

    def get_sensor_metadata(self, sensor_id):
        """Retrieve metadata for a given sensor ID."""
        return self.sensor_metadata.get_sensor(sensor_id)

    def get_sensor_reading(self, sensor_id, timestamp):
        """Retrieve a specific time-series reading for a sensor."""
        return self.time_series_data.get_reading(sensor_id, timestamp)

    def get_all_readings(self, sensor_id):
        """Retrieve all readings for a specific sensor."""
        return self.time_series_data.get_all_readings(sensor_id)

    def get_top_anomalies(self):
        """Retrieve the top-K anomalies detected so far."""
        return self.top_k_anomalies.get_top_anomalies()

# Demonstration of the Predictive Maintenance System
if __name__ == "__main__":
    # Initialize system with top-3 anomalies tracker
    system = PredictiveMaintenanceSystem(K=3)

    # Adding sensors
    system.add_sensor("sensor_1", "Factory Floor A", "Machine_1", 50)
    system.add_sensor("sensor_2", "Factory Floor B", "Machine_2", 75)

    # Adding readings
    system.add_sensor_reading("sensor_1", "2024-10-01 12:00", 55)  # Deviation 5 (Anomaly)
    system.add_sensor_reading("sensor_1", "2024-10-01 12:05", 60)  # Deviation 10 (Anomaly)
    system.add_sensor_reading("sensor_1", "2024-10-01 12:10", 45)  # Deviation 5 (Anomaly)
    system.add_sensor_reading("sensor_1", "2024-10-01 12:15", 70)  # Deviation 20 (Top-K anomaly)
    system.add_sensor_reading("sensor_2", "2024-10-01 12:00", 80)  # Deviation 5 (Anomaly)
    system.add_sensor_reading("sensor_2", "2024-10-01 12:05", 100) # Deviation 25 (Top-K anomaly)

    # Retrieve metadata
    print("Metadata for sensor_1:", system.get_sensor_metadata("sensor_1"))

    # Retrieve a specific reading
    print("Reading for sensor_1 at 12:05:", system.get_sensor_reading("sensor_1", "2024-10-01 12:05"))

    # Retrieve all readings for a sensor
    print("All readings for sensor_1:", system.get_all_readings("sensor_1"))

    # Retrieve top-3 anomalies detected
    print("Top-3 anomalies:", system.get_top_anomalies())

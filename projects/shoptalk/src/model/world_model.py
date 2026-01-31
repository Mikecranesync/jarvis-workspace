#!/usr/bin/env python3
"""
ShopTalk World Model
Learns equipment behavior and predicts expected states.

A "world model" learns the dynamics of a system - given a state and action,
what state comes next? For industrial equipment, this means learning:
- Normal operating patterns
- Correlations between sensors
- Expected responses to control inputs

Anomalies are detected when reality diverges from prediction.
"""

import numpy as np
import json
import pickle
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from collections import deque
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WorldModel")


@dataclass
class EquipmentState:
    """Represents equipment state at a point in time."""
    timestamp: float
    sensors: Dict[str, float]  # sensor_name -> value
    controls: Dict[str, float]  # control_name -> value
    discrete: Dict[str, bool]  # digital I/O states
    
    def to_vector(self, feature_order: List[str]) -> np.ndarray:
        """Convert to feature vector."""
        values = []
        for f in feature_order:
            if f in self.sensors:
                values.append(self.sensors[f])
            elif f in self.controls:
                values.append(self.controls[f])
            elif f in self.discrete:
                values.append(1.0 if self.discrete[f] else 0.0)
            else:
                values.append(0.0)
        return np.array(values, dtype=np.float32)
    
    @classmethod
    def from_vector(cls, vector: np.ndarray, feature_order: List[str],
                    timestamp: float = 0.0) -> 'EquipmentState':
        """Create from feature vector."""
        sensors = {}
        controls = {}
        discrete = {}
        
        for i, f in enumerate(feature_order):
            if f.startswith('ctrl_'):
                controls[f] = float(vector[i])
            elif f.startswith('dig_'):
                discrete[f] = bool(vector[i] > 0.5)
            else:
                sensors[f] = float(vector[i])
        
        return cls(timestamp=timestamp, sensors=sensors, 
                   controls=controls, discrete=discrete)


class WorldModel:
    """
    Equipment World Model using simple but effective techniques.
    
    For edge deployment, we use:
    1. Running statistics (mean, std) for each sensor
    2. Correlation matrix for sensor relationships
    3. Autoregressive model for temporal patterns
    
    This is lightweight enough for BeagleBone while still catching anomalies.
    """
    
    def __init__(self, window_size: int = 100, anomaly_threshold: float = 3.0):
        """
        Initialize world model.
        
        Args:
            window_size: Number of samples for statistics
            anomaly_threshold: Z-score threshold for anomaly detection
        """
        self.window_size = window_size
        self.anomaly_threshold = anomaly_threshold
        
        # Feature configuration
        self.feature_order: List[str] = []
        self.n_features = 0
        
        # Running statistics
        self.means: Optional[np.ndarray] = None
        self.stds: Optional[np.ndarray] = None
        self.correlation: Optional[np.ndarray] = None
        
        # Temporal model (simple AR coefficients)
        self.ar_coefficients: Optional[np.ndarray] = None
        
        # History buffer
        self.history = deque(maxlen=window_size)
        
        # Training state
        self.is_trained = False
        self.training_samples = 0
        
    def configure_features(self, feature_names: List[str]):
        """Configure which features to track."""
        self.feature_order = feature_names
        self.n_features = len(feature_names)
        logger.info(f"Configured {self.n_features} features: {feature_names}")
    
    def update(self, state: EquipmentState) -> Dict:
        """
        Update model with new state and return predictions/anomalies.
        
        Args:
            state: Current equipment state
            
        Returns:
            Dict with predictions, anomaly scores, and diagnostics
        """
        vector = state.to_vector(self.feature_order)
        self.history.append(vector)
        
        if not self.is_trained:
            return {"status": "training", "samples": len(self.history)}
        
        # Calculate anomaly scores
        z_scores = self._calculate_z_scores(vector)
        anomalies = self._detect_anomalies(z_scores)
        
        # Predict next state
        prediction = self._predict_next(vector)
        
        # Calculate prediction error
        if len(self.history) > 1:
            prev_prediction = self._predict_next(self.history[-2])
            prediction_error = np.abs(vector - prev_prediction)
        else:
            prediction_error = np.zeros(self.n_features)
        
        return {
            "status": "monitoring",
            "z_scores": {self.feature_order[i]: float(z_scores[i]) 
                        for i in range(self.n_features)},
            "anomalies": anomalies,
            "prediction": {self.feature_order[i]: float(prediction[i])
                          for i in range(self.n_features)},
            "prediction_error": {self.feature_order[i]: float(prediction_error[i])
                                for i in range(self.n_features)},
            "is_anomaly": len(anomalies) > 0
        }
    
    def _calculate_z_scores(self, vector: np.ndarray) -> np.ndarray:
        """Calculate Z-scores for each feature."""
        if self.means is None or self.stds is None:
            return np.zeros(self.n_features)
        
        # Avoid division by zero
        safe_stds = np.where(self.stds > 1e-6, self.stds, 1.0)
        return (vector - self.means) / safe_stds
    
    def _detect_anomalies(self, z_scores: np.ndarray) -> List[Dict]:
        """Detect anomalies based on Z-scores."""
        anomalies = []
        for i, z in enumerate(z_scores):
            if abs(z) > self.anomaly_threshold:
                anomalies.append({
                    "feature": self.feature_order[i],
                    "z_score": float(z),
                    "severity": "high" if abs(z) > 5 else "medium",
                    "direction": "high" if z > 0 else "low"
                })
        return anomalies
    
    def _predict_next(self, vector: np.ndarray) -> np.ndarray:
        """Predict next state using AR model."""
        if self.ar_coefficients is None:
            return vector  # Naive prediction: same as current
        
        # Simple AR(1): next = mean + coefficient * (current - mean)
        prediction = self.means + self.ar_coefficients * (vector - self.means)
        return prediction
    
    def train(self, data: List[EquipmentState], epochs: int = 1):
        """
        Train world model on historical data.
        
        Args:
            data: List of equipment states
            epochs: Not used for statistical model (here for API consistency)
        """
        if len(data) < 10:
            logger.warning(f"Insufficient data: {len(data)} samples")
            return
        
        logger.info(f"Training on {len(data)} samples...")
        
        # Convert to matrix
        X = np.array([s.to_vector(self.feature_order) for s in data])
        
        # Calculate statistics
        self.means = np.mean(X, axis=0)
        self.stds = np.std(X, axis=0)
        
        # Calculate correlation matrix
        self.correlation = np.corrcoef(X.T)
        
        # Fit AR(1) coefficients
        if len(X) > 1:
            X_t = X[:-1]  # States at time t
            X_t1 = X[1:]  # States at time t+1
            
            # For each feature, fit AR(1)
            self.ar_coefficients = np.zeros(self.n_features)
            for i in range(self.n_features):
                if self.stds[i] > 1e-6:
                    # AR coefficient = correlation between consecutive values
                    self.ar_coefficients[i] = np.corrcoef(X_t[:, i], X_t1[:, i])[0, 1]
        
        self.is_trained = True
        self.training_samples = len(data)
        logger.info(f"Training complete. Model ready.")
    
    def train_incremental(self, state: EquipmentState):
        """
        Incrementally update model with new sample.
        Useful for online learning on edge devices.
        """
        vector = state.to_vector(self.feature_order)
        
        if self.means is None:
            self.means = vector.copy()
            self.stds = np.ones(self.n_features)
            self.training_samples = 1
        else:
            # Online update of mean and variance (Welford's algorithm)
            self.training_samples += 1
            n = self.training_samples
            
            delta = vector - self.means
            self.means += delta / n
            
            if n > 1:
                # Update running variance
                delta2 = vector - self.means
                variance = self.stds ** 2
                variance = ((n - 2) * variance + delta * delta2) / (n - 1)
                self.stds = np.sqrt(np.maximum(variance, 1e-6))
        
        if self.training_samples >= 50 and not self.is_trained:
            self.is_trained = True
            logger.info(f"Model ready after {self.training_samples} samples")
    
    def diagnose(self, anomalies: List[Dict]) -> str:
        """
        Generate human-readable diagnosis from anomalies.
        
        Args:
            anomalies: List of detected anomalies
            
        Returns:
            Diagnostic message
        """
        if not anomalies:
            return "All systems operating normally."
        
        # Group by severity
        high_severity = [a for a in anomalies if a.get("severity") == "high"]
        medium_severity = [a for a in anomalies if a.get("severity") == "medium"]
        
        parts = []
        
        if high_severity:
            features = [a["feature"] for a in high_severity]
            parts.append(f"CRITICAL: {', '.join(features)} outside normal range")
        
        if medium_severity:
            features = [a["feature"] for a in medium_severity]
            parts.append(f"Warning: {', '.join(features)} showing unusual values")
        
        # Add specific insights based on known patterns
        for a in anomalies:
            feature = a["feature"]
            direction = a["direction"]
            
            if "current" in feature.lower() and direction == "high":
                parts.append("High current may indicate mechanical binding or overload")
            elif "temperature" in feature.lower() and direction == "high":
                parts.append("Elevated temperature - check cooling and lubrication")
            elif "speed" in feature.lower() and direction == "low":
                parts.append("Reduced speed - possible belt slip or motor issue")
            elif "vibration" in feature.lower() and direction == "high":
                parts.append("High vibration - check bearings and alignment")
        
        return ". ".join(parts) + "."
    
    def save(self, path: str):
        """Save model to file."""
        state = {
            "feature_order": self.feature_order,
            "means": self.means.tolist() if self.means is not None else None,
            "stds": self.stds.tolist() if self.stds is not None else None,
            "ar_coefficients": self.ar_coefficients.tolist() if self.ar_coefficients is not None else None,
            "window_size": self.window_size,
            "anomaly_threshold": self.anomaly_threshold,
            "is_trained": self.is_trained,
            "training_samples": self.training_samples
        }
        
        with open(path, 'w') as f:
            json.dump(state, f, indent=2)
        logger.info(f"Model saved to {path}")
    
    def load(self, path: str):
        """Load model from file."""
        with open(path, 'r') as f:
            state = json.load(f)
        
        self.feature_order = state["feature_order"]
        self.n_features = len(self.feature_order)
        self.means = np.array(state["means"]) if state["means"] else None
        self.stds = np.array(state["stds"]) if state["stds"] else None
        self.ar_coefficients = np.array(state["ar_coefficients"]) if state["ar_coefficients"] else None
        self.window_size = state["window_size"]
        self.anomaly_threshold = state["anomaly_threshold"]
        self.is_trained = state["is_trained"]
        self.training_samples = state["training_samples"]
        
        logger.info(f"Model loaded from {path}")


# Convenience functions for common scenarios
def create_conveyor_model() -> WorldModel:
    """Create a world model configured for conveyor systems."""
    model = WorldModel(window_size=200, anomaly_threshold=2.5)
    model.configure_features([
        "motor_speed",
        "motor_current",
        "conveyor_speed",
        "temperature",
        "sensor_1",
        "sensor_2",
        "sensor_3",
        "sensor_4"
    ])
    return model


def create_pump_model() -> WorldModel:
    """Create a world model configured for pump systems."""
    model = WorldModel(window_size=300, anomaly_threshold=2.0)
    model.configure_features([
        "flow_rate",
        "pressure_in",
        "pressure_out",
        "motor_current",
        "temperature",
        "vibration"
    ])
    return model


if __name__ == "__main__":
    # Demo
    print("ShopTalk World Model Demo")
    print("=" * 40)
    
    model = create_conveyor_model()
    
    # Generate synthetic training data
    print("\nGenerating synthetic training data...")
    training_data = []
    for i in range(500):
        state = EquipmentState(
            timestamp=float(i),
            sensors={
                "motor_speed": 1500 + np.random.normal(0, 20),
                "motor_current": 4.5 + np.random.normal(0, 0.2),
                "conveyor_speed": 80 + np.random.normal(0, 2),
                "temperature": 45 + np.random.normal(0, 1)
            },
            controls={},
            discrete={
                "sensor_1": np.random.random() > 0.5,
                "sensor_2": np.random.random() > 0.5,
                "sensor_3": np.random.random() > 0.5,
                "sensor_4": np.random.random() > 0.5
            }
        )
        training_data.append(state)
    
    # Train
    print("Training model...")
    model.train(training_data)
    
    # Test normal operation
    print("\nTesting normal operation...")
    normal_state = EquipmentState(
        timestamp=1000.0,
        sensors={
            "motor_speed": 1510,
            "motor_current": 4.6,
            "conveyor_speed": 81,
            "temperature": 46
        },
        controls={},
        discrete={"sensor_1": True, "sensor_2": False, 
                  "sensor_3": True, "sensor_4": False}
    )
    result = model.update(normal_state)
    print(f"Anomalies: {result['anomalies']}")
    print(f"Diagnosis: {model.diagnose(result['anomalies'])}")
    
    # Test anomaly
    print("\nTesting anomaly (high current = possible jam)...")
    anomaly_state = EquipmentState(
        timestamp=1001.0,
        sensors={
            "motor_speed": 1200,  # Low speed
            "motor_current": 8.5,  # High current
            "conveyor_speed": 30,  # Low conveyor speed
            "temperature": 52  # Elevated temp
        },
        controls={},
        discrete={"sensor_1": True, "sensor_2": True, 
                  "sensor_3": True, "sensor_4": True}
    )
    result = model.update(anomaly_state)
    print(f"Anomalies: {result['anomalies']}")
    print(f"Diagnosis: {model.diagnose(result['anomalies'])}")
    
    # Save model
    model.save("/tmp/conveyor_model.json")
    print("\nModel saved!")

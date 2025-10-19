#!/usr/bin/env python3
"""
ML Model Accuracy Testing Script for Streetly Disaster Predictions
Tests the accuracy of flood and earthquake prediction models
"""

import pickle
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import json
import os
from datetime import datetime, timedelta

class MLModelTester:
    def __init__(self):
        self.models = {}
        self.test_data = {}
        self.results = {}
        
    def load_models(self):
        """Load the trained ML models"""
        model_paths = {
            'flood': 'backend/app/rf_flood_7day_model.pkl',
            'earthquake': 'backend/app/rf_quake_7day_model.pkl'
        }
        
        for model_name, path in model_paths.items():
            try:
                if os.path.exists(path):
                    with open(path, 'rb') as f:
                        self.models[model_name] = pickle.load(f)
                    print(f"✅ Loaded {model_name} model from {path}")
                else:
                    print(f"⚠️ Model file not found: {path}")
            except Exception as e:
                print(f"❌ Error loading {model_name} model: {e}")
                
    def generate_test_data(self):
        """Generate synthetic test data for model validation"""
        print("🔄 Generating test data...")
        
        # Generate test data for Northern Pakistan locations
        locations = {
            'Hunza Valley': {'lat': 36.3167, 'lon': 74.65},
            'Skardu': {'lat': 35.2979, 'lon': 75.6333},
            'Naran': {'lat': 34.91, 'lon': 73.6522},
            'Swat Valley': {'lat': 35.2228, 'lon': 72.4258},
            'Neelum Valley': {'lat': 34.5869, 'lon': 73.9014},
            'Chitral': {'lat': 35.8511, 'lon': 71.7864}
        }
        
        # Generate synthetic features for testing
        np.random.seed(42)  # For reproducible results
        
        test_data = []
        for location, coords in locations.items():
            for day in range(7):  # 7 days of predictions
                # Generate realistic feature values
                features = {
                    'latitude': coords['lat'],
                    'longitude': coords['lon'],
                    'elevation': np.random.uniform(1000, 5000),  # Elevation in meters
                    'precipitation': np.random.uniform(0, 50),   # mm
                    'temperature': np.random.uniform(-10, 35),   # Celsius
                    'humidity': np.random.uniform(20, 90),       # Percentage
                    'wind_speed': np.random.uniform(0, 20),     # m/s
                    'pressure': np.random.uniform(950, 1050),   # hPa
                    'day_of_year': (datetime.now() + timedelta(days=day)).timetuple().tm_yday,
                    'month': (datetime.now() + timedelta(days=day)).month,
                    'season': self._get_season((datetime.now() + timedelta(days=day)).month)
                }
                
                # Add some realistic patterns
                if features['precipitation'] > 30:
                    features['flood_risk'] = 'high'
                elif features['precipitation'] > 15:
                    features['flood_risk'] = 'medium'
                else:
                    features['flood_risk'] = 'low'
                    
                if features['elevation'] > 3000 and features['temperature'] < 0:
                    features['earthquake_risk'] = 'medium'
                elif features['elevation'] > 4000:
                    features['earthquake_risk'] = 'high'
                else:
                    features['earthquake_risk'] = 'low'
                
                test_data.append({
                    'location': location,
                    'features': features,
                    'expected_flood_risk': features['flood_risk'],
                    'expected_earthquake_risk': features['earthquake_risk']
                })
        
        self.test_data = test_data
        print(f"✅ Generated {len(test_data)} test samples")
        return test_data
    
    def _get_season(self, month):
        """Get season based on month"""
        if month in [12, 1, 2]:
            return 'winter'
        elif month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        else:
            return 'autumn'
    
    def test_flood_model(self):
        """Test flood prediction model accuracy"""
        if 'flood' not in self.models:
            print("❌ Flood model not loaded")
            return None
            
        print("🌊 Testing Flood Prediction Model...")
        
        # Prepare test data
        X_test = []
        y_test = []
        
        for sample in self.test_data:
            features = sample['features']
            X_test.append([
                features['latitude'],
                features['longitude'],
                features['elevation'],
                features['precipitation'],
                features['temperature'],
                features['humidity'],
                features['wind_speed'],
                features['pressure'],
                features['day_of_year'],
                features['month']
            ])
            
            # Convert risk level to numeric for testing
            risk_mapping = {'low': 0, 'medium': 1, 'high': 2}
            y_test.append(risk_mapping[sample['expected_flood_risk']])
        
        X_test = np.array(X_test)
        y_test = np.array(y_test)
        
        # Make predictions
        try:
            y_pred = self.models['flood'].predict(X_test)
            
            # Calculate metrics
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
            recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
            f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
            
            results = {
                'model': 'flood',
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'total_samples': len(y_test),
                'correct_predictions': sum(y_test == y_pred)
            }
            
            print(f"📊 Flood Model Results:")
            print(f"   Accuracy: {accuracy:.3f}")
            print(f"   Precision: {precision:.3f}")
            print(f"   Recall: {recall:.3f}")
            print(f"   F1-Score: {f1:.3f}")
            print(f"   Correct Predictions: {sum(y_test == y_pred)}/{len(y_test)}")
            
            return results
            
        except Exception as e:
            print(f"❌ Error testing flood model: {e}")
            return None
    
    def test_earthquake_model(self):
        """Test earthquake prediction model accuracy"""
        if 'earthquake' not in self.models:
            print("❌ Earthquake model not loaded")
            return None
            
        print("🌍 Testing Earthquake Prediction Model...")
        
        # Prepare test data
        X_test = []
        y_test = []
        
        for sample in self.test_data:
            features = sample['features']
            X_test.append([
                features['latitude'],
                features['longitude'],
                features['elevation'],
                features['temperature'],
                features['humidity'],
                features['wind_speed'],
                features['pressure'],
                features['day_of_year'],
                features['month']
            ])
            
            # Convert risk level to numeric for testing
            risk_mapping = {'low': 0, 'medium': 1, 'high': 2}
            y_test.append(risk_mapping[sample['expected_earthquake_risk']])
        
        X_test = np.array(X_test)
        y_test = np.array(y_test)
        
        # Make predictions
        try:
            y_pred = self.models['earthquake'].predict(X_test)
            
            # Calculate metrics
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
            recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
            f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
            
            results = {
                'model': 'earthquake',
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'total_samples': len(y_test),
                'correct_predictions': sum(y_test == y_pred)
            }
            
            print(f"📊 Earthquake Model Results:")
            print(f"   Accuracy: {accuracy:.3f}")
            print(f"   Precision: {precision:.3f}")
            print(f"   Recall: {recall:.3f}")
            print(f"   F1-Score: {f1:.3f}")
            print(f"   Correct Predictions: {sum(y_test == y_pred)}/{len(y_test)}")
            
            return results
            
        except Exception as e:
            print(f"❌ Error testing earthquake model: {e}")
            return None
    
    def test_model_predictions(self):
        """Test model predictions with real-world scenarios"""
        print("🔮 Testing Model Predictions with Real Scenarios...")
        
        # Test scenarios for Northern Pakistan
        test_scenarios = [
            {
                'name': 'High Flood Risk Scenario',
                'features': {
                    'latitude': 35.2228, 'longitude': 72.4258, 'elevation': 1200,
                    'precipitation': 45, 'temperature': 15, 'humidity': 85,
                    'wind_speed': 8, 'pressure': 980, 'day_of_year': 180, 'month': 6
                },
                'expected_flood_risk': 'high'
            },
            {
                'name': 'Low Risk Scenario',
                'features': {
                    'latitude': 36.3167, 'longitude': 74.65, 'elevation': 2500,
                    'precipitation': 5, 'temperature': 20, 'humidity': 40,
                    'wind_speed': 3, 'pressure': 1020, 'day_of_year': 90, 'month': 3
                },
                'expected_flood_risk': 'low'
            },
            {
                'name': 'High Earthquake Risk Scenario',
                'features': {
                    'latitude': 35.2979, 'longitude': 75.6333, 'elevation': 4500,
                    'precipitation': 10, 'temperature': -5, 'humidity': 30,
                    'wind_speed': 12, 'pressure': 950, 'day_of_year': 300, 'month': 10
                },
                'expected_earthquake_risk': 'high'
            }
        ]
        
        for scenario in test_scenarios:
            print(f"\n🧪 Testing: {scenario['name']}")
            
            # Test flood prediction
            if 'flood' in self.models:
                try:
                    flood_features = [
                        scenario['features']['latitude'],
                        scenario['features']['longitude'],
                        scenario['features']['elevation'],
                        scenario['features']['precipitation'],
                        scenario['features']['temperature'],
                        scenario['features']['humidity'],
                        scenario['features']['wind_speed'],
                        scenario['features']['pressure'],
                        scenario['features']['day_of_year'],
                        scenario['features']['month']
                    ]
                    
                    flood_pred = self.models['flood'].predict([flood_features])[0]
                    risk_levels = ['low', 'medium', 'high']
                    predicted_risk = risk_levels[flood_pred]
                    
                    print(f"   🌊 Flood Prediction: {predicted_risk} (Expected: {scenario['expected_flood_risk']})")
                    
                except Exception as e:
                    print(f"   ❌ Flood prediction error: {e}")
            
            # Test earthquake prediction
            if 'earthquake' in self.models:
                try:
                    eq_features = [
                        scenario['features']['latitude'],
                        scenario['features']['longitude'],
                        scenario['features']['elevation'],
                        scenario['features']['temperature'],
                        scenario['features']['humidity'],
                        scenario['features']['wind_speed'],
                        scenario['features']['pressure'],
                        scenario['features']['day_of_year'],
                        scenario['features']['month']
                    ]
                    
                    eq_pred = self.models['earthquake'].predict([eq_features])[0]
                    risk_levels = ['low', 'medium', 'high']
                    predicted_risk = risk_levels[eq_pred]
                    
                    print(f"   🌍 Earthquake Prediction: {predicted_risk} (Expected: {scenario.get('expected_earthquake_risk', 'N/A')})")
                    
                except Exception as e:
                    print(f"   ❌ Earthquake prediction error: {e}")
    
    def generate_accuracy_report(self):
        """Generate comprehensive accuracy report"""
        print("\n" + "="*60)
        print("📊 ML MODEL ACCURACY TESTING REPORT")
        print("="*60)
        
        # Load models
        self.load_models()
        
        # Generate test data
        self.generate_test_data()
        
        # Test models
        flood_results = self.test_flood_model()
        earthquake_results = self.test_earthquake_model()
        
        # Test real scenarios
        self.test_model_predictions()
        
        # Generate summary
        print("\n" + "="*60)
        print("📈 SUMMARY")
        print("="*60)
        
        if flood_results:
            print(f"🌊 Flood Model Accuracy: {flood_results['accuracy']:.1%}")
        else:
            print("🌊 Flood Model: Not available")
            
        if earthquake_results:
            print(f"🌍 Earthquake Model Accuracy: {earthquake_results['accuracy']:.1%}")
        else:
            print("🌍 Earthquake Model: Not available")
        
        # Save results to file
        results = {
            'timestamp': datetime.now().isoformat(),
            'flood_model': flood_results,
            'earthquake_model': earthquake_results
        }
        
        with open('ml_accuracy_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved to: ml_accuracy_results.json")
        
        return results

def main():
    """Main testing function"""
    print("🚀 Starting ML Model Accuracy Testing...")
    
    tester = MLModelTester()
    results = tester.generate_accuracy_report()
    
    print("\n✅ Testing completed!")
    return results

if __name__ == "__main__":
    main()

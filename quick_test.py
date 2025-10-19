#!/usr/bin/env python3
"""
Quick ML Model Test Script
Simple testing for model accuracy and predictions
"""

import requests
import json
import time
from datetime import datetime

def test_api_endpoint():
    """Test if the ML API endpoint is working"""
    print("🔍 Testing ML API Endpoint...")
    
    try:
        response = requests.get("http://localhost:8081/ml-predictions", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Endpoint is working!")
            print(f"📊 Response time: {response.elapsed.total_seconds():.2f}s")
            
            if 'earthquake_predictions' in data:
                print(f"🌍 Earthquake predictions: {len(data['earthquake_predictions'])} locations")
            if 'flood_predictions' in data:
                print(f"🌊 Flood predictions: {len(data['flood_predictions'])} locations")
                
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API endpoint. Is the backend running?")
        print("💡 Start the backend with: cd backend/app && python3 disasters_api.py")
        return False
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def test_prediction_accuracy():
    """Test prediction accuracy with sample data"""
    print("\n🎯 Testing Prediction Accuracy...")
    
    # Sample test cases for Northern Pakistan
    test_cases = [
        {
            "name": "Hunza Valley - Low Risk",
            "lat": 36.3167,
            "lon": 74.65,
            "expected_flood": "low",
            "expected_earthquake": "low"
        },
        {
            "name": "Swat Valley - Medium Risk",
            "lat": 35.2228,
            "lon": 72.4258,
            "expected_flood": "medium",
            "expected_earthquake": "low"
        },
        {
            "name": "High Elevation - Earthquake Risk",
            "lat": 35.2979,
            "lon": 75.6333,
            "expected_flood": "low",
            "expected_earthquake": "medium"
        }
    ]
    
    correct_predictions = 0
    total_predictions = 0
    
    for case in test_cases:
        print(f"\n🧪 Testing: {case['name']}")
        
        try:
            # Make prediction request
            response = requests.get("http://localhost:8081/ml-predictions", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if we can find predictions for this location
                found_flood = False
                found_earthquake = False
                
                # Check flood predictions
                if 'flood_predictions' in data:
                    for location, prediction in data['flood_predictions'].items():
                        if abs(prediction.get('latitude', 0) - case['lat']) < 0.1:
                            found_flood = True
                            predicted_flood = prediction.get('risk_level', 'unknown')
                            print(f"   🌊 Flood prediction: {predicted_flood}")
                            break
                
                # Check earthquake predictions
                if 'earthquake_predictions' in data:
                    for location, prediction in data['earthquake_predictions'].items():
                        if abs(prediction.get('latitude', 0) - case['lat']) < 0.1:
                            found_earthquake = True
                            predicted_earthquake = prediction.get('risk_level', 'unknown')
                            print(f"   🌍 Earthquake prediction: {predicted_earthquake}")
                            break
                
                if found_flood or found_earthquake:
                    correct_predictions += 1
                else:
                    print(f"   ⚠️ No predictions found for this location")
                
                total_predictions += 1
                
            else:
                print(f"   ❌ API error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    if total_predictions > 0:
        accuracy = (correct_predictions / total_predictions) * 100
        print(f"\n📊 Prediction Accuracy: {accuracy:.1f}% ({correct_predictions}/{total_predictions})")
        
        if accuracy >= 80:
            print("✅ Model accuracy is good!")
        elif accuracy >= 60:
            print("⚠️ Model accuracy is acceptable")
        else:
            print("❌ Model accuracy needs improvement")
    else:
        print("❌ No predictions could be tested")

def test_model_performance():
    """Test model performance metrics"""
    print("\n⚡ Testing Model Performance...")
    
    try:
        start_time = time.time()
        response = requests.get("http://localhost:8081/ml-predictions", timeout=10)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        print(f"📈 Performance Metrics:")
        print(f"   Response Time: {response_time:.3f}s")
        
        if response_time < 1.0:
            print("   ✅ Excellent performance")
        elif response_time < 3.0:
            print("   ✅ Good performance")
        elif response_time < 5.0:
            print("   ⚠️ Acceptable performance")
        else:
            print("   ❌ Slow performance")
        
        if response.status_code == 200:
            data = response.json()
            data_size = len(json.dumps(data))
            print(f"   Data Size: {data_size} bytes")
            print(f"   Throughput: {data_size / response_time:.0f} bytes/s")
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")

def generate_test_report():
    """Generate a comprehensive test report"""
    print("\n" + "="*60)
    print("📋 ML MODEL TESTING REPORT")
    print("="*60)
    print(f"🕐 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test API endpoint
    api_working = test_api_endpoint()
    
    if api_working:
        # Test predictions
        test_prediction_accuracy()
        
        # Test performance
        test_model_performance()
        
        print("\n" + "="*60)
        print("✅ TESTING COMPLETED")
        print("="*60)
        print("💡 Recommendations:")
        print("   - Monitor model accuracy over time")
        print("   - Update training data regularly")
        print("   - Test with real-world scenarios")
        print("   - Compare predictions with actual events")
    else:
        print("\n❌ Cannot run tests - API endpoint not available")
        print("💡 Make sure the backend is running:")
        print("   cd backend/app && python3 disasters_api.py")

if __name__ == "__main__":
    generate_test_report()

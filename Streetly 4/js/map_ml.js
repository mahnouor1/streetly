// js/map_ml.js - ML Disaster Predictions Integration
let mlPredictionMarkers = [];
let currentInfoWindow = null;

// ML Prediction API Configuration
const ML_API_BASE = "http://localhost:8081";
const DISASTER_API_BASE = "http://localhost:8081";

// Initialize ML predictions on map load
function initMLPredictions() {
    console.log("🤖 Initializing ML predictions...");
    clearMLPredictionMarkers();
}

// Clear all ML prediction markers
function clearMLPredictionMarkers() {
    mlPredictionMarkers.forEach(marker => marker.setMap(null));
    mlPredictionMarkers = [];
    console.log("🧹 Cleared ML prediction markers");
}

// Fetch ML predictions from backend
async function fetchMLPredictions() {
    try {
        console.log("🔮 Fetching ML predictions...");
        const response = await fetch(`${ML_API_BASE}/ml-predictions`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log("📊 ML predictions data:", data);
        
        // Extract predictions from the response
        const predictions = [];
        
        // Process earthquake predictions
        if (data.earthquake_predictions) {
            Object.entries(data.earthquake_predictions).forEach(([location, prediction]) => {
                if (prediction.latitude && prediction.longitude) {
                    predictions.push({
                        type: 'earthquake',
                        location: location,
                        latitude: prediction.latitude,
                        longitude: prediction.longitude,
                        risk: prediction.risk_level || 'medium',
                        probability: prediction.probability || 0.5,
                        confidence: prediction.confidence || 0.7
                    });
                }
            });
        }
        
        // Process flood predictions
        if (data.flood_predictions) {
            Object.entries(data.flood_predictions).forEach(([location, prediction]) => {
                if (prediction.latitude && prediction.longitude) {
                    predictions.push({
                        type: 'flood',
                        location: location,
                        latitude: prediction.latitude,
                        longitude: prediction.longitude,
                        risk: prediction.risk_level || 'medium',
                        probability: prediction.probability || 0.5,
                        confidence: prediction.confidence || 0.7
                    });
                }
            });
        }
        
        console.log(`🎯 Found ${predictions.length} predictions`);
        return predictions;
        
    } catch (error) {
        console.error("❌ Error fetching ML predictions:", error);
        return [];
    }
}

// Plot ML predictions on map
async function plotMLPredictions() {
    try {
        console.log("🗺️ Plotting ML predictions on map...");
        
        // Clear existing markers
        clearMLPredictionMarkers();
        
        // Fetch predictions
        const predictions = await fetchMLPredictions();
        
        if (predictions.length === 0) {
            console.log("⚠️ No ML predictions available");
            return;
        }
        
        // Plot each prediction
        predictions.forEach((prediction, index) => {
            plotMLPredictionMarker(prediction, index);
        });
        
        console.log(`✅ Plotted ${predictions.length} ML prediction markers`);
        
    } catch (error) {
        console.error("❌ Error plotting ML predictions:", error);
    }
}

// Plot individual ML prediction marker
function plotMLPredictionMarker(prediction, index) {
    const position = {
        lat: parseFloat(prediction.latitude),
        lng: parseFloat(prediction.longitude)
    };
    
    // Determine marker color and size based on risk level
    let markerColor, markerSize, markerSymbol;
    
    switch (prediction.risk) {
        case 'high':
            markerColor = '#dc2626'; // Red
            markerSize = 40;
            markerSymbol = '🔴';
            break;
        case 'medium':
            markerColor = '#f59e0b'; // Amber
            markerSize = 35;
            markerSymbol = '🟡';
            break;
        case 'low':
            markerColor = '#10b981'; // Green
            markerSize = 30;
            markerSymbol = '🟢';
            break;
        default:
            markerColor = '#6b7280'; // Gray
            markerSize = 30;
            markerSymbol = '⚪';
    }
    
    // Create custom SVG icon
    const icon = {
        url: `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(`
            <svg xmlns="http://www.w3.org/2000/svg" width="${markerSize}" height="${markerSize}" viewBox="0 0 24 24">
                <defs>
                    <filter id="glow">
                        <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                        <feMerge> 
                            <feMergeNode in="coloredBlur"/>
                            <feMergeNode in="SourceGraphic"/>
                        </feMerge>
                    </filter>
                </defs>
                <circle cx="12" cy="12" r="10" fill="${markerColor}" filter="url(#glow)" opacity="0.8"/>
                <circle cx="12" cy="12" r="8" fill="white" opacity="0.9"/>
                <text x="12" y="16" text-anchor="middle" font-size="12" font-weight="bold" fill="${markerColor}">
                    ${prediction.type === 'earthquake' ? 'E' : 'F'}
                </text>
            </svg>
        `)}`,
        scaledSize: new google.maps.Size(markerSize, markerSize),
        anchor: new google.maps.Point(markerSize/2, markerSize/2)
    };
    
    // Create marker
    const marker = new google.maps.Marker({
        position: position,
        map: map,
        icon: icon,
        title: `${prediction.type.toUpperCase()} Risk: ${prediction.risk} - ${prediction.location}`,
        animation: google.maps.Animation.DROP
    });
    
    // Create info window content
    const infoHtml = `
        <div style="max-width: 250px; font-family: 'Poppins', sans-serif;">
            <div style="background: linear-gradient(135deg, ${markerColor}20, ${markerColor}40); padding: 12px; border-radius: 8px; border-left: 4px solid ${markerColor};">
                <h3 style="margin: 0 0 8px 0; color: ${markerColor}; font-size: 16px; font-weight: 600;">
                    ${markerSymbol} ${prediction.type.toUpperCase()} PREDICTION
                </h3>
                <p style="margin: 0 0 6px 0; font-size: 14px; color: #374151; font-weight: 500;">
                    📍 ${prediction.location}
                </p>
                <div style="display: flex; justify-content: space-between; margin: 8px 0;">
                    <span style="font-size: 12px; color: #6b7280;">Risk Level:</span>
                    <span style="font-size: 12px; font-weight: 600; color: ${markerColor}; text-transform: uppercase;">
                        ${prediction.risk}
                    </span>
                </div>
                <div style="display: flex; justify-content: space-between; margin: 4px 0;">
                    <span style="font-size: 12px; color: #6b7280;">Probability:</span>
                    <span style="font-size: 12px; font-weight: 600; color: #374151;">
                        ${Math.round(prediction.probability * 100)}%
                    </span>
                </div>
                <div style="display: flex; justify-content: space-between; margin: 4px 0;">
                    <span style="font-size: 12px; color: #6b7280;">Confidence:</span>
                    <span style="font-size: 12px; font-weight: 600; color: #374151;">
                        ${Math.round(prediction.confidence * 100)}%
                    </span>
                </div>
                <div style="margin-top: 8px; padding: 6px; background: #f3f4f6; border-radius: 4px; font-size: 11px; color: #6b7280;">
                    🤖 ML Model Prediction (7-day forecast)
                </div>
            </div>
        </div>
    `;
    
    // Create info window
    const infoWindow = new google.maps.InfoWindow({
        content: infoHtml
    });
    
    // Add click listener
    marker.addListener('click', () => {
        // Close previous info window
        if (currentInfoWindow) {
            currentInfoWindow.close();
        }
        
        // Open new info window
        infoWindow.open(map, marker);
        currentInfoWindow = infoWindow;
    });
    
    // Add to markers array
    mlPredictionMarkers.push(marker);
}

// Handle Predict Disaster button click
async function handlePredictDisaster() {
    console.log("🔮 Predict Disaster button clicked");
    
    const btn = document.getElementById('predictDisasterBtn');
    if (!btn) {
        console.error("❌ Predict Disaster button not found");
        return;
    }
    
    try {
        // Update button state
        btn.textContent = 'Loading...';
        btn.disabled = true;
        
        // Plot ML predictions
        await plotMLPredictions();
        
        // Reset button
        btn.textContent = '🔮 Predict Disaster';
        btn.disabled = false;
        
        console.log("✅ ML predictions loaded successfully");
        
    } catch (error) {
        console.error("❌ Error in Predict Disaster:", error);
        
        // Reset button on error
        btn.textContent = '🔮 Predict Disaster';
        btn.disabled = false;
        
        // Show error message
        alert("❌ Failed to load disaster predictions. Please try again.");
    }
}

// Fetch real disaster events
async function fetchDisasterEvents() {
    try {
        console.log("🚨 Fetching real disaster events...");
        const response = await fetch(`${DISASTER_API_BASE}/disasters?country=Pakistan`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log("📊 Disaster events data:", data);
        
        return data.events || [];
        
    } catch (error) {
        console.error("❌ Error fetching disaster events:", error);
        return [];
    }
}

// Plot real disaster events
async function plotDisasterEvents() {
    try {
        console.log("🗺️ Plotting real disaster events...");
        
        const events = await fetchDisasterEvents();
        
        if (events.length === 0) {
            console.log("ℹ️ No active disaster events found");
            return;
        }
        
        events.forEach(event => {
            plotDisasterEventMarker(event);
        });
        
        console.log(`✅ Plotted ${events.length} disaster event markers`);
        
    } catch (error) {
        console.error("❌ Error plotting disaster events:", error);
    }
}

// Plot individual disaster event marker
function plotDisasterEventMarker(event) {
    const position = {
        lat: parseFloat(event.lat),
        lng: parseFloat(event.lon)
    };
    
    // Create warning icon
    const icon = {
        url: `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(`
            <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24">
                <defs>
                    <filter id="warningGlow">
                        <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
                        <feMerge> 
                            <feMergeNode in="coloredBlur"/>
                            <feMergeNode in="SourceGraphic"/>
                        </feMerge>
                    </filter>
                </defs>
                <circle cx="12" cy="12" r="11" fill="#dc2626" filter="url(#warningGlow)" opacity="0.9"/>
                <path d="M12 8v4M12 16h.01" stroke="white" stroke-width="2" stroke-linecap="round"/>
                <circle cx="12" cy="12" r="1" fill="white"/>
            </svg>
        `)}`,
        scaledSize: new google.maps.Size(36, 36),
        anchor: new google.maps.Point(18, 18)
    };
    
    // Create marker
    const marker = new google.maps.Marker({
        position: position,
        map: map,
        icon: icon,
        title: `⚠️ ${event.name} (${event.type})`,
        animation: google.maps.Animation.BOUNCE
    });
    
    // Create info window
    const infoHtml = `
        <div style="max-width: 250px; font-family: 'Poppins', sans-serif;">
            <div style="background: linear-gradient(135deg, #fef2f2, #fee2e2); padding: 12px; border-radius: 8px; border-left: 4px solid #dc2626;">
                <h3 style="margin: 0 0 8px 0; color: #dc2626; font-size: 16px; font-weight: 600;">
                    ⚠️ ACTIVE DISASTER EVENT
                </h3>
                <p style="margin: 0 0 6px 0; font-size: 14px; color: #374151; font-weight: 500;">
                    ${event.name}
                </p>
                <div style="display: flex; justify-content: space-between; margin: 4px 0;">
                    <span style="font-size: 12px; color: #6b7280;">Type:</span>
                    <span style="font-size: 12px; font-weight: 600; color: #374151; text-transform: uppercase;">
                        ${event.type}
                    </span>
                </div>
                ${event.severity ? `
                <div style="display: flex; justify-content: space-between; margin: 4px 0;">
                    <span style="font-size: 12px; color: #6b7280;">Severity:</span>
                    <span style="font-size: 12px; font-weight: 600; color: #dc2626;">
                        ${event.severity}
                    </span>
                </div>
                ` : ''}
                ${event.magnitude ? `
                <div style="display: flex; justify-content: space-between; margin: 4px 0;">
                    <span style="font-size: 12px; color: #6b7280;">Magnitude:</span>
                    <span style="font-size: 12px; font-weight: 600; color: #374151;">
                        ${event.magnitude}
                    </span>
                </div>
                ` : ''}
                <div style="margin-top: 8px; padding: 6px; background: #fef2f2; border-radius: 4px; font-size: 11px; color: #dc2626;">
                    🚨 Real-time disaster event
                </div>
            </div>
        </div>
    `;
    
    const infoWindow = new google.maps.InfoWindow({
        content: infoHtml
    });
    
    // Add click listener
    marker.addListener('click', () => {
        if (currentInfoWindow) {
            currentInfoWindow.close();
        }
        infoWindow.open(map, marker);
        currentInfoWindow = infoWindow;
    });
    
    // Add to markers array
    mlPredictionMarkers.push(marker);
}

// Initialize ML predictions when map is ready
function startMLPredictions() {
    console.log("🤖 Starting ML predictions system...");
    initMLPredictions();
}

// Export functions for global access
window.handlePredictDisaster = handlePredictDisaster;
window.plotMLPredictions = plotMLPredictions;
window.clearMLPredictionMarkers = clearMLPredictionMarkers;
window.startMLPredictions = startMLPredictions;

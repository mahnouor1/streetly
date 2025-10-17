# Streetly Travel Assistant

A comprehensive travel assistant application that provides weather information, navigation, nearby places, and intelligent recommendations for travelers.

## 🏗️ Project Structure

```
stee/
├─ colab/ 
│  └─ Streetly_Travel_Assistant_Training.ipynb
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ weather.py
│  │  ├─ maps.py
│  │  ├─ places.py
│  │  └─ fcm_utils.py
│  ├─ requirements.txt
│  └─ Dockerfile
├─ frontend/
│  └─ (your frontend repo code or cloned/staged files)
├─ firebase/
│  ├─ firebase.json
│  └─ firestore.rules
└─ README.md
```

## 🚀 Features

### Backend Services
- **Weather Service**: Real-time weather data and forecasts using OpenWeather API
- **Maps Service**: Directions, distance calculations, and geocoding using Google Maps API
- **Places Service**: Nearby places search and detailed place information
- **FCM Service**: Push notifications for travel updates and alerts

### AI/ML Components
- **Intent Classification**: LSTM-based model for understanding user queries
- **Travel Recommendations**: Personalized suggestions based on user preferences
- **Weather Pattern Analysis**: Predictive weather insights for travel planning

### Firebase Integration
- **Authentication**: User management and security
- **Firestore**: Real-time database for user data and preferences
- **Cloud Functions**: Serverless backend processing
- **Hosting**: Frontend deployment

## 🛠️ Setup and Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- Firebase CLI
- Docker (optional)

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**:
   ```bash
   export OPENWEATHER_API_KEY="your_openweather_api_key"
   export GOOGLE_MAPS_API_KEY="your_google_maps_api_key"
   export GOOGLE_PLACES_API_KEY="your_google_places_api_key"
   export FCM_SERVER_KEY="your_fcm_server_key"
   ```

4. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

### Docker Setup

1. **Build the Docker image**:
   ```bash
   docker build -t streetly-backend .
   ```

2. **Run the container**:
   ```bash
   docker run -p 8000:8000 streetly-backend
   ```

### Firebase Setup

1. **Install Firebase CLI**:
   ```bash
   npm install -g firebase-tools
   ```

2. **Login to Firebase**:
   ```bash
   firebase login
   ```

3. **Initialize Firebase project**:
   ```bash
   cd firebase
   firebase init
   ```

4. **Deploy Firebase services**:
   ```bash
   firebase deploy
   ```

## 📊 API Endpoints

### Weather
- `GET /weather/{location}` - Get current weather for a location
- `GET /weather/forecast/{location}` - Get weather forecast

### Maps & Navigation
- `GET /directions` - Get directions between two points
- `GET /distance-matrix` - Calculate distances between multiple points
- `GET /geocode` - Convert address to coordinates

### Places
- `GET /places/nearby` - Find nearby places
- `GET /places/details/{place_id}` - Get detailed place information
- `GET /places/search` - Search for places

### Notifications
- `POST /notifications/send` - Send push notification
- `POST /notifications/multicast` - Send to multiple devices
- `POST /notifications/topic` - Send to topic subscribers

## 🤖 AI Model Training

The Jupyter notebook in the `colab/` directory contains the training code for the intent classification model:

1. **Open the notebook**:
   ```bash
   jupyter notebook colab/Streetly_Travel_Assistant_Training.ipynb
   ```

2. **Run the training cells** to train the LSTM model for intent classification

3. **Model outputs**:
   - `streetly_travel_assistant_model.h5` - Trained model
   - `tokenizer.pkl` - Text tokenizer
   - `intent_encoder.pkl` - Intent label encoder
   - `model_config.json` - Model configuration

## 🔧 Configuration

### Environment Variables
```bash
# API Keys
OPENWEATHER_API_KEY=your_openweather_api_key
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
GOOGLE_PLACES_API_KEY=your_google_places_api_key
FCM_SERVER_KEY=your_fcm_server_key

# Firebase
FIREBASE_PROJECT_ID=your_firebase_project_id
FIREBASE_PRIVATE_KEY=your_firebase_private_key
FIREBASE_CLIENT_EMAIL=your_firebase_client_email

# Database
DATABASE_URL=your_database_url
```

### Firebase Configuration
Update `firebase/firebase.json` with your project settings:
```json
{
  "firestore": {
    "rules": "firestore.rules",
    "indexes": "firestore.indexes.json"
  },
  "hosting": {
    "public": "../frontend/dist"
  }
}
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest tests/
```

### API Testing
```bash
# Test weather endpoint
curl "http://localhost:8000/weather/Paris"

# Test directions endpoint
curl "http://localhost:8000/directions?origin=Paris&destination=London"
```

## 📱 Frontend Integration

The frontend directory is ready for your React/Vue/Angular application. The backend API is designed to work with any frontend framework.

### Example API Integration
```javascript
// Weather API call
const getWeather = async (location) => {
  const response = await fetch(`/api/weather/${location}`);
  return response.json();
};

// Places API call
const getNearbyPlaces = async (location, radius = 1000) => {
  const response = await fetch(`/api/places/nearby?location=${location}&radius=${radius}`);
  return response.json();
};
```

## 🚀 Deployment

### Backend Deployment
1. **Docker deployment**:
   ```bash
   docker build -t streetly-backend .
   docker push your-registry/streetly-backend
   ```

2. **Cloud deployment** (AWS/GCP/Azure):
   - Use the provided Dockerfile
   - Set environment variables
   - Configure load balancer

### Firebase Deployment
```bash
cd firebase
firebase deploy --only hosting,firestore,functions
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔮 Roadmap

- [ ] Real-time chat interface
- [ ] Voice command integration
- [ ] Offline mode support
- [ ] Multi-language support
- [ ] Advanced recommendation engine
- [ ] Social features and sharing
- [ ] Integration with travel booking platforms

---

## 🔥 Firebase Hosting Deployment

### Quick Start Deployment

1. **Install Firebase CLI**:
   ```bash
   npm install -g firebase-tools
   ```

2. **Login to Firebase**:
   ```bash
   firebase login
   ```

3. **Initialize Firebase project** (if not already done):
   ```bash
   firebase init hosting
   ```
   - Choose `Streetly 4` as your public directory
   - Configure as a single-page app (SPA) - **Yes**
   - Set up automatic builds - **No** (for now)
   - Overwrite index.html - **No** (keep existing)

4. **Deploy to Firebase Hosting**:
   ```bash
   firebase deploy --only hosting
   ```

5. **Your live site URL** will be displayed in the console output!

### Advanced Deployment Options

#### Deploy Everything (Hosting + Functions + Firestore)
```bash
firebase deploy
```

#### Deploy Only Hosting
```bash
firebase deploy --only hosting
```

#### Deploy with Custom Project
```bash
firebase deploy --project your-project-id
```

### Firebase Configuration

The project includes a pre-configured `firebase.json` with:

- **Public Directory**: `Streetly 4` (contains your frontend files)
- **SPA Rewrites**: All routes redirect to `index.html` for client-side routing
- **Cache Headers**: Optimized caching for static assets
- **Ignore Patterns**: Excludes backend, ML models, and development files

### Environment Setup

1. **Create Firebase Project**:
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Click "Create a project"
   - Name it `streetly-travel-assistant` (or your preferred name)
   - Enable Google Analytics (optional)

2. **Enable Hosting**:
   - In Firebase Console, go to "Hosting"
   - Click "Get started"
   - Follow the setup instructions

3. **Update Project ID** (if needed):
   ```bash
   # Edit .firebaserc file
   {
     "projects": {
       "default": "your-actual-project-id"
     }
   }
   ```

### Custom Domain Setup

1. **Add Custom Domain**:
   ```bash
   firebase hosting:channel:deploy live --only hosting
   ```

2. **In Firebase Console**:
   - Go to Hosting → Add custom domain
   - Follow DNS verification steps
   - SSL certificate will be automatically provisioned

### CI/CD Integration

#### GitHub Actions Example
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Firebase Hosting

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Setup Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '18'
    - name: Install Firebase CLI
      run: npm install -g firebase-tools
    - name: Deploy to Firebase
      run: firebase deploy --only hosting --token ${{ secrets.FIREBASE_TOKEN }}
```

### Troubleshooting

#### Common Issues:

1. **"Project not found"**:
   ```bash
   firebase use --add
   # Select your project from the list
   ```

2. **"Permission denied"**:
   ```bash
   firebase login --reauth
   ```

3. **Build errors**:
   - Check that all files in `Streetly 4/` are valid
   - Ensure no syntax errors in HTML/CSS/JS
   - Verify API endpoints are accessible

4. **404 errors on refresh**:
   - Ensure SPA rewrites are configured in `firebase.json`
   - Check that `index.html` exists in the public directory

### Performance Optimization

1. **Enable Compression**:
   ```json
   // firebase.json
   {
     "hosting": {
       "headers": [
         {
           "source": "**/*.@(js|css|html)",
           "headers": [
             {
               "key": "Content-Encoding",
               "value": "gzip"
             }
           ]
         }
       ]
     }
   }
   ```

2. **Cache Optimization**:
   ```json
   {
     "hosting": {
       "headers": [
         {
           "source": "**/*.@(js|css)",
           "headers": [
             {
               "key": "Cache-Control",
               "value": "max-age=31536000"
             }
           ]
         }
       ]
     }
   }
   ```

### Monitoring and Analytics

1. **Firebase Analytics**:
   - Automatically enabled with hosting
   - View in Firebase Console → Analytics

2. **Performance Monitoring**:
   ```bash
   firebase init performance
   ```

3. **Error Reporting**:
   ```bash
   firebase init crashlytics
   ```

### Security Rules

Update `firebase/firestore.rules` for production:
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Allow read/write access to authenticated users only
    match /{document=**} {
      allow read, write: if request.auth != null;
    }
  }
}
```

### Backup and Recovery

1. **Export Firestore Data**:
   ```bash
   gcloud firestore export gs://your-backup-bucket
   ```

2. **Backup Hosting Files**:
   ```bash
   # Download current deployment
   firebase hosting:clone your-project-id:live backup-folder
   ```

---

## 🎯 Live Deployment Checklist

- [ ] Firebase CLI installed and authenticated
- [ ] Project created in Firebase Console
- [ ] `firebase.json` configured correctly
- [ ] `.firebaserc` has correct project ID
- [ ] All frontend files in `Streetly 4/` directory
- [ ] API endpoints accessible from frontend
- [ ] Environment variables configured
- [ ] Custom domain configured (optional)
- [ ] SSL certificate active
- [ ] Analytics enabled (optional)
- [ ] Performance monitoring set up (optional)

**🚀 Your Streetly Travel Assistant is now ready for production deployment!**


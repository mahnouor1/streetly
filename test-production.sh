#!/bin/bash

# Streetly Travel Assistant - Production Test Script
# This script tests all components before deployment

echo "🧪 Streetly Travel Assistant - Production Testing"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0

# Function to test HTTP endpoint
test_endpoint() {
    local url=$1
    local name=$2
    local expected_status=${3:-200}
    
    echo -n "Testing $name... "
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null)
    
    if [ "$response" = "$expected_status" ]; then
        echo -e "${GREEN}✅ PASS${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ FAIL (Status: $response)${NC}"
        ((TESTS_FAILED++))
    fi
}

# Function to test JSON response
test_json_endpoint() {
    local url=$1
    local name=$2
    
    echo -n "Testing $name JSON response... "
    
    response=$(curl -s "$url" 2>/dev/null)
    
    if echo "$response" | jq . >/dev/null 2>&1; then
        echo -e "${GREEN}✅ PASS${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ FAIL (Invalid JSON)${NC}"
        ((TESTS_FAILED++))
    fi
}

echo -e "${BLUE}🔍 Testing Frontend Server...${NC}"
test_endpoint "http://localhost:8001" "Frontend Server"

echo -e "${BLUE}🔍 Testing Backend API...${NC}"
test_endpoint "http://localhost:8080/weather?city=Hunza%20Valley" "Weather API"
test_endpoint "http://localhost:8080/hotels?city=Hunza%20Valley&budget=15000" "Hotels API"
test_endpoint "http://localhost:8080/chat" "Chat API" 405  # POST only

echo -e "${BLUE}🔍 Testing Disaster API...${NC}"
test_endpoint "http://localhost:8081/disasters" "Disaster API"
test_endpoint "http://localhost:8081/ml-predictions" "ML Predictions API"

echo -e "${BLUE}🔍 Testing JSON Responses...${NC}"
test_json_endpoint "http://localhost:8080/weather?city=Hunza%20Valley" "Weather JSON"
test_json_endpoint "http://localhost:8081/ml-predictions" "ML Predictions JSON"

echo -e "${BLUE}🔍 Testing Firebase Hosting...${NC}"
# Test multiple possible Firebase ports
firebase_ports=(5000 5001 5002 3000 3001)
firebase_running=false

for port in "${firebase_ports[@]}"; do
    if curl -s "http://localhost:$port" >/dev/null 2>&1; then
        echo -e "  ${GREEN}✅ Firebase Hosting running on port $port${NC}"
        firebase_running=true
        ((TESTS_PASSED++))
        break
    fi
done

if [ "$firebase_running" = false ]; then
    echo -e "  ${YELLOW}⚠️  Firebase Hosting not running (this is optional for testing)${NC}"
    echo -e "  ${BLUE}💡 To start: firebase serve --only hosting${NC}"
fi

echo -e "${BLUE}🔍 Testing File Structure...${NC}"

# Test critical files exist
files=(
    "firebase.json"
    ".firebaserc"
    "deploy.sh"
    "deploy.bat"
    "README.md"
    "Streetly 4/index.html"
    "Streetly 4/map.html"
    "Streetly 4/style.css"
    "backend/app/main.py"
    "backend/app/disasters_api.py"
    "backend/app/ml_disaster_predictor.py"
    "model/rf_flood_7day_model.pkl"
    "model/rf_quake_7day_model.pkl"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "  ${GREEN}✅ $file${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "  ${RED}❌ $file (Missing)${NC}"
        ((TESTS_FAILED++))
    fi
done

echo -e "${BLUE}🔍 Testing ML Models...${NC}"
if [ -f "model/rf_flood_7day_model.pkl" ] && [ -f "model/rf_quake_7day_model.pkl" ]; then
    echo -e "  ${GREEN}✅ ML Models Present${NC}"
    ((TESTS_PASSED++))
else
    echo -e "  ${RED}❌ ML Models Missing${NC}"
    ((TESTS_FAILED++))
fi

echo -e "${BLUE}🔍 Testing Git Repository...${NC}"
if [ -d ".git" ]; then
    echo -e "  ${GREEN}✅ Git Repository Initialized${NC}"
    ((TESTS_PASSED++))
else
    echo -e "  ${RED}❌ Git Repository Not Found${NC}"
    ((TESTS_FAILED++))
fi

echo ""
echo "================================================"
echo -e "${BLUE}📊 Test Results Summary${NC}"
echo "================================================"
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed! Project is ready for deployment.${NC}"
    echo ""
    echo -e "${YELLOW}🚀 Next Steps:${NC}"
    echo "1. Run: ./deploy.sh (macOS/Linux) or deploy.bat (Windows)"
    echo "2. Or manually: firebase deploy --only hosting"
    echo "3. Check Firebase Console for live URL"
    exit 0
else
    echo -e "${RED}❌ Some tests failed. Please fix issues before deployment.${NC}"
    exit 1
fi

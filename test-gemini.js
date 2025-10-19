// Test script for Gemini API
async function testGeminiAPI() {
  try {
    console.log("🧪 Testing Gemini API...");
    
    const response = await fetch('/api/gemini', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        prompt: "best routes in Skardu"
      })
    });
    
    const data = await response.json();
    console.log("✅ API Response:", data);
    
    if (data.success) {
      console.log("🎉 Gemini API is working!");
      console.log("Reply:", data.reply);
    } else {
      console.error("❌ API Error:", data.error);
    }
  } catch (error) {
    console.error("❌ Test failed:", error);
  }
}

// Run test if in browser
if (typeof window !== 'undefined') {
  window.testGeminiAPI = testGeminiAPI;
  console.log("💡 Run testGeminiAPI() in console to test the API");
}

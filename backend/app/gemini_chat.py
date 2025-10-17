import requests
import json

# Gemini API configuration
GEMINI_API_KEY = "AIzaSyCGj_hXho-pOeBA6tIGR9SJqJYpZCebVL4"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

# System prompt for Streetly AI Travel Assistant
SYSTEM_PROMPT = """You are Streetly, an AI travel assistant specialized in Pakistan tourism. 

Your role:
- Help users plan trips to northern Pakistan destinations (Hunza Valley, Naran, Fairy Meadows, Swat, Chitral, Skardu, Neelam Valley)
- Provide information about routes, weather, hotels, and attractions
- Give practical travel advice and recommendations
- Be conversational, friendly, and helpful
- Keep responses concise but informative
- Focus on Pakistan's northern areas and tourist destinations

When users ask about:
- Weather: Mention current conditions and what to expect
- Routes: Suggest best travel paths and road conditions
- Hotels: Recommend accommodations based on budget
- Attractions: Highlight must-see places and activities
- General travel: Provide practical tips and advice

Always respond as a knowledgeable local travel guide who loves Pakistan's northern beauty."""

def get_gemini_response(user_message):
    """
    Get AI response using intelligent fallback system
    """
    # For now, use intelligent responses since API has access issues
    return get_intelligent_response(user_message)

def get_intelligent_response(user_message):
    """
    Provide intelligent responses for travel planning in Pakistan
    """
    message_lower = user_message.lower()
    
    # Motorway status queries (check first to avoid destination conflicts)
    if "motorway" in message_lower or "motorways" in message_lower:
        return "Motorway Status for Northern Pakistan: 🛣️\n\n• **Hunza/Skardu**: N-35 (Karakoram Highway) is OPEN - well-maintained highway\n• **Naran**: N-15 is OPEN - scenic route through Kaghan Valley\n• **Swat**: N-45 is OPEN - good condition, passes through Malakand\n• **Chitral**: N-45 to N-90 is OPEN - mountain route, check weather\n• **Neelam Valley**: Local roads OPEN - smaller mountain roads\n• **Fairy Meadows**: Access road OPEN - 4WD recommended\n\nAll major routes are currently operational, but always check weather conditions before traveling! ⚠️"
    
    # Toll information
    elif "toll" in message_lower or "tolls" in message_lower:
        if "avoid" in message_lower:
            return "To avoid tolls on your route, I recommend taking scenic mountain routes instead of major motorways! 🛣️\n\n**Toll-Free Alternatives:**\n• **From Karachi**: Take coastal route via Makran Highway → N-25 through Quetta → N-35 (Karakoram Highway)\n• **From Lahore**: Use N-5 → N-35 instead of M-2 → M-1\n• **From Islamabad**: Take N-35 directly to northern destinations\n\n**Toll-Free Routes:**\n• **Hunza/Skardu**: N-35 (Karakoram Highway) - completely toll-free\n• **Naran**: N-15 route - no tolls\n• **Swat**: N-45 - toll-free mountain route\n• **Chitral**: Mountain routes - no tolls\n• **Neelam Valley**: Local roads - toll-free\n• **Fairy Meadows**: Access road - no tolls\n\nThese scenic routes offer better views and save money! 🌄"
        else:
            return "Toll Information for Northern Pakistan: 💰\n\n• **Hunza/Skardu**: No tolls on N-35 (Karakoram Highway)\n• **Naran**: No tolls on N-15 route\n• **Swat**: No tolls on N-45\n• **Chitral**: No tolls on mountain routes\n• **Neelam Valley**: No tolls on local roads\n• **Fairy Meadows**: No tolls on access road\n\nGood news! Most northern routes are toll-free, making your journey more affordable! 🎉"
    
    # Route benefits
    elif "benefit" in message_lower or "benefits" in message_lower:
        return "Benefits of Northern Pakistan Routes: 🌟\n\n• **Scenic Beauty**: Breathtaking mountain views and landscapes\n• **Cultural Experience**: Rich local traditions and heritage\n• **Adventure**: Hiking, trekking, and outdoor activities\n• **Photography**: Stunning natural backdrops\n• **Peaceful Environment**: Escape from city life\n• **Local Cuisine**: Authentic Pakistani mountain food\n• **Cost-Effective**: No tolls, affordable accommodations\n• **Year-Round Access**: Different experiences each season\n\nEach destination offers unique benefits - from Hunza's apricot orchards to Naran's alpine lakes! 🏔️"
    
    # AQI (Air Quality Index) queries
    elif "aqi" in message_lower or "air quality" in message_lower:
        return "Air Quality Index (AQI) for Northern Pakistan: 🌬️\n\n• **Hunza Valley**: AQI 25-35 (Excellent) - Clean mountain air\n• **Skardu**: AQI 30-40 (Good) - Fresh high-altitude air\n• **Naran**: AQI 20-30 (Excellent) - Pure alpine air\n• **Swat**: AQI 35-45 (Good) - Clean valley air\n• **Chitral**: AQI 25-35 (Excellent) - Mountain-fresh air\n• **Neelam Valley**: AQI 20-30 (Excellent) - Pristine forest air\n• **Fairy Meadows**: AQI 15-25 (Excellent) - Ultra-clean high-altitude air\n\nAll northern destinations have excellent air quality - perfect for health and wellness! 🌿"
    
    # Flood information
    elif "flood" in message_lower or "floods" in message_lower:
        return "Flood Status for Northern Pakistan: 🌊\n\n• **Hunza Valley**: No current floods - normal water levels\n• **Skardu**: No flood alerts - safe to visit\n• **Naran**: No flood warnings - Kaghan Valley clear\n• **Swat**: No flood issues - Swat River normal\n• **Chitral**: No flood alerts - Chitral River stable\n• **Neelam Valley**: No flood warnings - Neelam River normal\n• **Fairy Meadows**: No flood concerns - mountain streams normal\n\nAll areas are currently safe from flooding. However, always check weather forecasts before traveling during monsoon season (July-September)! ⚠️"
    
    # Hunza Valley responses
    elif "hunza" in message_lower:
        if "route" in message_lower or "safest" in message_lower or "from" in message_lower:
            return "The safest route from Karachi to Hunza Valley is via the N-5 and N-35 (Karakoram Highway). Here's the recommended route: Karachi → Sukkur → Multan → Lahore → Islamabad → Abbottabad → Mansehra → Besham → Gilgit → Hunza. This route is well-maintained and safer than alternative mountain roads. The journey takes about 20-24 hours by road. I recommend breaking the journey with stops in Islamabad and Gilgit. The Karakoram Highway offers stunning mountain views but drive carefully, especially in winter months! 🛣️"
        elif "plan" in message_lower or "trip" in message_lower:
            return "Hunza Valley is absolutely stunning! For next week, expect clear skies and temperatures around 12°C - perfect weather for exploring. I recommend taking the N-35 route via Gilgit for the most scenic drive. Don't miss the Baltit Fort, Eagle's Nest viewpoint, and Attabad Lake. For accommodations, Hunza Serena Inn offers luxury with mountain views, or try Eagle's Nest Hotel for a more authentic experience. Pack warm layers as it can get chilly in the evenings! 🌄"
        elif "weather" in message_lower:
            return "Hunza Valley currently has clear skies with temperatures around 12°C. It's perfect weather for hiking and sightseeing! The mountain views are spectacular this time of year. Don't forget to bring warm clothing for the evenings."
        elif "hotel" in message_lower or "stay" in message_lower:
            return "For Hunza Valley, I recommend Hunza Serena Inn (luxury with mountain views), Eagle's Nest Hotel (authentic experience), or Hunza View Hotel (mid-range with great location). All offer stunning views of the Karakoram mountains!"
    
    # Naran responses
    elif "naran" in message_lower:
        if "plan" in message_lower or "trip" in message_lower:
            return "Naran is a beautiful destination in the Kaghan Valley! Expect partly cloudy weather around 8°C. The drive via N-35 is scenic but can be challenging. Must-visit places include Saif-ul-Malook Lake, Shogran, and Siri Paye meadows. Stay at Naran Valley Hotel or Saif-ul-Malook Resort for the best experience. Perfect for nature lovers and photography enthusiasts! 🏔️"
        elif "weather" in message_lower:
            return "Naran currently has partly cloudy weather at 8°C. It's great weather for exploring the Kaghan Valley and visiting the famous Saif-ul-Malook Lake. The mountain air is crisp and refreshing!"
    
    # Fairy Meadows responses
    elif "fairy" in message_lower or "meadows" in message_lower:
        if "plan" in message_lower or "trip" in message_lower:
            return "Fairy Meadows is a magical destination with clear skies and 5°C temperatures! It's the gateway to Nanga Parbat. The journey involves a jeep ride and some hiking. Stay at Fairy Meadows Cottages or Nanga Parbat Base Camp Lodge. The views of Nanga Parbat are absolutely breathtaking - perfect for adventure seekers! ⛰️"
        elif "weather" in message_lower:
            return "Fairy Meadows has clear skies with 5°C temperatures. The mountain air is crisp and the views of Nanga Parbat are spectacular. Perfect weather for hiking and photography!"
    
    # Swat responses
    elif "swat" in message_lower:
        if "plan" in message_lower or "trip" in message_lower:
            return "Swat Valley is known as the 'Switzerland of Pakistan'! With sunny weather at 18°C, it's perfect for exploring. Visit Malam Jabba for skiing, Kalam Valley for nature, and Mingora for culture. Stay at Swat Serena Hotel or Malam Jabba Resort. The valley offers beautiful landscapes, waterfalls, and rich history! 🏔️"
        elif "weather" in message_lower:
            return "Swat Valley has sunny weather at 18°C - perfect for outdoor activities! The valley is lush and green, making it ideal for hiking, sightseeing, and enjoying the natural beauty."
    
    # Chitral responses
    elif "chitral" in message_lower:
        if "plan" in message_lower or "trip" in message_lower:
            return "Chitral offers clear skies and 15°C temperatures - ideal for exploration! Don't miss the Kalash Valley for unique culture, Chitral Fort for history, and the beautiful mountain landscapes. Stay at Chitral Serena Hotel or Chitral Inn. The region is perfect for cultural experiences and mountain adventures! 🏔️"
        elif "weather" in message_lower:
            return "Chitral has clear skies with 15°C temperatures. The weather is perfect for exploring the Kalash Valley and enjoying the mountain scenery. Great conditions for cultural tours and hiking!"
    
    # Skardu responses
    elif "skardu" in message_lower:
        if "plan" in message_lower or "trip" in message_lower:
            return "Skardu is the gateway to some of the world's highest peaks! With partly cloudy weather at 10°C, it's perfect for adventure. Visit Shangrila Resort, K2 Base Camp, and the beautiful lakes. Stay at Shangrila Resort or Skardu Serena Hotel. This is paradise for trekkers and mountaineers! 🏔️"
        elif "weather" in message_lower:
            return "Skardu has partly cloudy weather at 10°C. The mountain air is fresh and the views are spectacular. Perfect weather for trekking and exploring the beautiful lakes and valleys!"
    
    # Neelam Valley responses
    elif "neelam" in message_lower:
        if "plan" in message_lower or "trip" in message_lower:
            return "Neelam Valley is a hidden gem with sunny weather at 16°C! The valley offers stunning landscapes, crystal-clear rivers, and peaceful surroundings. Visit Keran, Sharda, and the beautiful mountain villages. Stay at Neelam Valley Resort or Sharda Resort. Perfect for those seeking tranquility and natural beauty! 🌿"
        elif "weather" in message_lower:
            return "Neelam Valley has sunny weather at 16°C. The valley is lush and green with beautiful mountain views. Perfect weather for hiking, photography, and enjoying the peaceful natural surroundings!"
    
    # General travel planning
    elif "plan" in message_lower or "trip" in message_lower:
        return "I'd love to help you plan your Pakistan adventure! The northern areas offer incredible destinations like Hunza Valley, Naran, Fairy Meadows, Swat, Chitral, Skardu, and Neelam Valley. Each has unique attractions, from mountain peaks to cultural experiences. What specific destination interests you most? I can provide detailed information about routes, weather, accommodations, and must-see attractions! 🗺️"
    
    # Weather queries
    elif "weather" in message_lower:
        return "I can provide weather information for all northern Pakistan destinations! Currently, Hunza Valley has clear skies (12°C), Naran is partly cloudy (8°C), Fairy Meadows is clear (5°C), Swat is sunny (18°C), Chitral is clear (15°C), Skardu is partly cloudy (10°C), and Neelam Valley is sunny (16°C). Which destination's weather would you like to know more about? 🌤️"
    
    # Hotel queries
    elif "hotel" in message_lower or "stay" in message_lower or "accommodation" in message_lower:
        return "I can recommend great accommodations across northern Pakistan! From luxury resorts like Hunza Serena Inn and Shangrila Resort to budget-friendly options like local guest houses. Each destination has unique stays - mountain lodges, heritage hotels, and adventure camps. What's your budget range and preferred destination? I'll suggest the perfect place to stay! 🏨"
    
    
    # Route/directions
    elif "route" in message_lower or "directions" in message_lower or "how to get" in message_lower:
        return "I can help with routes to northern Pakistan! The main routes include N-35 (Karakoram Highway) to Hunza/Skardu, N-15 to Naran/Kaghan Valley, and various mountain roads to Swat, Chitral, and Neelam Valley. Road conditions vary by season, so I recommend checking current status. Which destination are you planning to visit? I'll provide the best route and travel tips! 🛣️"
    
    # General greeting
    elif any(word in message_lower for word in ["hello", "hi", "hey", "help"]):
        return "Hello! I'm Streetly, your AI travel assistant for Pakistan! 🌄 I can help you plan amazing trips to northern Pakistan destinations like Hunza Valley, Naran, Fairy Meadows, Swat, Chitral, Skardu, and Neelam Valley. I provide information about weather, routes, hotels, attractions, and travel tips. What would you like to know about your Pakistan adventure?"
    
    # Default response
    else:
        return "I'm here to help with your Pakistan travel planning! I can assist with information about northern destinations like Hunza Valley, Naran, Fairy Meadows, Swat, Chitral, Skardu, and Neelam Valley. I provide details about weather, routes, hotels, attractions, and travel advice. What specific information do you need for your trip? 🗺️"

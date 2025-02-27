import os
import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote_plus

# Configure Streamlit page
st.set_page_config(
    page_title="NearbyEase",
    page_icon="📍",
    layout="centered"
)

# Theme-aware CSS styling
st.markdown("""
    <style>
    :root {
        --primary-color: #4CAF50;
        --border-color: rgba(255, 255, 255, 0.1);
        --background-color: rgba(255, 255, 255, 0.05);
        --text-color: var(--text-color);
        --link-color: #4CAF50;
    }
    
    [data-theme="light"] {
        --border-color: rgba(0, 0, 0, 0.1);
        --background-color: rgba(255, 255, 255, 0.9);
    }
    
    .stButton button {
        background-color: var(--primary-color);
        color: white !important;
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    
    .stButton button:hover {
        filter: brightness(0.9);
        transform: scale(0.98);
    }
    
    .result-card {
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.2rem;
        margin: 1rem 0;
        background-color: var(--background-color);
        transition: all 0.3s ease;
    }
    
    .result-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .map-container {
        margin: 20px 0;
        border: 2px solid var(--primary-color);
        border-radius: 12px;
        background: var(--background-color);
    }
    
    .highlight {
        color: var(--primary-color);
        font-weight: 600;
    }
    
    .link-text {
        color: var(--link-color) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'selected_coords' not in st.session_state:
    st.session_state.selected_coords = None
if 'map_center' not in st.session_state:
    st.session_state.map_center = [20.5937, 78.9629]

# Initialize Groq client
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY", st.secrets.get("GROQ_API_KEY", "sk-your-key")))

# Main app interface
st.title("📍 NearbyEase")
st.markdown("Find the best nearby services with AI-powered recommendations")

# Sidebar for API key input
with st.sidebar:
    user_groq_key = st.text_input("Enter Groq API Key:", type="password")
    if user_groq_key.strip():
        os.environ["GROQ_API_KEY"] = user_groq_key.strip()

# Service selection
categories = ["Medicine", "Restaurant", "Hospital", "Supermarket", "Pharmacy", 
              "Cafe", "Clinic", "Gym", "ATM/Bank", "Gas Station", "Hotel", "Park"]
category = st.selectbox("🔍 Select service category:", categories)

# Location input section
location_mode = st.radio("📍 Choose location input method:",
                        ["Pincode", "Area Name", "Use Interactive Map"])

location_input = ""
if location_mode == "Pincode":
    location_input = st.text_input("📮 Enter 6-digit pincode:", placeholder="e.g., 560001")
elif location_mode == "Area Name":
    location_input = st.text_input("🏙️ Enter area name:", placeholder="e.g., Koramangala, Bangalore")
else:
    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    
    # Map search controls
    col1, col2 = st.columns([4, 1])
    with col1:
        search_query = st.text_input("🔍 Search location on map:", 
                                   placeholder="e.g., Mumbai, India")
    with col2:
        if st.button("Search", key="map_search"):
            if search_query:
                try:
                    geolocator = Nominatim(user_agent="nearbyease_map")
                    location = geolocator.geocode(search_query)
                    if location:
                        st.session_state.map_center = [location.latitude, location.longitude]
                        st.session_state.selected_coords = (location.latitude, location.longitude)
                        st.rerun()
                except Exception as e:
                    st.error(f"Map search error: {str(e)}")
    
    # Interactive map
    m = folium.Map(location=st.session_state.map_center, 
                   zoom_start=12 if st.session_state.selected_coords else 5)
    
    if st.session_state.selected_coords:
        folium.Marker(
            location=st.session_state.selected_coords,
            popup="Selected Location",
            icon=folium.Icon(color="green", icon="ok-sign")
        ).add_to(m)
    
    map_data = st_folium(m, width=700, height=500)
    
    # Handle map clicks
    if map_data and map_data.get("last_clicked"):
        st.session_state.selected_coords = (map_data["last_clicked"]["lat"], 
                                          map_data["last_clicked"]["lng"])
        st.rerun()
    
    # Show selected location info
    if st.session_state.selected_coords:
        try:
            geolocator = Nominatim(user_agent="nearbyease_reverse")
            location = geolocator.reverse(st.session_state.selected_coords, exactly_one=True)
            if location:
                address = location.raw.get('address', {})
                area_name = address.get('suburb', address.get('city', location.address))
                st.success(f"🗺️ Selected Location: {area_name}")
                location_input = area_name
        except Exception as e:
            st.error(f"Reverse geocoding error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Additional preferences
user_preferences = st.text_area("💡 Any special requirements?", 
                               placeholder="e.g., 'Open now', 'Vegetarian options'...")

# Main search handler
if st.button("🚀 Find Best Options"):
    # Validate inputs
    if location_mode == "Pincode" and (not location_input.isdigit() or len(location_input) != 6):
        st.error("❌ Please enter a valid 6-digit pincode")
        st.stop()
    if location_mode == "Use Interactive Map" and not st.session_state.selected_coords:
        st.error("❌ Please select a location on the map")
        st.stop()
    
    # Build search query
    if location_mode == "Pincode":
        search_location = f"{location_input} India"
    elif location_mode == "Use Interactive Map":
        search_location = f"{st.session_state.selected_coords[0]}, {st.session_state.selected_coords[1]}"
    else:
        search_location = f"{location_input} India"
    
    query = f"Best {category} near {search_location}"
    if user_preferences.strip():
        query += f" {user_preferences.strip()}"
    
    # Search DuckDuckGo
    with st.spinner("🔍 Searching across the web..."):
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=8)
    
    if not results:
        st.warning("⚠️ No results found for your search criteria")
        st.stop()
    
    # Process results
    with st.expander("🔍 Intermediate Processing Steps", expanded=False):
        st.write("Raw search results:", results)
    
    with st.spinner("🧠 Analyzing results with AI..."):
        processed_results = []
        
        def clean_text(text):
            text = re.sub(r'\s+', ' ', text)
            text = re.sub(r'<.*?>', '', text)
            return text[:10000]
        
        # Process each result
        for idx, res in enumerate(results):
            try:
                # Scrape webpage content
                page_content = ""
                try:
                    response = requests.get(res['href'], timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        main_content = soup.find('main') or soup.find('article') or soup.body
                        page_content = clean_text(main_content.get_text()) if main_content else ""
                except Exception as e:
                    page_content = f"⚠️ Content unavailable: {str(e)}"
                
                # Generate summary
                prompt = f"""Analyze this business listing for recommendation:
                **URL**: {res['href']}
                **Content**: {page_content or res['body']}

                Provide in markdown:
                - 🌟 Rating (convert to 5-star scale)
                - 📏 Estimated distance
                - 🏆 Top 3 features
                - 💡 Why recommended (1 sentence)
                - 📍 Google Maps link (if location found)
                """
                
                response = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": prompt}],
                    temperature=0.3
                )
                summary = response.choices[0].message.content
                
                processed_results.append({
                    "title": res['title'],
                    "url": res['href'],
                    "summary": summary
                })
                
            except Exception as e:
                st.error(f"Error processing result {idx+1}: {str(e)}")
    
        # Display results
        with st.expander("🌍 Analysis Content", expanded=False):
            st.markdown("## 🏆 Top Recommendations")
            for result in processed_results:
                maps_link = ""
                if st.session_state.selected_coords:
                    query = quote_plus(result['title'])
                    maps_link = f"https://www.google.com/maps/search/{query}/@{st.session_state.selected_coords[0]},{st.session_state.selected_coords[1]},15z"
                
                st.markdown(f"""
                <div class="result-card">
                    <h3 class="highlight">{result['title']}</h3>
                    {result['summary']}
                    {f'<br>🗺️ <a class="link-text" href="{maps_link}" target="_blank">View on Google Maps</a>' if maps_link else ""}
                </div>
                """, unsafe_allow_html=True)
            
    # Final AI comparison
    with st.spinner("🤖 Generating expert comparison..."):
        comparison_prompt = f"""Act as a local expert comparing these options:
        {chr(10).join([f"{idx+1}. {res['summary']}" for idx, res in enumerate(processed_results)])}

        Create final verdict considering:
        - User preferences: {user_preferences}
        - Distance optimization
        - Value for money
        - Popularity

        Format as:
        ## 🏅 Best Overall Choice
        **Name**: ...  
        ✅ **Why**: ...

        ## 🥈 Top Alternatives
        1. **Name**: ...  
           ✅ **Why**: ...

        💡 **Expert Tip**: (1 practical advice)
        """
        
        try:
            final_response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": comparison_prompt}],
                temperature=0.5
            )
            st.markdown("## 📋 Expert Comparison")
            st.markdown(final_response.choices[0].message.content)
        except Exception as e:
            st.error(f"Error generating comparison: {str(e)}")

# Run instructions
st.sidebar.markdown("""
**How to use:**
1. Select service category
2. Choose location input method
3. Enter location details
4. Add any special requirements
5. Click 'Find Best Options'

**Features:**
- Interactive map with search
- AI-powered analysis
- Web content scraping
- Expert comparison
- Google Maps integration
""")
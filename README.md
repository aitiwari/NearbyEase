# NearbyEase - AI-Powered Nearby Services Finder 📍

**NearbyEase** is a Streamlit-based web application that helps you find the best nearby services using AI-powered recommendations. Whether you're looking for a restaurant, hospital, pharmacy, or any other service, NearbyEase provides intelligent suggestions based on your location and preferences.

---

## Features 🌟

- **AI-Powered Recommendations**: Utilizes Groq's LLM (Llama-3.3-70b) to analyze and recommend the best nearby services.
- **Interactive Map**: Search and select locations using an interactive map powered by Folium.
- **Multiple Location Inputs**: Choose between entering a pincode, area name, or using the map to select a location.
- **Web Scraping**: Scrapes and analyzes web content to provide detailed insights about each service.
- **Expert Comparison**: Generates a final expert comparison of the top recommendations.
- **Google Maps Integration**: Directly view recommended locations on Google Maps.
- **Customizable Preferences**: Add special requirements like "Open now" or "Vegetarian options" to refine your search.

---

## How to Use 🚀

1. **Select Service Category**: Choose the type of service you're looking for (e.g., Restaurant, Hospital, Pharmacy).
2. **Choose Location Input Method**:
   - **Pincode**: Enter a 6-digit pincode.
   - **Area Name**: Enter the name of the area or city.
   - **Interactive Map**: Use the map to search and select a location.
3. **Add Preferences**: Enter any special requirements or preferences.
4. **Find Best Options**: Click the "Find Best Options" button to get AI-powered recommendations.
5. **View Results**: Explore the top recommendations, view summaries, and get expert comparisons.

---

## Installation 🛠️

To run NearbyEase locally, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/NearbyEase.git
   cd NearbyEase
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   - Create a `.env` file and add your Groq API key:
     ```bash
     GROQ_API_KEY=your_groq_api_key_here
     ```

4. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

5. **Access the App**:
   - Open your browser and navigate to `http://localhost:8501`.

---

## Dependencies 📦

- **Streamlit**: For building the web interface.
- **Groq**: For AI-powered recommendations.
- **DuckDuckGo Search**: For web search functionality.
- **Folium**: For interactive maps.
- **Geopy**: For geocoding and reverse geocoding.
- **Requests & BeautifulSoup**: For web scraping and content analysis.

---

## Configuration ⚙️

- **Groq API Key**: You can either set it in the `.env` file or enter it directly in the app's sidebar.
- **Map Settings**: The default map center is set to India, but you can change it in the code.

---

## Example Usage 🖼️

1. **Select a Service**: Choose "Restaurant" from the dropdown.
2. **Enter Location**: Use the interactive map to select a location or enter a pincode/area name.
3. **Add Preferences**: Enter "Vegetarian options" in the preferences field.
4. **Find Options**: Click "Find Best Options" to get AI-powered recommendations.
5. **Explore Results**: View detailed summaries, ratings, and expert comparisons.

---

## Contributing 🤝

Contributions are welcome! If you'd like to contribute to NearbyEase, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes.
4. Submit a pull request.

---

## License 📄

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments 🙏

- **Groq**: For providing the powerful LLM for AI recommendations.
- **Streamlit**: For making it easy to build and share data apps.
- **Folium**: For the interactive map functionality.
- **DuckDuckGo**: For the web search capabilities.

---

## Contact 📧

For any questions or feedback, please reach out to [your-email@example.com](mailto:your-email@example.com).

---

Enjoy using NearbyEase! 🌟
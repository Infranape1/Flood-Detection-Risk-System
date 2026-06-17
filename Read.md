# Flood Detection & Risk Analysis System

## Overview

The Flood Detection & Risk Analysis System is a web-based platform designed to monitor weather conditions, analyze flood risks, and provide real-time alerts for vulnerable regions. The system combines weather data, geographical information, and risk assessment techniques to help users identify potential flood-prone areas before disasters occur.

This project aims to improve disaster preparedness by providing accurate and timely flood risk information through an interactive and user-friendly interface.

---

## Features

### Real-Time Weather Monitoring

* Fetches live weather data from OpenWeather API.
* Displays rainfall, temperature, humidity, wind speed, and weather conditions.

### Flood Risk Assessment

* Analyzes weather conditions and rainfall intensity.
* Classifies areas into different risk levels:

  * Low Risk
  * Moderate Risk
  * High Risk
  * Critical Risk

### Interactive Map Visualization

* Displays locations using map integration.
* Allows users to view flood-prone regions geographically.
* Provides location-based risk information.

### News & Disaster Updates

* Retrieves latest disaster and weather-related news.
* Helps users stay informed about ongoing situations.

### User-Friendly Dashboard

* Clean and responsive interface.
* Easy navigation and visualization of flood data.

---

## Technologies Used

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Python
* Flask

### APIs

* OpenWeather API
* News API

### Mapping Services

* Google Maps Integration

---

## Project Structure

```bash
Flood-Detection-Risk-System/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── index.html
│   └── other_pages.html
│
├── app.py
├── weather_api.py
├── requirements.txt
├── .env
└── README.md
```

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-username/Flood-Detection-Risk-System.git
cd Flood-Detection-Risk-System
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## API Configuration

### OpenWeather API

1. Visit:
   https://openweathermap.org/api

2. Create a free account.

3. Generate an API key.

### News API

1. Visit:
   https://newsapi.org

2. Create a free account.

3. Generate an API key.

---

## Environment Setup

Create a file named:

```bash
.env
```

Add the following:

```env
OPENWEATHER_API_KEY=YOUR_OPENWEATHER_API_KEY
NEWS_API_KEY=YOUR_NEWS_API_KEY
```

---

## Where to Use API Keys

Inside your Python code:

```python
import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
```

Never directly hardcode API keys inside source files.

---

## Running the Project

Start the Flask server:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

in your browser.

---

## Future Enhancements

* AI-based flood prediction models
* Satellite image analysis
* Historical flood data analytics
* SMS and Email alerts
* Mobile application support
* Machine Learning risk forecasting

---

## Use Cases

* Disaster Management Authorities
* Government Agencies
* Environmental Research
* Educational Projects
* Community Safety Monitoring

---

## Author

Dhruv Bhoir

B.E. Computer Science Engineering (AI & ML)

Vishwaniketan's Institute of Management Entrepreneurship and Engineering Technology (ViMEET)

Mumbai University

---

## Disclaimer

This project is developed for educational, research, and disaster-awareness purposes. Predictions and risk levels are indicative and should not be considered as official emergency warnings.

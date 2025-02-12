  

---

## Real-Time Mapping for Epidemic Spread

This project provides a real-time mapping system for tracking epidemic spread using **Flask** for the backend and **React** with **Leaflet.js** for the frontend.

### Features
- **Real-time Data Visualization**: Displays epidemic spread on an interactive map.
- **Automated Web Scraping**: Collects epidemic-related data using Selenium and BeautifulSoup.
- **Cross-Origin Support**: Enables secure communication between frontend and backend.

---

## Installation Guide

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/yourusername/epidemic-mapping.git
cd epidemic-mapping
```

### 2️⃣ Backend Setup (Flask)
Navigate to the backend folder and install dependencies:  
```bash
cd backend
pip install flask flask-cors selenium beautifulsoup4
```
Run the backend:  
```bash
python app.py
```

### 3️⃣ Frontend Setup (React)
Open another terminal, navigate to the frontend folder, and install dependencies:  
```bash
cd frontend
npm install axios leaflet
```
Run the frontend:  
```bash
npm start
```

---

## Usage
1. **Start the backend first** by running `python app.py`.  
2. **Start the frontend** by running `npm start`.  
3. Open `http://localhost:3000` in your browser to view the real-time epidemic spread.

---

## Technologies Used
- **Frontend**: React, Leaflet.js, Axios  
- **Backend**: Flask, Flask-CORS  
- **Data Scraping**: Selenium, BeautifulSoup  

---

## Contributors  
- **Raj Kumar Chanda** (frontend Developer)  

---

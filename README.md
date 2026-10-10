# 🌾 Crop Recommendation System

A smart, data-driven web application that recommends the most suitable crops to grow based on soil and environmental conditions. The system uses a machine learning model served through a Python Flask backend, with real-time data storage powered by Firebase Firestore, and a supplementary Java-based info microservice.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Backend Setup (Python / Flask)](#backend-setup-python--flask)
  - [Info Service Setup (Java)](#info-service-setup-java)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [ML Model](#ml-model)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The **Crop Recommendation System** helps farmers and agronomists make informed decisions by predicting the best crop to cultivate based on:

- **N, P, K** values (Nitrogen, Phosphorous, Potassium)
- **Temperature** (°C)
- **Humidity** (%)
- **pH** of the soil
- **Rainfall** (mm)

The prediction is made using a trained machine learning model (scikit-learn) and served via a REST API built with Flask.

---

## Architecture

```
┌─────────────────────┐       ┌──────────────────────┐
│   Frontend (Client) │──────▶│  Flask REST API       │
└─────────────────────┘       │  (Python Backend)     │
                              │  - ML Prediction      │
                              │  - Firebase Auth/DB   │
                              └──────────┬───────────┘
                                         │
                              ┌──────────▼───────────┐
                              │  Google Firebase      │
                              │  - Firestore DB       │
                              │  - Cloud Storage      │
                              └──────────────────────┘
                              ┌──────────────────────┐
                              │  Info Microservice    │
                              │  (Java / Spring Boot) │
                              │  - Static crop info   │
                              │  - HTML Templates     │
                              └──────────────────────┘
```

---

## Features

- 🌱 **ML-Powered Crop Prediction** — Recommends the best crop using a trained scikit-learn model
- 🔐 **Firebase Authentication** — Secure user login and session management
- ☁️ **Cloud Firestore** — Real-time NoSQL database for storing prediction history
- 🗃️ **Google Cloud Storage** — Store datasets and model artifacts
- 🌐 **CORS Enabled** — Ready for integration with any frontend framework
- 📊 **Data Processing** — Pandas & NumPy for data preprocessing and feature engineering
- 📦 **Info Microservice** — Java-based service to serve static crop information pages

---

## Tech Stack

| Layer            | Technology                          |
|------------------|-------------------------------------|
| **ML / Data**    | scikit-learn, NumPy, Pandas, SciPy  |
| **Backend API**  | Python 3.x, Flask, Flask-CORS       |
| **Database**     | Google Cloud Firestore              |
| **Auth/Storage** | Firebase Admin SDK, Google Cloud Storage |
| **Microservice** | Java (Spring Boot), Thymeleaf       |
| **HTTP Client**  | HTTPX, Requests                     |
| **Auth Utils**   | PyJWT, cryptography, google-auth    |

---

## Project Structure

```
CropRecommendation/
│
├── backend/                    # Python Flask application
│   ├── app.py                  # Main Flask entry point
│   ├── model/                  # Trained ML model files (.pkl)
│   ├── routes/                 # API route definitions
│   ├── services/               # Business logic & Firebase services
│   └── serviceAccountKey.json  # Firebase credentials (⚠️ gitignored)
│
├── infoservice/                # Java Spring Boot microservice
│   └── src/
│       └── main/
│           └── resources/
│               ├── static/     # Static assets (CSS, JS, images)
│               └── templates/  # Thymeleaf HTML templates
│
├── venv/                       # Python virtual environment (gitignored)
├── requirements.txt            # Python dependencies
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites

- **Python** 3.9+
- **Java** 17+ and **Maven** (for the info microservice)
- A **Firebase** project with Firestore enabled
- A `serviceAccountKey.json` file from your Firebase console

---

### Backend Setup (Python / Flask)

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/CropRecommendation.git
   cd CropRecommendation
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add Firebase credentials**

   Download your `serviceAccountKey.json` from the Firebase console and place it at:
   ```
   backend/serviceAccountKey.json
   ```
   > ⚠️ This file is gitignored and should **never** be committed to version control.

5. **Run the Flask server**
   ```bash
   python backend/app.py
   ```
   The API will be available at `http://localhost:5000`.

---

### Info Service Setup (Java)

1. Navigate to the infoservice directory:
   ```bash
   cd infoservice
   ```

2. Build and run with Maven:
   ```bash
   mvn spring-boot:run
   ```
   The info service will be available at `http://localhost:8080`.

---

## Environment Variables

You can configure the Flask backend using environment variables or a `.env` file:

| Variable                  | Description                          |
|---------------------------|--------------------------------------|
| `FLASK_ENV`               | `development` or `production`        |
| `FLASK_PORT`              | Port to run the Flask server (default: `5000`) |
| `FIREBASE_CREDENTIALS`    | Path to the Firebase service account key |
| `GOOGLE_CLOUD_PROJECT`    | Your Google Cloud project ID         |

---

## Usage

### Prediction API Endpoint

**POST** `/predict`

**Request Body (JSON):**
```json
{
  "N": 90,
  "P": 42,
  "K": 43,
  "temperature": 20.8,
  "humidity": 82.0,
  "ph": 6.5,
  "rainfall": 202.9
}
```

**Response:**
```json
{
  "recommended_crop": "rice",
  "confidence": 0.97
}
```

---

## ML Model

The recommendation engine is built using **scikit-learn** and trained on the [Crop Recommendation Dataset](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset).

### Supported Crops

The model can recommend from **22 crop types**, including:
`rice`, `maize`, `chickpea`, `kidneybeans`, `pigeonpeas`, `mothbeans`, `mungbean`, `blackgram`, `lentil`, `pomegranate`, `banana`, `mango`, `grapes`, `watermelon`, `muskmelon`, `apple`, `orange`, `papaya`, `coconut`, `cotton`, `jute`, `coffee`

### Training Features

| Feature       | Unit     |
|---------------|----------|
| N             | mg/kg    |
| P             | mg/kg    |
| K             | mg/kg    |
| Temperature   | °C       |
| Humidity      | %        |
| pH            | 0–14     |
| Rainfall      | mm       |

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

<p align="center">Made with ❤️ for smarter farming 🌾</p>

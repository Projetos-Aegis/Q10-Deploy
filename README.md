# HUD Q10 API

## Overview
The HUD Q10 API is a Flask-based web application designed to provide key performance indicator (KPI) data from a PostgreSQL database. This API allows users to retrieve performance metrics based on specified time ranges, facilitating data analysis and reporting.

## Features
- Connects to a PostgreSQL database to fetch KPI data.
- Provides an endpoint to retrieve KPI metrics based on time ranges (1 hour, 24 hours, 7 days).
- Returns structured JSON responses with relevant KPI information.

## Setup Instructions

### Prerequisites
- Python 3.x
- PostgreSQL database

### Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd hud-q10-api
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure the database connection in `api.py` by updating the `DB_CONFIG` dictionary with your PostgreSQL credentials.

### Running the API
To start the API, run the following command:
```
python api.py
```
The API will be accessible at `http://127.0.0.1:5000/api/kpis`.

## Usage
To retrieve KPI data, send a GET request to the `/api/kpis` endpoint with an optional query parameter `timeRange`. For example:
```
GET /api/kpis?timeRange=24 hour
```

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
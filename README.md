# BatchBoard

A minimalist, autonomous dashboard for displaying live telemetry data for microbreweries (fermentation temperature, specific gravity, and tank pressure).

The solution consists of a FastAPI backend providing a REST endpoint and serving a plain HTML/CSS/JavaScript frontend based on Chart.js.

---

## Development Setup

Follow these steps to run the project locally:

### 1. Prerequisites
* Python 3.10+ installed
* Git

### 2. Clone the repository
``
git clone <repository-url>
cd brew-kiosk``

### 3. Create and activate virtual environment (Windows / PowerShell)
``python -m venv venv
.\venv\Scripts\Activate.ps1``

### 4. Configure environment variables
Copy the example environment file and adjust the values as needed:  
``Cope-Item .env.example .env``

### 4. Install dependencies
``pip install -r requirements.txt``

### 5. Start the development server
``uvicorn main:app --reload``


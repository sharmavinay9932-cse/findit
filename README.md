# FindIt - Intelligent Campus Lost & Found System

## Overview
FindIt is a full-stack web application designed for college campuses to manage lost and found items. It helps students report missing belongings, log found items, and uses a matching system to suggest potential matches, simplifying the recovery process.

## Features
- **User Authentication**: Secure registration and login.
- **Report Items**: Submit detailed reports for lost or found items with image uploads.
- **Image Uploads**: Drag-and-drop or browse to upload photos (JPG, PNG, WEBP, max 5MB).
- **Browse & Search**: Filter and search items by category, location, and keywords.
- **Intelligent Matching**: Basic matching algorithm based on category, name, brand, color, location, date, and description similarity.
- **Responsive Design**: Works perfectly on mobile, tablet, and desktop.
- **Dashboard**: Track your reported items and potential matches.

## Technology Stack
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (Fetch API)
- **Backend**: Python 3, Flask, Werkzeug, Pillow
- **Storage**: JSON files (temporary, structured for easy migration to MySQL)

## Installation & Setup

1. **Clone the repository or navigate to the project directory:**
   ```bash
   cd FindIt
   ```

2. **Create a virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```
   The application will be available at `http://127.0.0.1:5000/`.

## Architecture
The backend is built with a 3-tier architecture:
`Routes -> Services -> Repositories -> MySQL`

## MySQL Setup & Database Integration
This application has been upgraded to use **MySQL 8.x** as the persistence layer instead of JSON files.

### 1. Database Configuration
Create a `.env` file in the root of your project using the provided `.env.example`:
```bash
cp .env.example .env
```
Update the `.env` file with your MySQL credentials:
```text
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=findit_db
```

### 2. Database Initialization
Log into MySQL:
```bash
mysql -u root -p
```
Then execute the schema and seed scripts:
```sql
SOURCE database/schema.sql;
SOURCE database/seed.sql;
```

### 3. Run the application
```bash
python app.py
```

## Demo Credentials
After running the seed script, you can log in using:
- **Email**: admin@findit.edu
- **Password**: admin123
*(Or you can freely register a new account on the `/register` page to start testing!)*

## Future Improvements
- **Complete Claims & Returns Workflow**: The frontend UI for claiming items and admin dashboards can be expanded.
- **MySQL Integration**: Replace the JSON repositories with SQLAlchemy models.
- **Advanced AI Matching**: Implement vector search for image or deep text similarity.

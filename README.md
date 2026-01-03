# GP Stats: MotoGP RESTful Data Service

A Django-based RESTful API service for managing and querying MotoGP race data, including riders, teams, circuits, races, and results.

## Project Overview

This project is a comprehensive RESTful web service built as part of the CM3035 Advanced Web Development coursework at the University of London. The application provides a robust API for accessing and manipulating MotoGP racing data from multiple seasons, allowing users to query race results, rider statistics, and team performance across different categories and years.

The dataset contains MotoGP race information including circuits, riders, teams, and race results with detailed statistics such as finishing positions, points earned, average speeds, and race times.

## Why This Project Was Created

This application was developed to:

1. **Academic Requirement**: Fulfill the requirements for the CM3035 Advanced Web Development module coursework (50% of module grade)
2. **Demonstrate Django REST Framework Skills**: Showcase proficiency in building RESTful APIs using Django, including proper use of models, serializers, views, and URL routing
3. **Data Management**: Provide a practical solution for managing and querying motorsport statistics in a structured, accessible manner
4. **API Design**: Demonstrate best practices in RESTful API design with CRUD operations, complex queries, and proper serialization
5. **Real-World Application**: Create a functional service that could be used by motorsport enthusiasts, analysts, or applications needing access to MotoGP data

## Technologies Used

### Core Framework
- **Python 3.x**: Primary programming language
- **Django 5.1.4**: High-level Python web framework for rapid development
- **Django REST Framework 3.15.2**: Powerful toolkit for building Web APIs

### API Documentation
- **drf-yasg 1.21.8**: Yet Another Swagger Generator for automatic API documentation
- **Swagger UI**: Interactive API documentation interface
- **ReDoc**: Alternative clean API documentation interface

### Database
- **SQLite3**: Default Django relational database (as per project requirements)

### Supporting Libraries
- **asgiref 3.8.1**: ASGI specification reference implementation
- **attrs 24.3.0**: Python classes without boilerplate
- **inflection 0.5.1**: String transformation library
- **jsonschema 4.23.0**: JSON Schema validation
- **jsonschema-specifications 2024.10.1**: JSON Schema meta-schemas
- **packaging 24.2**: Core utilities for Python packages
- **pytz 2024.2**: World timezone definitions
- **PyYAML 6.0.2**: YAML parser and emitter
- **referencing 0.35.1**: JSON reference resolution
- **rpds-py 0.22.3**: Python bindings to Rust's persistent data structures
- **sqlparse 0.5.3**: Non-validating SQL parser
- **tzdata 2024.2**: Timezone database
- **uritemplate 4.1.1**: URI template parsing

## Project Structure

```
GP_stats/
├── GP_stats/                  # Main project configuration
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL routing with Swagger integration
│   ├── wsgi.py               # WSGI configuration
│   └── asgi.py               # ASGI configuration
├── mrds/                      # Main application (MotoGP Results Data Service)
│   ├── models.py             # Data models (Circuit, Rider, Team, Race, Result)
│   ├── serializers.py        # REST Framework serializers
│   ├── api.py                # RESTful API endpoints
│   ├── views.py              # Traditional Django views
│   ├── urls.py               # Application URL routing
│   ├── tests.py              # Unit tests
│   ├── admin.py              # Django admin configuration
│   └── migrations/           # Database migrations
├── Scripts/
│   └── populate_mrds.py      # Data loading script for CSV import
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── db.sqlite3                # SQLite database
└── output_file.txt           # Database dump in text format
```

## Database Schema

The application uses a relational database with the following models:

### Circuit
- `shortname`: Short identifier for the circuit
- `circuit_name`: Full name of the racing circuit

### Rider
- `name`: Rider's full name
- `country`: Rider's country of origin
- `number`: Rider's racing number

### Team
- `name`: Team name
- `bike_name`: Motorcycle manufacturer/model

### Race
- `year`: Season year
- `category`: Race category (e.g., MotoGP, Moto2, Moto3)
- `sequence`: Race sequence number in the season
- `circuit`: Foreign key to Circuit model

### Result
- `race`: Foreign key to Race model
- `rider`: Foreign key to Rider model
- `team`: Foreign key to Team model
- `position`: Finishing position (nullable)
- `points`: Championship points earned (nullable)
- `speed`: Average speed in km/h (nullable)
- `time`: Race time or time behind winner (nullable)

## RESTful API Endpoints

The application provides 6 comprehensive RESTful endpoints:

### 1. POST `/api/add_rider/`
Add a new rider to the database with validation.

### 2. POST `/api/add_race_result/<race_id>/`
Add a new race result for a specific race.

### 3. GET `/api/top_riders/<category>/<year>/`
Retrieve top riders ranked by total points for a specific category and year.

### 4. PATCH `/api/edit_race_result/<result_id>/`
Update an existing race result (partial updates supported).

### 5. DELETE `/api/remove_race_result/<result_id>/`
Remove a race result from the database.

### 6. GET `/api/list_riders/`
List all riders with their total points and teams (uses custom serialization).

### 7. GET `/api/list_results_sorted/<year>/`
Get all race results for a specific year, organized by category and circuit.

## Installation and Setup

### Prerequisites
- Python 3.x installed
- pip package manager

### Installation Steps

1. **Extract the project files**
   ```bash
   unzip GP_stats.zip
   cd GP_stats
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

4. **Populate the database**
   ```bash
   python Scripts/populate_mrds.py
   ```

5. **Create admin superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main page: http://127.0.0.1:8000/
   - Swagger API docs: http://127.0.0.1:8000/swagger/
   - ReDoc API docs: http://127.0.0.1:8000/redoc/
   - Django admin: http://127.0.0.1:8000/admin/

## Running Tests

Execute the unit tests to verify API functionality:

```bash
python manage.py test mrds
```

## Data Loading

The [Scripts/populate_mrds.py](Scripts/populate_mrds.py) script loads MotoGP data from a CSV file into the database. It:
- Clears existing data to prevent duplicates
- Parses the CSV file with race data
- Creates Circuit, Rider, Team, Race, and Result entries
- Handles missing or null values appropriately
- Maintains referential integrity between related models

## Features

- Full CRUD operations on race results
- Complex querying with aggregations (SUM, filtering)
- Proper REST serialization using Django REST Framework
- Comprehensive API documentation with Swagger/ReDoc
- Input validation and error handling
- Bulk data loading from CSV files
- Admin interface for data management
- Unit tests for API endpoints

## API Usage Examples

### Add a New Rider (POST)
```bash
curl -X POST http://127.0.0.1:8000/api/add_rider/ \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "country": "USA", "number": 99}'
```

### Get Top Riders for MotoGP 2023 (GET)
```bash
curl http://127.0.0.1:8000/api/top_riders/MotoGP/2023/
```

### Update Race Result (PATCH)
```bash
curl -X PATCH http://127.0.0.1:8000/api/edit_race_result/1/ \
  -H "Content-Type: application/json" \
  -d '{"position": 2, "points": 20}'
```

### Delete Race Result (DELETE)
```bash
curl -X DELETE http://127.0.0.1:8000/api/remove_race_result/1/
```

## Development Environment

- **Operating System**: Windows 10/11
- **Python Version**: 3.x
- **Database**: SQLite3 (included with Python)
- **Development Server**: Django development server

## Admin Access

The Django admin interface is available at `/admin/`. Contact the project administrator for credentials.

## License

This project was created for educational purposes as part of the University of London BSc Computer Science program.

## Author

Created as coursework for CM3035 - Advanced Web Development module.

## Acknowledgments

- MotoGP dataset sourced from public motorsport statistics
- Django and Django REST Framework documentation
- University of London course materials and guidance

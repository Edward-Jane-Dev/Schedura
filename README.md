# Django Scheduling Tool

This project is a scheduling application built with Python and Django. It provides a foundation for managing and scheduling events, appointments, or tasks.

## Getting Started

### Prerequisites
- Python 3.12 or later
- pip (Python package manager)

### Installation
1. **Clone the repository:**
   ```sh
   git clone <repository-url>
   cd django_scheduling_tool
   ```
2. **Create and activate a virtual environment:**
   - On Windows:
     ```sh
     python -m venv venv
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```sh
     python3 -m venv venv
     source venv/bin/activate
     ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Apply migrations:**
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```
5. **Run the development server:**
   ```sh
   python manage.py runserver
   ```

## Project Structure
- `schedura/` - Main Django project settings and URLs
- `scheduler/` - App for scheduling features
- `requirements.txt` - Python dependencies
- `manage.py` - Django project management script

## License
This project is licensed under the MIT License.

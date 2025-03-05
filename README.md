# Website PC Architecture

## Purpose

This project is web development endeavor, aimed at building a comprehensive understanding of web technologies and frameworks.

## Description

Website PC Architecture is a web application that allows users to:
- Register and manage their accounts.
- Update their profiles.
- Explore topics related to computer architecture.
- Send inquiries through a contact form.
- Manage favorite topics.

## Technologies Used

- **Flask**: A lightweight web framework for Python.
- **Flask-SQLAlchemy**: For database management.
- **Flask-Login**: For user session management.
- **Flask-WTF**: For form handling and CSRF protection.
- **SQLite**: A simple database for storing user and topic data.
- **HTML/CSS**: For front-end design and layout.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/fotinov/Website-PC-Architecture.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Website-PC-Architecture
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   - Create a `.env` file in the root directory and add the following:
     ```
     SECRET_KEY=KEY_HERE
     DATABASE_URL=sqlite:///site.db
     ```

5. Set the Flask environment variables in your terminal:
   ```bash
   # For Windows PowerShell
   taskkill /IM python.exe /F
   $env:FLASK_APP="app.py"
   $env:FLASK_ENV="development"
   $env:FLASK_DEBUG="1"
   flask run
   ```

6. Initialize the database:
   ```bash
   python app.py
   ```

## Generating a Secret Key

To generate a secure secret key, you can use the following Python code:

```python
import secrets

print(secrets.token_hex(32))
```

Run this code in a Python environment to generate a random secret key, and replace `KEY_HERE` in your `.env` file with the generated key.

## Usage

- Open your web browser and go to `http://127.0.0.1:5000` to access the application.
- Register for a new account or log in with an existing account.
- Explore topics, manage your profile, and send messages through the contact form.



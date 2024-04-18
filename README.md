# My Django and FastAPI Project

## Description
This is a financial application that allows users to manage a portfolio of stocks. It uses Django for the backend, Bootstrap and HTMX for the frontend, and FastAPI and SQLAlchemy for the API and database operations.

## Technologies Used
- Django
- Bootstrap
- HTMX
- FastAPI
- SQLAlchemy
- PostgreSQL

## Features

### Google Integration
This application integrates with Google services. To set this up, you will need to create a Google OAuth client ID and download the JSON file.

### Discord Integration
This application also integrates with Discord. To set this up, you will need to create a Discord application and obtain a token.

## Setup

This application uses environment variables for configuration. To set up your environment variables:

1. Rename `env.sample` to `.env`.
2. Replace the placeholder values with your actual values.

The `.env` file is used to store sensitive information such as:

- Google client ID and secret
- Discord token
- Database credentials

Never commit your `.env` file to the repository. It is ignored by Git to prevent exposing your sensitive information.

### OAuth
This application uses OAuth for user authentication. The necessary setup is included in the Django settings.

## Installation
1. Clone the repository: `git clone https://github.com/username/repository.git`
2. Install the dependencies: `pip install -r requirements.txt`
3. Set up the database: `python manage.py migrate`
4. Run the server: `python manage.py runserver`

## Usage
To use this application, navigate to `localhost:8000` in your web browser.

## License
This project is licensed under the MIT License.

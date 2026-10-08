# Expense Tracker

A command-line personal finance management application built with Python.

## Features

- Add expenses with descriptions, categories, and amounts.
- Add income and update the available balance.
- Edit and confirm transactions before saving them.
- View expenses and total spending.
- Filter spending totals by category.
- Identify the largest expense.
- Calculate average expense amounts.
- Save financial data locally using JSON.
- Validate user input and handle invalid data.

## Technologies

- Python 3
- JSON for local data storage
- Git and GitHub for version control

## How to Run

1. Install Python 3.
2. Clone or download this repository.
3. Open a terminal in the project folder.
4. Run the application:

   `python main.py`

No third-party dependencies are required.

## Data Storage

The application stores financial information locally in `data.json`. This file is excluded from version control to protect personal data.

When the application runs for the first time, it asks the user to enter an initial balance.

## Project Purpose

This project was developed to practice Python programming fundamentals, including functions, loops, conditional statements, input validation, file handling, and JSON persistence.

## Future Improvements

- Transaction history with dates.
- Edit and delete previously saved transactions.
- Database integration with PostgreSQL.
- REST API development using FastAPI.
- Automated testing.
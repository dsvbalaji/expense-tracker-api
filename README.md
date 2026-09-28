# Personal Expense Tracker API

A REST API built with FastAPI and MongoDB that allows users to record, view, update, delete, and analyze their daily expenses.

## Technologies Used

- Python
- FastAPI
- MongoDB
- PyMongo
- Pydantic
- Uvicorn

## Features

- Add a new expense
- View all expenses
- View an expense by ID
- Update an expense
- Delete an expense
- Filter expenses by category
- Filter expenses by month
- Calculate total expenses
- Calculate total expenses for a specific category
- Validate expense amount
- Validate category
- Prevent future expense dates

## Project Structure

```text
expense-tracker-api/
│
├── database.py
├── examples.md
├── main.py
├── models.py
├── requirements.txt
├── README.md
├── .gitignore
└── venv/
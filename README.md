# MiniStock

**MiniStock** is a desktop inventory management application built with Python, CustomTkinter and SQLite.

It is designed to help small shops manage their products, monitor stock levels and keep track of inventory.

## Features

- **Dashboard:** Displays inventory statistics, including total products, total units and stock value.
- **Product Management:** Add, edit and delete products.
- **Product Search:** Search through the inventory.
- **Low-Stock Alerts:** Identify products that are running low.
- **Local Database:** Stores product information using SQLite, so data persists between sessions.

## Screenshots

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/a4b458db-ff8d-490a-9272-1dd477f12c44" />
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/d0f2ba86-3539-468a-bc24-61f38ee21c6a" />

## Technologies Used

- Python
- CustomTkinter — graphical user interface
- SQLite — database management

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/GameEmpire/MiniStock.git
   ```

2. Navigate into the project folder:

   ```bash
   cd MiniStock
   ```

3. Install the required dependencies:

   ```bash
   pip install customtkinter
   ```

4. Run the application:

   ```bash
   python main.py
   ```

The SQLite database is initialized automatically when the application starts.

## Project Structure

```text
MiniStock/
├── main.py
├── database.py
├── requirements.txt
├── README.md
└── .gitignore
```

- `main.py` — Application interface and user interactions.
- `database.py` — Database initialization and operations.
- `requirements.txt` — Required Python packages.
- `.gitignore` — Files excluded from Git tracking.

## Project Purpose

This project was developed as a school project to explore Python application development, graphical user interfaces, database integration and software organization.

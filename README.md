# Restaurant Management System

A simple, human-friendly web application for managing a restaurant's menu, reservations, and orders. Built with Python (Flask), SQLite, HTML/CSS.

## Features

- **Menu Management:** Add, view, and delete menu items.
- **Table Reservations:** Add, view, and delete reservations.
- **Order Management:** Add, view, update, and delete orders.
- **Simple Authentication:** Login system for admin/staff.
- **Dashboard:** Overview of key stats.

## Installation

1. **Clone this repository:**
   ```bash
   git clone <your-repo-url>
   cd restaurant-management
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

   The app will initialize the database (`restaurant.db`) on first run.

4. **Access in your browser:**
   - Go to: http://127.0.0.1:5000

   - Login with:
     - Username: `admin`
     - Password: `admin`

## File Structure

```
restaurant-management/
├── app.py
├── schema.sql
├── requirements.txt
├── static/
│   ├── style.css
│   └── script.js
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── login.html
│   ├── menu.html
│   ├── reservations.html
│   └── orders.html
└── README.md
```

## Notes

- **Password Storage:** For demo purposes, passwords are stored in plain text. For real-world use, always hash and salt passwords!
- **Database:** Uses SQLite for simplicity. You can extend to other databases as needed.
- **Customization:** Feel free to expand features, improve UI, or integrate with more advanced JS frameworks.

## License

MIT License. Use freely for learning or as a starter project!

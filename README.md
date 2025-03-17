Billing App

A simple and efficient Billing Application built with Python (PyQt5) and SQLite to manage customer invoices and export billing data to CSV.

Features 🚀

Add, Edit, and Delete Bills

Search Bills by Customer Name or Item

Auto Calculation of Total Amount

Tooltips for User Inputs

CSV Export for easy data management

Responsive UI with a Clean Design

Persistent Storage using SQLite

Tech Stack 🛠️

Python (3.x)

PyQt5 (for GUI Development)

SQLite (for local database storage)

Pandas (for exporting CSV)

Installation 📥

Clone the repository:

git clone https://github.com/dgizhere/billing-app.git
cd billing-app

Install dependencies:

pip install -r requirements.txt

Run the application:

python main.py

Usage 📝

Add a Bill – Enter customer details, item name, quantity, and price.

Search Bills – Use the search bar to filter results.

Edit/Delete Bills – Click on a bill entry to modify or delete it.

Export to CSV – Click the 'Export' button to save data.

Screenshots 📸



Folder Structure 📂

📦 billing-app
├── 📂 billing_app
│   ├── database.py  # Handles SQLite operations
│   ├── main.py      # Main application file
│   ├── bills.csv    # Exported CSV data (optional)
├── README.md        # Project documentation
├── requirements.txt # Dependencies

Issues & Contributions 🤝

Found a bug? Report it under Issues

Want to contribute? Fork the repo and submit a PR!

License 📜

This project is licensed under the MIT License.

🌟 If you like this project, please ⭐ it on GitHub!

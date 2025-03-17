import sys
import csv
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QLabel
from database import Database
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression

class BillingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Billing Form Application")
        self.setGeometry(100, 100, 600, 400)

        # Initialize database
        self.db = Database()

        # Main layout
        self.layout = QVBoxLayout()

        # Form for customer details
        self.form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.address_input = QLineEdit()

        self.form_layout.addRow("Name:", self.name_input)
        self.form_layout.addRow("Phone:", self.phone_input)
        self.form_layout.addRow("Email:", self.email_input)
        self.form_layout.addRow("Address:", self.address_input)

        # Form for billing details
        self.item_name_input = QLineEdit()
        self.quantity_input = QLineEdit()
        self.price_input = QLineEdit()
        self.total_input = QLineEdit()

        self.form_layout.addRow("Item Name:", self.item_name_input)
        self.form_layout.addRow("Quantity:", self.quantity_input)
        self.form_layout.addRow("Price:", self.price_input)
        self.form_layout.addRow("Total:", self.total_input)

        # Buttons
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_form)

        self.retrieve_button = QPushButton("Retrieve Bills")
        self.retrieve_button.clicked.connect(self.retrieve_bills)

        # Table to display bills
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Bill ID", "Customer Name", "Item Name", "Quantity", "Total"])

        # Add widgets to layout
        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(self.submit_button)
        self.layout.addWidget(self.retrieve_button)
        self.layout.addWidget(self.table)

        # Add validation for phone and email fields
        phone_regex = QRegularExpression("^[0-9]{10}$")  # 10-digit phone number
        email_regex = QRegularExpression("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$")

        self.phone_input.setValidator(QRegularExpressionValidator(phone_regex, self))
        self.email_input.setValidator(QRegularExpressionValidator(email_regex, self))

        # Add validation for quantity and price fields
        self.quantity_input.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]*"), self))
        self.price_input.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]*\\.?[0-9]*"), self))

        # Add buttons for edit and delete
        self.edit_button = QPushButton("Edit Bill")
        self.edit_button.clicked.connect(self.edit_bill)

        self.delete_button = QPushButton("Delete Bill")
        self.delete_button.clicked.connect(self.delete_bill)

        # Add buttons to the layout
        self.layout.addWidget(self.edit_button)
        self.layout.addWidget(self.delete_button)

        # Add search bar
        self.search_layout = QHBoxLayout()
        self.search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by customer or item name")
        self.search_input.textChanged.connect(self.filter_bills)

        self.search_layout.addWidget(self.search_label)
        self.search_layout.addWidget(self.search_input)
        self.layout.addLayout(self.search_layout)

        # Add Export Button
        self.export_button = QPushButton("Export to CSV")
        self.export_button.clicked.connect(self.export_to_csv)
        self.layout.addWidget(self.export_button)

        # Add tooltips
        self.name_input.setToolTip("Enter the customer's full name")
        self.phone_input.setToolTip("Enter a 10-digit phone number")
        self.email_input.setToolTip("Enter a valid email address")
        self.item_name_input.setToolTip("Enter the item name")
        self.quantity_input.setToolTip("Enter the quantity (numeric value)")
        self.price_input.setToolTip("Enter the price (numeric value)")
        self.total_input.setToolTip("Total is auto-calculated")

        # Add styling
        self.setStyleSheet("""
    QWidget { 
        font-size: 14px; 
    }
    QPushButton { 
        padding: 5px; 
    }
    QTableWidget { 
        background: transparent;  /* Makes the table background transparent */
        color: white;  /* Ensures text remains visible */
        gridline-color: #A27B5C;  /* Warm Brown Grid Lines */
    }
    QHeaderView::section {
        background: transparent;  /* Makes headers transparent */
        color: white;
        font-weight: bold;
        padding: 5px;
        border: 1px solid #A27B5C;
    }
    QTableWidget::item {
        padding: 5px;
        background: transparent;  /* Makes table items transparent */
    }
""")

        self.setLayout(self.layout)


        # Initialize current_bill_id
        self.current_bill_id = None

        # Connect calculate_total to quantity and price inputs
        self.quantity_input.textChanged.connect(self.calculate_total)
        self.price_input.textChanged.connect(self.calculate_total)

    def submit_form(self):
        if self.current_bill_id:
            self.update_bill()
        else:
            try:
                # Insert customer details
                customer_id = self.db.insert_customer(
                    self.name_input.text(),
                    self.phone_input.text(),
                    self.email_input.text(),
                    self.address_input.text()
                )

                # Insert billing details
                self.db.insert_bill(
                    customer_id,
                    self.item_name_input.text(),
                    int(self.quantity_input.text()),
                    float(self.price_input.text()),
                    float(self.total_input.text())
                )

                QMessageBox.information(self, "Success", "Form submitted successfully!")
                self.clear_form()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def retrieve_bills(self):
        try:
            # Fetch bills from the database
            bills = self.db.retrieve_bills()

            # Display bills in the table
            self.table.setRowCount(len(bills))
            for row, bill in enumerate(bills):
                for col, data in enumerate(bill):
                    self.table.setItem(row, col, QTableWidgetItem(str(data)))

            QMessageBox.information(self, "Info", "Bills retrieved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def closeEvent(self, event):
        # Close the database connection when the application is closed
        self.db.close_connection()
        event.accept()

    def calculate_total(self):
        try:
            quantity_text = self.quantity_input.text()
            price_text = self.price_input.text()
            if quantity_text and price_text:
                quantity = int(quantity_text)
                price = float(price_text)
                total = quantity * price
                self.total_input.setText(f"{total:.2f}")
            else:
                self.total_input.setText("0.00")
        except ValueError:
            self.total_input.setText("0.00")

    def edit_bill(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Warning", "Please select a bill to edit.")
            return

        bill_id = int(self.table.item(selected_row, 0).text())
        customer_name = self.table.item(selected_row, 1).text()
        item_name = self.table.item(selected_row, 2).text()
        quantity = int(self.table.item(selected_row, 3).text())
        total = float(self.table.item(selected_row, 4).text())

        # Populate the form with selected bill details
        self.name_input.setText(customer_name)
        self.item_name_input.setText(item_name)
        self.quantity_input.setText(str(quantity))
        self.total_input.setText(f"{total:.2f}")

        # Store the bill ID for updating
        self.current_bill_id = bill_id

    def delete_bill(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Warning", "Please select a bill to delete.")
            return

        bill_id = int(self.table.item(selected_row, 0).text())
        confirm = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this bill?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                self.db.cursor.execute("DELETE FROM bills WHERE bill_id = %s", (bill_id,))
                self.db.db.commit()
                self.retrieve_bills()  # Refresh the table
                QMessageBox.information(self, "Success", "Bill deleted successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def filter_bills(self):
        search_text = self.search_input.text().strip().lower()
        for row in range(self.table.rowCount()):
            match = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and search_text in item.text().lower():
                    match = True
                    break
            self.table.setRowHidden(row, not match)

    def export_to_csv(self):
        try:
            with open("bills.csv", mode="w", newline="") as file:
                writer = csv.writer(file)
                # Write header
                writer.writerow(["Bill ID", "Customer Name", "Item Name", "Quantity", "Total"])
                # Write data
                for row in range(self.table.rowCount()):
                    row_data = []
                    for col in range(self.table.columnCount()):
                        item = self.table.item(row, col)
                        row_data.append(item.text())
                    writer.writerow(row_data)
            QMessageBox.information(self, "Success", "Data exported to bills.csv!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def clear_form(self):
        self.name_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        self.address_input.clear()
        self.item_name_input.clear()
        self.quantity_input.clear()
        self.price_input.clear()
        self.total_input.clear()
        self.current_bill_id = None  # Reset the bill ID

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BillingApp()
    window.show()
    sys.exit(app.exec())
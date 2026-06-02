import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import mysql.connector
import random
import datetime
from decimal import Decimal

def connect_to_db():
    """ Connect to the MySQL database """
    try:
        conn = mysql.connector.connect(
            host='localhost',        # Typically 'localhost' or an IP address
            user='root',
            password='Aksh@t27',
            database='VITBank'
        )
        if conn.is_connected():
            # messagebox.showinfo("","Connected to MySQL database")
            pass
        return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"{e}")
        return None

def generate_account_number():
    """ Generate a unique 10-digit account number """
    return ''.join([str(random.randint(0, 9)) for _ in range(10)])

def open_account(aadhaar, pan, dob, photo, sign, mobile, email, address, account_type):
    """ Create a new bank account """
    conn = connect_to_db()
    if conn is not None:
        cursor = conn.cursor()
        account_number = generate_account_number()
        try:
            cursor.execute("""
                INSERT INTO AccountHolders (
                    AccountNumber, AadhaarNumber, PANNumber, DateOfBirth, PhotoFileName,
                    SignatureFileName, MobileNumber, EmailAddress, Address, AccountType, Balance
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (account_number, aadhaar, pan, dob, photo, sign, mobile, email, address, account_type, 500 if account_type == 'current' else 0))
            conn.commit()
            messagebox.showinfo("",f"Account successfully created. Your account number is {account_number}.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"{e}")
        finally:
            cursor.close()
            conn.close()

def check_account_exists(account_number):
    """ Check if the account number exists in the database """
    conn = connect_to_db()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("SELECT AccountNumber FROM AccountHolders WHERE AccountNumber = %s", (account_number,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None
    return False

def generate_unique_username():
    """ Generate a unique username for online banking """
    conn = connect_to_db()
    if conn is not None:
        username = None
        while True:
            username = 'User' + ''.join([str(random.randint(0, 9)) for _ in range(6)])
            cursor = conn.cursor()
            cursor.execute("SELECT Username FROM OnlineBankingCredentials WHERE Username = %s", (username,))
            if cursor.fetchone() is None:
                break
        cursor.close()
        conn.close()
        return username
    return None

def get_credentials(account_number):
    """ Generate and store credentials for online banking """
    
    if check_account_exists(account_number):
        username = generate_unique_username()
         # Use a secure password entry dialog
        password = simpledialog.askstring("Password", "Please enter your desired password:", show='*')        
        conn = connect_to_db()
        if conn is not None:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO OnlineBankingCredentials (AccountNumber, Username, Password)
                    VALUES (%s, %s, %s)
                """, (account_number, username, password))
                conn.commit()
                messagebox.showinfo("",f"Credentials created successfully. Your username is {username}.")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"{e}")
            finally:
                cursor.close()
                conn.close()
    else:
        messagebox.showerror("Invalid account number.")

def update_password(account_number):
    """ Change the password for online banking """
    if check_account_exists(account_number):
        conn = connect_to_db()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("SELECT Username FROM OnlineBankingCredentials WHERE AccountNumber = %s", (account_number,))
            if cursor.fetchone() is not None:  # Check if credentials exist
                 # Use a secure password entry dialog
                new_password = simpledialog.askstring("Password Update", "Please enter your new password:", show='*')
                #new_password = input("Please enter your new password: ")  # In real applications, ensure this input is handled securely
                try:
                    cursor.execute("""
                        UPDATE OnlineBankingCredentials
                        SET Password = %s
                        WHERE AccountNumber = %s
                    """, (new_password, account_number))
                    conn.commit()
                    messagebox.showinfo("","Password updated successfully.")
                except mysql.connector.Error as e:
                    messagebox.showerror("Error", f"{e}")
                finally:
                    cursor.close()
                    conn.close()
            else:
                messagebox.showwarning("Warning","No online banking credentials found for this account.")
    else:
        messagebox.showwarning("Warning","Invalid account number.")

def generate_card_number():
    """ Generate a unique 16-digit card number """
    return ''.join([str(random.randint(0, 9)) for _ in range(16)])

def request_debit_card(account_number):
    """ Create a request for a new debit card """
    if check_account_exists(account_number):
        conn = connect_to_db()
        if conn is not None:
            card_number = generate_card_number()
            issue_date = datetime.date.today()
            expiry_date = issue_date + datetime.timedelta(days=5*365)  # Expiry in 5 years
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO Cards (CardNumber, AccountNumber, CardType, IssueDate, ExpiryDate)
                    VALUES (%s, %s, 'debit', %s, %s)
                """, (card_number, account_number, issue_date, expiry_date))
                conn.commit()
                messagebox.showinfo("",f"Debit card successfully issued. Your card number is {card_number}.")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"{e}")
            finally:
                cursor.close()
                conn.close()
    else:
        messagebox.showwarning("Warning","Invalid account number.")

def request_credit_card(account_number):
    """ Create a request for a new credit card """
    if check_account_exists(account_number):
        conn = connect_to_db()
        if conn is not None:
            card_number = generate_card_number()  # Reuse the card number generator from the debit card function
            issue_date = datetime.date.today()
            expiry_date = issue_date + datetime.timedelta(days=5*365)  # Expiry in 5 years
            cursor = conn.cursor()
            try:
                # Before issuing a credit card, you might want to check for eligibility criteria such as account balance, account type, etc.
                # For simplicity, assuming if they have an account, they are eligible
                cursor.execute("""
                    INSERT INTO Cards (CardNumber, AccountNumber, CardType, IssueDate, ExpiryDate)
                    VALUES (%s, %s, 'credit', %s, %s)
                """, (card_number, account_number, issue_date, expiry_date))
                conn.commit()
                messagebox.showinfo("",f"Credit card successfully issued. Your card number is {card_number}.")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"{e}")
            finally:
                cursor.close()
                conn.close()
    else:
        messagebox.showwarning("Warning","Invalid account number.")

def generate_cheque_book_number():
    """ Generate a unique cheque book number """
    return ''.join([str(random.randint(0, 9)) for _ in range(12)])

def request_cheque_book(account_number):
    """ Create a request for a new cheque book """
    if check_account_exists(account_number):
        conn = connect_to_db()
        if conn is not None:
            cheque_book_number = generate_cheque_book_number()
            issue_date = datetime.date.today()
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO ChequeBooks (ChequeBookNumber, AccountNumber, IssueDate)
                    VALUES (%s, %s, %s)
                """, (cheque_book_number, account_number, issue_date))
                conn.commit()
                messagebox.showinfo("",f"Cheque book successfully issued. Your cheque book number is {cheque_book_number}.")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"{e}")
            finally:
                cursor.close()
                conn.close()
    else:
        messagebox.showwarning("Warning","Invalid account number.")

def deposit_money(account_number, amount):
    """ Deposit money into a bank account """
    if check_account_exists(account_number):
        if amount > 0:
            conn = connect_to_db()
            if conn is not None:
                cursor = conn.cursor()
                try:
                    # Update the balance
                    cursor.execute("""
                        UPDATE AccountHolders
                        SET Balance = Balance + %s
                        WHERE AccountNumber = %s
                    """, (amount, account_number))
                    conn.commit()
                    messagebox.showinfo("",f"Successfully deposited ${amount} to account {account_number}.")
                    log_transaction(account_number, 'deposit', amount, 'branch')
                except mysql.connector.Error as e:
                    messagebox.showerror("Error", f"{e}")
                finally:
                    cursor.close()
                    conn.close()
        else:
            messagebox.showinfo("","The deposit amount must be positive.")
    else:
        messagebox.showwarning("Warning","Invalid account number.")

def has_card_or_book(account_number, item_type):
    """ Check if the user has a specific type of card or a cheque book issued """
    conn = connect_to_db()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("SELECT CardNumber FROM Cards WHERE AccountNumber = %s AND CardType = %s", (account_number, item_type))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None


def check_sufficient_balance(account_number, amount):
    """ Check if there is enough balance in the account for the withdrawal """
    conn = connect_to_db()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("SELECT Balance FROM AccountHolders WHERE AccountNumber = %s", (account_number,))
        current_balance = cursor.fetchone()
        cursor.close()
        conn.close()
        if current_balance is not None and current_balance[0] >= amount:
            return True
        else:
            return False
    return False
def has_cheque_book(account_number):
    """ Check if the user has a cheque book issued """
    conn = connect_to_db()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT ChequeBookNumber FROM ChequeBooks WHERE AccountNumber = %s", (account_number,))
            result = cursor.fetchone()
            return bool(result)  # Returns True if a cheque book exists, False otherwise
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"{e}")
            return False
        finally:
            cursor.close()
            conn.close()
    else:
        messagebox.showwarning("Warning","Failed to connect to the database.")
        return False
    
def has_method(account_number, method_type):
    conn = connect_to_db()
    if conn is not None:
        cursor = conn.cursor(buffered=True)
        try:
            if method_type in ['debit card', 'credit card']:
                cursor.execute("SELECT CardNumber FROM Cards WHERE AccountNumber = %s AND CardType = %s", (account_number, method_type.split()[0]))
            elif method_type == 'cheque':
                cursor.execute("SELECT ChequeBookNumber FROM ChequeBooks WHERE AccountNumber = %s", (account_number,))
            result = cursor.fetchall()  # Use fetchall to ensure all results are consumed
            return bool(result)
        except mysql.connector.Error as e:
            messagebox.showinfo("",f"Error checking method: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    else:
        messagebox.showwarning("Warning","Failed to connect to the database.")
        return False


def interactive_withdraw_money(account_number):
    """ Interactive function to process withdrawals using different methods """
    def on_withdraw():
        method = method_var.get()  # Default to branch if invalid choice
        window.destroy()

        if method in ['debit card', 'credit card', 'cheque'] and not has_method(account_number, method):
            issue_new = messagebox.askyesno("Issue New", f"You do not have a valid {method}.\n Do you want to issue a new {method}?")
            if issue_new:            
                # Assume request_method is a function that handles issuing new cards or cheque books
                # request_method(account_number, method)
                if method == 'cheque' and not has_cheque_book(account_number):
                    request_cheque_book(account_number)
                elif method == 'debit card' and not has_card_or_book(account_number, 'debit'):
                    request_debit_card(account_number)
                else:
                    request_credit_card(account_number)
                return
            else:
                messagebox.showinfo("","Withdrawal cancelled.")
                return

        #amount = float(input("Enter the amount to withdraw: "))
        amount = simpledialog.askfloat("Withdrawal Amount", "Enter the amount to withdraw:")

        if process_withdrawal(account_number, amount, method):
            messagebox.showinfo("",f"{amount} has been successfully withdrawn from your account via {method}.")
        else:
            messagebox.showinfo("","Withdrawal failed.")
            
    window = tk.Toplevel()
    window.title("Withdrawal Method Selection")

    method_var = tk.StringVar(value='branch')

    tk.Radiobutton(window, text='Debit Card', variable=method_var, value='debit card').pack(anchor=tk.W)
    tk.Radiobutton(window, text='Credit Card', variable=method_var, value='credit card').pack(anchor=tk.W)
    tk.Radiobutton(window, text='Cheque Book', variable=method_var, value='cheque').pack(anchor=tk.W)
    tk.Radiobutton(window, text='Physical Branch', variable=method_var, value='branch').pack(anchor=tk.W)

    withdraw_button = tk.Button(window, text="Withdraw", command=on_withdraw)
    withdraw_button.pack(pady=10)

    
def process_withdrawal(account_number, amount, method):
    """ Update the database to reflect the withdrawal """
    conn = connect_to_db()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE AccountHolders SET Balance = Balance - %s WHERE AccountNumber = %s AND Balance >= %s", (amount, account_number, amount))
            if cursor.rowcount == 0:
                messagebox.showinfo("","Insufficient funds or account not found.")
                return False
            # Log the transaction
            cursor.execute("INSERT INTO Transactions (AccountNumber, TransactionType, Amount, TransactionDate, Method) VALUES (%s, 'withdraw', %s, CURDATE(), %s)", (account_number, amount, method))
            conn.commit()
            return True
        except mysql.connector.Error as e:
            messagebox.showinfo("",f"Error during withdrawal: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
    else:
        messagebox.showwarning("Warning","Failed to connect to the database.")
        return False
transactions1 = [
     (123, 'Deposit', 100.00, '2024-05-02', 'Online Transfer'),
     (124, 'Withdrawal', 50.00, '2024-05-03', 'ATM')
]

def view_transactions(account_number):
    """ Display the transaction history for an account """
    root = tk.Toplevel()
    root.title("Transaction History")

    if check_account_exists(account_number):
        conn = connect_to_db()
        if conn is not None:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    SELECT TransactionID, TransactionType, Amount, TransactionDate, Method
                    FROM Transactions
                    WHERE AccountNumber = %s
                    ORDER BY TransactionDate DESC
                """, (account_number,))
                transactions = cursor.fetchall()
                if transactions:
                    columns = ('id', 'type', 'amount', 'date', 'method')
                    tree = ttk.Treeview(root, columns=columns, show='headings')

                    # Define the column headings
                    tree.heading('id', text='ID')
                    tree.heading('type', text='Type')
                    tree.heading('amount', text='Amount')
                    tree.heading('date', text='Date')
                    tree.heading('method', text='Method')
                    
                    tree.column('id', anchor='center')
                    tree.column('type', anchor='center')
                    tree.column('amount', anchor='center')
                    tree.column('date', anchor='center')
                    tree.column('method', anchor='center')

                    # Add data to the treeview
                    for transaction in transactions:
                        tree.insert('', tk.END, values=transaction)

                    tree.pack(expand=True, fill='both')
                else:
                    messagebox.showinfo("","No transactions found.")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"{e}")
            finally:
                cursor.close()
                conn.close()
    else:
        messagebox.showwarning("Warning","Invalid account number.")
    root.mainloop()  # Keep the window open to display the transactions


def check_balance(account_number):
    """ Display the current balance for an account """
    if check_account_exists(account_number):
        conn = connect_to_db()
        if conn is not None:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT Balance FROM AccountHolders WHERE AccountNumber = %s", (account_number,))
                balance = cursor.fetchone()
                if balance is not None:
                    messagebox.showinfo("",f"Current balance: ${balance[0]}")
                else:
                    messagebox.showinfo("","Account not found.")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"{e}")
            finally:
                cursor.close()
                conn.close()
    else:
        messagebox.showwarning("Warning","Invalid account number.")

def check_loan_eligibility(account_number):
    """ Determine if the account holder is eligible for a loan based on specific criteria """
    conn = connect_to_db()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Balance, AccountType
            FROM AccountHolders
            WHERE AccountNumber = %s
        """, (account_number,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        # Example criteria: Balance over $1000 and account type is not 'current'
        if result and result[0] > 1000 and result[1] != 'current':
            return True
        else:
            return False
    return False

def request_loan(account_number, loan_amount):
    """ Process a loan request """
    if check_account_exists(account_number):
        if check_loan_eligibility(account_number):
            conn = connect_to_db()
            if conn is not None:
                cursor = conn.cursor()
                loan_date = datetime.date.today()
                try:
                    cursor.execute("""
                        INSERT INTO Loans (AccountNumber, LoanAmount, LoanDate, LoanType, EligibilityStatus)
                        VALUES (%s, %s, %s, 'personal', 1)
                    """, (account_number, loan_amount, loan_date))
                    conn.commit()
                    messagebox.showinfo("",f"Loan successfully issued. Loan amount: ${loan_amount}.")
                    log_transaction(account_number, 'loan_granted', loan_amount, 'branch')
                except mysql.connector.Error as e:
                    messagebox.showerror("Error", f"{e}")
                finally:
                    cursor.close()
                    conn.close()
        else:
            messagebox.showinfo("","You are not eligible for a loan based on our criteria.")
    else:
        messagebox.showwarning("Warning","Invalid account number.")

def open_fd_account(account_number, fd_amount):
    """ Open a new Fixed Deposit account """
    if check_account_exists(account_number):
        if check_sufficient_balance(account_number, fd_amount):
            conn = connect_to_db()
            if conn is not None:
                cursor = conn.cursor()
                fd_start_date = datetime.date.today()
                fd_end_date = fd_start_date + datetime.timedelta(days=365)  # Assuming a 1-year term for the FD
                try:
                    # Deduct the FD amount from the main account balance
                    cursor.execute("""
                        UPDATE AccountHolders
                        SET Balance = Balance - %s
                        WHERE AccountNumber = %s
                    """, (fd_amount, account_number))
                    # Insert the FD record
                    cursor.execute("""
                        INSERT INTO FixedDeposits (AccountNumber, FDAmount, StartDate, EndDate)
                        VALUES (%s, %s, %s, %s)
                    """, (account_number, fd_amount, fd_start_date, fd_end_date))
                    conn.commit()
                    messagebox.showinfo("",f"Fixed Deposit opened successfully. Amount: ${fd_amount}, Maturity Date: {fd_end_date}")
                    log_transaction(account_number, 'open_fd', fd_amount, 'branch')
                except mysql.connector.Error as e:
                    messagebox.showerror("Error", f"{e}")
                finally:
                    cursor.close()
                    conn.close()
        else:
            messagebox.showwarning("Warning","Insufficient funds to open FD.")
    else:
        messagebox.showwarning("Warning","Invalid account number.")

def delete_account(account_number):
    conn = connect_to_db()
    if conn is not None:
        cursor = conn.cursor()
        try:
            # Start transaction
            conn.start_transaction()

            # Delete related entries from FixedDeposits
            cursor.execute("DELETE FROM FixedDeposits WHERE AccountNumber = %s", (account_number,))

            # Delete related entries from other tables
            cursor.execute("DELETE FROM OnlineBankingCredentials WHERE AccountNumber = %s", (account_number,))
            cursor.execute("DELETE FROM Cards WHERE AccountNumber = %s", (account_number,))
            cursor.execute("DELETE FROM ChequeBooks WHERE AccountNumber = %s", (account_number,))
            cursor.execute("DELETE FROM Transactions WHERE AccountNumber = %s", (account_number,))
            cursor.execute("DELETE FROM Loans WHERE AccountNumber = %s", (account_number,))

            # Finally, delete the account holder record
            cursor.execute("DELETE FROM AccountHolders WHERE AccountNumber = %s", (account_number,))
            
            # Commit all changes
            conn.commit()
            messagebox.showinfo("","Account and all related data deleted successfully.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error",f"Failed to delete account: {e}")
            conn.rollback()  # Roll back the transaction on error
        finally:
            cursor.close()
            conn.close()
    else:
        messagebox.showwarning("Warning","Failed to connect to the database.")

def terms_and_conditions():
    """ Display the terms and conditions for different types of accounts """
    terms = {
        'savings': "Savings Account: \n- No minimum balance requirement.\n- Interest rate of 4% per annum.",
        'current': "Current Account: \n- Minimum balance requirement of $500.\n- No interest is provided on the balance."
    }
    messagebox.showinfo("","Terms and Conditions:")
    for account_type, details in terms.items():
        print(details)

def pay_loan(account_number):
    """ Pay towards an outstanding loan """
    root = tk.Toplevel()
    root.title("Outstanding Loans:")    
    if check_account_exists(account_number):
        conn = connect_to_db()
        if conn is not None:
            cursor = conn.cursor()
            # Fetch loans that have an outstanding amount greater than zero
            cursor.execute("SELECT LoanID, LoanAmount FROM Loans WHERE AccountNumber = %s AND LoanAmount > 0", (account_number,))
            loans = cursor.fetchall()
            if loans:
                columns = ('id',  'amount')
                tree = ttk.Treeview(root, columns=columns, show='headings')

                # Define the column headings
                tree.heading('id', text='Loan ID')              
                tree.heading('amount', text='Amount')              
                tree.column('id', anchor='center')                 
                tree.column('amount', anchor='center')                
                # Add data to the treeview
                for loan in loans:
                    tree.insert('', tk.END, values=f"{loan[0]} ${loan[1]}")

                tree.pack(expand=True, fill='both')                
                
                #loan_id = int(input("Enter the Loan ID you want to pay towards: "))
                #payment = Decimal(input("Enter the payment amount: "))  # Convert input directly to Decimal
                loan_id = simpledialog.askinteger("Loan ID", "Enter the Loan ID you want to pay towards:")
                payment = simpledialog.askstring("Payment Amount", "Enter the payment amount:")
                payment = Decimal(payment)

                # Fetch the specific loan to confirm it's valid and get the current amount
                cursor.execute("SELECT LoanAmount FROM Loans WHERE LoanID = %s", (loan_id,))
                loan_amount = cursor.fetchone()
                if loan_amount:
                    if payment > 0 and payment <= loan_amount[0]:
                        new_balance = loan_amount[0] - payment  # Both operands are now Decimal
                        # Update the loan with the new balance
                        cursor.execute("UPDATE Loans SET LoanAmount = %s WHERE LoanID = %s", (new_balance, loan_id))
                        conn.commit()
                        messagebox.showinfo("",f"Payment of ${payment} applied to Loan ID {loan_id}. Remaining balance: ${new_balance}.")
                        log_transaction(account_number, 'loan_payment', payment, 'online')
                    else:
                        messagebox.showwarning("Warning","Invalid payment amount. It must be positive and no greater than the loan balance.")
                else:
                    messagebox.showwarning("Warning","Invalid Loan ID.")
            else:
                messagebox.showinfo("","No outstanding loans found.")
            cursor.close()
            conn.close()
    else:
        messagebox.showwarning("Warning","Invalid account number.")
    root.destroy()

def quit_program():
    """ Cleanly exit the program """
    messagebox.showinfo("","Thank you for using VITBank services. Goodbye!")
    exit()

def log_transaction(account_number, transaction_type, amount, method):
    conn = connect_to_db()
    if conn is not None:
        cursor = conn.cursor()
        try:
            transaction_date = datetime.date.today()
            cursor.execute("""
                INSERT INTO Transactions (AccountNumber, TransactionType, Amount, TransactionDate, Method)
                VALUES (%s, %s, %s, %s, %s)
            """, (account_number, transaction_type, amount, transaction_date, method))
            conn.commit()
        except mysql.connector.Error as e:
            messagebox.showerror("Error",f"Error logging transaction: {e}")
        finally:
            cursor.close()
            conn.close()

# Assuming the functions like open_account, get_credentials, etc., are already defined

def open_account_form():
    # Create a new window for the account opening form
    form_window = tk.Toplevel()
    form_window.title("Open Account")

    # Add form fields
    aadhaar_var = tk.StringVar()
    pan_var = tk.StringVar()
    dob_var = tk.StringVar()
    photo_var = tk.StringVar()
    sign_var = tk.StringVar()
    mobile_var = tk.StringVar()
    email_var = tk.StringVar()
    address_var = tk.StringVar()
    account_type_var = tk.StringVar()

    tk.Label(form_window, text="Enter Aadhaar Number (12 digits):").pack()
    tk.Entry(form_window, textvariable=aadhaar_var).pack()

    tk.Label(form_window, text="Enter PAN Number (10 characters):").pack()
    tk.Entry(form_window, textvariable=pan_var).pack()

    tk.Label(form_window, text="Enter Date of Birth (YYYY-MM-DD):").pack()
    tk.Entry(form_window, textvariable=dob_var).pack()

    tk.Label(form_window, text="Enter file name for photo:").pack()
    tk.Entry(form_window, textvariable=photo_var).pack()

    tk.Label(form_window, text="Enter file name for signature:").pack()
    tk.Entry(form_window, textvariable=sign_var).pack()

    tk.Label(form_window, text="Enter Mobile Number (10 digits):").pack()
    tk.Entry(form_window, textvariable=mobile_var).pack()

    tk.Label(form_window, text="Enter Email Address:").pack()
    tk.Entry(form_window, textvariable=email_var).pack()

    tk.Label(form_window, text="Enter Address:").pack()
    tk.Entry(form_window, textvariable=address_var).pack()

    tk.Label(form_window, text="Enter Account Type (savings/current):").pack()
    tk.Entry(form_window, textvariable=account_type_var).pack()

    # Submit button
    tk.Button(form_window, text="Submit", command=lambda: open_account(
        aadhaar_var.get(), pan_var.get(), dob_var.get(), photo_var.get(),
        sign_var.get(), mobile_var.get(), email_var.get(), address_var.get(),
        account_type_var.get())).pack(pady=15)
    
def get_credentials_gui():
    account_number = simpledialog.askstring("Get Online Banking Credentials", "Enter your account number:")
    if account_number:
        get_credentials(account_number)

def update_password_gui():
    account_number = simpledialog.askstring("Change Password for Online Banking", "Enter your account number:")
    if account_number:
        update_password(account_number)

def request_debit_card_gui():
    account_number = simpledialog.askstring("Request Debit Card", "Enter your account number:")
    if account_number:
        request_debit_card(account_number)

def request_credit_card_gui():
    account_number = simpledialog.askstring("Request Credit Card", "Enter your account number:")
    if account_number:
        request_credit_card(account_number)

def request_cheque_book_gui():
    account_number = simpledialog.askstring("Request Cheque Book", "Enter your account number:")
    if account_number:
        request_cheque_book(account_number)

def deposit_money_gui():
    account_number = simpledialog.askstring("Deposit Money", "Enter your account number:")
    if account_number:
        amount = simpledialog.askfloat("Deposit Money", "Enter the amount to deposit:")
        if amount is not None:
            deposit_money(account_number, amount)

def interactive_withdraw_money_gui():
    account_number = simpledialog.askstring("Withdraw Money", "Enter your account number:")
    if account_number:
        interactive_withdraw_money(account_number)
def view_transactions_gui():
    account_number = simpledialog.askstring("View Transactions", "Enter your account number:")
    if account_number:
        view_transactions(account_number)

def check_balance_gui():
    account_number = simpledialog.askstring("Check Balance", "Enter your account number:")
    if account_number:
        check_balance(account_number)

def request_loan_gui():
    account_number = simpledialog.askstring("Request Loan", "Enter your account number:")
    if account_number:
        loan_amount = simpledialog.askfloat("Request Loan", "Enter the loan amount:")
        if loan_amount is not None:
            request_loan(account_number, loan_amount)

def open_fd_account_gui():
    account_number = simpledialog.askstring("Open FD Account", "Enter your account number:")
    if account_number:
        fd_amount = simpledialog.askfloat("Open FD Account", "Enter FD amount:")
        if fd_amount is not None:
            open_fd_account(account_number, fd_amount)

def terms_and_conditions_gui():
    terms =  "Savings Account:\n  - No minimum balance requirement.\n  - Interest rate of 4% per annum. \n\n Current Account: \n  - Minimum balance requirement of $500.\n  - No interest is provided on the balance.";
    #messagebox.showinfo("","Terms and Conditions:")
    messagebox.showinfo("Terms and Conditions", terms)

def pay_loan_gui():
    account_number = simpledialog.askstring("Pay Loan", "Enter your account number:")
    if account_number:
        pay_loan(account_number)

def delete_account_gui():
    account_number = simpledialog.askstring("Delete Account", "Enter your account number:")
    if account_number:
        delete_account(account_number)

def main_menu_gui():
    window = tk.Tk()
    window.title("VITBank Main Menu")
    window.geometry("250x600")

    # Create buttons for each menu option
    tk.Button(window, text="1. Open Account", command=open_account_form).pack(fill='x', pady=5, padx=10)
    # ... Add other buttons for each option ...
    tk.Button(window, text="2. Get Online Banking Credentials", command=get_credentials_gui).pack(fill='x', pady=5, padx=10)
    tk.Button(window, text="3. Change Password for Online Banking", command=update_password_gui).pack(fill='x', pady=5, padx=10)
    tk.Button(window, text="4. Request Debit Card", command=request_debit_card_gui).pack(fill='x', pady=5, padx=10)
    tk.Button(window, text="5. Request Credit Card", command=request_credit_card_gui).pack(fill='x', pady=5, padx=10)
    tk.Button(window, text="6. Request Cheque Book", command=request_cheque_book_gui).pack(fill='x', pady=5, padx=10)
    tk.Button(window, text="7. Deposit Money", command=deposit_money_gui).pack(fill='x', pady=5, padx=10)
    tk.Button(window, text="8. Withdraw Money", command=interactive_withdraw_money_gui).pack(fill='x', pady=5, padx=10)
    tk.Button(window, text="9. View Transactions", command=view_transactions_gui).pack(fill='x', pady=5, padx=10)
    tk.Button(window, text="10. Check Balance", command=check_balance_gui).pack(fill='x', pady=5, padx=10)
    tk.Button(window, text="11. Request Loan", command=request_loan_gui).pack(fill='x', pady=5, padx=10)
    tk.Button(window, text="12. Open FD Account", command=open_fd_account_gui).pack(fill='x', pady=5, padx=10)
    tk.Button(window, text="13. Terms and Conditions", command=terms_and_conditions_gui).pack(fill='x', pady=5, padx=10)
    tk.Button(window, text="14. Pay Loan", command=pay_loan_gui).pack(fill='x', pady=5, padx=10)
    tk.Button(window, text="15. Delete Account", command=delete_account_gui).pack(fill='x', pady=5, padx=10)
    tk.Button(window, text="16. Quit", command=quit_program).pack(fill='x', pady=5, padx=10)
   
    window.mainloop()

if __name__ == "__main__":
    main_menu_gui()
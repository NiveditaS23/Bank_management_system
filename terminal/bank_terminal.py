# Write me a python code to create a bank account management system using python and MySQL connectivity from python I want the following functions 
# 1 open account (after opening account display the account number to the user)
# 2 get credential for online banking (while getting the credentials we need to check if the account number is valid or not also the credials are unique for all)
# 3 change password for online banking (while changing the password we need to check if the account number is valid or not)
# 4 request for debit card (while requesting for atm card we need to check if the account number is valid or not and also display the debit card number to the user)
# 5 request for credit card (while requesting for credit card we need to check if the account number is valid or not and also display the credit card number to the user)
# 6 request for cheque book (while requesting for cheque book we need to check if the account number is valid or not and also display the cheque book number to the user)
# 7 deposit (while depositing the amount we need to check if the account number is valid or not)
# 8 withdraw (while withdrawing the amount we need to check if the account number is valid or not and also check if the user has enough balance or not and we need to prompt the user if he wants to witdraw themoney using debit card,credit card , cheque or by visiting the physical bank branch if the user selects to witdraw from debit card,credit card,cheque but he is not assigned with the desired requirements then ask him if he wanted the desired accessory if he answers yes then redirect him to the request for debit card,credit card,cheque book respectively else return him to main menu)
# 9 check for previous transactions (while checking for previous transactions we need to check if the account number is valid or not)
# 10 balance check (while checking for balance we need to check if the account number is valid or not)
# 11 request for loan (while giving loan we need to check if the account number is valid or not and also check if the user is eligible for the loan or not (think eligibility criteria from your end))
# 12 open a FD account (while opening the FD account we need to check if the account number is valid or not)
# 13 terms and conditions (savings account can have a 0 balance but current account should have a minimum balance of 500)
# 14 delete account (while deleting the account we need to check if the account number is valid or not)
# 15 quit from the program 

# MINIMUM BALANCE SHOULD BE 500
# Let the name of the bank be VITBank and all the details should be fetched and send to MySQL using python MySQL connectivity.

# to make a new account we need the following:-
# 1 aadhaar card (aadhaar number should contain only numbers and should be of 12 digits)
# 2 pan card (pan number can be a combination of both chaarcters and numbers and its length should be of 10 )
# 3 date of birth (date of birth should be in the format of YYYY-MM-DD)
# 4 photo (for photo just make them enter the name of the file for photo)
# 5 sign (for sign just make them enter the name of the file for sign)
# 6 mobile number (mobile number should contain only number and should be of 10 digits)
# 7 email address
# 8 address

# on opening the account show the account number to the user (ACCOUNT NUMBER SHOULD BE OF 10 RANDOM DIGITS)
# ACCOUNT NUMBER IS UNIQUE FOR EVERY USER

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
            # print("Connected to MySQL database")
            pass
        return conn
    except mysql.connector.Error as e:
        print(f"Error: {e}")
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
            print(f"Account successfully created. Your account number is {account_number}.")
        except mysql.connector.Error as e:
            print(f"Error: {e}")
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
        password = input("Please enter your desired password: ")  # In real applications, ensure this input is handled securely
        conn = connect_to_db()
        if conn is not None:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO OnlineBankingCredentials (AccountNumber, Username, Password)
                    VALUES (%s, %s, %s)
                """, (account_number, username, password))
                conn.commit()
                print(f"Credentials created successfully. Your username is {username}.")
            except mysql.connector.Error as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                conn.close()
    else:
        print("Invalid account number.")

def update_password(account_number):
    """ Change the password for online banking """
    if check_account_exists(account_number):
        conn = connect_to_db()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("SELECT Username FROM OnlineBankingCredentials WHERE AccountNumber = %s", (account_number,))
            if cursor.fetchone() is not None:  # Check if credentials exist
                new_password = input("Please enter your new password: ")  # In real applications, ensure this input is handled securely
                try:
                    cursor.execute("""
                        UPDATE OnlineBankingCredentials
                        SET Password = %s
                        WHERE AccountNumber = %s
                    """, (new_password, account_number))
                    conn.commit()
                    print("Password updated successfully.")
                except mysql.connector.Error as e:
                    print(f"Error: {e}")
                finally:
                    cursor.close()
                    conn.close()
            else:
                print("No online banking credentials found for this account.")
    else:
        print("Invalid account number.")

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
                print(f"Debit card successfully issued. Your card number is {card_number}.")
            except mysql.connector.Error as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                conn.close()
    else:
        print("Invalid account number.")

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
                print(f"Credit card successfully issued. Your card number is {card_number}.")
            except mysql.connector.Error as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                conn.close()
    else:
        print("Invalid account number.")

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
                print(f"Cheque book successfully issued. Your cheque book number is {cheque_book_number}.")
            except mysql.connector.Error as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                conn.close()
    else:
        print("Invalid account number.")

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
                    print(f"Successfully deposited ${amount} to account {account_number}.")
                    log_transaction(account_number, 'deposit', amount, 'branch')
                except mysql.connector.Error as e:
                    print(f"Error: {e}")
                finally:
                    cursor.close()
                    conn.close()
        else:
            print("The deposit amount must be positive.")
    else:
        print("Invalid account number.")

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

import mysql.connector

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
            print(f"Error: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to connect to the database.")
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
            print(f"Error checking method: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to connect to the database.")
        return False


def interactive_withdraw_money(account_number):
    """ Interactive function to process withdrawals using different methods """
    print("Select withdrawal method:")
    print("1. Debit Card\n2. Credit Card\n3. Cheque Book\n4. Physical Branch")
    method_choice = int(input("Enter your choice (1-4): "))
    methods = {1: 'debit card', 2: 'credit card', 3: 'cheque', 4: 'branch'}
    method = methods.get(method_choice, 'branch')  # Default to branch if invalid choice

    if method in ['debit card', 'credit card', 'cheque'] and not has_method(account_number, method):
        print(f"You do not have a valid {method}.")
        issue_new = input(f"Do you want to issue a new {method}? (yes/no): ")
        if issue_new.lower() == 'yes':
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
            print("Withdrawal cancelled.")
            return

    amount = float(input("Enter the amount to withdraw: "))
    if process_withdrawal(account_number, amount, method):
        print(f"{amount} has been successfully withdrawn from your account via {method}.")
    else:
        print("Withdrawal failed.")

def process_withdrawal(account_number, amount, method):
    """ Update the database to reflect the withdrawal """
    conn = connect_to_db()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE AccountHolders SET Balance = Balance - %s WHERE AccountNumber = %s AND Balance >= %s", (amount, account_number, amount))
            if cursor.rowcount == 0:
                print("Insufficient funds or account not found.")
                return False
            # Log the transaction
            cursor.execute("INSERT INTO Transactions (AccountNumber, TransactionType, Amount, TransactionDate, Method) VALUES (%s, 'withdraw', %s, CURDATE(), %s)", (account_number, amount, method))
            conn.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Error during withdrawal: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to connect to the database.")
        return False

def view_transactions(account_number):
    """ Display the transaction history for an account """
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
                    print("Transaction History:")
                    for transaction in transactions:
                        print(f"ID: {transaction[0]}, Type: {transaction[1]}, Amount: ${transaction[2]}, Date: {transaction[3]}, Method: {transaction[4]}")
                else:
                    print("No transactions found.")
            except mysql.connector.Error as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                conn.close()
    else:
        print("Invalid account number.")

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
                    print(f"Current balance: ${balance[0]}")
                else:
                    print("Account not found.")
            except mysql.connector.Error as e:
                print(f"Error: {e}")
            finally:
                cursor.close()
                conn.close()
    else:
        print("Invalid account number.")

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
                    print(f"Loan successfully issued. Loan amount: ${loan_amount}.")
                    log_transaction(account_number, 'loan_granted', loan_amount, 'branch')
                except mysql.connector.Error as e:
                    print(f"Error: {e}")
                finally:
                    cursor.close()
                    conn.close()
        else:
            print("You are not eligible for a loan based on our criteria.")
    else:
        print("Invalid account number.")

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
                    print(f"Fixed Deposit opened successfully. Amount: ${fd_amount}, Maturity Date: {fd_end_date}")
                    log_transaction(account_number, 'open_fd', fd_amount, 'branch')
                except mysql.connector.Error as e:
                    print(f"Error: {e}")
                finally:
                    cursor.close()
                    conn.close()
        else:
            print("Insufficient funds to open FD.")
    else:
        print("Invalid account number.")

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
            print("Account and all related data deleted successfully.")
        except mysql.connector.Error as e:
            print(f"Failed to delete account: {e}")
            conn.rollback()  # Roll back the transaction on error
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

def terms_and_conditions():
    """ Display the terms and conditions for different types of accounts """
    terms = {
        'savings': "Savings Account: \n- No minimum balance requirement.\n- Interest rate of 4% per annum.",
        'current': "Current Account: \n- Minimum balance requirement of $500.\n- No interest is provided on the balance."
    }
    print("Terms and Conditions:")
    for account_type, details in terms.items():
        print(details)

def pay_loan(account_number):
    """ Pay towards an outstanding loan """
    if check_account_exists(account_number):
        conn = connect_to_db()
        if conn is not None:
            cursor = conn.cursor()
            # Fetch loans that have an outstanding amount greater than zero
            cursor.execute("SELECT LoanID, LoanAmount FROM Loans WHERE AccountNumber = %s AND LoanAmount > 0", (account_number,))
            loans = cursor.fetchall()
            if loans:
                print("Outstanding Loans:")
                for loan in loans:
                    print(f"Loan ID: {loan[0]}, Amount: ${loan[1]}")
                
                loan_id = int(input("Enter the Loan ID you want to pay towards: "))
                payment = Decimal(input("Enter the payment amount: "))  # Convert input directly to Decimal

                # Fetch the specific loan to confirm it's valid and get the current amount
                cursor.execute("SELECT LoanAmount FROM Loans WHERE LoanID = %s", (loan_id,))
                loan_amount = cursor.fetchone()
                if loan_amount:
                    if payment > 0 and payment <= loan_amount[0]:
                        new_balance = loan_amount[0] - payment  # Both operands are now Decimal
                        # Update the loan with the new balance
                        cursor.execute("UPDATE Loans SET LoanAmount = %s WHERE LoanID = %s", (new_balance, loan_id))
                        conn.commit()
                        print(f"Payment of ${payment} applied to Loan ID {loan_id}. Remaining balance: ${new_balance}.")
                        log_transaction(account_number, 'loan_payment', payment, 'online')
                    else:
                        print("Invalid payment amount. It must be positive and no greater than the loan balance.")
                else:
                    print("Invalid Loan ID.")
            else:
                print("No outstanding loans found.")
            cursor.close()
            conn.close()
    else:
        print("Invalid account number.")

def quit_program():
    """ Cleanly exit the program """
    print("Thank you for using VITBank services. Goodbye!")
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
            print(f"Error logging transaction: {e}")
        finally:
            cursor.close()
            conn.close()

def main_menu():
    """ Main menu function to navigate through different functionalities of the bank system """
    while True:
        print("\nWelcome to VITBank Main Menu")
        print("1. Open Account")
        print("2. Get Online Banking Credentials")
        print("3. Change Password for Online Banking")
        print("4. Request Debit Card")
        print("5. Request Credit Card")
        print("6. Request Cheque Book")
        print("7. Deposit Money")
        print("8. Withdraw Money")
        print("9. Check Transaction History")
        print("10. Check Balance")
        print("11. Request Loan")
        print("12. Open FD Account")
        print("13. Terms and Conditions")
        print("14. Pay Loan")
        print("15. Delete Account")
        print("16. Quit")

        choice = input("Enter your choice (1-16): ")
        if choice == '1':
            aadhaar = input("Enter Aadhaar Number (12 digits): ")
            pan = input("Enter PAN Number (10 characters): ")
            dob = input("Enter Date of Birth (YYYY-MM-DD): ")
            photo = input("Enter file name for photo: ")
            sign = input("Enter file name for signature: ")
            mobile = input("Enter Mobile Number (10 digits): ")
            email = input("Enter Email Address: ")
            address = input("Enter Address: ")
            account_type = input("Enter Account Type (savings/current): ")
            open_account(aadhaar, pan, dob, photo, sign, mobile, email, address, account_type)
        elif choice == '2':
            account_number = input("Enter your account number: ")
            get_credentials(account_number)
        elif choice == '3':
            account_number = input("Enter your account number: ")
            update_password(account_number)
        elif choice == '4':
            account_number = input("Enter your account number: ")
            request_debit_card(account_number)
        elif choice == '5':
            account_number = input("Enter your account number: ")
            request_credit_card(account_number)
        elif choice == '6':
            account_number = input("Enter your account number: ")
            request_cheque_book(account_number)
        elif choice == '7':
            account_number = input("Enter your account number: ")
            amount = float(input("Enter the amount to deposit: "))
            deposit_money(account_number, amount)
        elif choice == '8':
            account_number = input("Enter your account number: ")
            interactive_withdraw_money(account_number)
        elif choice == '9':
            account_number = input("Enter your account number: ")
            view_transactions(account_number)
        elif choice == '10':
            account_number = input("Enter your account number: ")
            check_balance(account_number)
        elif choice == '11':
            account_number = input("Enter your account number: ")
            loan_amount = float(input("Enter the loan amount: "))
            request_loan(account_number, loan_amount)
        elif choice == '12':
            account_number = input("Enter your account number: ")
            fd_amount = float(input("Enter FD amount: "))
            open_fd_account(account_number, fd_amount)
        elif choice == '13':
            terms_and_conditions()
        elif choice == '14':
            account_number = input("Enter your account number: ")
            pay_loan(account_number)
        elif choice == '15':
            account_number = input("Enter your account number: ")
            delete_account(account_number)
        elif choice == '16':
            quit_program()
            break
        else:
            print("Invalid choice. Please try again.")

main_menu()
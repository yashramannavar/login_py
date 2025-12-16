import tkinter as tk
from tkinter import messagebox

# --- Configuration ---
# The name of the file where credentials will be stored.
CREDENTIALS_FILE = "user_credentials.txt" 
# File format: username|password\n

# --- Core Logic Functions (File Handling) ---

def create_credentials_file():
    """Ensures the credentials file exists."""
    try:
        # Open in 'a' (append) mode. If the file doesn't exist, it is created.
        with open(CREDENTIALS_FILE, 'a') as f:
            pass 
    except Exception as e:
        messagebox.showerror("File Error", f"Could not initialize credentials file: {e}")

def load_credentials():
    """Loads all credentials from the file into a dictionary for quick lookup."""
    credentials = {}
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 2:
                    username, password = parts
                    credentials[username] = password
        return credentials
    except FileNotFoundError:
        # If the file doesn't exist, return an empty dictionary
        return {}
    except Exception as e:
        messagebox.showerror("File Error", f"An error occurred reading credentials: {e}")
        return {}

def check_login(username, password):
    """
    Checks the provided credentials against the stored data.
    Called when the user clicks 'Login'.
    """
    if not username or not password:
        messagebox.showwarning("Input Error", "Username and Password cannot be empty.")
        return

    credentials = load_credentials()
    
    if username in credentials and credentials[username] == password:
        messagebox.showinfo("Login Success", "You have successfully logged in!")
        # On success, show the personalized success screen
        show_success_screen(username) 
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

def create_account(username, password):
    """
    Appends a new user to the credentials file if the username is unique.
    Called when the user clicks 'Create Account' on the signup screen.
    """
    if not username or not password:
        messagebox.showwarning("Input Error", "Username and Password cannot be empty.")
        return

    credentials = load_credentials()
    
    if username in credentials:
        messagebox.showerror("Creation Failed", "This username already exists. Please choose another one.")
    else:
        try:
            # Append the new user to the file in the required format
            with open(CREDENTIALS_FILE, 'a') as f:
                f.write(f"{username}|{password}\n")
            
            messagebox.showinfo("Account Created", "Account created successfully! Please log in now.")
            # Redirect to the login screen as requested
            show_login_screen() 
            
        except Exception as e:
            messagebox.showerror("File Error", f"Could not save account details: {e}")

# --- GUI Management Functions ---

def destroy_current_frame():
    """Clears all content from the main window before drawing a new screen."""
    for widget in root.winfo_children():
        widget.destroy()

def show_main_menu():
    """
    The initial screen: Shows 'Login' or 'Create Account' buttons.
    
    """
    destroy_current_frame()

    main_frame = tk.Frame(root)
    main_frame.pack(padx=30, pady=50)
    
    tk.Label(main_frame, text="Simple Login System", font=('Arial', 18, 'bold')).pack(pady=20)
    
    # Login Option
    tk.Button(main_frame, text="Login", command=show_login_screen, width=20, height=2, font=('Arial', 12)).pack(pady=10)
    
    # Create Account Option (Signup)
    tk.Button(main_frame, text="Create Account", command=show_create_account_screen, width=20, height=2, font=('Arial', 12)).pack(pady=10)


def show_login_screen():
    """
    The Login screen: Two entry fields for credentials and a 'Login' button.
    
    """
    destroy_current_frame()
    
    login_frame = tk.Frame(root)
    login_frame.pack(padx=20, pady=20)
    
    tk.Label(login_frame, text="--- User Login ---", font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
    
    # Username Field
    tk.Label(login_frame, text="Username:").grid(row=1, column=0, sticky='w', pady=5)
    username_entry = tk.Entry(login_frame)
    username_entry.grid(row=1, column=1, pady=5, padx=10)
    
    # Password Field (with hiding characters)
    tk.Label(login_frame, text="Password:").grid(row=2, column=0, sticky='w', pady=5)
    password_entry = tk.Entry(login_frame, show='*') 
    password_entry.grid(row=2, column=1, pady=5, padx=10)
    
    # Login Button: Calls check_login with the current entry values
    tk.Button(login_frame, text="Login", 
              command=lambda: check_login(username_entry.get(), password_entry.get()),
              width=15, bg='lightblue').grid(row=3, column=0, columnspan=2, pady=15)
    
    # Back Button
    tk.Button(login_frame, text="Back to Main", command=show_main_menu).grid(row=4, column=0, columnspan=2)


def show_create_account_screen():
    """
    The Signup screen: Two entry fields for new credentials and a 'Create Account' button.
    
    """
    destroy_current_frame()

    create_frame = tk.Frame(root)
    create_frame.pack(padx=20, pady=20)
    
    tk.Label(create_frame, text="--- Create Account ---", font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
    
    # New Username Field
    tk.Label(create_frame, text="New Username:").grid(row=1, column=0, sticky='w', pady=5)
    new_username_entry = tk.Entry(create_frame)
    new_username_entry.grid(row=1, column=1, pady=5, padx=10)
    
    # New Password Field
    tk.Label(create_frame, text="New Password:").grid(row=2, column=0, sticky='w', pady=5)
    new_password_entry = tk.Entry(create_frame, show='*')
    new_password_entry.grid(row=2, column=1, pady=5, padx=10)
    
    # Create Button: Calls create_account with the current entry values
    tk.Button(create_frame, text="Create Account", 
              command=lambda: create_account(new_username_entry.get(), new_password_entry.get()),
              width=15, bg='lightgreen').grid(row=3, column=0, columnspan=2, pady=15)
              
    # Back Button
    tk.Button(create_frame, text="Back to Main", command=show_main_menu).grid(row=4, column=0, columnspan=2)

def show_success_screen(username):
    """Displays a simple welcome/success message after a successful login."""
    destroy_current_frame()
    
    success_frame = tk.Frame(root)
    success_frame.pack(padx=20, pady=20)
    
    tk.Label(success_frame, text="Login Successful!", font=('Arial', 16, 'bold'), fg='green').pack(pady=10)
    tk.Label(success_frame, text=f"Welcome, {username}!", font=('Arial', 12)).pack(pady=5)
    
    tk.Button(success_frame, text="Logout", command=show_main_menu).pack(pady=20)


# --- Application Entry Point ---
if __name__ == "__main__":
    # 1. Initialize the main window
    root = tk.Tk()
    root.title("Simple GUI Login")
    root.geometry("400x350") # Set a fixed size
    
    # 2. Ensure the credentials file exists
    create_credentials_file()
    
    # 3. Start the application on the main menu
    show_main_menu()
    
    # 4. Run the Tkinter event loop
    root.mainloop()
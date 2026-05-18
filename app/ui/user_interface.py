from tkinter import *
from tkinter import ttk
from app.db.database import Database

class Application():
    def __init__(self):
        self.root = Tk()
        self.root.title("Wallet App")
        self.current_frame = None
        self.db = Database()
        self.current_user_id = None
        self.current_username = None

    def show_frame(self, frame_class):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.root.config(menu="")
        self.current_frame = frame_class(self.root, self)
        self.current_frame.pack(fill="both",expand=True)  
    
    def set_menu_at_mainPage(self):
        menu = Menu(self.root)
        main_menu = Menu(menu, tearoff=0)
        main_menu.add_command(label="New entry",command= lambda: self.show_frame(NewEntry))
        main_menu.add_command(label="Inspect existing entries")
        main_menu.add_command(label="Entries statistics")
        main_menu.add_command(label="Quit",command=self.root.destroy)
        menu.add_cascade(label="Menu",menu=main_menu)
        self.root.config(menu=menu)

    def run(self):
        self.show_frame(WelcomeFrame)
        self.root.mainloop()


class WelcomeFrame(Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        

        welcome_label = Label(self, text="Welcome to Wallet-App!\n\nSign up to create an account or sign in to access an existing one.")
        welcome_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        access_buttons_frame = Frame(self)
        access_buttons_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        sign_up_button = Button(access_buttons_frame, text="Sign up", command= lambda: self.app.show_frame(SignUpFrame))
        sign_up_button.pack(side="left", padx=5)

        sign_in_button = Button(access_buttons_frame, text="Sign in", command= lambda: self.app.show_frame(SignInFrame))
        sign_in_button.pack(side="left", padx=5)


class SignUpFrame(Frame):
    def __init__(self,parent,app):
        super().__init__(parent)
        self.app = app

        signin_title = Label(self, text="Wallet App - Sign Up", font=("Arial",10))
        signin_title.grid(row=0, column=0, columnspan=2, pady=10)

        label_username = Label(self, text= "Username")
        label_username.grid(row=1, column=0, padx=5, pady=10)

        #Κάνουμε τα entry (usernmae & password) attributes για να μπορέσουμε να πάρουμε με .get() τα values
        self.entry_username = Entry(self)
        self.entry_username.grid(row=1, column=1, padx=5, pady=10)

        label_password = Label(self, text= "Password")
        label_password.grid(row=2, column=0, padx=5, pady=5)
        
        self.entry_password = Entry(self)
        self.entry_password.grid(row=2, column=1, padx=5, pady=5)

        label_password_requirements = Label(self, text= "Use at least 2 characters (one Letter & one Number)")
        label_password_requirements.grid(row=3, column=1,padx=5, pady=2)

        self.label_status = Label(self, text="", fg='red')
        self.label_status.grid(row=5, column=0, columnspan=2, pady=5)

        control_signup_buttons_frame = Frame(self)
        control_signup_buttons_frame.grid(row=3, column=2, padx=5, pady=5)

        button_save = Button(control_signup_buttons_frame, text="Create account", command = self.create_account)
        button_save.pack(side="left", padx=5)

        button_back = Button(control_signup_buttons_frame, text="Back", command = lambda: self.app.show_frame(WelcomeFrame))
        button_back.pack(side="left", padx=5)
     
    def create_account(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if username == "" or password == "":
            self.label_status.config(text="Please fill in both fields.", fg='red')
            return

        success = self.app.db.create_user(username,password)
        if success: #Γιατί επιστρέφει bool με IntegrityError αν σκάσει στο unique username ή κάτι άλλο
            self.label_status.config(text="Account created successfully!", fg='green')
            self.app.show_frame(SignInFrame)
        else:
            self.label_status.config(text="Username already exists. Try another one.", fg='red')

class SignInFrame(Frame):
    def __init__(self,parent,app):
        super().__init__(parent)
        self.app = app
        signin_title = Label(self, text="Wallet App - Sign In", font=("Arial",10))
        signin_title.grid(row = 0, column=0, columnspan = 2, pady=5)

        self.label_signin_status = Label(self, text="", fg = 'red')
        self.label_signin_status.grid(row = 4, column=0, columnspan = 2, pady=5)

        label_username = Label(self, text= "Username")
        label_username.grid(row=1, column=0, padx=5, pady=10)

        self.entry_username = Entry(self)
        self.entry_username.grid(row=1, column=1, padx=5, pady=10)

        label_password = Label(self, text= "Password")
        label_password.grid(row=2, column=0, padx=5, pady=5)
        
        self.entry_password = Entry(self, show='*')
        self.entry_password.grid(row=2, column=1, padx=5, pady=5)    

        control_signin_buttons_frame = Frame(self)
        control_signin_buttons_frame.grid(row=3, column=3, columnspan=2, pady=10)

        button_signin = Button(control_signin_buttons_frame, text="Sign in", command=self.check_account)
        button_signin.pack(side="left",padx=5)

        button_back = Button(control_signin_buttons_frame, text="Back", command = lambda: self.app.show_frame(WelcomeFrame))
        button_back.pack(side="left",padx=5)

    def check_account(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if username == "" or password == "":
            self.label_signin_status.config(text="Please fill in both fields.", fg='red')
            return
        
        account_status = self.app.db.validate_user(username,password)
        if account_status:
            self.app.current_user_id = account_status[0]
            self.app.current_username = account_status[1]
            self.app.show_frame(MainPage)
        else:
            self.label_signin_status.config(text="Invalid username or password. Please try again.", fg='red')



class MainPage(Frame):
    def __init__(self,parent,app):
        super().__init__(parent)
        self.app = app
        self.app.root.title("Wallet App - Dashboard")
        self.app.set_menu_at_mainPage()
        
        mainframe_title = Label(self, text="Wallet App Dashboard", font=("Arial",18))
        mainframe_title.pack(pady=20)

        welcome_label = Label(self, text="You are logged in to your personal account.")
        welcome_label.pack(pady=10)

        new_entry_button = Button(self, text="New entry", command=lambda: self.app.show_frame(NewEntry))
        new_entry_button.pack(pady=5)

        inspect_button = Button(self, text="Inspect entries")
        inspect_button.pack(pady=5)        
        
        stats_button = Button(self, text="Entries statistics")
        stats_button.pack(pady=5)   
        
        logout_button = Button(self, text="Log out", command=lambda: self.app.show_frame(WelcomeFrame))
        logout_button.pack(pady=20) 

class NewEntry(Frame):
    def __init__(self,parent,app):
        super().__init__(parent)
        self.app = app
        self.app.root.title("Wallet App - New Entry")
        self.revenue_categories = ["Salary", "Bonus", "Freelance", "Business", "Gift","Refund", "Investment", "Rental Income", "Other"]
        self.expense_categories = ["Food", "Utilities", "Fuel", "Transport", "Rent", "Bills", "Shopping", "Health", "Entertainment", "Education", "Travel", "Other"]        self.recurring_var = IntVar()
        self.date_entry = None
        self.amount_entry = None
        self.category_combo= None
        self.description_entry = None
        self.entry_type = None
        self.name_entry = None
        self.status_combo = None
        self.link_entry = None

        self.form_frame = Frame(self)
        self.form_frame.pack(pady=20)

        label_entry_type = Label(self.form_frame, text= "Entry type")
        label_entry_type.grid(row=0, column=0, padx=5, pady=10)

        self.entry_type = ttk.Combobox(self.form_frame,values=["Revenue", "Expense", "Obligation", "Wishlist"], state="readonly")
        self.entry_type.grid(row=0,column=0,padx=5,pady=10)
        self.entry_type.bind("<<ComboboxSelected>>", self.handle_entry_type)

        back_button = Button(self,text='Back',command=lambda: self.app.show_frame(MainPage))
        back_button.pack(pady=5)
        #Για να επιστρέφω την κατάσταση μετά το press save button
        self.status_label = Label(self,text="",fg='red')
        self.status_label.pack(pady=10)

    def handle_entry_type(self, event):
        selected_type = self.entry_type.get()

        if selected_type == "Revenue" or selected_type == "Expense":
            self.revenue_expense_view(selected_type)

    def revenue_expense_view(self):
        
        date_label = Label(self, text="Date (dd/mm/yyyy)")
        date_label.grid(row=1,column=0,padx=5,pady=10)

        self.date_entry = Entry(self)
        self.date_entry.grid(row=1,column=1,padx=5,pady=10)

        value_label = Label(self, text="Amount")
        value_label.grid(row=2,column=0,padx=5,pady=10)

        self.amount_entry = Entry(self)
        self.amount_entry.grid(row=2,column=1,padx=5,pady=10)


new_app = Application()
new_app.run()
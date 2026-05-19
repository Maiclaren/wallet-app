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
        self.expense_categories = ["Food", "Utilities", "Fuel", "Transport", "Rent", "Bills", "Shopping", "Health", "Entertainment",
                                    "Education", "Travel", "Other"]        
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

    #Εξηγώ: Ανάλογα το entry type (Exchange ή Task) θα αλλάζει η φόρμα. Με αυτόν τον handler θα ορίζω ποιο builder form (exchange or task) θα παίζει μπάλα. 
    def handle_entry_type(self, event):
        selected_type = self.entry_type.get()
        self.clear_widgets()
        if selected_type in ["Revenue","Expense"]:
            self.build_exhange_form(selected_type) #το στήνω πιο κάτω
        elif selected_type in ["Obligation","Wishlist"]:
            self.build_exchange_form(selected_type) #το στήνω πιο κάτω

    #def για να διαγράφω τα πεδία των widgets κάτω από το entry_type (γι αυτό και βάζω ow_in_grid.grid_info()["row"]>0 εφόσον το combobox και το label 
    #του είναι στο row: 0)
    def clear_widgets(self):
        for row_in_grid in self.form_frame.grid_slaves(): #παίρνω τα παιδιά του grid
            if int(row_in_grid.grid_info()["row"]>0): #και από αυτά από το row:1 και κάτω
                row_in_grid.destroy()
        self.date_entry = None
        self.amount_entry = None
        self.category_combo= None
        self.description_entry = None
        self.name_entry = None
        self.status_combo = None
        self.link_entry = None
        self.status_label.config(text="",fg='red')

    def build_exhange_form(self,selected_type):
        
        date_label = Label(self.form_frame, text="Date (dd/mm/yyyy)")
        date_label.grid(row=1,column=0,padx=5,pady=10)

        self.date_entry = Entry(self.form_frame)
        self.date_entry.grid(row=1,column=1,padx=5,pady=10)

        amount_label = Label(self.form_frame, text="Amount")
        amount_label.grid(row=2,column=0,padx=5,pady=10)

        self.amount_entry = Entry(self.form_frame)
        self.amount_entry.grid(row=2,column=1,padx=5,pady=10)

        category_label = Label(self.form_frame, text="Category")
        category_label.grid(row=3,column=0,padx=5,pady=10)

        #categories -> αναλόγως το exhange type:
        categories = self.revenue_categories if selected_type=="Revenue" else self.expense_categories
        self.categories_combo = ttk.Combobox(self.form_frame, values=categories, state='readonly')
        self.categories_combo.grid(row=3,column=1,padx=5,pady=10)

        description_label = Label(self.form_frame,text="Description")
        description_label.grid(row=4,column=0,padx=5,pady=10)

        self.description_entry = Entry(self.form_frame)
        self.description_entry.grid(row=4,column=1,padx=5,pady=10)

        save_button = Button(self.form_frame, text='Save', command=self.save_entry)
        save_button.grid(row=5,column=0,columnspan=2,pady=10)

    def build_task_form(self,selected_type):

        name_label = Label(self.form_frame,text="Description")
        name_label.grid(row=1,column=0,padx=5,pady=10)

        self.name_entry = Entry(self.form_frame)
        self.name_entry.grid(row=1,column=1,padx=5,pady=10)

        amount_label = Label(self.form_frame, text="Amount")
        amount_label.grid(row=2,column=0,padx=5,pady=10)

        self.amount_entry = Entry(self.form_frame)
        self.amount_entry.grid(row=2,column=1,padx=5,pady=10)
        
        date_label = Label(self.form_frame, text="Date (dd/mm/yyyy)")
        date_label.grid(row=3,column=0,padx=5,pady=10)

        self.date_entry = Entry(self.form_frame)
        self.date_entry.grid(row=3,column=1,padx=5,pady=10)

        status_label = Label(self.form_frame)
        status_label.grid(row=4,column=0,padx=5,pady=10)
        
        self.status_combo = ttk.Combobox(self.form_frame, values=["Pending","Completed"], state='readonly')
        self.status_combo.grid(row=3,column=1,padx=5,pady=10)

        save_button = Button(self.form_frame, text='Save', command=self.save_entry)
        save_button.grid(row=5,column=0,columnspan=2,pady=10)

        #Αν είναι wishlist να εμφανίζει και πεδίο link - στοιχίζω και το save button ανάλογα
        if selected_type == "Wishlist":

            link_label = Label(self.form_frame, text="Link")
            link_label.grid(row=5, column=0, padx=5, pady=10)

            self.link_entry = Entry(self.form_frame)
            self.link_entry.grid(row=5, column=1, padx=5, pady=10)
            save_row = 6
        else:

            save_row = 5

        save_button = Button(self.form_frame, text="Save Entry", command=self.save_entry)
        save_button.grid(row=save_row, column=0, columnspan=2, pady=10)
    
    #Ομοίως με τις φόρμες ανά κατηγορία, φτιάχνω saves ανα περίπτωση
    def save_entry(self):
        selected_type = self.entry_type.get().strip()
        if selected_type in ["Revenue","Expense"]:
            self.save_exchange(selected_type)
        elif selected_type in ["Obligation","Wishlist"]:
            self.save_task(selected_type)

    def save_exchange(self,selected_type):
        date = self.date_entry.get().strip() if self.date_entry else ""
        amount = self.amount_entry.get().strip() if self.amount_entry else ""
        category = self.category_combo.get().strip() if self.category_combo else ""
        description = self.description_entry.get().strip() if self.description_entry else ""
        #Αν ένα από τα κύρια πεδία δεν είναι συμπληρωμένα -> αμυντικός προγραμματισμός
        if date == "" or amount == "" or category == "":
            self.status_label.config(text="Please fill in all required fileds.",fg='red')
        #Κάνω έναν επί πρόσθετο αμυντικό με casting του amount σε float με try - except
        try:
            amount = float(amount)
        except ValueError:
            self.status_label.config(text="Please use valid numbers.",fg='red')
        #Καλώ ΒΔ για δημιουργία εγγραφής - πάλι με αμυντικό για να μη σκάσει:
        try:
            self.app.db.create_exchange(
                self.app.current_user_id, #-> που το έχω από την κλάση SigninFrame στην def: check_account 
                selected_type.lower(), #ώστε όλα να είναι ίδια
                amount,
                date,
                category,
                description,             
            )
            self.status_label.config(text=f"{selected_type} saved successfully.",fg='green')
        except Exception as e:
            self.status_label.config(text=f"Error: {e} trying to save exchange",fg='red')
    
    def save_task(self,selected_type):
        name = self.name_entry.get().strip() if self.name_entry else ""
        amount = self.amount_entry.get().strip() if self.amount_entry else ""
        date = self.date_entry.get().strip() if self.date_entry else ""
        status = self.status_combo.get().strip() if self.status_combo else ""
        link = self.link_entry.get.strip() if self.link_entry else ""
        #Αν ένα από τα κύρια πεδία δεν είναι συμπληρωμένα -> αμυντικός προγραμματισμός
        if date == "" or amount == "" or name == "" or status == "":
            self.status_label.config(text="Please fill in all required fileds.",fg='red')
        #Κάνω έναν επί πρόσθετο αμυντικό με casting του amount σε float με try - except
        try:
            amount = float(amount)
        except ValueError:
            self.status_label.config(text="Please use valid numbers.",fg='red')
        #Καλώ ΒΔ για δημιουργία εγγραφής - πάλι με αμυντικό για να μη σκάσει:
        try:
            self.app.db.create_exchange(
                self.app.current_user_id, #-> που το έχω από την κλάση SigninFrame στην def: check_account 
                selected_type.lower(), #ώστε όλα να είναι ίδια
                name,
                amount,
                date,
                status,
                link                
            )
            self.status_label.config(text=f"{selected_type} saved successfully.",fg='green')
        except Exception as e:
            self.status_label.config(text=f"Error: {e} trying to save exchange",fg='red')


new_app = Application()
new_app.run()
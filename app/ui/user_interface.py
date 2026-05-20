from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
from app.db.database import Database
from datetime import datetime

#Η λογική που εφαρμόζουμε είναι ένα παράθυρο του App και μέσα σε αυτό εναλλάσσουμε ξεχωριστά object frames
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
        main_menu.add_command(label="Inspect existing entries",command=lambda: self.show_frame(InspectFrame))
        main_menu.add_command(label="Entries statistics")
        main_menu.add_command(label="Quit",command=self.root.destroy)
        menu.add_cascade(label="Menu",menu=main_menu)
        self.root.config(menu=menu)

    def run(self):
        self.show_frame(WelcomeFrame)
        self.root.mainloop()

#Το αρχικό Frame μόλις ανοίγει η εφαρμογή
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

#Το sign up Frame για δημιουργία account αν δεν υπάρχει (γίνεται store σε ξεχωριστό sqlite3 table με reference στα main tables των exchanges & tasks)
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

#Frame για log in (κάνουμε hold το id που συνδέθηκε ώστε το account που εισήλθε να βλέπει - προσθέτει - μετατρέπει μόνο τα δικά του data )
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

#Μετά το sign in Frame το MainFrame γίνεται το κεντρικό Frame επιλογής κατεύθυνσης ανά ενέργεια. Η κάθε ενέργεια είναι και αυτή με τη σειρά της
#ένα object Frame: New Entry κλπ.. 
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

        inspect_button = Button(self, text="Inspect entries", command=lambda: self.app.show_frame(InspectFrame))
        inspect_button.pack(pady=5)        
        
        stats_button = Button(self, text="Entries statistics")
        stats_button.pack(pady=5)   
        
        logout_button = Button(self, text="Log out", command=lambda: self.app.show_frame(WelcomeFrame))
        logout_button.pack(pady=20) 

#Δημιουργία νέας εγγραφής
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
            self.build_exchange_form(selected_type) #το στήνω πιο κάτω
        elif selected_type in ["Obligation","Wishlist"]:
            self.build_task_form(selected_type) #το στήνω πιο κάτω

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

    #Με αυτό χτίζω το exchange form
    def build_exchange_form(self,selected_type):
        
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

    #Με αυτό χτίζω το task form
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

        status_label = Label(self.form_frame, text="Category")
        status_label.grid(row=4,column=0,padx=5,pady=10)
        
        self.status_combo = ttk.Combobox(self.form_frame, values=["Pending","Completed"], state='readonly')
        self.status_combo.grid(row=4,column=1,padx=5,pady=10)

        #save_button = Button(self.form_frame, text='Save', command=self.save_entry)
        #save_button.grid(row=6,column=0,columnspan=2,pady=10)

        #Αν είναι wishlist να εμφανίζει και πεδίο link - στοιχίζω και το save button ανάλογα
        if selected_type == "Wishlist":
            link_label = Label(self.form_frame, text="Link")
            link_label.grid(row=5, column=0, padx=5, pady=10)

            self.link_entry = Entry(self.form_frame)
            self.link_entry.grid(row=5, column=1, padx=5, pady=10)
            save_row = 7
        else:
            save_row = 6

        save_button = Button(self.form_frame, text="Save Entry", command=self.save_entry)
        save_button.grid(row=save_row, column=0, columnspan=2, pady=10)

    #Διορθώνω το date format για σωστό σορτάρισμα μετά με pandas
    def fix_date(self, date_text):
        try:
            parsed_date = datetime.strptime(date_text, "%d/%m/%Y")
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            return None
        
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
        category = self.categories_combo.get().strip() if self.categories_combo else ""
        description = self.description_entry.get().strip() if self.description_entry else ""
        #Αν ένα από τα κύρια πεδία δεν είναι συμπληρωμένα -> αμυντικός προγραμματισμός
        if date == "" or amount == "" or category == "":
            self.status_label.config(text="Please fill in all required fileds.",fg='red')
        #Κάνω έναν επί πρόσθετο αμυντικό με casting του amount σε float με try - except
        try:
            amount = float(amount)
        except ValueError:
            self.status_label.config(text="Please use valid numbers.",fg='red')
            return
        
        fixed_date = self.fix_date(date)
        if fixed_date is None:
            self.status_label.config(text="Date must be in format dd/mm/yyyy.", fg="red")
            return
        #Καλώ ΒΔ για δημιουργία εγγραφής - πάλι με αμυντικό για να μη σκάσει:
        try:
            self.app.db.create_exchange(
                self.app.current_user_id, #-> που το έχω από την κλάση SigninFrame στην def: check_account 
                selected_type.lower(), #ώστε όλα να είναι ίδια
                amount,
                fixed_date,
                category,
                description             
            )
            self.status_label.config(text=f"{selected_type} saved successfully.",fg='green')
        except Exception as e:
            self.status_label.config(text=f"Error: {e} trying to save exchange",fg='red')
    
    def save_task(self,selected_type):
        name = self.name_entry.get().strip() if self.name_entry else ""
        amount = self.amount_entry.get().strip() if self.amount_entry else ""
        date = self.date_entry.get().strip() if self.date_entry else ""
        status = self.status_combo.get().strip() if self.status_combo else ""
        link = self.link_entry.get().strip() if self.link_entry else ""
        #Αν ένα από τα κύρια πεδία δεν είναι συμπληρωμένα -> αμυντικός προγραμματισμός
        if date == "" or amount == "" or name == "" or status == "":
            self.status_label.config(text="Please fill in all required fileds.",fg='red')
        #Κάνω έναν επί πρόσθετο αμυντικό με casting του amount σε float με try - except
        try:
            amount = float(amount)
        except ValueError:
            self.status_label.config(text="Please use valid numbers.",fg='red')
        fixed_date = self.fix_date(date)

        if fixed_date is None:
            self.status_label.config(text="Date must be in format dd/mm/yyyy.", fg="red")
            return
        #Καλώ ΒΔ για δημιουργία εγγραφής - πάλι με αμυντικό για να μη σκάσει:
        try:
            self.app.db.create_task(
                self.app.current_user_id, #-> που το έχω από την κλάση SigninFrame στην def: check_account 
                selected_type.lower(), #ώστε όλα να είναι ίδια
                name,
                amount,
                fixed_date,
                status,
                link                
            )
            self.status_label.config(text=f"{selected_type} saved successfully.",fg='green')
        except Exception as e:
            self.status_label.config(text=f"Error: {e} trying to save exchange",fg='red')
            
#Ανασκόπηση καταχωρημένων εγγραφών με view correlated του user_id που έκανε log in 
class InspectFrame(Frame):
    def __init__(self,parent,app):
        super().__init__(parent)
        self.app = app
        self.app.root.title("Wallet App - Inspect Entries")

        #Αρχικόποιώ τα dataframes τα οποία θα χτίσω μετά και θα τα σερβίρω στα export σε xlsx
        self.df_exchanges = pd.DataFrame()
        self.df_tasks = pd.DataFrame()

        title_label = Label(self, text="Inspect entries", font=("Arial", 14))
        title_label.pack(pady=10)

        #Θα φτιάξω δύο ξεχωριστά treeview (1.exchanges 2. tasks) ώστε να μη γεμίσουμε με στήλες άκυρες κατά περίπτωση
        #Για exchanges:
        exchanges_label = Label(self, text="Exchanges", font=("Arial", 12))
        exchanges_label.pack(pady=(10, 5))

        exchange_frame = Frame(self)
        exchange_frame.pack(fill="x", padx=10)

        exchange_scrollbar = Scrollbar(exchange_frame, orient=VERTICAL)
        exchange_scrollbar.pack(side=RIGHT, fill=Y)

        self.exchange_tree = ttk.Treeview(
            exchange_frame,
            columns=("id", "type", "amount", "date", "category", "description"),
            show="headings", height=8, yscrollcommand=exchange_scrollbar.set)
        self.exchange_tree.pack(side=LEFT, fill="x", expand=True)
        exchange_scrollbar.config(command=self.exchange_tree.yview)
        self.exchange_tree.heading("id", text="ID")
        self.exchange_tree.heading("type", text="Type")
        self.exchange_tree.heading("amount", text="Amount")
        self.exchange_tree.heading("date", text="Date")
        self.exchange_tree.heading("category", text="Category")
        self.exchange_tree.heading("description", text="Description")   
        #Για tasks:
        tasks_label = Label(self, text="Tasks", font=("Arial", 12))
        tasks_label.pack(pady=(15, 5))

        task_frame = Frame(self)
        task_frame.pack(fill="x", padx=10)

        task_scrollbar = Scrollbar(task_frame, orient=VERTICAL)
        task_scrollbar.pack(side=RIGHT, fill=Y)

        self.task_tree = ttk.Treeview(
            task_frame,
            columns=("id", "type", "name", "amount", "date", "status", "link"),
            show="headings",height=8, yscrollcommand=task_scrollbar.set)
        self.task_tree.pack(side=LEFT, fill="x", expand=True)

        task_scrollbar.config(command=self.task_tree.yview)

        self.task_tree.heading("id", text="ID")
        self.task_tree.heading("type", text="Type")
        self.task_tree.heading("name", text="Name")
        self.task_tree.heading("amount", text="Amount")
        self.task_tree.heading("date", text="Date")
        self.task_tree.heading("status", text="Status")
        self.task_tree.heading("link", text="Link")

        buttons_frame = Frame(self)
        buttons_frame.pack(pady=15)

        #Μια loaf_entries ουσιαστικά είναι απλά τη δίνεις με button - την έβαλα τυπικά
        refresh_button = Button(buttons_frame, text="Refresh", command=self.load_entries)
        refresh_button.pack(side=LEFT, padx=5)

        export_button = Button(buttons_frame, text="Export to Excel", command=self.export_to_excel)
        export_button.pack(side=LEFT, padx=5)

        back_button = Button(buttons_frame, text="Back", command=lambda: self.app.show_frame(MainPage))
        back_button.pack(side=LEFT, padx=5)

        self.load_entries()

    def load_entries(self):
        #Αρχικά σβήνω ότι έχει μείνει από προηγούμενο load
        for data in self.exchange_tree.get_children():
            self.exchange_tree.delete(data)
        for data in self.task_tree.get_children():
            self.task_tree.delete(data)

        #Καλώ ΒΔ να μου επιστρέψει τα rows για το self.user_id
        exchanges = self.app.db.get_user_exchanges(self.app.current_user_id)
        tasks = self.app.db.get_user_tasks(self.app.current_user_id)

        exchange_cols = ["id","user_id","exchange_type","amount","date","category","description"]
        task_cols = ["id", "user_id", "task_type", "name", "amount", "date", "status", "link"]
        self.df_exchanges = pd.DataFrame(exchanges, columns=exchange_cols)
        self.df_tasks = pd.DataFrame(tasks, columns=task_cols)

        for row_data in exchanges:
            record_id, user_id, exchange_type, amount, date, category, description = row_data
            self.exchange_tree.insert("",END,
                values=(record_id, exchange_type, amount, date, category, description))

        for row_data in tasks:
            record_id, user_id, task_type, name, amount, date, status, link = row_data
            self.task_tree.insert("",END,
                values=(record_id, task_type, name, amount, date, status, link))
            
    def export_to_excel(self):
        if self.df_exchanges.empty and self.df_tasks.empty:
            return
        #το εβαλα xlsx γιατί καμιά φορά αν ανοιγείς xls σου εμφανίζει προειδοποίηση στα 365 για παλιά χχρήση αρχείου
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return
        #Το κάνω με ExcelWriter αντί κατευθείαν με to_excel για να βάλω όλο το worksheet σε διαφορετικά spreadsheets
        with pd.ExcelWriter(file_path) as writer:
            self.df_exchanges.to_excel(writer, sheet_name="Exchanges", index=False)
            self.df_tasks.to_excel(writer, sheet_name="Tasks", index=False)

new_app = Application()
new_app.run()
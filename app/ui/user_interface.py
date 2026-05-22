from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
from app.db.database import Database
from datetime import datetime

ENTRY_TYPE_TO_DB = {"Έσοδα": "revenue","Έξοδα": "expense","Υποχρεώσεις": "obligation","Επιθυμίες": "wishlist"}
DB_TO_ENTRY_TYPE = {v: k for k, v in ENTRY_TYPE_TO_DB.items()}
STATUS_TO_DB = {"Εκκρεμεί": "pending","Ολοκληρώθηκε": "completed"}
DB_TO_STATUS = {v: k for k, v in STATUS_TO_DB.items()}

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
        main_menu.add_command(label="Νέα εγγραφή",command= lambda: self.show_frame(NewEntry))
        main_menu.add_command(label="Ανασκόπηση εγγραφών",command=lambda: self.show_frame(InspectFrame))
        main_menu.add_command(label="Στατιστικά εγγραφών")
        main_menu.add_command(label="Έξοδος",command=self.root.destroy)
        menu.add_cascade(label="Κεντρικό μενού",menu=main_menu)
        self.root.config(menu=menu)

    def run(self):
        self.show_frame(WelcomeFrame)
        self.root.mainloop()

#Το αρχικό Frame μόλις ανοίγει η εφαρμογή
class WelcomeFrame(Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        

        welcome_label = Label(self, text="Καλώς ορίσατε στο Wallet-App!\n\nΠιέστε Εγγραφή για δημιουργία λογαριασμού ή Σύνδεση για να εισέλθετε.")
        welcome_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        access_buttons_frame = Frame(self)
        access_buttons_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        sign_up_button = Button(access_buttons_frame, text="Εγγραφή", command= lambda: self.app.show_frame(SignUpFrame))
        sign_up_button.pack(side="left", padx=5)

        sign_in_button = Button(access_buttons_frame, text="Σύνδεση", command= lambda: self.app.show_frame(SignInFrame))
        sign_in_button.pack(side="left", padx=5)

#Το sign up Frame για δημιουργία account αν δεν υπάρχει (γίνεται store σε ξεχωριστό sqlite3 table με reference στα main tables των exchanges & tasks)
class SignUpFrame(Frame):
    def __init__(self,parent,app):
        super().__init__(parent)
        self.app = app

        signin_title = Label(self, text="Wallet App - Εγγραφή", font=("Arial",10))
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

        label_password_requirements = Label(self, text= "Χρησιμοποιήστε τουλάχιστον 2 χαρακτήρες (1 γράμμα & 1 νούμερο)")
        label_password_requirements.grid(row=3, column=1,padx=5, pady=2)

        self.label_status = Label(self, text="", fg='red')
        self.label_status.grid(row=5, column=0, columnspan=2, pady=5)

        control_signup_buttons_frame = Frame(self)
        control_signup_buttons_frame.grid(row=3, column=2, padx=5, pady=5)

        button_save = Button(control_signup_buttons_frame, text="Δημιουργία λογαριασμού", command = self.create_account)
        button_save.pack(side="left", padx=5)

        button_back = Button(control_signup_buttons_frame, text="Επιστροφή", command = lambda: self.app.show_frame(WelcomeFrame))
        button_back.pack(side="left", padx=5)
     
    def create_account(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if username == "" or password == "":
            self.label_status.config(text="Παρακαλώ συμπληρώστε και τα 2 πεδία.", fg='red')
            return

        success = self.app.db.create_user(username,password)
        if success: #Γιατί επιστρέφει bool με IntegrityError αν σκάσει στο unique username ή κάτι άλλο
            self.label_status.config(text="Ο λογαριασμός σας δημιουργήθηκε επιτυχώς!", fg='green')
            self.app.show_frame(SignInFrame)
        else:
            self.label_status.config(text="Το Username υπάρχει ήδη. Δοκιμάστε ξανά.", fg='red')

#Frame για log in (κάνουμε hold το id που συνδέθηκε ώστε το account που εισήλθε να βλέπει - προσθέτει - μετατρέπει μόνο τα δικά του data )
class SignInFrame(Frame):
    def __init__(self,parent,app):
        super().__init__(parent)
        self.app = app
        signin_title = Label(self, text="Wallet App - Σύνδεση", font=("Arial",10))
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

        button_signin = Button(control_signin_buttons_frame, text="Σύνδεση", command=self.check_account)
        button_signin.pack(side="left",padx=5)

        button_back = Button(control_signin_buttons_frame, text="Επιστροφή", command = lambda: self.app.show_frame(WelcomeFrame))
        button_back.pack(side="left",padx=5)

    def check_account(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if username == "" or password == "":
            self.label_signin_status.config(text="Παρακαλώ συμπληρώστε και τα 2 πεδία.", fg='red')
            return
        
        account_status = self.app.db.validate_user(username,password)
        if account_status:
            self.app.current_user_id = account_status[0]
            self.app.current_username = account_status[1]
            self.app.show_frame(MainPage)
        else:
            self.label_signin_status.config(text="Λάθος username ή password. Δοκιμάστε ξανά.", fg='red')

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

        welcome_label = Label(self, text="Έχετε συνδεθεί στον προσωπικό σας λογαριασμό.")
        welcome_label.pack(pady=10)

        new_entry_button = Button(self, text="Νέα εγγραφή", command=lambda: self.app.show_frame(NewEntry))
        new_entry_button.pack(pady=5)

        inspect_button = Button(self, text="Ανασκόπηση εγγραφών", command=lambda: self.app.show_frame(InspectFrame))
        inspect_button.pack(pady=5)        
        
        stats_button = Button(self, text="Στατιστικά εγγραφών")
        stats_button.pack(pady=5)   
        
        logout_button = Button(self, text="Έξοδος", command=lambda: self.app.show_frame(WelcomeFrame))
        logout_button.pack(pady=20) 

#Δημιουργία νέας εγγραφής
class NewEntry(Frame):
    def __init__(self,parent,app):
        super().__init__(parent)
        self.app = app
        self.app.root.title("Wallet App - New Entry")
        self.selected_entry_type = None
        self.revenue_categories = ["Μισθοδοσία", "Bonus", "Freelance", "Business", "Δώρα","Αποζημίωση", "Επενδύσεις", "Έσοδα ακινήτων", "Άλλο"]
        self.expense_categories = ["Τρόφιμα", "Λογαριασμοί ΔΕΚΟ", "Καύσιμα","Ασφάλειες", "Μεταφορικά έξοδα", "Ενοίκιο", "Ψώνια", "Υγεία", "Διασκέδαση",
                                    "Εκπαίδευση", "Ταξίδια", "Άλλο"]        
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
        label_general_text = Label(self.form_frame, text="Επιλέξτε τύπο εγγραφής", font=("Arial",10))
        label_general_text.grid(row=0,column=0,columnspan=2,pady=10)

        label_entry_type = Label(self.form_frame, text= "Τύπος εγγραφής")
        label_entry_type.grid(row=1, column=0, padx=5, pady=10)

        self.entry_type = ttk.Combobox(self.form_frame,values=["Έσοδα", "Έξοδα", "Υποχρεώσεις", "Επιθυμίες"], state="readonly")
        self.entry_type.grid(row=1,column=1,padx=5,pady=10)
        self.entry_type.bind("<<ComboboxSelected>>", self.handle_entry_type)

        back_button = Button(self,text='Επιστροφή',command=lambda: self.app.show_frame(MainPage))
        back_button.pack(pady=5)
        #Για να επιστρέφω την κατάσταση μετά το press save button
        self.status_label = Label(self,text="",fg='red')
        self.status_label.pack(pady=10)

    #Εξηγώ: Ανάλογα το entry type (Exchange ή Task) θα αλλάζει η φόρμα. Με αυτόν τον handler θα ορίζω ποιο builder form (exchange or task) θα παίζει μπάλα. 
    def handle_entry_type(self, event):
        self.selected_entry_type = self.entry_type.get().strip()
        
        self.clear_widgets()
        if self.selected_entry_type in ["Έσοδα", "Έξοδα"]:
            self.build_exchange_form(self.selected_entry_type) #το στήνω πιο κάτω
        elif self.selected_entry_type in ["Υποχρεώσεις", "Επιθυμίες"]:
            self.build_task_form(self.selected_entry_type) #το στήνω πιο κάτω

    #def για να διαγράφω τα πεδία των widgets κάτω από το entry_type (γι αυτό και βάζω ow_in_grid.grid_info()["row"]>0 εφόσον το combobox και το label 
    #του είναι στο row: 0)
    def clear_widgets(self):
        for row_in_grid in self.form_frame.grid_slaves(): #παίρνω τα παιδιά του grid
            if int(row_in_grid.grid_info()["row"])>1: #και από αυτά από το row:1 και κάτω
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
        
        date_label = Label(self.form_frame, text="Ημερομηνία (dd/mm/yyyy)")
        date_label.grid(row=2,column=0,padx=5,pady=10)

        self.date_entry = Entry(self.form_frame)
        self.date_entry.grid(row=2,column=1,padx=5,pady=10)

        amount_label = Label(self.form_frame, text="Ποσό")
        amount_label.grid(row=3,column=0,padx=5,pady=10)

        self.amount_entry = Entry(self.form_frame)
        self.amount_entry.grid(row=3,column=1,padx=5,pady=10)

        category_label = Label(self.form_frame, text="Κατηγορία")
        category_label.grid(row=4,column=0,padx=5,pady=10)

        #categories -> αναλόγως το exhange type:
        categories = self.revenue_categories if selected_type=="Έσοδα" else self.expense_categories
        self.category_combo = ttk.Combobox(self.form_frame, values=categories, state='readonly')
        self.category_combo.grid(row=4,column=1,padx=5,pady=10)

        description_label = Label(self.form_frame,text="Περιγραφή")
        description_label.grid(row=5,column=0,padx=5,pady=10)

        self.description_entry = Entry(self.form_frame)
        self.description_entry.grid(row=5,column=1,padx=5,pady=10)

        save_button = Button(self.form_frame, text='Αποθήκευση', command=self.save_entry)
        save_button.grid(row=6,column=0,columnspan=2,pady=10)

    #Με αυτό χτίζω το task form
    def build_task_form(self,selected_type):

        name_label = Label(self.form_frame,text="Περιγραφή")
        name_label.grid(row=2,column=0,padx=5,pady=10)

        self.name_entry = Entry(self.form_frame)
        self.name_entry.grid(row=2,column=1,padx=5,pady=10)

        amount_label = Label(self.form_frame, text="Ποσό")
        amount_label.grid(row=3,column=0,padx=5,pady=10)

        self.amount_entry = Entry(self.form_frame)
        self.amount_entry.grid(row=3,column=1,padx=5,pady=10)
        
        date_label = Label(self.form_frame, text="Ημερομηνία (dd/mm/yyyy)")
        date_label.grid(row=4,column=0,padx=5,pady=10)

        self.date_entry = Entry(self.form_frame)
        self.date_entry.grid(row=4,column=1,padx=5,pady=10)

        status_label = Label(self.form_frame, text="Κατάσταση")
        status_label.grid(row=5,column=0,padx=5,pady=10)
        
        self.status_combo = ttk.Combobox(self.form_frame, values=["Εκκρεμεί", "Ολοκληρώθηκε"], state='readonly')
        self.status_combo.grid(row=5,column=1,padx=5,pady=10)

        #save_button = Button(self.form_frame, text='Save', command=self.save_entry)
        #save_button.grid(row=6,column=0,columnspan=2,pady=10)

        #Αν είναι wishlist να εμφανίζει και πεδίο link - στοιχίζω και το save button ανάλογα
        if selected_type == "Επιθυμίες":
            link_label = Label(self.form_frame, text="Link")
            link_label.grid(row=6, column=0, padx=5, pady=10)

            self.link_entry = Entry(self.form_frame)
            self.link_entry.grid(row=6, column=1, padx=5, pady=10)
            save_row = 7
        else:
            save_row = 6

        save_button = Button(self.form_frame, text="Αποθήκευση εγγραφής", command=self.save_entry)
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
        selected_type = self.selected_entry_type
        if not selected_type:
            self.status_label.config(text="Παρακαλώ επιλέξτε τύπο εγγραφής.", fg="red")
            return

        if selected_type in ["Έσοδα", "Έξοδα"]:
            self.save_exchange(selected_type)
        elif selected_type in ["Υποχρεώσεις", "Επιθυμίες"]:
            self.save_task(selected_type)

    def save_exchange(self,selected_type):
        date = self.date_entry.get().strip() if self.date_entry else ""
        amount = self.amount_entry.get().strip() if self.amount_entry else ""
        category = self.category_combo.get().strip() if self.category_combo else ""
        description = self.description_entry.get().strip() if self.description_entry else ""
        #Αν ένα από τα κύρια πεδία δεν είναι συμπληρωμένα -> αμυντικός προγραμματισμός
        if date == "" or amount == "" or category == "":
            self.status_label.config(text="Παρακαλώ συμπληρώστε όλα τα πεδία.",fg='red')
            return
        #Κάνω έναν επί πρόσθετο αμυντικό με casting του amount σε float με try - except
        try:
            amount = float(amount)
        except ValueError:
            self.status_label.config(text="Χρησιμοποιήστε μόνο έγκυρο τύπο αριθμών.",fg='red')
            return
        
        fixed_date = self.fix_date(date)
        if fixed_date is None:
            self.status_label.config(text="Διατηρείστε το ημερολογιακό format: dd/mm/yyyy.", fg="red")
            return
        db_exchange_type = ENTRY_TYPE_TO_DB[selected_type]
        #Καλώ ΒΔ για δημιουργία εγγραφής - πάλι με αμυντικό για να μη σκάσει:
        try:
            self.app.db.create_exchange(
                self.app.current_user_id, #-> που το έχω από την κλάση SigninFrame στην def: check_account 
                db_exchange_type, #ώστε όλα να είναι ίδια
                amount,
                fixed_date,
                category,
                description)
            self.status_label.config(text=f"{selected_type} αποθηκέυτηκε επιτυχώς.",fg='green')
        except Exception as e:
            self.status_label.config(text=f"Error: {e} κατά την αποθήκευση.",fg='red')
    
    def save_task(self,selected_type):
        name = self.name_entry.get().strip() if self.name_entry else ""
        amount = self.amount_entry.get().strip() if self.amount_entry else ""
        date = self.date_entry.get().strip() if self.date_entry else ""
        status = self.status_combo.get().strip() if self.status_combo else ""
        link = self.link_entry.get().strip() if self.link_entry else ""
        #Αν ένα από τα κύρια πεδία δεν είναι συμπληρωμένα -> αμυντικός προγραμματισμός
        if date == "" or amount == "" or name == "" or status == "":
            self.status_label.config(text="Παρακαλώ συμπληρώστε όλα τα πεδία.",fg='red')
            return
        #Κάνω έναν επί πρόσθετο αμυντικό με casting του amount σε float με try - except
        try:
            amount = float(amount)
        except ValueError:
            self.status_label.config(text="Χρησιμοποιήστε μόνο έγκυρο τύπο αριθμών.",fg='red')
            return
        fixed_date = self.fix_date(date)
        if fixed_date is None:
            self.status_label.config(text="Διατηρείστε το ημερολογιακό format: dd/mm/yyyy.", fg="red")
            return
        db_task_type = ENTRY_TYPE_TO_DB[selected_type]
        db_status = STATUS_TO_DB[status]
        #Καλώ ΒΔ για δημιουργία εγγραφής - πάλι με αμυντικό για να μη σκάσει:
        try:
            self.app.db.create_task(
                self.app.current_user_id, #-> που το έχω από την κλάση SigninFrame στην def: check_account 
                db_task_type, #ώστε όλα να είναι ίδια
                name,
                amount,
                fixed_date,
                db_status,
                link)
            self.status_label.config(text=f"{selected_type} αποθηκέυτηκε επιτυχώς.",fg='green')
        except Exception as e:
            self.status_label.config(text=f"Error: {e} στην προσπάθεια να αποθηκεύσει.",fg='red')
            
#Ανασκόπηση καταχωρημένων εγγραφών με view correlated του user_id που έκανε log in 
class InspectFrame(Frame):
    def __init__(self,parent,app):
        super().__init__(parent)
        self.app = app
        self.app.root.title("Wallet App - Ανασκόπηση εγγραφών")

        #Αρχικόποιώ τα dataframes τα οποία θα χτίσω μετά και θα τα σερβίρω στα export σε xlsx
        self.df_exchanges = pd.DataFrame()
        self.df_tasks = pd.DataFrame()

        title_label = Label(self, text="Ανασκόπηση εγγραφών", font=("Arial", 14))
        title_label.pack(pady=10)

        #Θα φτιάξω δύο ξεχωριστά treeview (1.exchanges 2. tasks) ώστε να μη γεμίσουμε με στήλες άκυρες κατά περίπτωση
        #Για exchanges:
        exchanges_label = Label(self, text="Συναλλαγές", font=("Arial", 12))
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
        self.exchange_tree.heading("type", text="Τύπος")
        self.exchange_tree.heading("amount", text="Ποσό")
        self.exchange_tree.heading("date", text="Ημερομηνία")
        self.exchange_tree.heading("category", text="Κατηγορία")
        self.exchange_tree.heading("description", text="Περιγραφή")   
        #Για tasks:
        tasks_label = Label(self, text="Δραστηριότητες", font=("Arial", 12))
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
        self.task_tree.heading("type", text="Τύπος")
        self.task_tree.heading("name", text="Όνομα")
        self.task_tree.heading("amount", text="Ποσό")
        self.task_tree.heading("date", text="Ημερομηνία")
        self.task_tree.heading("status", text="Κατάσταση")
        self.task_tree.heading("link", text="Link")

        #Μαζευω λίγο column width
        self.exchange_tree.column("id", width=60)
        self.exchange_tree.column("type", width=100)
        self.exchange_tree.column("amount", width=100)
        self.exchange_tree.column("date", width=110)
        self.exchange_tree.column("category", width=140)
        self.exchange_tree.column("description", width=240)

        self.task_tree.column("id", width=60)
        self.task_tree.column("type", width=110)
        self.task_tree.column("name", width=160)
        self.task_tree.column("amount", width=100)
        self.task_tree.column("date", width=110)
        self.task_tree.column("status", width=110)
        self.task_tree.column("link", width=260)
        buttons_frame = Frame(self)
        buttons_frame.pack(pady=15)
        
        #Κουμπιά διαγραφής εγγραφών
        delete_exchange_button = Button(buttons_frame,text="Διαγραφή επιλεγμένων συναλλαγών",command=self.delete_selected_exchange)
        delete_exchange_button.pack(side=LEFT,padx=5)

        delete_task_button = Button(buttons_frame,text="Διαγραφή επιλεγμένων δραστηριοτήτων",command=self.delete_selected_task)
        delete_task_button.pack(side=LEFT,padx=5)

        #Μια loaf_entries ουσιαστικά είναι απλά τη δίνεις με button - την έβαλα τυπικά
        refresh_button = Button(buttons_frame, text="Ανανέωση", command=self.load_entries)
        refresh_button.pack(side=LEFT, padx=5)

        export_button = Button(buttons_frame, text="Εξαγωγή σε Excel", command=self.export_to_excel)
        export_button.pack(side=LEFT, padx=5)
        #Button για edit των selected rows
        edit_exchange_Button = Button(buttons_frame, text="Επεξεργασία επιλεγμένων συναλλαγών", command=self.edit_selected_exchange)
        edit_exchange_Button.pack(side=LEFT,padx=5)
        
        edit_task_Button = Button(buttons_frame, text="Επεξεργασία επιλεγμένων δραστηριοτητων", command=self.edit_selected_task)
        edit_task_Button.pack(side=LEFT,padx=5)
        
        back_button = Button(buttons_frame, text="Επιστροφή", command=lambda: self.app.show_frame(MainPage))
        back_button.pack(side=LEFT, padx=5)

        new_entry_button = Button(buttons_frame,text="Νέα εγγραφή",command=lambda: self.app.show_frame(NewEntry))
        new_entry_button.pack(side=LEFT, padx=5)

        self.load_entries()

    def delete_selected_exchange(self):
        selected_row = self.exchange_tree.selection()#κρατάει την επιλεγμένη γραμμή
        if not selected_row: #για να μη σκάσει
            return
        row_values = self.exchange_tree.item(selected_row[0],"values")
        record_id = row_values[0] #<-το πρώτο στοιχείο της tuple
        try:
            self.app.db.delete_exchange(record_id)
            self.load_entries()
        except Exception as e:
            print(f"Σφάλμα κατά τη διαγραφή: {e}")

    def delete_selected_task(self):
        selected_row = self.task_tree.selection()#κρατάει την επιλεγμένη γραμμή
        if not selected_row: #για να μη σκάσει
            return
        row_values = self.task_tree.item(selected_row[0],"values")
        record_id = row_values[0] #<-το πρώτο στοιχείο της tuple
        try:
            self.app.db.delete_task(record_id)
            self.load_entries()
        except Exception as e:
            print(f"Σφάλμα κατά τη διαγραφή: {e}")

    def load_entries(self):
        #Αρχικά σβήνω ότι έχει μείνει από προηγούμενο load
        for data in self.exchange_tree.get_children():
            self.exchange_tree.delete(data)
        for data in self.task_tree.get_children():
            self.task_tree.delete(data)

        #Καλώ ΒΔ να μου επιστρέψει τα rows για το self.user_id
        exchanges = self.app.db.get_user_exchanges(self.app.current_user_id)
        tasks = self.app.db.get_user_tasks(self.app.current_user_id)

        exchange_cols = ["id", "user_id", "exchange_type", "amount", "date", "category", "description"]
        task_cols = ["id", "user_id", "task_type", "name", "amount", "date", "status", "link"]
        self.df_exchanges = pd.DataFrame(exchanges, columns=exchange_cols)
        self.df_tasks = pd.DataFrame(tasks, columns=task_cols)

        for row_data in exchanges:
            record_id, user_id, exchange_type, amount, date, category, description = row_data
            display_type = DB_TO_ENTRY_TYPE.get(exchange_type, exchange_type)
            self.exchange_tree.insert("",END,
                values=(record_id, display_type, amount, date, category, description))

        for row_data in tasks:
            record_id, user_id, task_type, name, amount, date, status, link = row_data
            display_type = DB_TO_ENTRY_TYPE.get(task_type, task_type)
            display_status = DB_TO_STATUS.get(status, status)
            self.task_tree.insert("",END,
                values=(record_id, display_type, name, amount, date, display_status, link))
            
    def edit_selected_exchange(self):
        selected_row = self.exchange_tree.selection()
        if not selected_row:
            return
        
        selected_values = self.exchange_tree.item(selected_row[0],"values")
        record_id = selected_values[0]
        exchange_type = selected_values[1]
        amount = selected_values[2]
        date = selected_values[3]
        category = selected_values[4]
        description = selected_values[5]

        #Χρησιμοποιώ lambda για να περάσω class & arguments
        self.app.show_frame(lambda parent,app:EditExchangeFrame(parent,app,record_id,exchange_type,amount,date,category,description))
    def edit_selected_task(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            return
        item_values = self.task_tree.item(selected_item[0], "values")
        record_id = item_values[0]
        task_type = item_values[1]
        name = item_values[2]
        amount = item_values[3]
        date = item_values[4]
        status = item_values[5]
        link = item_values[6]

        self.app.show_frame(lambda parent, app: EditTaskFrame(parent,app,record_id,task_type,name,amount,date,status,link))

    def export_to_excel(self):
        if self.df_exchanges.empty and self.df_tasks.empty:
            return
        #το εβαλα xlsx γιατί καμιά φορά αν ανοιγείς xls σου εμφανίζει προειδοποίηση στα 365 για παλιά χχρήση αρχείου
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return
        #Το κάνω με ExcelWriter αντί κατευθείαν με to_excel για να βάλω όλο το worksheet σε διαφορετικά spreadsheets
        with pd.ExcelWriter(file_path) as writer:
            self.df_exchanges.to_excel(writer, sheet_name="Συναλλαγές", index=False)
            self.df_tasks.to_excel(writer, sheet_name="Δραστηριότητες", index=False)

class EditExchangeFrame(Frame):
    def __init__(self,parent,app,record_id,exchange_type,amount,date,category,description):
        super().__init__(parent)
        self.app = app
        self.record_id = record_id
        self.app.root.title("Wallet App - Επεξεργασία συναλλαγής")

        self.revenue_categories = ["Μισθοδοσία", "Bonus", "Freelance", "Business", "Δώρα","Αποζημίωση", "Επενδύσεις", "Έσοδα ακινήτων", "Άλλο"]
        self.expense_categories = ["Τρόφιμα", "Λογαριασμοί ΔΕΚΟ", "Καύσιμα","Ασφάλειες", "Μεταφορικά έξοδα", "Ενοίκιο", "Ψώνια", "Υγεία", "Διασκέδαση",
                                    "Εκπαίδευση", "Ταξίδια", "Άλλο"]   
        
        self.status_label = Label(self,text="",fg="red")
        self.status_label.pack(pady=10)
        form_frame = Frame(self)
        form_frame.pack(pady=20)

        Label(form_frame, text="Τύπος").grid(row=0, column=0, padx=5, pady=10)
        self.entry_type = ttk.Combobox(form_frame, values=["Έσοδα", "Έξοδα"], state="readonly")
        self.entry_type.grid(row=0, column=1, padx=5, pady=10)
        self.entry_type.set(DB_TO_ENTRY_TYPE.get(exchange_type, exchange_type))
        self.entry_type.bind("<<ComboboxSelected>>", self.update_category_values)

        Label(form_frame, text="Ημερομηνία (dd/mm/yyyy)").grid(row=1,column=0,padx=5,pady=10)
        self.date_entry = Entry(form_frame)
        self.date_entry.grid(row=1,column=1,padx=5,pady=10)
        self.date_entry.insert(0, self.display_date(date))

        Label(form_frame, text="Πόσο").grid(row=2,column=0,padx=5,pady=10)
        self.amount_entry = Entry(form_frame)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=10)
        self.amount_entry.insert(0, str(amount))

        Label(form_frame, text="Κατηγορία").grid(row=3,column=0,padx=5,pady=10)
        self.category_combo = ttk.Combobox(form_frame, state="readonly")
        self.category_combo.grid(row=3,column=1,padx=5,pady=10)

        self.update_category_values()
        self.category_combo.set(category)      

        Label(form_frame, text="Περιγραφή").grid(row=4,column=0,padx=5,pady=10)
        self.description_entry = Entry(form_frame)
        self.description_entry.grid(row=4,column=1,padx=5, pady=10)
        self.description_entry.insert(0,description if description else "")

        save_button = Button(form_frame,text="Αποθήκευση αλλαγών",command=self.save_changes)
        save_button.grid(row=5,column=0,columnspan=2,pady=10)

        back_button = Button(self,text="Επιστροφή",command=lambda:self.app.show_frame(InspectFrame))
        back_button.pack(pady=5)

    #Παίρνω το entry type και το πετάω απευθείας στην κατηγορία
    def update_category_values(self, event=None):
        selected_type = self.entry_type.get()
        if selected_type == "Έσοδα":
            self.category_combo["values"] = self.revenue_categories
        else:
            self.category_combo["values"] = self.expense_categories       
    
    #Ομοίως όπως και στο αρχικό data input process
    def normalize_date(self, date_text):
        try:
            parsed_date = datetime.strptime(date_text, "%d/%m/%Y")
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            return None
    def display_date(self, stored_date):
        try:
            parsed_date = datetime.strptime(stored_date, "%Y-%m-%d")
            return parsed_date.strftime("%d/%m/%Y")
        except ValueError:
            return stored_date

    def save_changes(self):
        db_exchange_type = ENTRY_TYPE_TO_DB[self.entry_type.get().strip()]
        date =self.date_entry.get().strip()
        amount =self.amount_entry.get().strip()
        category= self.category_combo.get().strip()
        description =self.description_entry.get().strip()

        if db_exchange_type == "" or date == "" or amount == "" or category == "":
            self.status_label.config(text="Παρακαλώ συμπληρώστε όλα τα πεδία.", fg="red")
            return
        try:
            amount = float(amount)
        except ValueError:
            self.status_label.config(text="Χρησιμοποιήστε μόνο έγκυρο τύπο αριθμών.", fg="red")
            return
        normalized_date = self.normalize_date(date)
        if normalized_date is None:
            self.status_label.config(text="Διατηρείστε το ημερολογιακό format: dd/mm/yyyy.", fg="red")
            return
        try:
            self.app.db.update_exchange(
                self.record_id,
                db_exchange_type,
                amount,
                normalized_date,
                category,
                description)
            self.app.show_frame(InspectFrame)
        except Exception as e:
            self.status_label.config(text=f"Σφάλμα κατά την ανανέωση συναλλαγής: {e}",fg="red")

#copy paste σχεδόν από πάνω για τα task
class EditTaskFrame(Frame):
    def __init__(self,parent,app,record_id,task_type,name,amount,date,status,link):
        super().__init__(parent)
        self.app = app
        self.record_id = record_id
        self.app.root.title("Wallet App - Επεξεργασία δραστηριότητας")

        self.status_label = Label(self,text="",fg="red")
        self.status_label.pack(pady=10)

        form_frame = Frame(self)
        form_frame.pack(pady=20)

        Label(form_frame, text="Τύπος").grid(row=0, column=0,padx=5,pady=10)
        self.task_type_combo = ttk.Combobox(
            form_frame,
            values=["Υποχρεώσεις", "Επιθυμίες"],
            state="readonly")
        self.task_type_combo.grid(row=0,column=1,padx=5,pady=10)
        self.task_type_combo.set(DB_TO_ENTRY_TYPE.get(task_type, task_type))
        self.task_type_combo.bind("<<ComboboxSelected>>", self.toggle_link_field)

        Label(form_frame, text="Όνομα").grid(row=1,column=0,padx=5,pady=10)
        self.name_entry = Entry(form_frame)
        self.name_entry.grid(row=1, column=1, padx=5,pady=10)
        self.name_entry.insert(0, name)

        Label(form_frame, text="Ποσό").grid(row=2,column=0,padx=5,pady=10)
        self.amount_entry = Entry(form_frame)
        self.amount_entry.grid(row=2,column=1,padx=5,pady=10)
        self.amount_entry.insert(0, str(amount))

        Label(form_frame, text="Ημερομηνία (dd/mm/yyyy)").grid(row=3, column=0,padx=5,pady=10)
        self.date_entry = Entry(form_frame)
        self.date_entry.grid(row=3,column=1, padx=5, pady=10)
        self.date_entry.insert(0,self.display_date(date))

        Label(form_frame, text="Κατάσταση").grid(row=4,column=0,padx=5,pady=10)
        self.status_combo = ttk.Combobox(
            form_frame,
            values=["Εκκρεμεί", "Ολοκληρώθηκε"],
            state="readonly"
        )
        self.status_combo.set(DB_TO_STATUS.get(status, status))
        self.status_combo.grid(row=4,column=1,padx=5,pady=10)
        #self.status_combo.set(status)

        self.link_label = Label(form_frame, text="Link")
        self.link_entry = Entry(form_frame)

        if task_type.lower() == "wishlist":
            self.link_label.grid(row=5,column=0,padx=5,pady=10)
            self.link_entry.grid(row=5,column=1,padx=5,pady=10)
            self.link_entry.insert(0, link if link else "")
            save_row = 6
        else:
            save_row = 5

        save_button = Button(form_frame,text="Αποθήκευση αλλαγών",command=self.save_changes)
        save_button.grid(row=save_row,column=0,columnspan=2,pady=10)

        back_button = Button(self,text="Επιστροφή",command=lambda: self.app.show_frame(InspectFrame))
        back_button.pack(pady=5)

    def toggle_link_field(self, event=None):
        selected_type = self.task_type_combo.get()

        self.link_label.grid_forget()
        self.link_entry.grid_forget()

        if selected_type == "Επιθυμίες":
            self.link_label.grid(row=5,column=0,padx=5,pady=10)
            self.link_entry.grid(row=5,column=1,padx=5,pady=10)

    def normalize_date(self, date_text):
        try:
            parsed_date = datetime.strptime(date_text,"%d/%m/%Y")
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            return None

    def display_date(self, stored_date):
        try:
            parsed_date = datetime.strptime(stored_date,"%Y-%m-%d")
            return parsed_date.strftime("%d/%m/%Y")
        except ValueError:
            return stored_date

    def save_changes(self):
        db_task_type = ENTRY_TYPE_TO_DB[self.task_type_combo.get().strip()]
        name = self.name_entry.get().strip()
        amount = self.amount_entry.get().strip()
        date = self.date_entry.get().strip()
        db_status = STATUS_TO_DB[self.status_combo.get().strip()]
        link = self.link_entry.get().strip() if db_task_type == "wishlist" else None
        if db_task_type == "" or name == "" or amount == "" or date == "" or db_status == "":
            self.status_label.config(text="Παρακαλώ συμπληρώστε όλα τα πεδία.", fg="red")
            return
        try:
            amount = float(amount)
        except ValueError:
            self.status_label.config(text="Χρησιμοποιήστε μόνο έγκυρο τύπο αριθμών.", fg="red")
            return
        normalized_date = self.normalize_date(date)
        if normalized_date is None:
            self.status_label.config(text="Διατηρείστε το ημερολογιακό format: dd/mm/yyyy.", fg="red")
            return
        try:
            self.app.db.update_task(
                self.record_id,
                db_task_type,
                name,
                amount,
                normalized_date,
                db_status,
                link)
            self.app.show_frame(InspectFrame)
        except Exception as e:
            self.status_label.config(text=f"Σφάλμα κατά την ανανέωση δραστηριότητας: {e}",fg="red")

class StatsFrame(Frame):
    def __init__(self,parent,app):
        super().__init__(parent)
        self.app = app
        self.app.root.title("Wallet App - Στατιστικά")

        exchanges = self.app.db.get_user_exchanges(self.app.current_user_id)
        tasks = self.app.db.get_user_tasks(self.app.current_user_id)

        exchange_cols = ["id", "user_id", "exchange_type", "amount", "date", "category", "description"]
        task_cols = ["id", "user_id", "task_type", "name", "amount", "date", "status", "link"]

        exchanges_df = pd.DataFrame(exchanges,columns=exchange_cols)
        tasks_df = pd.DataFrame(tasks,columns=task_cols)

        stats_label = Label(self)
        stats_label.pack(pady=10)

        

        exchanges = self
new_app = Application()
new_app.run()
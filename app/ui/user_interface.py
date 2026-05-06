from tkinter import *
from tkinter import ttk

class Application():
    def __init__(self):
        self.root = Tk()
        self.root.title("Wallet App")
        
        self.current_frame = None
    
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

        welcome_label = Label(self, text="Welcome!\n\nSign up to create an account or sign in to access an existing one.")
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

        label_username = Label(self, text= "Username")
        label_username.grid(row=0, column=0, padx=5, pady=10)

        entry_username = Entry(self)
        entry_username.grid(row=0, column=1, padx=5, pady=10)

        label_password = Label(self, text= "Password")
        label_password.grid(row=1, column=0, padx=5, pady=5)
        
        entry_password = Entry(self)
        entry_password.grid(row=1, column=1, padx=5, pady=5)

        label_password_requirements = Label(self, text= "Use at least 2 characters (one Letter & one Number)")
        label_password_requirements.grid(row=2, column=1,padx=5, pady=2)

        control_signup_buttons_frame = Frame(self)
        control_signup_buttons_frame.grid(row=2, column=2, padx=5, pady=5)

        button_save = Button(control_signup_buttons_frame, text="Create account")
        button_save.pack(side="left", padx=5)

        button_back = Button(control_signup_buttons_frame, text="Back", command = lambda: self.app.show_frame(WelcomeFrame))
        button_back.pack(side="left", padx=5)


class SignInFrame(Frame):
    def __init__(self,parent,app):
        super().__init__(parent)
        self.app = app

        label_username = Label(self, text= "Username")
        label_username.grid(row=0, column=0, padx=5, pady=10)

        entry_username = Entry(self)
        entry_username.grid(row=0, column=1, padx=5, pady=10)

        label_password = Label(self, text= "Password")
        label_password.grid(row=1, column=0, padx=5, pady=5)
        
        entry_password = Entry(self, show='*')
        entry_password.grid(row=1, column=1, padx=5, pady=5)    

        control_signin_buttons_frame = Frame(self)
        control_signin_buttons_frame.grid(row=2, column=2, padx=5, pady=5)

        button_save = Button(control_signin_buttons_frame, text="Sign in", command=lambda: self.app.show_frame(MainPage))
        button_save.pack(side="left", padx=5)

        button_back = Button(control_signin_buttons_frame, text="Back", command = lambda: self.app.show_frame(WelcomeFrame))
        button_back.pack(side="left", padx=5)   


class MainPage(Frame):
    def __init__(self,parent,app):
        super().__init__(parent)
        self.app = app
        self.app.set_menu_at_mainPage()


class NewEntry(Frame):
    def __init__(self,parent,app):
        super().__init__(parent)
        self.app = app
        
        label_entry_type = Label(self, text= "Entry type")
        label_entry_type.grid(row=0, column=0, padx=5, pady=10)

        self.entry_type = ttk.Combobox(self,values=["Revenue", "Expense", "Task", "Wishlist"],
                                       state="readonly")
        self.entry_type.grid(row=0,column=1,padx=5,pady=10)
        self.entry_type.bind("<<ComboboxSelected>>", self.handle_entry_type)
        self.recurring_var = IntVar()

    def handle_entry_type(self, event):
        selected_type = self.entry_type.get()

        if selected_type == "Revenue" or selected_type == "Expense":
            self.revenue_view()

    def revenue_view(self):
        
            date_label = Label(self, text="Date (dd/mm/yyyy)")
            date_label.grid(row=1,column=0,padx=5,pady=10)

            date_entry = Entry(self)
            date_entry.grid(row=1,column=1,padx=5,pady=10)

            value_label = Label(self, text="Amount")
            value_label.grid(row=2,column=0,padx=5,pady=10)

            value_entry = Entry(self)
            value_entry.grid(row=2,column=1,padx=5,pady=10)
            
            make_recurring_chkbox = Checkbutton(self,text='Make Recurring', variable=self.recurring_var,command=self.handle_recurring)
            make_recurring_chkbox.grid(row=3,column=1,padx=5,pady=5)
    
    def handle_recurring(self):
        if self.recurring_var.get() == 1:
            self.make_recurring_view()

    def make_recurring_view(self):
            rec_period_label = Label(self, text="Recurring period")
            rec_period_label.grid(row=4,column=0,padx=5,pady=10)

            rec_period_choice_frame = Frame(self)
            rec_period_choice_frame.grid(row=4,column=2, padx=5, pady=10)

            basis = IntVar()
            r1 = Radiobutton(rec_period_choice_frame,text="Daily",value=1,variable=basis)
            r1.pack(side=LEFT)
            r2 = Radiobutton(rec_period_choice_frame,text="Weekly",value=2,variable=basis)
            r2.pack(side=LEFT)
            r3 = Radiobutton(rec_period_choice_frame,text="Monthly",value=3,variable=basis)
            r3.pack(side=LEFT)




new_app = Application()
new_app.run()
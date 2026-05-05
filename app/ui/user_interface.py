from tkinter import *


class Application():
    def __init__(self):
        self.root = Tk()
        self.root.title("Wallet App")
        #self.root.geometry("600x400")
        self.current_frame = None
    
    def show_frame(self, frame_class):
        if self.current_frame is not None:
            self.current_frame.destroy()
        
        self.current_frame = frame_class(self.root, self)
        self.current_frame.pack(fill="both",expand=True)  
    
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

        button_save = Button(control_signin_buttons_frame, text="Sign in")
        button_save.pack(side="left", padx=5)

        button_back = Button(control_signin_buttons_frame, text="Back", command = lambda: self.app.show_frame(WelcomeFrame))
        button_back.pack(side="left", padx=5)   


new_app = Application()
new_app.run()
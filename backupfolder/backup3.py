import tkinter as tk
import re
from passlib.hash import pbkdf2_sha256

# noinspection PyAttributeOutsideInit
class StartGui(tk.Tk):
    """starting gui here"""

    #  help( shows everything about StartGui )
    #  print(help(StartGui))
    def __init__(self):
        super().__init__()
        self.state('zoomed')  # maxscreensize
        self.resizable(0, 0)  # don't allow resizing
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)
        self.title("Salvation Army Pantry Inventory")  # app title
        self.iconbitmap(r'salogo_YMx_icon.ico')  # icon
        # exit program button
        self.exitButton = tk.Button(self, text="Exit",
                                    background='white', font="Helvetica",
                                    command=quit)
        self.exitButton.configure(padx=10)
        self.exitButton.place(relx=.94, rely=.9325)

        #logoutButton
        self.logoutButton = tk.Button(self, text="Logout",
                                      background='white', font="Helvetica",
                                      command=lambda: self.login_screen())
        # add and remove items buttons
        self.remove_items_button = tk.Button(self, text="Remove Items", background='white',
                                             font="Helvetica")
        self.add_items_button = tk.Button(self, text="Add Items",
                                          background='white', font="Helvetica")
        self.username_verify = tk.StringVar()


        # registration errors username exists, to short, has a space in it.   pw too short, has a space in it
        self.registration_info_error = tk.Label(self, font=("Helvetica", 18))
        self.user_register_success = tk.Label(self, font=("Helvetica", 18), text="Successfully Registered")
        self.login_info_error = tk.Label(self, font=("Helvetica", 18))
        self.password_verify = tk.StringVar()
        self.login_screen()

    def login_screen(self):
        #SA army logo
        login_army_logo = tk.PhotoImage(file="SA_doing_the_most_good.png").subsample(4,4)
        self.login_army_label = tk.Label(self, image=login_army_logo)
        self.login_army_label.place(relx=.175, rely=.05) # where to place the image
        self.image = login_army_logo           # save a reference through garbarge pickup

        # login screen label
        self.loginlabel = tk.Label(self, text="Inventory Managment Login", font=("Helvetica", 30))
        self.loginlabel.place(relx=.300, rely=.30)

        # login screen address
        self.addresslabel = tk.Label(self, text="The Salvation Army of San Antonio"
                                                " Metropolitian Area Command\n"
                                                "521 W. Elmira\n"
                                                "San Antonio, TX 78212",
                                     font=("Helvetica", 18))
        self.addresslabel.place(relx=.250, rely=.85)



        # username label
        self.usernamelabel = tk.Label(self, text="User Name :", font=("Helvetica", 20))
        self.usernamelabel.place(relx=.300, rely=.450)

        # password label
        self.passwordlabel = tk.Label(self, text="Password :", font=("Helvetica", 20))
        self.passwordlabel.place(relx=.315, rely=.540)

        # username entry box

        self.username_entry = tk.Entry(self, font=("Helvetica", 18), textvariable=self.username_verify)
        self.username_entry.focus()  # defaults entry to this box
        self.username_entry.place(relx=.440, rely=.46)

        # password entry box

        # show='*'
        self.password_entry = tk.Entry(self, font=("Helvetica", 18), textvariable=self.password_verify)
        self.password_entry.place(relx=.440, rely=.545)

        # login button
        self.loginbutton = tk.Button(self, text="Login",
                                     background='#ff9194', font="Helvetica", command=lambda: self.login_verify())
        self.loginbutton.configure(activebackground='#e4fcdc', padx=10)
        self.loginbutton.place(relx=.550, rely=.6)

        # register button
        self.registerbutton = tk.Button(self, text="Register",
                                        background='#ff9194', font="Helvetica", command=lambda: self.register_user())
        self.registerbutton.configure(activebackground='#e4fcdc', padx=10)
        self.registerbutton.place(relx=.450, rely=.6)

        # remove logout button
        self.logoutButton.place_forget()
        self.remove_items_button.place_forget()
        self.add_items_button.place_forget()


    def user_view(self):
        self.clear_login_screen()
        self.logout_button_place()

    # registration validation
    def register_user(self):
        self.username_info = self.username_verify.get()
        self.password_info = self.password_verify.get()
        self.clear_registration_errors()
        self.ready_to_register = True
        __username_length = 8
        __password_length = 8
        __max_password_length = 20
        __max_username_length = 20


        # plug into regex101.com for a clear explanation
        # (?=.*[a-z]) positive lookahead for a-z
        regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
        pattern = re.compile(regex)

        # check for username too short
        if len(self.username_info) < __username_length:
            self.registration_error("Username must be atleast 8 letters", .65, .455)

        # check for non chars in username
        elif re.search("[^a-zA-Z]", self.username_info):
            self.registration_error("Only use letters a-z for username", .65, .455)

        # check if password too short
        elif len(self.password_info) < __password_length:
            self.registration_error("Password must be atleast 8 characters", .65, .55)

        # limit password & username length
        elif len(self.password_info) > __max_password_length: # or
            self.registration_error("Password must be LESS than\n"
                                    "{} characters".format(__max_password_length), .65, .55)
        elif len(self.username_info) > __max_username_length:
            self.registration_error("Username must be LESS than \n"
                                    "{} characters".format(__max_username_length), .65, .455)

        # check password objects used a-z !@#$%^&*
        elif not re.search(pattern, self.password_info):
            self.registration_error("Password must contain atleast\n"
                                    "one uppercase, one lowercase\n"
                                    "one number, and one\n"
                                    "special character @$!#%*?&", .65, .55)

        # check if username to register already exists
        else:
            with open('username_password_file.txt', "r+") as readf:
                for line in readf:
                    tokens = re.split(" ", line.strip())
                    if tokens[0] == self.username_info:
                        self.registration_error("username already exists", .65, .455)
                        break

        # username is a new user, and password is ok, REGISTER THE USER
        if self.ready_to_register:

            # hash the password
            self.hash = pbkdf2_sha256.hash(self.password_info)

            # add username to the username file
            with open('username_password_file.txt', "a+") as writef:
                writef.write(self.username_info + " ")
                writef.write(self.hash + "\n")

            # successfully registered
            self.user_register_success.place(relx=.440, rely=.4)
            #testing added clear login screen
            self.clear_login_screen()
            self.login_screen()

        # clear user info

    def logout_button_place(self):
        self.logoutButton.place(relx=.87, rely=.9325)

    def login_verify(self):
        #self.clear_login_screen()
        #self.logout_button_place()
        self.clear_registration_errors()
        self.clear_registration_success()

        # login works here
        self.username_info = self.username_verify.get()
        self.password_info = self.password_verify.get()

        # check username and hashed password
        self.ready_to_login = False
        with open('username_password_file.txt', "r+") as readf:
            for line in readf:
                tokens = re.split(" ", line.strip())
                if tokens[0] == self.username_info:
                    # check password here
                    # TODO : pbkdf2_sha256.verify(self.password_info, str(tokens[1])):
                    self.ready_to_login = True
                    break

        if self.ready_to_login:
            # testing here clear login
            self.clear_login_screen()
            self.user_screen()
        else:
            self.login_failure("username & password invalid", .65, .455)
            self.login_screen()

    # usable functions
    # TODO clear entry info

    def user_screen(self):
        self.clear_login_screen()

        self.logout_button_place()
        self.login_army_label.place(relx=.175, rely=.05)
        # add items

        self.add_items_button.place(relx=.30, rely=.500)
        # remove items

        self.remove_items_button.place(relx=.5, rely=.5)

# ------------------- HERE




    def login_failure(self, text, x, y):
        self.login_info_error.place(relx=x, rely=y)
        self.login_info_error["text"] = text

    def registration_error(self, text, x, y):
        self.ready_to_register = False
        self.registration_info_error.place(relx=x, rely=y)
        self.registration_info_error["text"] = text
        self.clear_registration_success()
        self.login_screen()

    def clear_registration_errors(self):
        self.registration_info_error.place_forget()

    def clear_registration_success(self):
        self.user_register_success.place_forget()

    def clear_login_screen(self):
        self.login_army_label.place_forget()
        self.loginlabel.place_forget()
        self.addresslabel.place_forget()
        self.usernamelabel.place_forget()
        self.username_entry.place_forget()
        self.password_entry.place_forget()
        self.passwordlabel.place_forget()
        self.loginbutton.place_forget()
        self.registerbutton.place_forget()
        self.add_items_button.place_forget()
        self.remove_items_button.place_forget()

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.attributes("-fullscreen", self.state)

    def end_fullscreen(self, event=None):
        self.state = False
        self.attributes("-fullscreen", False)





        # Example code don't edit the samples
        #-------------------------------------------------------

        # ToolTip(self.Button1, tooltip_font, '''some words''', delay=0.5)

        # photo example
        # subsample resizes the image (3,3) uses every 3rd x and y
        # put the image in the same folder as SAP (top folder)
        """
        photo = tk.PhotoImage(file="SA_doing_the_most_good.png").subsample(3,3)
        self.label = tk.Label(self, image=photo)
        self.label.place(x=10, y=10) # where to place the image
        self.image = photo           # save a reference through garbarge pickup
        """

        # label example
        """
        self.L1 = tk.Label(self, text="Words in a Label")
        self.L1.place(x=500, y=500)
        """

        # hide button example
        """
        self.aHideButton = tk.Button(self, text="hide",
                                     background='white', font=("Helvetica"),
                                     command=lambda: self.hide_me(self.aHideButton))
        self.aHideButton.place(x=650, y=100)
        """

        # show button example
        """
        self.aShowButton = tk.Button(self, text="show",
                                     background='white', font=("Helvetica"),
                                     command=lambda: self.show_me(self.aHideButton, 650, 100))
        self.aShowButton.place(x=650, y=300)
        """

        # show / hide function examples
        """
        def show_me(self, event, xposition, yposition):
            print("show {} at position {} , {} ".format(str(event), xposition, yposition))
            event.place(x=xposition, y=yposition)

        def hide_me(self, event):
            print("hide {} ".format(str(event)))
            event.place_forget()
        """

        # Entry Box example & retrieve entry box info
        """
        self.text_entry = tk.Entry(self)
        # defaults entry to this box
        self.text_entry.focus()
        self.text_entry.place(x=300, y=400)
        # disable entry box
        # self.text_entry.configure(state='disabled')

        # get the value entered in text_entry
        self.get_entry_button = tk.Button(self, text="get text entry",
                                          command=lambda: [self.clicked(), (self.text_entry.get())])
        self.get_entry_button.place(x=10, y=10)

    def clicked(self):
        self.get_entry_button["text"]=self.text_entry.get()
        """




    # everything above this line
    # ----------------------------------------------------------------------


if __name__ == '__main__':
    StartGui().mainloop()

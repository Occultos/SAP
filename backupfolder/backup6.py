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

        # back button to return to previous screen
        self.backup_button = tk.Button(self, text ="Back",
                                       background = 'white', font = "Helvetica",
                                       command=lambda: self.back_button(self.previous_view))
        self.backup_button.configure(padx=10)

        # logoutButton
        self.logoutButton = tk.Button(self, text="Logout",
                                      background='white', font="Helvetica",
                                      command=lambda: self.login_screen())
        # remove items button screen
        self.remove_items_button = tk.Button(self, text="Remove Items", background='white',
                                             font="Helvetica")
        # add items button screen
        self.add_items_button = tk.Button(self, text="Add Items",
                                          background='white', font="Helvetica",
                                          command=lambda: self.add_items_screen())

        #remove bag button after logging in
        self.remove_bag_button = tk.Button(self, text="Remove Bag",
                                           background='white', font="Helvetica")
        self.remove_bag_button.configure(activebackground='#e4fcdc', padx=10)

        #buttons in user add items screen
        # manual entry button
        self.manual_entry_button = tk.Button(self, text="Manual Entry",
                                             background='white', font="Helvetica",
                                             command=lambda: self.manual_entry_screen())
        self.manual_entry_button.configure(activebackground='#e4fcdc', padx=10)
        
        # barcode scanner button
        self.barcode_scanner_button = tk.Button(self, text="Barcode Scan",
                                                background='white', font="Helvetica",
                                                command=lambda: self.barcode_scanner_screen())
        self.barcode_scanner_button.configure(activebackground='#e4fcdc', padx=10)

        # scale button
        self.by_scale_button = tk.Button(self, text="Scale",
                                         background='white', font="Helvetica",
                                         command=lambda: self.by_scale_screen())
        self.by_scale_button.configure(activebackground='#e4fcdc', padx=10)

        # view inventory button
        self.view_inventory_button = tk.Button(self, text="View Inventory",
                                               font="Helvetica")
        self.view_inventory_button.configure(activebackground='#e4fcdc', padx=10)



        # buttons on admin screen
        self.admin_button = tk.Button(self, text="Do some admin stuff", background='white',
                                      font="Helvetica")

        # registration errors username exists, to short, has a space in it.   pw too short, has a space in it
        self.registration_info_error = tk.Label(self, font=("Helvetica", 18))
        self.user_register_success = tk.Label(self, font=("Helvetica", 18), text="Successfully Registered")
        self.login_info_error = tk.Label(self, font=("Helvetica", 18))

        # entry boxes
        self.username_verify = tk.StringVar()
        self.username_verify.set('')
        self.username_entry = tk.Entry(self, font=("Helvetica", 18), textvariable=self.username_verify)
        self.password_verify = tk.StringVar()
        self.password_verify.set('')
        self.password_entry = tk.Entry(self, font=("Helvetica", 18), textvariable=self.password_verify, show='*')

        # print("Login_screen from init")
        self.login_screen()

    def login_screen(self):
        # SA army logo
        login_army_logo = tk.PhotoImage(file="SA_doing_the_most_good.png").subsample(4, 4)
        self.login_army_label = tk.Label(self, image=login_army_logo)
        self.login_army_label.place(relx=.175, rely=.05)  # where to place the image
        self.image = login_army_logo  # save a reference through garbarge pickup

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
        self.username_entry.focus()  # defaults entry to this box
        self.username_entry.place(relx=.440, rely=.46)

        # password entry box
        self.password_entry.place(relx=.440, rely=.545)

        # login button
        self.loginbutton = tk.Button(self, text="Login",
                                     background='#ff9194', font="Helvetica",
                                     command=lambda: self.login_verify())

        self.loginbutton.configure(activebackground='#e4fcdc', padx=10)
        self.loginbutton.place(relx=.550, rely=.6)

        # register button
        self.registerbutton = tk.Button(self, text="Register",
                                        background='#ff9194', font="Helvetica",
                                        command=lambda: self.register_user())

        self.registerbutton.configure(activebackground='#e4fcdc', padx=10)
        self.registerbutton.place(relx=.450, rely=.6)

        # remove other buttons
        self.clear_to_login()

    def clear_to_login(self):
        self.logoutButton.place_forget()
        self.remove_items_button.place_forget()
        self.add_items_button.place_forget()
        self.admin_button.place_forget()
        self.remove_bag_button.place_forget()
        self.view_inventory_button.place_forget()
        self.manual_entry_button.place_forget()
        self.barcode_scanner_button.place_forget()
        self.by_scale_button.place_forget()
        self.backup_button.place_forget()

    # registration validation
    def register_user(self):
        # deleting entry boxes
        self.username_info = self.username_verify.get()
        self.password_info = self.password_verify.get()
        self.clear_registration_errors()
        self.clear_login_info_error()
        self.clear_login_screen()
        # print("cleared login screen in register user")
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
        elif len(self.password_info) > __max_password_length:  # or
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
            # testing added clear login screen
            self.clear_login_screen()
            self.clear_verify()
            # print("cleared login screen READY TO REGISER TRUE, registered and loading login screen")
            self.login_screen()

        # clear user info

    def login_verify(self):
        self.clear_registration_errors()
        self.clear_registration_success()
        self.clear_login_screen()  # test
        # print("cleared login screen in login_verify, now verifying password")
        # login works here
        self.username_info = self.username_verify.get()
        self.password_info = self.password_verify.get()

        # check username and hashed password
        self.ready_to_login = False
        with open('username_password_file.txt', "r+") as readf:
            for line in readf:
                tokens = re.split(" ", line.strip())
                if tokens[0] == self.username_info and len(tokens[0]) > 7 and pbkdf2_sha256.verify(self.password_info,
                                                                                                   tokens[1]):
                    self.ready_to_login = True
                    # print("confirmed password")
                    break
        self.clear_verify()
        self.clear_login_screen()
        self.user_screen()
        """
        if self.ready_to_login:
            # testing here clear login
            self.clear_verify()
            self.clear_login_screen()  # test
            # print("cleared screen in ready_to_login, moving to user screen")
            if tokens[0] == 'adminarmy':
                self.admin_screen()
            else:
                self.user_screen()
        else:
            self.login_failure("username & password invalid", .65, .455)
            self.clear_verify()
            self.clear_login_screen()
            # print("login screen clered in ! ready to login, moving to loginscreen")
            self.login_screen()
        """

    # usable functions
    #TODO test here for backbutton functionality
    def back_button(self, words):
        #goes back to user screen
        if words == "user_screen":
            self.user_screen()
            self.clear_add_items_screen()
        #goes back to add items screen
        elif words == "add_items_screen":
            self.add_items_screen()

    def view_inventory(self):
        self.clear_admin_screen()
        self.logout_button_place()
        print("view inventory button pushed\n")

    def admin_screen(self):
        self.clear_login_screen()
        self.logout_button_place()
        self.clear_login_info_error()
        self.login_army_label.place(relx=.175, rely=.05)
        self.admin_button.place(relx=.5, rely=.5)
        # TODO put stuff here
        # view inventory
        self.view_inventory_button.place(relx=.4, rely=.7)
        # TODO: view inventory

    def user_screen(self):
        self.clear_login_screen()
        self.logout_button_place()
        self.clear_login_info_error()
        self.backup_button.place_forget()
        #TODO: exitbuttonplace??
        self.login_army_label.place(relx=.175, rely=.05)
        # add items
        self.add_items_button.place(relx=.30, rely=.500)
        # remove items
        self.remove_items_button.place(relx=.5, rely=.5)
        # remove bag
        self.remove_bag_button.place(relx=.4, rely=.4)
        # TODO do more stuff here

    # in add items screen
    def add_items_screen(self):
        # remove extra stuff
        self.clear_user_screen()
        # input options
        self.manual_entry_button.place(relx=.25, rely=.5)
        self.barcode_scanner_button.place(relx=.4, rely=.5)
        self.by_scale_button.place(relx=.55, rely=.5)
        self.backup_button.place(relx=.07, rely=.9325)
        self.previous_view = "user_screen"

    # in barcode scanner screen
    def barcode_scanner_screen(self):
        self.clear_add_items_screen()
        #self.backup_button.place(relx=.07, rely=.9325)
        self.previous_view = "add_items_screen"

    def by_scale_screen(self):
        self.clear_add_items_screen()
        self.previous_view = "add_items_screen"

    def manual_entry_screen(self):
        self.clear_add_items_screen()
        self.previous_view = "add_items_screen"


    def clear_user_screen(self):
        self.add_items_button.place_forget()
        self.remove_items_button.place_forget()
        self.remove_bag_button.place_forget()

    # clears if one of the options is selected
    def clear_add_items_screen(self):
        self.manual_entry_button.place_forget()
        self.barcode_scanner_button.place_forget()
        self.by_scale_button.place_forget()




    def clear_admin_screen(self):
        self.admin_button.place_forget()
        self.view_inventory_button.place_forget()

    def logout_button_place(self):
        self.logoutButton.place(relx=.87, rely=.9325)

    def exit_button_place(self):
        self.exitButton.place(relx=.91, rely=.9325)

    def clear_verify(self):
        self.username_verify.set('')
        self.password_verify.set('')

    def clear_login_info_error(self):
        self.login_info_error.place_forget()

    def login_failure(self, text, x, y):
        self.login_info_error.place(relx=x, rely=y)
        self.login_info_error["text"] = text

    def registration_error(self, words, x, y):
        self.ready_to_register = False
        self.registration_info_error.place(relx=x, rely=y)
        self.registration_info_error["text"] = words
        self.clear_registration_success()
        self.clear_verify()
        self.clear_login_screen()
        # print("registration error clear_login_screen, moving to login screen")
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
        # -------------------------------------------------------

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

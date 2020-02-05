import tkinter as tk
import re
from passlib.hash import pbkdf2_sha256
from time import *
# from time import time, localtime, strftime
import shutil
import yagmail


# TODO: go to line 857 to skip login

# noinspection PyAttributeOutsideInit,PyMethodMayBeStatic
class StartGui(tk.Tk):
    """starting gui here"""

    #  help( shows everything about StartGui )
    #  print(help(StartGui))
    def __init__(self):
        super().__init__()
        # =======================================================================================================
        #                                               MISC. - INIT
        # ========================================================================================================
        self.state('zoomed')  # TODO: maxscreensize DOESN"T WORK ON MAC, fix this
        self.resizable(0, 0)  # TODO: don't allow resizing, DISABLE ON MAC DUE TO 'zoomed' not working
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)
        self.title("Salvation Army Pantry Inventory")  # app title
        self.iconbitmap(r'salogo_YMx_icon.ico')  # icon
        self._bgcolor = 'white'
        self._fgcolor = '#000000'
        self._activebgcolor = '#e4fcdc'
        self._font = "Helvetica"
        self._fgcolor = '#ff9194'
        # make a dict
        self.d = {}

        # =======================================================================================================
        #                                              buttons - INIT
        # =======================================================================================================
        # exit program button
        self.exitButton = tk.Button(self, text="Exit",
                                    background=self._bgcolor, font=self._font,
                                    command=quit)
        self.exitButton.configure(activebackground=self._activebgcolor, padx=10)
        self.exitButton.place(relx=.94, rely=.9325)

        # login button
        self.loginbutton = tk.Button(self, text="Login",
                                     background=self._fgcolor, font=self._font,
                                     command=lambda: self.login_verify())

        self.loginbutton.configure(activebackground=self._activebgcolor, padx=25)

        # back button to return to previous screen
        self.backup_button = tk.Button(self, text="Back",
                                       background=self._bgcolor, font=self._font,
                                       command=lambda: self.back_button(self.previous_view))
        self.backup_button.configure(padx=10)

        # logoutButton
        self.logoutButton = tk.Button(self, text="Logout",
                                      background=self._bgcolor, font=self._font,
                                      command=lambda: self.login_screen())
        self.logoutButton.configure(padx=10)

        # remove items button screen
        self.remove_items_button = tk.Button(self, text="Remove Items", background=self._fgcolor,
                                             font=self._font, command=lambda: self.remove_items_screen())
        self.remove_items_button.configure(activebackground=self._activebgcolor, padx=10)

        # add items button screen
        self.add_items_button = tk.Button(self, text="Add Items",
                                          background=self._fgcolor, font=self._font,
                                          command=lambda: self.add_items_screen())
        self.add_items_button.configure(activebackground=self._activebgcolor, padx=22)

        # buttons in user add items screen
        # manual entry button
        self.manual_entry_button = tk.Button(self, text="Manual Entry",
                                             background=self._fgcolor, font=self._font,
                                             command=lambda: self.manual_entry_screen())
        self.manual_entry_button.configure(activebackground=self._activebgcolor, padx=10)

        # barcode scanner button
        self.barcode_scanner_button = tk.Button(self, text="Barcode Scan",
                                                background=self._fgcolor, font=self._font,
                                                command=lambda: self.barcode_scanner_screen())
        self.barcode_scanner_button.configure(activebackground=self._activebgcolor, padx=12)

        # scale button
        self.by_scale_button = tk.Button(self, text="Scale",
                                         background=self._fgcolor, font=self._font,
                                         command=lambda: self.by_scale_screen())
        self.by_scale_button.configure(activebackground=self._activebgcolor, padx=42)

        # view inventory button
        self.display_inventory_button = tk.Button(self, text="View Inventory",
                                                  font=self._font, background=self._fgcolor,
                                                  command=lambda: self.view_inventory(self.d))
        self.display_inventory_button.configure(activebackground=self._activebgcolor, padx=10)

        # buttons on admin screen
        self.admin_button = tk.Button(self, text="Do admin stuff", background=self._fgcolor,
                                      font=self._font)
        # open email entry
        self.admin_email_button = tk.Button(self, text="Email inventory", background=self._fgcolor,
                                            font=self._font, command=lambda: self.email_entry(self.d))
        self.admin_email_button.configure(activebackground=self._activebgcolor, padx=10)

        # send email
        self.admin_email_send_button = tk.Button(self, text="Send", background=self._fgcolor,
                                                 font=self._font,
                                                 command=lambda: self.admin_email_inventory(self.d))


        # remove bag button after logging in
        self.make_bag_screen_button = tk.Button(self, text="Make Bag",
                                                background=self._fgcolor, font=self._font,
                                                command=lambda: self.make_bag_screen())
        self.make_bag_screen_button.configure(activebackground=self._activebgcolor, padx=10)

        # make A bag button
        self.make_ONE_bag_button = tk.Button(self, text="Make ONE bag",
                                             background=self._fgcolor, font=self._font,
                                             command=lambda: self.made_a_bag_screen())
        self.make_ONE_bag_button.configure(activebackground=self._activebgcolor)

        # make ANOTHER bag
        self.make_another_bag_button = tk.Button(self, text="Make ANOTHER bag",
                                                 background=self._fgcolor, font=self._font,
                                                 command=lambda: self.back_button(self.previous_view))
        self.make_another_bag_button.configure(activebackground=self._activebgcolor, padx=10)

        # dictionary buttons
        self.make_dictionary = tk.Button(self, text="Build a dictionary",
                                         background=self._bgcolor, font=self._font,
                                         command=lambda: self.make_dict(self.d))
        self.make_dictionary.configure(activebackground=self._activebgcolor, padx=10)

        # print dictionary
        self.print_dictionary_button = tk.Button(self, text="print a dictionary",
                                                 background=self._bgcolor, font=self._font,
                                                 command=lambda: self.print_dict(self.d))
        self.print_dictionary_button.configure(activebackground=self._activebgcolor, padx=10)



        # ==================================================================================================
        #                                            labels - INIT
        # ===================================================================================================

        self.loginlabel = tk.Label(self, text="Inventory Managment Login", font=(self._font, 30))
        self.help_label = tk.Label(self, text="Registration Help",
                                   background='#c1bcf5', font=self._font)
        self.help_label.configure(padx=20, pady=15)
        self.admin_email_label = tk.Label(self, text="Email sent", font=(self._font, 18))
        # registration errors username exists, to short, has a space in it.   pw too short, has a space in it
        self.registration_info_error = tk.Label(self, font=(self._font, 18))
        self.user_register_success = tk.Label(self, font=(self._font, 18), text="Successfully Registered")
        self.login_info_error = tk.Label(self, font=(self._font, 18))
        self.todo_label = tk.Label(self, text="TODO: more stuff here and delete this label afterwards",
                                   font=(self._font, 20))
        self.addresslabel = tk.Label(self, text="The Salvation Army of San Antonio"
                                                " Metropolitian Area Command\n"
                                                "521 W. Elmira\n"
                                                "San Antonio, TX 78212",
                                     font=(self._font, 18))
        self.usernamelabel = tk.Label(self, text="User Name :", font=(self._font, 20))
        self.passwordlabel = tk.Label(self, text="Password :", font=(self._font, 20))
        self.username_label = tk.Label(self, font=(self._font, 18))
        self.enter_email_add_label = tk.Label(self, font=(self._font, 18))

        # ===================================================================================================
        #                                         SA army logo - INIT
        # ===================================================================================================
        self.login_army_logo = tk.PhotoImage(file="SA_doing_the_most_good.png").subsample(4, 4)
        self.login_army_label = tk.Label(self, image=self.login_army_logo)
        self.login_army_label.place(relx=.175, rely=.05)  # where to place the image
        self.image = self.login_army_logo  # save a reference through garbarge pickup

        # =====================================================================================================
        #                                           TOOLTIP - INIT
        # ======================================================================================================

        ToolTip(self.help_label, self._font, '''Username must be atleast 8 letters\n
Only use letters a-z for username\n
Password must be 8-20 characters\n
Password must contain atleast:\n
one uppercase,\n
one lowercase, \n
one number,\n
one special character: !@#$%*?\n''', delay=.25)

        # =======================================================================================================
        #                                         entry boxes - INIT
        # =======================================================================================================
        self.username_verify = tk.StringVar()
        self.username_verify.set('')
        self.username_entry = tk.Entry(self, font=(self._font, 18), textvariable=self.username_verify)
        self.password_verify = tk.StringVar()
        self.password_verify.set('')
        self.password_entry = tk.Entry(self, font=(self._font, 18), textvariable=self.password_verify, show='*')
        self.email_add = tk.StringVar()
        self.email_add.set('')
        self.enter_email_add_entry = tk.Entry(self, font=(self._font, 18), textvariable=self.email_add)

        # ========================================================================================================
        #                                    list boxes and labels - INIT
        # ========================================================================================================
        self.list_box_1 = tk.Listbox(self, font=(self._font, 12))
        self.list_box_2 = tk.Listbox(self, font=(self._font, 12))
        self.list_box_3 = tk.Listbox(self, font=(self._font, 12))
        self.list_box_1_label = tk.Label(self, font=(self._font, 14), text="OUT OF STOCK")
        self.list_box_2_label = tk.Label(self, font=(self._font, 14), text="LOW INVENTORY")
        self.list_box_3_label = tk.Label(self, font=(self._font, 14), text="INVENTORY")

        # ==================================================================================================
        #                                         check buttons - INIT
        # ===================================================================================================
        # TODO: 1 big or 2 small cans  : OR
        # TODO: bag of rice or beans : OR
        self.checkbutton_label = tk.Label(self, text="only select MISSING items", font=(self._font, 18))
        self.vegetable_cans_4_checkbutton = tk.Checkbutton(self, text="4 cans of vegetable items",
                                                           font=self._font)
        self.vegetable_cans_4_checkbutton.configure(activebackground=self._activebgcolor, padx=10)
        self.fruit_cans_3_checkbutton = tk.Checkbutton(self, text="3 fruit cans",
                                                       font=self._font)
        self.fruit_cans_3_checkbutton.configure(activebackground=self._activebgcolor, padx=10)
        self.meat_3_checkbutton = tk.Checkbutton(self, text="3 meat items",
                                                 font=self._font)
        self.meat_3_checkbutton.configure(activebackground=self._activebgcolor, padx=10)
        self.soup_can_1_large_checkbutton = tk.Checkbutton(self, text="1 large soup can or 2 small cans",
                                                           font=self._font)
        self.soup_can_1_large_checkbutton.configure(activebackground=self._activebgcolor, padx=10)
        self.spaghetti_sauce_1_checkbutton = tk.Checkbutton(self, text="1 spaghetti sauce can",
                                                            font=self._font)
        self.spaghetti_sauce_1_checkbutton.configure(activebackground=self._activebgcolor, padx=10)
        self.tomato_sauce_2_checkbutton = tk.Checkbutton(self, text="2 cans of tomato sauce",
                                                         font=self._font)
        self.tomato_sauce_2_checkbutton.configure(activebackground=self._activebgcolor, padx=10)
        self.beans_can_1_checkbutton = tk.Checkbutton(self, text="1 can of beans",
                                                      font=self._font)
        self.beans_can_1_checkbutton.configure(activebackground=self._activebgcolor, padx=10)
        self.ravioli_1_checkbutton = tk.Checkbutton(self, text="1 can of ravioli",
                                                    font=self._font)
        self.ravioli_1_checkbutton.configure(activebackground=self._activebgcolor, padx=10)
        self.peanut_butter_1_checkbutton = tk.Checkbutton(self, text="1 peanut butter",
                                                          font=self._font)
        self.peanut_butter_1_checkbutton.configure(activebackground=self._activebgcolor, padx=10)
        self.jelly_1_checkbutton = tk.Checkbutton(self, text="1 jelly",
                                                  font=self._font)
        self.jelly_1_checkbutton.configure(activebackground=self._activebgcolor, padx=10)
        self.mac_cheese_2_checkbutton = tk.Checkbutton(self, text="2 boxes of mac and cheese",
                                                       font=self._font)
        self.mac_cheese_2_checkbutton.configure(activebackground=self._activebgcolor, padx=10)
        self.bag_rice_1_checkbutton = tk.Checkbutton(self, text="1 bag of rice/bean",
                                                     font=self._font)
        self.bag_rice_1_checkbutton.configure(activebackground=self._activebgcolor, padx=10)
        self.juice_1_checkbutton = tk.Checkbutton(self, text="1 juice or drink",
                                                  font=self._font)
        self.juice_1_checkbutton.configure(activebackground=self._activebgcolor, padx=10)
        self.snacks_5_checkbutton = tk.Checkbutton(self, text="5 snacks",
                                                   font=self._font)
        self.snacks_5_checkbutton.configure(activebackground=self._activebgcolor, padx=10)
        self.misc_1_checkbutton = tk.Checkbutton(self, text="1 miscellaneous item",
                                                 font=self._font)
        self.misc_1_checkbutton.configure(activebackground=self._activebgcolor, padx=10)
        self.cereal_1_checkbutton = tk.Checkbutton(self, text="1 cereal",
                                                   font=self._font)
        self.cereal_1_checkbutton.configure(activebackground=self._activebgcolor, padx=10)
        self.nuts_1_checkbutton = tk.Checkbutton(self, text="1 large bag of nuts",
                                                 font=self._font)
        self.nuts_1_checkbutton.configure(activebackground=self._activebgcolor, padx=10)

        # starting program at the login screen
        self.login_screen()

    # =================================================================================================
    #                                    ^^^^^^^^  END OF INIT ^^^^^^^^^^
    # =================================================================================================

    # usable functions
    # =================================================================================================
    #                                                BACKUP
    # =================================================================================================

    def back_button(self, words):
        # goes back to user screen
        if words == "user_screen":
            self.clear_makebag_screen()
            self.user_screen()
            self.clear_add_items_screen()
            self.clear_todo_label()
        # goes back to add items screen
        elif words == "add_items_screen":
            self.add_items_screen()
            self.clear_todo_label()
        elif words == "make_bag_screen":
            self.make_bag_screen()
            self.clear_todo_label()
            self.make_dictionary.place_forget()
            self.print_dictionary_button.place_forget()
            self.clear_list_box()

    # ==========================================================================================
    #                                   EMAIL Functions
    # ===========================================================================================
    def email_entry(self, d):
        self.admin_email_label.place_forget()
        self.enter_email_add_label.configure(text='Enter Email Address')
        self.enter_email_add_label.place(relx=.2, rely=.9325)
        self.enter_email_add_entry.place(relx=.4, rely=.9325)
        self.admin_email_send_button.place(relx=.63, rely=.928)
        self.enter_email_add_entry.focus()

    def admin_email_inventory(self, d):
        self.print_dict(d)
        self.admin_email_label.place(relx=.85, rely=.70)
        emailpw = self.password_info
        try:
            yag = yagmail.SMTP('sanantoniopantrynoreply@gmail.com', emailpw)
            contents = [
                "Sent via SAP inventory program. Do not reply",
                "You can find current inventory status attached.", 'food_status.txt']
            yag.send(self.email_add.get(), 'Food Inventory', contents)
        # Alternatively, with a simple one-liner:
        # yagmail.SMTP('mygmailusername').send('to@someone.com', 'subject', contents)
        except Exception as e:
            print("error " + str(e))
            self.admin_email_label.configure(text="Email error")
        self.email_add.set('')
        self.enter_email_add_label.place_forget()
        self.enter_email_add_entry.place_forget()
        self.admin_email_send_button.place_forget()

    # ==============================================================================================
    #                                                 SCREENS
    # ==============================================================================================

    def admin_screen(self):
        self.clear_login_screen()
        self.logout_button_place()
        self.clear_login_info_error()
        self.login_army_label.place(relx=.175, rely=.05)
        # self.admin_button.place(relx=.85, rely=.85)
        self.admin_email_button.place(relx=.85, rely=.85)
        self.display_inventory_button.place(relx=.85, rely=.77)
        # TODO view inventory here

    def user_screen(self):
        self.clear_login_screen()
        self.logout_button_place()
        self.clear_login_info_error()
        self.backup_button.place_forget()
        self.login_army_label.place(relx=.175, rely=.05)
        # add items
        self.add_items_button.place(relx=.250, rely=.500)
        # remove items
        self.remove_items_button.place(relx=.4, rely=.5)
        # remove bag
        self.make_bag_screen_button.place(relx=.55, rely=.5)

    # made a bag
    def made_a_bag_screen(self):
        # TODO: lowerinventory by appropriate ammount according to check buttons
        self.lower_inventory()

        # checkbuttons.placeforget & make_ONE_bag.placeforget
        self.clear_makebag_screen()
        self.previous_view = "make_bag_screen"
        self.make_another_bag_button.place(relx=.7, rely=.3)
        self.view_inventory(self.d)

    # make bag screen
    def make_bag_screen(self):
        self.clear_user_screen()
        self.checkbutton_label.place(relx=.65, rely=.4)
        self.make_ONE_bag_button.place(relx=.7, rely=.3)
        self.vegetable_cans_4_checkbutton.place(relx=0.067, rely=0.271)
        self.vegetable_cans_4_checkbutton.deselect()
        self.fruit_cans_3_checkbutton.place(relx=0.067, rely=0.33)
        self.fruit_cans_3_checkbutton.deselect()
        self.meat_3_checkbutton.place(relx=0.067, rely=0.388)
        self.meat_3_checkbutton.deselect()
        self.soup_can_1_large_checkbutton.place(relx=0.067, rely=0.447)
        self.soup_can_1_large_checkbutton.deselect()
        self.spaghetti_sauce_1_checkbutton.place(relx=0.067, rely=0.506)
        self.spaghetti_sauce_1_checkbutton.deselect()
        self.tomato_sauce_2_checkbutton.place(relx=0.067, rely=0.564)
        self.tomato_sauce_2_checkbutton.deselect()
        self.beans_can_1_checkbutton.place(relx=0.067, rely=0.623)
        self.beans_can_1_checkbutton.deselect()
        self.ravioli_1_checkbutton.place(relx=0.067, rely=0.681)
        self.ravioli_1_checkbutton.deselect()
        self.peanut_butter_1_checkbutton.place(relx=0.067, rely=0.74)
        self.peanut_butter_1_checkbutton.deselect()
        self.jelly_1_checkbutton.place(relx=0.4, rely=0.271)
        self.jelly_1_checkbutton.deselect()
        self.mac_cheese_2_checkbutton.place(relx=0.4, rely=0.33)
        self.mac_cheese_2_checkbutton.deselect()
        self.bag_rice_1_checkbutton.place(relx=0.4, rely=0.388)
        self.bag_rice_1_checkbutton.deselect()
        self.juice_1_checkbutton.place(relx=0.4, rely=0.447)
        self.juice_1_checkbutton.deselect()
        self.snacks_5_checkbutton.place(relx=0.4, rely=0.506)
        self.snacks_5_checkbutton.deselect()
        self.misc_1_checkbutton.place(relx=0.4, rely=0.564)
        self.misc_1_checkbutton.deselect()
        self.cereal_1_checkbutton.place(relx=0.4, rely=0.623)
        self.cereal_1_checkbutton.deselect()
        self.nuts_1_checkbutton.place(relx=0.4, rely=0.681)
        self.nuts_1_checkbutton.deselect()
        self.backup_place()
        self.previous_view = "user_screen"

    # in add items screen
    def add_items_screen(self):
        # remove extra stuff
        self.clear_user_screen()
        # input options
        self.manual_entry_button.place(relx=.25, rely=.5)
        self.barcode_scanner_button.place(relx=.4, rely=.5)
        self.by_scale_button.place(relx=.55, rely=.5)
        self.backup_place()
        self.previous_view = "user_screen"

    def remove_items_screen(self):
        self.clear_user_screen()
        self.backup_place()
        self.previous_view = "user_screen"
        self.todo_label_place()

    # in barcode scanner screen
    def barcode_scanner_screen(self):
        self.clear_add_items_screen()
        self.todo_label_place()
        self.previous_view = "add_items_screen"

    def by_scale_screen(self):
        self.clear_add_items_screen()
        self.todo_label_place()
        self.previous_view = "add_items_screen"

    def manual_entry_screen(self):
        self.clear_add_items_screen()
        self.todo_label_place()
        self.previous_view = "add_items_screen"

    # ==============================================================================================
    #                                             Place functions
    # ==============================================================================================

    def backup_place(self):
        self.backup_button.place(relx=.02, rely=.9325)

    def todo_label_place(self):
        self.todo_label.place(relx=.300, rely=.450)

    def logout_button_place(self):
        self.logoutButton.place(relx=.85, rely=.9325)

    def exit_button_place(self):
        self.exitButton.place(relx=.91, rely=.9325)

    # ===============================================================================================
    #                                   Login & Registration ERRORS
    # ===============================================================================================

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
        self.login_screen()

    # ============================================================================================
    #                                           CLEAR FUNCTIONS
    # ============================================================================================

    # clear everything back to login screen
    def clear_to_login(self):
        self.username_label.place_forget()
        self.logoutButton.place_forget()
        self.remove_items_button.place_forget()
        self.add_items_button.place_forget()
        self.admin_button.place_forget()
        self.admin_email_button.place_forget()
        self.admin_email_label.place_forget()
        self.make_bag_screen_button.place_forget()
        self.display_inventory_button.place_forget()
        self.manual_entry_button.place_forget()
        self.barcode_scanner_button.place_forget()
        self.by_scale_button.place_forget()
        self.backup_button.place_forget()
        self.clear_todo_label()
        self.clear_makebag_screen()
        self.clear_user_screen()
        self.clear_list_box()
        self.enter_email_add_label.place_forget()
        self.enter_email_add_entry.place_forget()
        self.admin_email_send_button.place_forget()

    # clear list boxes
    def clear_list_box(self):
        self.list_box_1.delete(0, tk.END)
        self.list_box_2.delete(0, tk.END)
        self.list_box_3.delete(0, tk.END)
        self.list_box_1.place_forget()
        self.list_box_2.place_forget()
        self.list_box_3.place_forget()
        self.make_another_bag_button.place_forget()
        self.list_box_1_label.place_forget()
        self.list_box_2_label.place_forget()
        self.list_box_3_label.place_forget()

    # clear check buttons
    def clear_makebag_screen(self):
        self.make_ONE_bag_button.place_forget()
        self.checkbutton_label.place_forget()
        self.vegetable_cans_4_checkbutton.place_forget()
        self.fruit_cans_3_checkbutton.place_forget()
        self.meat_3_checkbutton.place_forget()
        self.soup_can_1_large_checkbutton.place_forget()
        self.spaghetti_sauce_1_checkbutton.place_forget()
        self.tomato_sauce_2_checkbutton.place_forget()
        self.beans_can_1_checkbutton.place_forget()
        self.ravioli_1_checkbutton.place_forget()
        self.peanut_butter_1_checkbutton.place_forget()
        self.jelly_1_checkbutton.place_forget()
        self.mac_cheese_2_checkbutton.place_forget()
        self.bag_rice_1_checkbutton.place_forget()
        self.juice_1_checkbutton.place_forget()
        self.snacks_5_checkbutton.place_forget()
        self.misc_1_checkbutton.place_forget()
        self.cereal_1_checkbutton.place_forget()
        self.nuts_1_checkbutton.place_forget()

    # clears user screen
    def clear_user_screen(self):
        self.add_items_button.place_forget()
        self.remove_items_button.place_forget()
        self.make_bag_screen_button.place_forget()
        self.print_dictionary_button.place_forget()
        self.make_dictionary.place_forget()

    # clears if one of the options is selected
    def clear_add_items_screen(self):
        self.manual_entry_button.place_forget()
        self.barcode_scanner_button.place_forget()
        self.by_scale_button.place_forget()

    def clear_admin_screen(self):
        self.admin_button.place_forget()
        self.admin_email_button.place_forget()
        self.display_inventory_button.place_forget()

    # clear remove items screen
    def clear_todo_label(self):
        self.todo_label.place_forget()

    def clear_verify(self):
        self.username_verify.set('')
        self.password_verify.set('')

    def clear_login_info_error(self):
        self.login_info_error.place_forget()

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
        self.help_label.place_forget()
        self.registerbutton.place_forget()
        self.add_items_button.place_forget()
        self.remove_items_button.place_forget()

    # ==================================================================================================
    #                                            FULL SCREEN
    # ==================================================================================================

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.attributes("-fullscreen", self.state)

    def end_fullscreen(self, event=None):
        self.state = False
        self.attributes("-fullscreen", False)

    # ================================================================================================
    #                                         DICTIONARY FUNCTIONS
    # ================================================================================================
    def print_dict(self, d):
        self.make_dict(d)
        out_of_line = ""
        low_line = ""
        current_inventory = ""
        printlocaltime = localtime(time())
        monthday = str(printlocaltime.tm_mon) + "/" + str(printlocaltime.tm_mday) + " "
        currenttime = monthday + str(printlocaltime.tm_hour) + ":" + str(printlocaltime.tm_min)
        try:
            with open("food_status.txt", "w") as dest:
                for item_id, item_info in d.items():
                    if item_info['amount'] <= 0:
                        out_of_line += item_id + '\n'
                    elif item_info['amount'] <= item_info['lowlevel']:
                        low_line += item_id + ' : ' + str(item_info['amount']) + '\n'
                    else:
                        current_inventory += item_id + ' : ' + str(item_info['amount']) + '\n'
                dest.write(currenttime + '\n' + '\n')
                dest.write('OUT OF STOCK' + '\n')
                dest.write(out_of_line)
                dest.write('\n' + 'LOW INVENTORY' + '\n')
                dest.write(low_line)
                dest.write('\n' + 'REMAINING INVENTORY' + '\n')
                dest.write(current_inventory)
        except Exception as e:
            print("error in print dict : " + str(e))

    # TODO: check_inventory_level not used
    def check_inventory_level(self, d):
        self.make_dict(d)
        for item_id, item_info in d.items():
            if item_info['amount'] <= 0:
                print("ran out of " + item_id)
            elif item_info['amount'] <= item_info['lowlevel']:
                print("running low on " + item_id)

    def make_dict(self, d):
        with open("food.txt") as f:
            next(f)
            for line in f:
                words = line.split(",")
                item = words[0]
                amount = int(words[1])
                lowlevel = int(words[2])
                weight = int(words[3])
                cost = int(words[4])
                d[item] = {}
                d[item]['item'] = item
                d[item]['amount'] = amount
                d[item]['lowlevel'] = lowlevel
                d[item]['weight'] = weight
                d[item]['cost'] = cost
                number_of_barcodes = len(words) - 5
                n = 1
                while n <= number_of_barcodes:
                    barcode = 'barcode' + str(n)
                    d[item][barcode] = int(words[4 + n])
                    n += 1

    # =============================================================================================
    #                                               View and/or change Inventory
    # =============================================================================================

    def view_inventory(self, d):
        self.make_dict(d)
        self.clear_list_box()
        self.list_box_1.place(relx=.14, rely=.4, relwidth=.14)
        self.list_box_2.place(relx=.39, rely=.4, relwidth=.14)
        self.list_box_3.place(relx=.65, rely=.4, relwidth=.14)
        self.list_box_1_label.place(relx=.14, rely=.35)
        self.list_box_2_label.place(relx=.39, rely=.35)
        self.list_box_3_label.place(relx=.65, rely=.35)
        box1count = 0
        box2count = 0
        box3count = 0
        # fill boxes
        for item_id, item_info in d.items():
            if item_info['amount'] <= 0:
                box1count += 1
                self.list_box_1.insert(box1count, item_id)
            elif item_info['amount'] <= item_info['lowlevel']:
                box2count += 1
                self.list_box_2.insert(box2count, item_id + ' : ' + str(item_info['amount']))
            else:
                box3count += 1
                self.list_box_3.insert(box3count, item_id + ' : ' + str(item_info['amount']))

        # adjust box height
        boxheight = .032
        maxboxheight = .48
        if (box1count * boxheight) > maxboxheight:
            self.list_box_1.place(relheight=maxboxheight)
        else:
            self.list_box_1.place(relheight=(box1count * boxheight))

        if (box2count * boxheight) > maxboxheight:
            self.list_box_2.place(relheight=maxboxheight)
        else:
            self.list_box_2.place(relheight=(box2count * boxheight))

        if (box3count * boxheight) > maxboxheight:
            self.list_box_3.place(relheight=maxboxheight)
        else:
            self.list_box_3.place(relheight=(box3count * boxheight))

        # clear unused boxes
        if box1count == 0:
            self.list_box_1.place_forget()
            self.list_box_1_label.place_forget()
        if box2count == 0:
            self.list_box_2.place_forget()
            self.list_box_2_label.place_forget()
        if box3count == 0:
            self.list_box_3.place_forget()
            self.list_box_3_label.place_forget()

    # TODO : make this relative to the checkboxes, currently reduces all inventory by one
    def lower_inventory(self):
        try:
            shutil.move("food.txt", "food.txt" + "~")
            with open("food.txt", "w") as dest:
                with open("food.txt" + "~", "r") as src:
                    n = 0
                    for line in src:
                        if n == 0:
                            dest.write(line)
                            n += 1
                        else:  # decrease amount by 1
                            line = line.strip()
                            words = line.split(",")
                            words[1] = str(int(words[1]) - 1)
                            line = ",".join(words)
                            line.strip()
                            line = line + '\n'
                            dest.write(line)
        except Exception as e:
            print("error in lower inventory " + str(e))

    # =========================================================================================
    #                                                  load login screen
    # =========================================================================================

    def login_screen(self):
        #    SA army logo
        self.login_army_label.place(relx=.175, rely=.05)  # where to place the image

        # login screen label
        self.loginlabel.place(relx=.300, rely=.30)

        # login screen address
        self.addresslabel.place(relx=.250, rely=.85)

        # username label
        self.usernamelabel.place(relx=.300, rely=.450)

        # password label
        self.passwordlabel.place(relx=.315, rely=.540)

        # username entry box
        self.username_entry.focus()  # defaults entry to this box
        self.username_entry.place(relx=.440, rely=.46)

        # password entry box
        self.password_entry.place(relx=.440, rely=.545)

        # login button
        self.loginbutton.place(relx=.550, rely=.6)
        self.help_label.place(relx=.05, rely=.9)

        # register button
        self.registerbutton = tk.Button(self, text="Register",
                                        background=self._fgcolor, font=self._font,
                                        command=lambda: self.register_user())

        self.registerbutton.configure(activebackground=self._activebgcolor, padx=10)
        self.registerbutton.place(relx=.450, rely=.6)

        # remove other buttons
        self.clear_to_login()

    # =====================================================================================================
    #                                                     REGISTRATION
    # =====================================================================================================
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

    # ===============================================================================================
    #                                              LOGIN VERIFICATION
    # ===============================================================================================

    def login_verify(self):
        self.clear_registration_errors()
        self.clear_registration_success()
        self.clear_login_screen()  # test
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

        # TODO: uncomment next few lines to skip login
        '''
        self.clear_verify()
        self.clear_login_screen()
        self.user_screen()
        #self.admin_screen()
        '''
        # TODO: commnted out if/else to skip login steps while building program, put back in for finished product

        if self.ready_to_login:
            self.clear_verify()
            self.clear_login_screen()
            self.username_label.configure(text=str(tokens[0]))
            self.username_label.place(relx=.02, rely=.88)
            # relx = .07, rely = .9325
            if tokens[0] == 'adminarmy':
                self.admin_screen()
            else:
                self.user_screen()
        else:
            self.login_failure("username & password invalid", .65, .455)
            self.clear_verify()
            self.clear_login_screen()
            self.login_screen()


# ======================================================
#            TOOLTIP CLASS
# ======================================================
# Found the original code at:
# http://code.activestate.com/recipes/576688-tooltip-for-tkinter/
# ======================================================


class ToolTip(tk.Toplevel):

    def __init__(self, wdgt, tooltip_font, msg=None, msgFunc=None, delay=1, follow=True):
        """
        Initialize the ToolTip
        Arguments:
        wdgt: The widget this ToolTip is assigned to
        tooltip_font: Font to be used
        msg:  A static string message assigned to the ToolTip
        msgFunc: A function that retrieves a string to use as the ToolTip text
        delay:   The delay in seconds before the ToolTip appears(may be float)
        follow:  If True, the ToolTip follows motion, otherwise hides
        """
        self.wdgt = wdgt
        # The parent of the ToolTip is the parent of the ToolTips widget
        self.parent = self.wdgt.master
        # Initalise the Toplevel
        tk.Toplevel.__init__(self, self.parent, bg='black', padx=1, pady=1)
        # Hide initially
        self.withdraw()
        # The ToolTip Toplevel should have no frame or title bar
        self.overrideredirect(True)
        # The msgVar will contain the text displayed by the ToolTip
        self.msgVar = tk.StringVar()
        if msg is None:
            self.msgVar.set('No message provided')
        else:
            self.msgVar.set(msg)
            self.msgFunc = msgFunc
            self.delay = delay
            self.follow = follow
            self.visible = 0
            self.lastMotion = 0
            # The text of the ToolTip is displayed in a Message widget
            tk.Message(self, textvariable=self.msgVar, bg='#FFFFDD',
                       font=tooltip_font, aspect=1000).grid()
            # Add bindings to the widget.  This will NOT override
            # bindings that the widget already has
            self.wdgt.bind('<Enter>', self.spawn, '+')
            self.wdgt.bind('<Leave>', self.hide, '+')
            self.wdgt.bind('<Motion>', self.move, '+')

    def spawn(self, event=None):
        """
        Spawn the ToolTip.  This simply makes the ToolTip eligible for display.
        Usually this is caused by entering the widget
        Arguments:
        event: The event that called this funciton
        """
        self.visible = 1
        # The after function takes a time argument in miliseconds
        self.after(int(self.delay * 1000), self.show)

    def show(self):
        """
        Displays the ToolTip if the time delay has been long enough
        """
        if self.visible == 1 and time() - self.lastMotion > self.delay:
            self.visible = 2
        if self.visible == 2:
            self.deiconify()

    def move(self, event):
        """
        Processes motion within the widget.
        Arguments:
        event: The event that called this function
        """
        self.lastMotion = time()
        # If the follow flag is not set, motion within the
        # widget will make the ToolTip disappear
        if self.follow is False:
            self.withdraw()
            self.visible = 1
        # Offset the ToolTip 10x10 pixes southwest of the pointer
        self.geometry('+%i+%i' % (event.x_root + 10, event.y_root - 350))
        try:
            # Try to call the message function.  Will not change
            # the message if the message function is None or
            # the message function fails
            self.msgVar.set(self.msgFunc())
        except:
            pass
        self.after(int(self.delay * 1000), self.show)

    def hide(self, event=None):
        """
        Hides the ToolTip.  Usually this is caused by leaving the widget
        Arguments:
        event: The event that called this function
        """
        self.visible = 0
        self.withdraw()


# ===========================================================
# End of Class ToolTip
# ===========================================================

# ----------------------------------------------------------------------
# everything above this line
# ----------------------------------------------------------------------


if __name__ == '__main__':
    StartGui().mainloop()

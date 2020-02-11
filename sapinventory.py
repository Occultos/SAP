import tkinter as tk
import re
from passlib.hash import pbkdf2_sha256
from time import *
import shutil
import yagmail
import os

# git notes:
#     only do once
# git clone https://github.com/Occultos/SAP.git
# git config --global user.email "you@mail.com"
#     uploading new file
# git add sapinventory.py
# git commit -m "words of whats new"
# git push
#     downloading newest files
# git pull

# TODO: go to login_verify line 950ish to skip login
# noinspection PyAttributeOutsideInit,PyMethodMayBeStatic
class StartGui(tk.Tk):
    """starting gui here"""

    #  help( shows everything about StartGui )
    #  print(help(StartGui))
    def __init__(self):
        super().__init__()
        # ============================================================================================
        #                                               MISC. - INIT
        # ============================================================================================
        self.state('zoomed')  # TODO: maxscreensize DOESN"T WORK ON MAC, fix this
        self.resizable(0, 0)  # TODO: don't allow resizing, DISABLE ON MAC DUE TO 'zoomed' not working
        # self.resizable(1, 1) # TODO: don't allow resizing, DISABLE ON MAC DUE TO 'zoomed' not working
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)
        self.title("Salvation Army Pantry Inventory")  # app title
        self.iconbitmap(r'salogo_YMx_icon.ico')  # icon
        self._bgcolor = 'white'
        self._activebgcolor = '#e4fcdc'
        self._font = "Helvetica"
        self._font_big = 26
        self._font_big_big = 34
        self._font_medium = 22
        self._font_small = 18
        self._fgcolor = '#ff9194'
        self._fgcolor2 = '#ac73fb'
        # make a dict
        self.d = {}

        # ============================================================================================
        #                                              buttons - INIT
        # ============================================================================================
        # exit program button
        self.exitButton = tk.Button(self, text="Exit",
                                    background=self._bgcolor, font=(self._font, self._font_big),
                                    command=quit)
        self.exitButton.configure(activebackground=self._activebgcolor, padx=25)
        self.exitButton.place(relx=.9, rely=.9)

        # load login screen
        # choose login or registration screen
        self.login_info_button = tk.Button(self, text="Login",
                                           background=self._fgcolor, font=(self._font, self._font_big),
                                           command=lambda: self.login_info_screen())
        self.login_info_button.configure(activebackground=self._activebgcolor, padx=66)

        # load registration
        # choose login or registration screen
        self.registration_info_button = tk.Button(self, text="Register",
                                                  background=self._fgcolor, font=(self._font, self._font_big),
                                                  command=lambda: self.registration_info_screen())
        self.registration_info_button.configure(activebackground=self._activebgcolor, padx=45)

        # login button
        self.loginbutton = tk.Button(self, text="Login",
                                     background=self._fgcolor, font=(self._font, self._font_big),
                                     command=lambda: self.login_verify())
        self.loginbutton.configure(activebackground=self._activebgcolor, padx=66)

        # back button to return to previous screen
        self.backup_button = tk.Button(self, text="Back",
                                       background=self._bgcolor, font=(self._font, self._font_big),
                                       command=lambda: self.back_button_func(self.previous_view))
        self.backup_button.configure(activebackground=self._activebgcolor, padx=25)

        # TODO: new : back button with dictionary
        self.backup_button_with_d_button = tk.Button(self, text="Back",
                                                     background=self._bgcolor, font=(self._font, self._font_big),
                                                     command=lambda: self.backup_button_with_d(self.d, "user_screen"))
        self.backup_button_with_d_button.configure(activebackground=self._activebgcolor, padx=25)

        # logoutButton
        self.logoutButton = tk.Button(self, text="Logout",
                                      background=self._bgcolor, font=(self._font, self._font_big),
                                      command=lambda: self.login_screen())
        self.logoutButton.configure(activebackground=self._activebgcolor, padx=25)

        # TODO: new : logoutButton with dictionary
        self.logoutButton_with_d = tk.Button(self, text="Logout",
                                             background=self._bgcolor, font=(self._font, self._font_big),
                                             command=lambda: self.logout_with_d(self.d, "user_screen"))
        self.logoutButton_with_d.configure(activebackground=self._activebgcolor, padx=25)

        # register account button
        self.registerbutton = tk.Button(self, text="Register",
                                        background=self._fgcolor, font=(self._font, self._font_big),
                                        command=lambda: self.register_user())

        self.registerbutton.configure(activebackground=self._activebgcolor, padx=45)

        # eyeball to show/hide passwords
        self.eyeball_closed_photo = tk.PhotoImage(file="closedeye.png").subsample(9, 9)
        self.eyeball_open_photo = tk.PhotoImage(file="openeye.png").subsample(9, 9)

        self.eyeball_button = tk.Button(self, image=self.eyeball_closed_photo, text='closed',
                                        command=lambda: self.swap_eyeball())
        '''
        # add items button screen
        self.adjust_inventory_button = tk.Button(self, text="Adjust Inventory",
                                                 background=self._fgcolor, font=(self._font, self._font_medium),
                                                 command=lambda: self.adjust_inventory_button_cmd())
        self.adjust_inventory_button.configure(activebackground=self._activebgcolor, padx=9)
        '''
        # =================================================================================
        # buttons in user add items screen
        # ==================================================================================
        # choose an item
        self.choose_an_item_button = tk.Button(self, text="Choose An Item",
                                               background=self._fgcolor, font=(self._font, self._font_medium),
                                               command=lambda: self.choose_an_item_to_change_cmd(self.d))
        self.choose_an_item_button.configure(activebackground=self._activebgcolor, padx=47)

        # choose a different item
        self.choose_new_item = tk.Button(self, text="Choose a New Item",
                                         background=self._fgcolor, font=(self._font, self._font_medium),
                                         command=lambda: self.adjust_item_quantity_button_cmd(self.d))
        self.choose_new_item.configure(activebackground=self._activebgcolor, padx=24)

        # manual entry button
        self.manual_entry_button = tk.Button(self, text="Manual Entry",
                                             background=self._fgcolor, font=(self._font, self._font_medium),
                                             command=lambda: self.manual_entry_screen())
        self.manual_entry_button.configure(activebackground=self._activebgcolor, padx=25)

        # button inside manual entry screen
        self.adjust_item_quantity_button = tk.Button(self, text="Adjust Item Quantity",
                                                     font=(self._font, self._font_medium), background=self._fgcolor,
                                                     command=lambda: self.adjust_item_quantity_button_cmd(self.d))
        self.adjust_item_quantity_button.configure(activebackground=self._activebgcolor, padx=20)

        # change value of items, currently in manual entry screen
        self.change_value_button = tk.Button(self, text="Change Value",
                                             font=(self._font, self._font_medium), background=self._fgcolor,
                                             command=lambda: self.change_value_of_item_chosen(self.d))
        self.change_value_button.configure(activebackground=self._activebgcolor, padx=20)

        # submit button
        self.submit_changes_button = tk.Button(self, text="Submit",
                                               font=(self._font, self._font_medium), background=self._fgcolor,
                                               command=lambda: self.submit_changes_button_cmd(self.d))
        self.submit_changes_button.configure(activebackground=self._activebgcolor, padx=20)

        self.add_button = tk.Button(self, text="Add",
                                    font=(self._font, self._font_medium), background=self._fgcolor,
                                    command=lambda: self.confirm_item_change('up'))
        self.add_button.configure(activebackground=self._activebgcolor, padx=30)

        self.subtract_button = tk.Button(self, text="Subtract",
                                         font=(self._font, self._font_medium), background=self._fgcolor,
                                         command=lambda: self.confirm_item_change('down'))
        self.subtract_button.configure(activebackground=self._activebgcolor)

        self.confirm_inventory_manual_button = tk.Button(self, text="Confirm",
                                                         font=(self._font, self._font_medium), background=self._fgcolor,
                                                         command=lambda: self.confirm_inventory_manual_button_cmd())
        self.confirm_inventory_manual_button.configure(activebackground=self._activebgcolor)

        self.cancel_inventory_manual_button = tk.Button(self, text="Cancel",
                                                        font=(self._font, self._font_medium), background=self._fgcolor,
                                                        command=lambda: self.back_button_func(self.previous_view))
        self.cancel_inventory_manual_button.configure(activebackground=self._activebgcolor)

        # ======================================================================================
        #            barcode screen buttons
        # =======================================================================================
        # barcode scanner button
        self.barcode_scanner_button = tk.Button(self, text="Barcode Scan",
                                                background=self._fgcolor, font=(self._font, self._font_medium),
                                                command=lambda: self.barcode_scanner_screen())
        self.barcode_scanner_button.configure(activebackground=self._activebgcolor, padx=18)

        # submit changes made with barcode scanner
        self.barcode_scanner_submit_button = tk.Button(self, text="Submit Barcode Scan",
                                                       background=self._fgcolor, font=(self._font, self._font_medium),
                                                       command=lambda: self.barcode_scanner_submit_button_cmd())
        self.barcode_scanner_submit_button.configure(activebackground=self._activebgcolor)

        # go to add or remove items screen using barcode
        self.barcode_scanner_add_button = tk.Button(self, text="Add items",
                                                    background=self._fgcolor, font=(self._font, self._font_medium),
                                                    command=lambda: self.barcode_scanner_add_remove_button_cmd(
                                                        'adding to '))
        self.barcode_scanner_add_button.configure(activebackground=self._activebgcolor, padx=29)

        # go to add or remove items screen using barcode
        self.barcode_scanner_remove_button = tk.Button(self, text="Remove items",
                                                       background=self._fgcolor, font=(self._font, self._font_medium),
                                                       command=lambda: self.barcode_scanner_add_remove_button_cmd(
                                                           'removing from '))
        self.barcode_scanner_remove_button.configure(activebackground=self._activebgcolor)

        # ==========================================================================
        #                     Create new inventory item
        # ==========================================================================
        self.create_new_item_button = tk.Button(self, text="Create New Item",
                                                font=(self._font, self._font_medium), background=self._fgcolor,
                                                command=lambda: self.create_new_item_screen(self.d))
        self.create_new_item_button.configure(activebackground=self._activebgcolor)

        # TODO: new: submit changes made with add item
        self.create_new_item_submit_button = tk.Button(self, text="Submit New Item",
                                                       background=self._fgcolor, font=(self._font, self._font_medium),
                                                       command=lambda: self.create_new_item_submit_button_cmd(self.d))
        self.create_new_item_submit_button.configure(activebackground=self._activebgcolor)

        # ===========================================================================
        #             View inventory in user view
        # ==========================================================================

        # view inventory button
        self.display_inventory_user_button = tk.Button(self, text="View Inventory",
                                                       font=(self._font, self._font_medium), background=self._fgcolor,
                                                       command=lambda: self.display_inventory_user_button_cmd())
        self.display_inventory_user_button.configure(activebackground=self._activebgcolor, padx=16)

        # ========================================================================
        #                    Admin screen buttons
        # ========================================================================

        # view inventory button
        self.display_inventory_button = tk.Button(self, text="View Inventory",
                                                  font=(self._font, self._font_medium), background=self._fgcolor,
                                                  command=lambda: self.swap_inventory_button())
        self.display_inventory_button.configure(activebackground=self._activebgcolor, padx=14)

        # view users
        self.display_users_button = tk.Button(self, text="View Users",
                                              font=(self._font, self._font_medium), background=self._fgcolor,
                                              command=lambda: self.swap_display_users_button())
        self.display_users_button.configure(activebackground=self._activebgcolor, padx=32)

        # Edit inventory
        self.edit_inventory_button = tk.Button(self, text="Edit Inventory",
                                              font=(self._font, self._font_medium), background=self._fgcolor,
                                              command=lambda: self.edit_inventory_button_cmd(self.d))
        self.edit_inventory_button.configure(activebackground=self._activebgcolor, padx=20)

        # choose an item to edit admin
        self.choose_an_item_to_edit_button = tk.Button(self, text="Choose An Item",
                                               background=self._fgcolor, font=(self._font, self._font_medium),
                                               command=lambda: self.choose_an_item_to_edit_button_cmd(self.d))
        self.choose_an_item_to_edit_button.configure(activebackground=self._activebgcolor, padx=47)

        # delete users : in admin screen
        self.delete_user_button = tk.Button(self, text="Delete User", font=(self._font, self._font_medium),
                                            background=self._fgcolor2,
                                            command=lambda: self.remove_username_func())
        self.delete_user_button.config(activebackground=self._activebgcolor, padx=29)

        # open email entry
        self.admin_email_inventory_button = tk.Button(self, text="Email inventory", background=self._fgcolor,
                                                      font=(self._font, self._font_medium),
                                                      command=lambda: self.email_entry(self.d))
        self.admin_email_inventory_button.configure(activebackground=self._activebgcolor, padx=9)

        # send email
        self.admin_email_send_button = tk.Button(self, text="Send", background=self._fgcolor,
                                                 font=(self._font, self._font_medium),
                                                 command=lambda: self.admin_email_inventory(self.d))
        self.admin_email_send_button.configure(activebackground=self._activebgcolor)

        # =============================================================================
        #                 END Admin screen buttons
        # =============================================================================

        # remove bag button after logging in
        self.make_bag_screen_button = tk.Button(self, text="Make A New Bag",
                                                background=self._fgcolor, font=(self._font, self._font_medium),
                                                command=lambda: self.make_bag_screen())
        self.make_bag_screen_button.configure(activebackground=self._activebgcolor)

        # make A bag button
        self.make_ONE_bag_button = tk.Button(self, text="Make ONE Full bag",
                                             background=self._fgcolor, font=(self._font, self._font_medium),
                                             command=lambda: self.made_a_bag_screen(self.d))
        self.make_ONE_bag_button.configure(activebackground=self._activebgcolor)

        # make ANOTHER bag
        self.make_another_bag_button = tk.Button(self, text="Make ANOTHER bag",
                                                 background=self._fgcolor, font=(self._font, self._font_medium),
                                                 command=lambda: self.back_button_func(self.previous_view))
        self.make_another_bag_button.configure(activebackground=self._activebgcolor, padx=10)

        # ========================================================================================
        #                                            labels - INIT
        # =======================================================================================

        self.loginlabel = tk.Label(self, text="Inventory Managment Login", font=(self._font, self._font_big))
        self.help_label = tk.Label(self, text="Registration Help",
                                   background='#c1bcf5', font=(self._font, self._font_medium))
        self.help_label.configure(padx=20, pady=15)
        self.admin_email_label = tk.Label(self, text="Email sent", font=(self._font, self._font_big))
        # registration errors username exists, to short, has a space in it.
        # pw too short, has a space in it
        self.registration_info_error = tk.Label(self, font=(self._font, self._font_medium), fg='red')
        self.user_register_success = tk.Label(self, font=(self._font, self._font_medium),
                                              text="Successfully Registered")
        self.login_info_error = tk.Label(self, font=(self._font, self._font_medium))
        self.food_file_error_label = tk.Label(self, font=(self._font, self._font_small),
                                              text="food.txt file missing")
        self.bag_of_food_removed_from_inventory = tk.Label(self, font=(self._font, self._font_small),
                                                           text="1 bag of food removed from inventory")
        # ==================================================================
        #                    new item labels
        # ==================================================================
        self.create_new_item = tk.Label(self, font=(self._font, self._font_big),
                                        text="Create new item screen")
        self.create_new_item_name = tk.Label(self, font=(self._font, self._font_small),
                                             text="Item Name: ")
        self.create_new_item_amount = tk.Label(self, font=(self._font, self._font_small),
                                               text="Current amount: ")
        self.create_new_item_low_level = tk.Label(self, font=(self._font, self._font_small),
                                                  text="Low amount warning at: ")
        self.create_new_item_weight = tk.Label(self, font=(self._font, self._font_small),
                                               text="Item weight: ")
        self.create_new_item_barcode = tk.Label(self, font=(self._font, self._font_small),
                                                text="Barcode: ")
        self.create_new_submit_error = tk.Label(self, font=(self._font, self._font_small),
                                                text="All boxes need to be filled")
        self.create_new_submit_error_alpha = tk.Label(self, font=(self._font, self._font_small),
                                                      text="Name needs to be letters only")
        self.create_new_submit_error_num = tk.Label(self, font=(self._font, self._font_small),
                                                    text="Amount, Low level, Weight, and Barcode\nall need to be numbers only")

        self.create_new_added = tk.Label(self, font=(self._font, self._font_small),
                                         text="Added item")
        # ==================================================================
        #                    end new item labels
        # ==================================================================

        self.todo_label = tk.Label(self,
                                   text="TODO: more stuff here and delete this label afterwards",
                                   font=(self._font, self._font_medium))
        self.addresslabel = tk.Label(self, text="The Salvation Army of San Antonio"
                                                " Metropolitian Area Command\n"
                                                "521 W. Elmira\n"
                                                "San Antonio, TX 78212",
                                     font=(self._font, self._font_medium))
        self.username_label = tk.Label(self, text="User Name :", font=(self._font, self._font_big))
        self.passwordlabel = tk.Label(self, text="Password :", font=(self._font, self._font_big))
        self.password_verify_label = tk.Label(self, text="Confirm Password :", font=(self._font, self._font_big))
        self.username_for_event_log = tk.Label(self, font=(self._font, self._font_big))
        self.enter_email_add_label = tk.Label(self, font=(self._font, self._font_big))
        self.item_to_be_changed_label_1 = tk.Label(self, font=(self._font, self._font_big))
        self.item_to_be_changed_label_2 = tk.Label(self, font=(self._font, self._font_big))
        self.item_to_be_changed_label_3 = tk.Label(self, font=(self._font, self._font_big))

        self.barcode_scanner_label = tk.Label(self, font=(self._font, self._font_big))
        self.list_of_items_label = tk.Label(self, text='', font=(self._font, self._font_small))
        self.list_of_items_label.configure(justify=tk.LEFT)
        # invalid entry label
        self.invalid_entry_error_label = tk.Label(self, font=(self._font, self._font_big), fg='red')

        # ======================================================================================
        #                                         SA army logo - INIT
        # ======================================================================================
        self.login_army_logo = tk.PhotoImage(file="SA_doing_the_most_good.png").subsample(3, 3)
        self.login_army_label = tk.Label(self, image=self.login_army_logo)
        self.image = self.login_army_logo  # save a reference through garbarge pickup

        # =======================================================================================
        #                                           TOOLTIP - INIT
        # =======================================================================================

        ToolTip(self.help_label, self._font, '''Username must be atleast 8 letters\n
Only use letters a-z for username\n
Password must be 8-20 characters\n
Password must contain atleast:\n
one uppercase,\n
one lowercase, \n
one number,\n
one special character: !@#$%*?\n''', delay=.25)

        # =======================================================================================
        #                                         entry boxes - INIT
        # =======================================================================================
        self.username_verify = tk.StringVar()
        self.username_verify.set('')
        self.username_entry = tk.Entry(self, font=(self._font, self._font_big),
                                       textvariable=self.username_verify)
        self.password_verify = tk.StringVar()
        self.password_verify.set('')
        self.password_entry = tk.Entry(self, font=(self._font, self._font_big),
                                       textvariable=self.password_verify, show='*')
        self.password_compare_verify = tk.StringVar()
        self.password_compare_verify.set('')
        self.password_compare_entry = tk.Entry(self, font=(self._font, self._font_big),
                                               textvariable=self.password_compare_verify, show='*')

        self.email_add = tk.StringVar()
        self.email_add.set('')
        self.enter_email_add_entry = tk.Entry(self, font=(self._font, self._font_big),
                                              textvariable=self.email_add)
        self.enter_email_add_entry.configure(width=35)

        # changing inventory entry box
        self.change_inventory_by_this_much = tk.StringVar()
        self.adjust_inventory_entry = tk.Entry(self, font=(self._font, self._font_big),
                                               textvariable=self.change_inventory_by_this_much, width=4)

        # barcode scanner entry box
        self.barcode_scanner_input = tk.StringVar()
        self.barcode_scanner_input_entry = tk.Entry(self, font=(self._font, self._font_big),
                                                    textvariable=self.barcode_scanner_input, width=20)
        # ===============================================================
        #                      new items entry
        # ==============================================================
        # create new item entry box (temps)
        self.create_new_item_input = tk.StringVar()
        self.create_new_item_input_entry = tk.Entry(self, font=(self._font, self._font_big),
                                                    textvariable=self.create_new_item_input, width=20)

        self.create_new_item_input_amount = tk.StringVar()
        self.create_new_item_input_amount_entry = tk.Entry(self, font=(self._font, self._font_big),
                                                           textvariable=self.create_new_item_input_amount, width=20)

        self.create_new_item_input_low_level = tk.StringVar()
        self.create_new_item_input_low_level_entry = tk.Entry(self, font=(self._font, self._font_big),
                                                              textvariable=self.create_new_item_input_low_level,
                                                              width=20)

        self.create_new_item_input_weight = tk.StringVar()
        self.create_new_item_input_weight_entry = tk.Entry(self, font=(self._font, self._font_big),
                                                           textvariable=self.create_new_item_input_weight, width=20)

        self.create_new_item_input_barcode = tk.StringVar()
        self.create_new_item_input_barcode_entry = tk.Entry(self, font=(self._font, self._font_big),
                                                            textvariable=self.create_new_item_input_barcode, width=20)

        # =======================================================================================
        #                                    list boxes and labels - INIT
        # ======================================================================================
        self.list_box_1 = tk.Listbox(self, font=(self._font, self._font_small))
        self.list_box_2 = tk.Listbox(self, font=(self._font, self._font_small))
        self.list_box_3 = tk.Listbox(self, font=(self._font, self._font_small))
        self.list_box_1_label = tk.Label(self, font=(self._font, self._font_medium), text="OUT OF STOCK")
        self.list_box_2_label = tk.Label(self, font=(self._font, self._font_medium), text="LOW INVENTORY")
        self.list_box_3_label = tk.Label(self, font=(self._font, self._font_medium), text="INVENTORY")

        # =====================================================================================
        #                                         check buttons - INIT
        # =====================================================================================
        # TODO: 1 big or 2 small cans  : OR
        # TODO: bag of rice or beans : OR
        # self.variable = IntVar()
        # onvalue = "RGB", offvalue = "L"
        # self.var.get()

        self.checkbutton_label = tk.Label(self, text="only select MISSING items",
                                          font=(self._font, self._font_medium))

        self.vegetable_can_var = tk.IntVar()
        self.vegetable_cans_4_checkbutton = tk.Checkbutton(self,
                                                           text="4 cans of vegetable items",
                                                           variable=self.vegetable_can_var,
                                                           font=(self._font, self._font_medium), onvalue=0, offvalue=4)
        self.vegetable_cans_4_checkbutton.configure(activebackground=self._activebgcolor, padx=10)

        self.fruit_can_var = tk.IntVar()
        self.fruit_cans_3_checkbutton = tk.Checkbutton(self, text="3 fruit cans",
                                                       variable=self.fruit_can_var,
                                                       font=(self._font, self._font_medium), onvalue=0, offvalue=3)
        self.fruit_cans_3_checkbutton.configure(activebackground=self._activebgcolor, padx=10)

        self.meat_var = tk.IntVar()
        self.meat_3_checkbutton = tk.Checkbutton(self, text="3 meat items",
                                                 variable=self.meat_var,
                                                 font=(self._font, self._font_medium), onvalue=0, offvalue=3)
        self.meat_3_checkbutton.configure(activebackground=self._activebgcolor, padx=10)

        self.soup_can_var = tk.IntVar()
        self.soup_can_1_large_checkbutton = tk.Checkbutton(self, variable=self.soup_can_var,
                                                           text="1 large soup can or 2 small cans",
                                                           font=(self._font, self._font_medium), onvalue=0, offvalue=1)
        self.soup_can_1_large_checkbutton.configure(activebackground=self._activebgcolor, padx=10)

        self.spaghetti_sauce_var = tk.IntVar()
        self.spaghetti_sauce_1_checkbutton = tk.Checkbutton(self, text="1 spaghetti sauce can",
                                                            variable=self.spaghetti_sauce_var,
                                                            font=(self._font, self._font_medium), onvalue=0, offvalue=1)
        self.spaghetti_sauce_1_checkbutton.configure(activebackground=self._activebgcolor, padx=10)

        self.tomato_sauce_var = tk.IntVar()
        self.tomato_sauce_2_checkbutton = tk.Checkbutton(self, text="2 cans of tomato sauce",
                                                         variable=self.tomato_sauce_var,
                                                         font=(self._font, self._font_medium), onvalue=0, offvalue=2)
        self.tomato_sauce_2_checkbutton.configure(activebackground=self._activebgcolor, padx=10)

        self.bean_can_var = tk.IntVar()
        self.beans_can_1_checkbutton = tk.Checkbutton(self, text="1 can of beans",
                                                      variable=self.bean_can_var,
                                                      font=(self._font, self._font_medium), onvalue=0, offvalue=2)
        self.beans_can_1_checkbutton.configure(activebackground=self._activebgcolor, padx=10)

        self.ravioli_var = tk.IntVar()
        self.ravioli_1_checkbutton = tk.Checkbutton(self, text="1 can of ravioli",
                                                    variable=self.ravioli_var,
                                                    font=(self._font, self._font_medium), onvalue=0, offvalue=1)
        self.ravioli_1_checkbutton.configure(activebackground=self._activebgcolor, padx=10)

        self.peanut_butter_var = tk.IntVar()
        self.peanut_butter_1_checkbutton = tk.Checkbutton(self, text="1 peanut butter",
                                                          variable=self.peanut_butter_var,
                                                          font=(self._font, self._font_medium), onvalue=0, offvalue=1)
        self.peanut_butter_1_checkbutton.configure(activebackground=self._activebgcolor, padx=10)

        self.jelly_var = tk.IntVar()
        self.jelly_1_checkbutton = tk.Checkbutton(self, text="1 jelly",
                                                  variable=self.jelly_var,
                                                  font=(self._font, self._font_medium), onvalue=0, offvalue=1)
        self.jelly_1_checkbutton.configure(activebackground=self._activebgcolor, padx=10)

        self.mac_cheese_var = tk.IntVar()
        self.mac_cheese_2_checkbutton = tk.Checkbutton(self, text="2 boxes of mac and cheese",
                                                       variable=self.mac_cheese_var,
                                                       font=(self._font, self._font_medium), onvalue=0, offvalue=2)
        self.mac_cheese_2_checkbutton.configure(activebackground=self._activebgcolor, padx=10)

        self.bag_rice_var = tk.IntVar()
        self.bag_rice_1_checkbutton = tk.Checkbutton(self, text="1 bag of rice/bean",
                                                     variable=self.bag_rice_var,
                                                     font=(self._font, self._font_medium), onvalue=0, offvalue=1)
        self.bag_rice_1_checkbutton.configure(activebackground=self._activebgcolor, padx=10)

        self.juice_var = tk.IntVar()
        self.juice_1_checkbutton = tk.Checkbutton(self, text="1 juice or drink",
                                                  variable=self.juice_var,
                                                  font=(self._font, self._font_medium), onvalue=0, offvalue=1)
        self.juice_1_checkbutton.configure(activebackground=self._activebgcolor, padx=10)

        self.snacks_var = tk.IntVar()
        self.snacks_5_checkbutton = tk.Checkbutton(self, text="5 snacks",
                                                   variable=self.snacks_var,
                                                   font=(self._font, self._font_medium), onvalue=0, offvalue=5)
        self.snacks_5_checkbutton.configure(activebackground=self._activebgcolor, padx=10)

        self.misc_var = tk.IntVar()
        self.misc_1_checkbutton = tk.Checkbutton(self, text="1 miscellaneous item",
                                                 variable=self.misc_var,
                                                 font=(self._font, self._font_medium), onvalue=0, offvalue=1)
        self.misc_1_checkbutton.configure(activebackground=self._activebgcolor, padx=10)

        self.cereal_var = tk.IntVar()
        self.cereal_1_checkbutton = tk.Checkbutton(self, text="1 cereal",
                                                   variable=self.cereal_var,
                                                   font=(self._font, self._font_medium), onvalue=0, offvalue=1)
        self.cereal_1_checkbutton.configure(activebackground=self._activebgcolor, padx=10)

        self.nuts_var = tk.IntVar()
        self.nuts_1_checkbutton = tk.Checkbutton(self, text="1 large bag of nuts",
                                                 variable=self.nuts_var,
                                                 font=(self._font, self._font_medium), onvalue=0, offvalue=1)
        self.nuts_1_checkbutton.configure(activebackground=self._activebgcolor, padx=10)

        # starting program at the login screen
        self.login_screen()

    # =====================================================================================
    #                                    ^^^^^^^^  END OF INIT ^^^^^^^^^^
    # =====================================================================================

    # usable functions
    # ======================================================================================
    #                                           MISC Functions
    # ======================================================================================

    # hides or shows password
    def swap_eyeball(self):
        eyeball_text = self.eyeball_button.cget('text')
        if eyeball_text == 'closed':
            self.eyeball_button.config(image=self.eyeball_open_photo, text='open')
            self.password_entry.config(show='')
            self.password_compare_entry.config(show='')
        else:
            self.eyeball_button.config(image=self.eyeball_closed_photo, text='closed')
            self.password_entry.config(show='*')
            self.password_compare_entry.config(show='*')

    # =====================================================================================
    #                                                BACKUP
    # =====================================================================================
    # TODO: new:
    def backup_button_with_d(self, d, words):
        # This is for removing labels from create new item that pass d
        if words == "user_screen":
            self.clear_create_new_item(d)

    def logout_with_d(self, d, words):
        # This is for removing labels from create new item that pass d with logout button
        if words == "user_screen":
            self.backup_button_with_d(d, "user_screen")
            self.logoutButton_with_d.place_forget()
            self.login_screen()

    def back_button_func(self, words):
        # goes back to user screen
        if words == "user_screen":
            self.clear_makebag_screen()
            self.user_screen()
            self.clear_todo_label()
            self.clear_list_box()
            self.bag_of_food_removed_from_inventory.place_forget()
            self.adjust_item_quantity_button.place_forget()
            self.choose_an_item_button.place_forget()
            self.choose_an_item_to_edit_button.place_forget()
            self.clear_barcode_screen()
            self.unbind_return_func()
            self.list_of_items_words = ''
            self.list_of_items_label.place_forget()
        # goes back to make a bag screen
        elif words == "make_bag_screen":
            self.make_bag_screen()
            self.clear_todo_label()
            self.clear_list_box()
            self.make_another_bag_button.place_forget()
            self.food_file_error_label.place_forget()
            self.bag_of_food_removed_from_inventory.place_forget()
            self.invalid_entry_error_label.place_forget()
        elif words == "login_screen":
            self.clear_login_info_screen()
            self.clear_login_info_error()
            self.clear_registration_errors()
            self.clear_registration_success()
            self.login_screen()
            self.eyeball_button.place_forget()
        elif words == "manual_entry_screen":
            self.clear_user_screen()
            self.manual_entry_screen()
            self.submit_changes_button.place_forget()
            self.invalid_entry_error_label.place_forget()
            self.subtract_button.place_forget()
            self.add_button.place_forget()
            self.item_to_be_changed_label_1.place_forget()
            self.item_to_be_changed_label_2.place_forget()
            self.change_value_button.place_forget()
            self.adjust_inventory_entry.place_forget()
        elif words == "choose_item_screen":
            self.item_to_be_changed_label_1.place_forget()
            self.item_to_be_changed_label_2.place_forget()
            self.adjust_item_quantity_button_cmd(self.d)
            self.choose_new_item.place_forget()
            self.adjust_inventory_entry.place_forget()
            self.add_button.place_forget()
            self.subtract_button.place_forget()
            self.invalid_entry_error_label.place_forget()
            self.confirm_inventory_manual_button.place_forget()
            self.cancel_inventory_manual_button.place_forget()

    # ====================================================================================
    #                                   EMAIL Functions
    # ===================================================================================
    def email_entry(self, d):
        self.admin_email_label.place_forget()
        self.enter_email_add_label.configure(text='Enter Email Address', font=(self._font, self._font_big))
        place_object(self.enter_email_add_label, .2, .9175)
        place_object(self.enter_email_add_entry, .3675, .92, True)
        place_object(self.admin_email_send_button, .73, .9125)

    def admin_email_inventory(self, d):
        self.print_dict_to_file(d)
        place_object(self.admin_email_label, .68, .9275)
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
            # print("error " + str(e))
            self.admin_email_label.configure(text="Email error", font=(self._font, self._font_big))
        self.email_add.set('')
        self.enter_email_add_label.place_forget()
        self.enter_email_add_entry.place_forget()
        self.admin_email_send_button.place_forget()

    # ===================================================================================
    #                                                 SCREENS
    # ===================================================================================

    # main login screen
    def login_screen(self):
        #    SA army logo
        self.army_image_place()
        # login screen label
        self.loginlabel.place(relx=.420, rely=.30)
        # login screen address
        self.addresslabel.place(relx=.32, rely=.85)
        # load login screen
        self.login_info_button.place(relx=.47, rely=.4)
        # load registration screen
        self.registration_info_button.place(relx=.47, rely=.5)
        # remove other buttons
        self.clear_to_login()

    def admin_screen(self):
        self.clear_login_screen()
        self.logout_button_place()
        self.clear_login_info_error()
        self.army_image_place()
        self.eyeball_button.place_forget()
        place_object(self.admin_email_inventory_button, .845, .835)
        place_object(self.display_inventory_button, .845, .77)
        place_object(self.display_users_button, .845, .705)
        # TODO edit inventory option
        place_object(self.edit_inventory_button, .845, .64)

    def user_screen(self):
        self.clear_login_screen()
        self.logout_button_place()
        self.clear_login_info_error()
        self.backup_button.place_forget()
        self.eyeball_button.place_forget()
        self.army_image_place()
        # place_object(self.adjust_inventory_button, .47, .4)
        place_object(self.make_bag_screen_button, .47, .4)
        place_object(self.display_inventory_user_button, .47, .5)
        place_object(self.barcode_scanner_button, .47, .6)
        place_object(self.manual_entry_button, .47, .7)
        place_object(self.create_new_item_button, .47, .8)
        # self.backup_place()
        # self.previous_view = "user_screen"

    # load login screen
    def login_info_screen(self):
        # clears any passwords input
        self.clear_verify()
        # clear login/register buttons
        self.registration_info_button.place_forget()
        self.login_info_button.place_forget()
        # if just registered, clear this success warning
        self.clear_registration_success()
        # set eyeball
        self.password_entry.config(show='*')
        place_object(self.eyeball_button, .64, .45)
        # enter login info
        place_object(self.username_entry, .430, .4, True)
        place_object(self.password_entry, .430, .46)
        place_object(self.loginbutton, .47, .55)
        place_object(self.username_label, .303, .4)
        place_object(self.passwordlabel, .315, .46)
        self.backup_place()
        self.previous_view = "login_screen"

    # load registration screen
    def registration_info_screen(self):
        # clear any passwords
        self.clear_verify()
        # clear login/register buttons
        self.registration_info_button.place_forget()
        self.login_info_button.place_forget()
        self.clear_registration_success()
        # enter registration info
        place_object(self.username_entry, .430, .4, True)
        place_object(self.password_entry, .430, .46)
        place_object(self.password_compare_entry, .430, .52)
        place_object(self.username_label, .303, .4)
        place_object(self.passwordlabel, .315, .46)
        place_object(self.password_verify_label, .248, .5225)
        place_object(self.registerbutton, .47, .6)
        place_object(self.eyeball_button, .64, .45)
        self.backup_place()
        self.previous_view = "login_screen"
        # TODO: help labels
        # todo: confirm pw label

    # made a bag
    def made_a_bag_screen(self, d):
        # TODO: lowerinventory by appropriate ammount according to check buttons
        self.lower_inventory(d)
        # checkbuttons.placeforget & make_ONE_bag.placeforget
        self.clear_makebag_screen()
        self.previous_view = "make_bag_screen"
        self.make_another_bag_button.place(relx=.8, rely=.3)
        self.view_inventory_3_list_boxes(d)

    # make bag screen
    def make_bag_screen(self):
        self.clear_user_screen()
        self.checkbutton_label.place(relx=.75, rely=.4)
        self.make_ONE_bag_button.place(relx=.8, rely=.3)
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

    '''
    # in add items screen
    def adjust_inventory_button_cmd(self):
        # remove extra stuff
        self.clear_user_screen()
        # input options
        place_object(self.manual_entry_button, .47, .4)
        place_object(self.barcode_scanner_button, .47, .5)
        place_object(self.display_inventory_user_button, .47, .6)
        place_object(self.create_new_item_button, .47, .7)
        self.backup_place()
        self.previous_view = "user_screen"
        '''
    # ========================================================
    #                 barcode screen functions
    # =======================================================
    # in barcode scanner screen
    def barcode_scanner_screen(self):
        # self.list_of_items_label.config(text=self.list_of_items_words)
        # self.clear_adjust_inventory_screen()
        self.clear_user_screen()
        self.backup_place()
        self.previous_view = "user_screen"
        place_object(self.barcode_scanner_add_button, .47, .4)
        place_object(self.barcode_scanner_remove_button, .47, .5)
        self.list_of_items_words = 'Inventory Changes\n'
        self.list_of_items_label.config(text=self.list_of_items_words)

    def barcode_scanner_add_remove_button_cmd(self, direction):
        # TODO: show/hide inventory
        # TODO: add barcode & qty columns
        # TODO: add entry box
        # TODO: if entry box != 1, adjust by entry box amount
        # TODO: else adjust by 1 - use direction
        self.previous_view = "user_screen"
        self.clear_barcode_screen()
        self.barcode_scanner_label.configure(text=direction + 'inventory : begin scanning')
        place_object(self.barcode_scanner_label, .35, .25)
        place_object(self.barcode_scanner_input_entry, .4, .3, True)
        place_object(self.list_of_items_label, .7, .3)
        self.barcode_scanner_input.set("")
        self.bind('<Return>', lambda x: self.search_for_item_in_food_file(direction, self.barcode_scanner_input.get()))

    def barcode_scanner_submit_button_cmd(self):
        pass

    def unbind_return_func(self):
        self.unbind('<Return>')

    def search_for_item_in_food_file(self, direction, item_to_find):
        # TODO: show/hide inventory
        # TODO: add barcode & qty columns
        # TODO: add entry box
        # TODO: if entry box != 1, adjust by entry box amount
        # TODO: else adjust by 1 - use direction
        try:
            shutil.move("food.txt", "food.txt" + "~")
            with open("food.txt", "w+") as dest:
                dest.seek(0, os.SEEK_SET)
                with open("food.txt" + "~", "r+") as src:
                    src.seek(0, os.SEEK_SET)
                    for line in src:
                        if not re.match(r'^\s*$', line):
                            found = False
                            tokens = re.split(",", line.strip())
                            for ndex in range(len(tokens))[4:]:
                                if str(tokens[ndex].strip()) == str(item_to_find):
                                    if direction == 'adding to ':
                                        self.list_of_items_words = self.list_of_items_words + \
                                                                   'added ' + tokens[0] + ' ' + \
                                                                   str(item_to_find) + '\n'

                                        self.list_of_items_label.config(text=self.list_of_items_words)
                                        tokens[1] = str(int(tokens[1]) + 1)
                                    if direction == 'removing from ':
                                        self.list_of_items_words = self.list_of_items_words + 'removed ' + \
                                                                   tokens[0] + ' ' + str(item_to_find) + '\n'

                                        self.list_of_items_label.config(text=self.list_of_items_words)
                                        tokens[1] = str(int(tokens[1]) - 1)
                                    found = True
                                    dest.write(",".join(tokens) + '\n')
                            if found is False:
                                dest.write(line)
            self.barcode_scanner_add_remove_button_cmd(direction)
        except Exception as e:
            print("error writing to food file : " + str(e))

    # ===================================================================
    #               New items screen and functions
    # ==================================================================

    def create_new_item_screen(self, d):
        # creates blank screen
        self.clear_user_screen()
        self.logoutButton.place_forget()
        self.logout_button_place_with_d(d, "user_screen")
        self.backup_place_with_d(d, "user_screen")
        # self.forget_create_new_item_screens(self, d)

        self.previous_view = "user_screen"
        self.create_new_item.place(relx=.4, rely=.23)

        self.create_new_item_name.place(relx=.2, rely=.3)
        self.create_new_item_amount.place(relx=.2, rely=.4)
        self.create_new_item_low_level.place(relx=.2, rely=.5)
        self.create_new_item_weight.place(relx=.2, rely=.6)
        self.create_new_item_barcode.place(relx=.2, rely=.7)

        place_object(self.create_new_item_submit_button, .7, .5)

        place_object(self.create_new_item_input_entry, .4, .3, True)
        place_object(self.create_new_item_input_amount_entry, .4, .4, True)
        place_object(self.create_new_item_input_low_level_entry, .4, .5, True)
        place_object(self.create_new_item_input_weight_entry, .4, .6, True)
        place_object(self.create_new_item_input_barcode_entry, .4, .7, True)

    def create_new_item_submit_button_cmd(self, d):
        newItem = "\n" + self.create_new_item_input.get() + "," + \
                  str(self.create_new_item_input_amount_entry.get()) + ", " + \
                  str(self.create_new_item_input_low_level_entry.get()) + ", " + \
                  str(self.create_new_item_input_weight_entry.get()) + ", " + \
                  str(self.create_new_item_input_barcode_entry.get())

        allFilled = self.isAllFilled(newItem)
        if allFilled == 0:
            self.create_new_item_input.set("")
            self.create_new_item_input_amount.set("")
            self.create_new_item_input_low_level.set("")
            self.create_new_item_input_weight.set("")
            self.create_new_item_input_barcode.set("")
            self.create_new_item_screen(d)
        else:
            self.append_food(d, newItem)
            self.create_new_item_input.set("")
            self.create_new_item_input_amount.set("")
            self.create_new_item_input_low_level.set("")
            self.create_new_item_input_weight.set("")
            self.create_new_item_input_barcode.set("")

    def isAllFilled(self, d):
        if (self.create_new_item_input.get() == "" or
                str(self.create_new_item_input_amount_entry.get()) == "" or
                str(self.create_new_item_input_low_level_entry.get()) == "" or
                str(self.create_new_item_input_weight_entry.get()) == "" or
                str(self.create_new_item_input_barcode_entry.get()) == ""):
            place_object(self.create_new_submit_error, .692, .6)

            self.create_new_submit_error_alpha.place_forget()
            self.create_new_submit_error_num.place_forget()
            self.create_new_added.place_forget()
            return 0
        elif not self.create_new_item_input.get().isalpha():
            place_object(self.create_new_submit_error_alpha, .68, .6)

            self.create_new_submit_error.place_forget()
            self.create_new_submit_error_num.place_forget()
            self.create_new_added.place_forget()
            return 0
        elif (str(self.create_new_item_input_amount_entry.get()).isnumeric() == False or
              str(self.create_new_item_input_low_level_entry.get().isnumeric()) == False or
              str(self.create_new_item_input_weight_entry.get()).isnumeric() == False or
              str(self.create_new_item_input_barcode_entry.get()).isnumeric() == False):
            place_object(self.create_new_submit_error_num, .655, .6)

            self.create_new_submit_error_alpha.place_forget()
            self.create_new_submit_error.place_forget()
            self.create_new_added.place_forget()
            return 0
        else:
            # remove all other error labels
            self.create_new_submit_error.place_forget()
            self.create_new_submit_error_alpha.place_forget()
            self.create_new_submit_error_num.place_forget()
            self.create_new_added.place_forget()
            place_object(self.create_new_added, .73, .6)
            return 1

    def manual_entry_screen(self):
        # self.clear_adjust_inventory_screen()
        self.clear_user_screen()
        self.backup_place()
        self.view_inventory_3_list_boxes(self.d)
        self.previous_view = "user_screen"
        place_object(self.adjust_item_quantity_button, .8, .835)

    # =================================================================================
    #                                             Place functions
    # =================================================================================
    def backup_place(self):
        self.backup_button.place(relx=.02, rely=.9)

    # TODO: new:
    def backup_place_with_d(self, d, words):
        self.backup_button_with_d_button.place(relx=.02, rely=.9)

    def todo_label_place(self):
        self.todo_label.place(relx=.300, rely=.450)

    def logout_button_place(self):
        self.logoutButton.place(relx=.8, rely=.9)

    def logout_button_place_with_d(self, d, words):
        self.logoutButton_with_d.place(relx=.8, rely=.9)

    def exit_button_place(self):
        self.exitButton.place(relx=.91, rely=.9325)

    def army_image_place(self):
        self.login_army_label.place(relx=.225, rely=.05)  # where to place the image

    # =================================================================================
    #                                   Login & Registration ERRORS
    # =================================================================================

    # TODO update each call of this after changing login page

    def login_failure(self, text, x, y):
        self.login_info_error.place(relx=x, rely=y)
        self.login_info_error["text"] = text

    def registration_error(self, words, x, y):
        self.ready_to_register = False
        self.registration_info_error.place(relx=x, rely=y)
        self.registration_info_error["text"] = words
        self.clear_registration_success()
        self.clear_verify()
        self.registration_info_screen()

    # ==================================================================================
    #                                           CLEAR FUNCTIONS
    # ==================================================================================

    # clear load login screen
    def clear_login_info_screen(self):
        self.username_entry.place_forget()
        self.password_entry.place_forget()
        self.password_compare_entry.place_forget()
        self.loginbutton.place_forget()
        self.registerbutton.place_forget()
        self.username_label.place_forget()
        self.passwordlabel.place_forget()
        self.password_verify_label.place_forget()

    def clear_create_new_item(self, d):
        self.create_new_item.place_forget()
        self.create_new_item_name.place_forget()
        self.create_new_item_amount.place_forget()
        self.create_new_item_low_level.place_forget()
        self.create_new_item_weight.place_forget()
        self.create_new_item_barcode.place_forget()

        self.create_new_item_submit_button.place_forget()
        self.create_new_item_input_entry.place_forget()
        self.create_new_item_input_amount_entry.place_forget()
        self.create_new_item_input_low_level_entry.place_forget()
        self.create_new_item_input_weight_entry.place_forget()
        self.create_new_item_input_barcode_entry.place_forget()

        self.create_new_submit_error.place_forget()
        self.create_new_submit_error_alpha.place_forget()
        self.create_new_submit_error_num.place_forget()
        self.create_new_added.place_forget()

        self.back_button_func("user_screen")
        self.backup_button_with_d_button.place_forget()

    # clear everything back to login screen
    def clear_to_login(self):
        self.username_for_event_log.place_forget()
        self.logoutButton.place_forget()
        # self.remove_items_button.place_forget()
        # self.adjust_inventory_button.place_forget()
        # self.admin_button.place_forget()
        self.admin_email_inventory_button.place_forget()
        self.admin_email_label.place_forget()
        self.food_file_error_label.place_forget()
        self.make_bag_screen_button.place_forget()
        self.display_inventory_button.place_forget()
        self.display_users_button.place_forget()
        self.edit_inventory_button.place_forget()
        self.delete_user_button.place_forget()
        # self.clear_adjust_inventory_screen()
        self.clear_barcode_screen()
        self.backup_button.place_forget()
        self.clear_todo_label()
        self.clear_makebag_screen()
        self.clear_user_screen()
        self.clear_list_box()
        self.enter_email_add_label.place_forget()
        self.enter_email_add_entry.place_forget()
        self.admin_email_send_button.place_forget()
        self.make_another_bag_button.place_forget()
        self.bag_of_food_removed_from_inventory.place_forget()
        # remove buttons from manual entry
        self.submit_changes_button.place_forget()
        self.invalid_entry_error_label.place_forget()
        self.subtract_button.place_forget()
        self.add_button.place_forget()
        self.item_to_be_changed_label_1.place_forget()
        self.item_to_be_changed_label_2.place_forget()
        self.change_value_button.place_forget()
        self.adjust_inventory_entry.place_forget()
        self.adjust_item_quantity_button.place_forget()
        self.adjust_item_quantity_button.place_forget()
        self.choose_an_item_button.place_forget()
        self.choose_an_item_to_edit_button.place_forget()
        self.choose_new_item.place_forget()
        self.adjust_inventory_entry.place_forget()
        self.confirm_inventory_manual_button.place_forget()
        self.cancel_inventory_manual_button.place_forget()
        self.unbind_return_func()
        self.list_of_items_label.place_forget()

    # clear list boxes
    def clear_list_box(self):
        self.list_box_1.delete(0, tk.END)
        self.list_box_2.delete(0, tk.END)
        self.list_box_3.delete(0, tk.END)
        self.list_box_1.place_forget()
        self.list_box_2.place_forget()
        self.list_box_3.place_forget()
        # self.make_another_bag_button.place_forget()
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
        # self.adjust_inventory_button.place_forget()
        self.make_bag_screen_button.place_forget()
        self.manual_entry_button.place_forget()
        self.barcode_scanner_button.place_forget()
        self.display_inventory_user_button.place_forget()
        self.create_new_item_button.place_forget()

    '''  
    # clears if one of the options is selected
    def clear_adjust_inventory_screen(self):
        self.manual_entry_button.place_forget()
        self.barcode_scanner_button.place_forget()
        self.display_inventory_user_button.place_forget()
        self.create_new_item_button.place_forget()
    '''

    def clear_admin_screen(self):
        # self.admin_button.place_forget()
        self.admin_email_inventory_button.place_forget()
        self.display_inventory_button.place_forget()
        self.display_users_button.place_forget()
        self.edit_inventory_button.place_forget()
        self.delete_user_button.place_forget()

    # clear remove items screen
    def clear_todo_label(self):
        self.todo_label.place_forget()

    def clear_verify(self):
        self.username_verify.set('')
        self.password_verify.set('')
        self.password_compare_verify.set('')

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
        self.username_label.place_forget()
        self.username_entry.place_forget()
        self.password_entry.place_forget()
        self.passwordlabel.place_forget()
        self.password_verify_label.place_forget()
        self.loginbutton.place_forget()
        self.login_info_button.place_forget()
        self.registration_info_button.place_forget()
        self.help_label.place_forget()
        self.registerbutton.place_forget()
        # self.adjust_inventory_button.place_forget()
        # self.remove_items_button.place_forget()

    def clear_barcode_screen(self):
        self.barcode_scanner_submit_button.place_forget()
        self.barcode_scanner_remove_button.place_forget()
        self.barcode_scanner_add_button.place_forget()
        self.barcode_scanner_label.place_forget()
        self.barcode_scanner_input_entry.place_forget()
        self.clear_todo_label()

    # =================================================================================
    #                                            FULL SCREEN
    # =================================================================================

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.attributes("-fullscreen", self.state)

    def end_fullscreen(self, event=None):
        self.state = False
        self.attributes("-fullscreen", False)

    # ====================================================================================
    #                                         DICTIONARY FUNCTIONS
    # ====================================================================================
    # TODO : prevent inputing comma

    def print_dict_to_file(self, d):
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

    # TODO add checkbox variables to dict
    def make_dict(self, d):
        try:
            with open("food.txt", "r+") as f:
                f.seek(0, os.SEEK_SET)
                next(f)
                for line in f:
                    if not re.match(r'^\s*$', line):
                        words = line.split(",")
                        item = words[0]
                        amount = int(words[1])
                        lowlevel = int(words[2])
                        weight = int(words[3])
                        d[item] = {}
                        d[item]['item'] = item
                        d[item]['amount'] = amount
                        d[item]['lowlevel'] = lowlevel
                        d[item]['weight'] = weight
                        number_of_barcodes = len(words) - 4
                        n = 1
                        while n <= number_of_barcodes:
                            barcode = 'barcode' + str(n)
                            d[item][barcode] = int(words[3 + n])
                            n += 1
        except Exception as e:
            self.food_file_error_label.place(relx=.75, rely=.60)
            print("error in open: make dict : " + str(e))

    def print_dict(self, d):
        for item_id, item_info in d.items():
            print('\n')
            for key in item_info:
                print(key + " : " + str(item_info[key]))

    def append_food(self, d, newItem):
        '''
        d.update({str(self.create_new_item_input.get()): {'item': str(self.create_new_item_input.get()),
                                                     'amount': int(self.create_new_item_input_amount_entry.get()),
                                                     'lowlevel': int(self.create_new_item_input_low_level_entry.get()),
                                                     'weight': int(self.create_new_item_input_weight_entry.get()),
                                                     'barcode1': int(self.create_new_item_input_barcode_entry.get())}})
        self.make_dict(d)
        '''
        # rewrites newest dict to txt
        # however if an item has more than one barcode it will only write the first one
        # TODO: allow multiple barcodes to be added via this method, if it is even worth it
        # open test.txt to see
        '''
        with open('test.txt', 'w') as f:
            print("item, amount, low level, weight, barcode", file=f)
            standard_item = ""
            for p_id, p_info in d.items():
                standard_item = d[p_id]['item'] + "," + str(d[p_id]['amount']) + ", " + str(d[p_id]['lowlevel']) + ", " + str(d[p_id]['weight']) + ", " + str(d[p_id]['barcode1'])
                print(standard_item, file=f)
        '''
        with open("food.txt", "a") as f:
            f.write(newItem)

    # =============================================================================
    #                Display inventory - user mode
    # =============================================================================

    # display full inventory, just to view
    def display_inventory_user_button_cmd(self):
        # self.clear_adjust_inventory_screen()
        self.clear_user_screen()
        self.backup_place()
        self.view_inventory_middle_list_box(self.d)
        self.previous_view = "user_screen"

    # ===================================================================================
    #                   View and/or change Inventory & users
    #                  TODO: split these into 2-3 sections for easier viewing
    # ===================================================================================
    # adjust inventory manually
    def adjust_item_quantity_button_cmd(self, d):
        self.view_inventory_middle_list_box(d)
        place_object(self.choose_an_item_button, .8, .835)
        # self.adjust_items_button['state'] = 'disabled'
        self.choose_new_item.place_forget()
        self.adjust_item_quantity_button.place_forget()
        self.submit_changes_button.place_forget()
        self.adjust_inventory_entry.place_forget()
        self.item_to_be_changed_label_1.place_forget()
        self.item_to_be_changed_label_2.place_forget()
        self.subtract_button.place_forget()
        self.add_button.place_forget()
        self.previous_view = "manual_entry_screen"

    def choose_an_item_to_change_cmd(self, d):
        try:
            self.selected_item_to_be_changed = self.list_box_2.curselection()
            if self.selected_item_to_be_changed != ():
                self.change_inventory_by_this_much.set(0)
                self.item_to_be_changed = self.list_box_2.get(self.selected_item_to_be_changed)
                self.invalid_entry_error_label.place_forget()
                self.change_value_of_item_chosen(d)
            else:
                self.invalid_entry_error_label.config(text="Choose an Item")
                place_object(self.invalid_entry_error_label, .8, .4)
        # TODO: change to pass
        except Exception as e:
            print("Change to pass")
            print("Error inside choose_an_item_to_change_cmd : " + str(e))

    def choose_an_item_to_edit_button_cmd(self, d):
        self.selected_item_to_be_changed = self.list_box_2.curselection()
        if self.selected_item_to_be_changed != ():
            self.change_inventory_by_this_much.set(0)
            self.item_to_be_changed = self.list_box_2.get(self.selected_item_to_be_changed)
            self.invalid_entry_error_label.place_forget()
            self.item_to_be_changed_label_1.configure(text="Item to be changed")
            self.item_to_be_changed_label_2.configure(text=self.item_to_be_changed)
            place_object(self.item_to_be_changed_label_1, .8, .21)
            place_object(self.item_to_be_changed_label_2, .8, .26)

            string_key = re.split(" :", self.item_to_be_changed.strip())[0]
            #str(self.item_to_be_changed)
            #print(open('food.txt', 'r').read().find(string_key))
            #print(self.d[string_key])

            # turn into string with commas (pre-modified)
            beautiful_string = str(d[str(self.d[string_key]['item'])].values())
            beautiful_string = str(re.split("dict_values", beautiful_string))
            beautiful_string = beautiful_string.replace("[\'\', \"([", '')
            beautiful_string = beautiful_string.replace('])"]', '')
            beautiful_string = beautiful_string.replace("'", '')

            print(beautiful_string)

        else:
            self.invalid_entry_error_label.config(text="Choose an Item")
            place_object(self.invalid_entry_error_label, .8, .4)

    def confirm_item_change(self, direction):
        self.add_button.place_forget()
        self.subtract_button.place_forget()
        self.adjust_inventory_entry.place_forget()
        self.previous_view = "choose_item_screen"
        # fails try:except if not an int
        # TODO: negative number
        try:
            try:
                if not isinstance(int(self.change_inventory_by_this_much.get()), int):
                    print("test in isinstance")
            except Exception as e:
                print("is instance error : " + str(e))
                self.catch_exception_bad_input()
                return
            try:
                self.invalid_entry_error_label.place_forget()
                # parsed_selection_to_be_changed = re.split(":", self.item_to_be_changed #unparsed item
                original_inventory_amount = re.split(":", self.item_to_be_changed.strip())[1]
                try:
                    if int(self.change_inventory_by_this_much.get()[0]) == 0 and \
                            ((len(self.change_inventory_by_this_much.get())) > 1):
                        self.change_inventory_by_this_much.set(self.change_inventory_by_this_much.get()[1:])
                except Exception as e:
                    print("bad input 1 : " + str(e))

                try:
                    if direction == 'up':
                        description = 'increased '
                        self.new_inventory_amount = (int(original_inventory_amount) +
                                                     int(self.change_inventory_by_this_much.get()))
                except Exception as e:
                    print("bad input 2 : " + str(e))

                try:
                    if direction == 'down':
                        description = 'reduced '
                        self.new_inventory_amount = (int(original_inventory_amount) -
                                                     int(self.change_inventory_by_this_much.get()))
                except Exception as e:
                    print("bad input 3 : " + str(e))

                if self.new_inventory_amount < 0:
                    self.new_inventory_amount = 0
                if self.new_inventory_amount > 1000:
                    self.new_inventory_amount = 1000

                # get name of item
                parsed_name_to_be_changed = re.split(":", self.item_to_be_changed.strip())[0]
                self.item_to_be_changed_label_1.configure(text="Confirm New Inventory Amount")
                # show change about to take place
                self.item_to_be_changed_label_2.configure(text=parsed_name_to_be_changed + description
                                                               + str(self.change_inventory_by_this_much.get())
                                                               + " for a new total of : "
                                                               + str(self.new_inventory_amount))
                place_object(self.confirm_inventory_manual_button, .4, .4)
                place_object(self.cancel_inventory_manual_button, .6, .4)
                # print("success in confirm item change")
            except Exception as e:
                print("inside try confirm item change : " + str(e))
                print("bad input 4 : " + str(e))

        except Exception as e:
            print("bottom exception:")
            self.catch_exception_bad_input()

    def catch_exception_bad_input(self):
        self.invalid_entry_error_label.config(text="Only Numbers allowed")
        place_object(self.invalid_entry_error_label, .8, .4)
        place_object(self.adjust_inventory_entry, .5, .45)
        place_object(self.add_button, .4, .4)
        place_object(self.subtract_button, .4, .5)
        self.change_inventory_by_this_much.set(0)

    def confirm_inventory_manual_button_cmd(self):
        try:
            parsed_name_to_be_changed = re.split(":", self.item_to_be_changed.strip())[0]
            shutil.move("food.txt", "food.txt" + "~")
            with open("food.txt", "w+") as dest:
                dest.seek(0, os.SEEK_SET)
                with open("food.txt" + "~", "r+") as src:
                    src.seek(0, os.SEEK_SET)
                    for line in src:
                        if not re.match(r'^\s*$', line):
                            tokens = re.split(",", line.strip())
                            if tokens[0] == parsed_name_to_be_changed.strip():
                                tokens[1] = str(self.new_inventory_amount)
                                dest.write(",".join(tokens) + '\n')
                            else:
                                dest.write(line)
            self.back_button_func(self.previous_view)
        except Exception as e:
            print("error writing to food file : " + str(e))

    # change name to select new item
    # change value of inventory - manual screen
    def change_value_of_item_chosen(self, d):
        try:
            self.item_to_be_changed_label_1.configure(text="Item to be changed")
            self.item_to_be_changed_label_2.configure(text=self.item_to_be_changed)
            place_object(self.item_to_be_changed_label_1, .42, .25)
            place_object(self.item_to_be_changed_label_2, .4, .3)
            place_object(self.choose_new_item, .8, .835)
            place_object(self.adjust_inventory_entry, .5, .45)
            place_object(self.add_button, .4, .4)
            place_object(self.subtract_button, .4, .5)
            # clear items
            self.invalid_entry_error_label.place_forget()
            self.list_box_2.place_forget()
            self.choose_an_item_button.place_forget()
            self.list_box_2_label.place_forget()
            # backup
            self.previous_view = "choose_item_screen"
        # TODO: change to pass
        except Exception as e:
            print("Change to pass")
            print("Error inside change_value_of_item_chosen : " + str(e))

    # delete user from list : list_box_2
    def remove_username_func(self):
        try:
            sel = self.list_box_2.curselection()
            user_to_be_deleted = self.list_box_2.get(sel)
            self.list_box_2.delete(sel)
            try:
                shutil.move("username_password_file.txt", "username_password_file.txt" + "~")
                with open("username_password_file.txt", "w+") as dest:
                    dest.seek(0, os.SEEK_SET)
                    with open("username_password_file.txt" + "~", "r+") as src:
                        src.seek(0, os.SEEK_SET)
                        for line in src:
                            if not re.match(r'^\s*$', line):
                                tokens = re.split(" ", line.strip())
                                if tokens[0] != user_to_be_deleted or tokens[0] == "adminarmy":
                                    dest.write(line)
            # TODO: change exceptions to pass
            except Exception as e:
                print("exception in remove_func : writing file : " + str(e))
        except Exception as e:
            print("exception in remove_func : selection : " + str(e))
            print("if error is : bad listbox index, clicked delete user without selecting a user")
            print("change error to pass for final version\n")

    # swap display inventory button
    def swap_inventory_button(self):
        inventory_button_text = self.display_inventory_button.cget('text')
        if inventory_button_text == 'View Inventory':
            self.display_inventory_button.config(text="Hide Inventory")
            self.display_users_button.config(text="View Users")
            self.delete_user_button.place_forget()
            self.view_inventory_3_list_boxes(self.d)
        else:
            self.display_inventory_button.config(text="View Inventory")
            self.clear_list_box()

    # show/hide users
    def swap_display_users_button(self):
        users_button_text = self.display_users_button.cget('text')
        if users_button_text == 'View Users':
            self.display_users_button.config(text="Hide Users")
            self.display_inventory_button.config(text="View Inventory")
            place_object(self.delete_user_button, .845, .640)
            self.view_users()
        else:
            self.display_users_button.config(text="View Users")
            self.delete_user_button.place_forget()
            self.clear_list_box()

    def edit_inventory_button_cmd(self, d):
        self.clear_admin_screen()
        # Jump to modify screen and be able to modify and delete items
        # def modify_inventory()?
        self.modify_inventory(d)
        #print("Here!")


    def modify_inventory(self,d):
        # reuse select item code from manual entry
        self.view_inventory_middle_list_box(d)

        self.list_box_2.place_forget()
        self.list_box_2_label.place_forget()

        self.list_box_2_label.configure(font=(self._font, self._font_big_big), text="\\\ Select Here! //")
        place_object(self.list_box_2_label, .0, .23)
        self.list_box_2.place(relx=.01, rely=.3, relwidth=.15, relheight=.55)

        place_object(self.choose_an_item_to_edit_button, .8, .835)



    # displays users in a box
    def view_users(self):
        self.clear_list_box()
        self.list_box_2.place(relx=.39, rely=.3, relwidth=.14)
        self.list_box_2_label.place(relx=.42, rely=.25)
        self.list_box_2_label.config(text="USERS")
        box2count = 0
        try:
            with open('username_password_file.txt', "r+") as readf:
                readf.seek(0, os.SEEK_SET)
                for line in readf:
                    if not re.match(r'^\s*$', line):
                        tokens = re.split(" ", line.strip())
                        box2count += 1
                        self.list_box_2.insert(box2count, tokens[0])
        except Exception as e:
            print("error in open: view_users: " + str(e))
        # adjust box height
        boxheight = .032
        maxboxheight = .59  # .48
        if (box2count * boxheight) > maxboxheight:
            self.list_box_2.place(relheight=maxboxheight)
        else:
            self.list_box_2.place(relheight=(box2count * boxheight))

    # display inventory in 1 list box
    def view_inventory_middle_list_box(self, d):
        self.make_dict(d)
        self.clear_list_box()
        place_object(self.list_box_2, .39, .3, .14)
        place_object(self.list_box_2_label, .39, .25)
        self.list_box_2_label.configure(text="Inventory")
        box2count = 0

        # fill boxes
        for item_id, item_info in sorted(d.items()):
            box2count += 1
            self.list_box_2.insert(box2count, item_id + ' : ' + str(item_info['amount']))

        # adjust box height
        boxheight = .028
        maxboxheight = .69
        if (box2count * boxheight) > maxboxheight:
            self.list_box_2.place(relheight=maxboxheight)
        else:
            self.list_box_2.place(relheight=(box2count * boxheight))
        # clear unused boxes
        if box2count == 0:
            self.list_box_2.place_forget()
            self.list_box_2_label.place_forget()

    # displays the inventory in 3 boxes, out of stock, low inventory, inventory
    def view_inventory_3_list_boxes(self, d):
        self.make_dict(d)
        self.clear_list_box()
        self.list_box_1.place(relx=.14, rely=.3, relwidth=.14)
        self.list_box_2.place(relx=.39, rely=.3, relwidth=.14)
        self.list_box_3.place(relx=.65, rely=.3, relwidth=.14)
        self.list_box_1_label.place(relx=.14, rely=.25)
        self.list_box_2_label.place(relx=.39, rely=.25)
        self.list_box_3_label.place(relx=.65, rely=.25)
        self.list_box_2_label.config(text="LOW INVENTORY")
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
        maxboxheight = .59
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
    def lower_inventory(self, d):
        try:
            self.make_dict(d)
            shutil.move("food.txt", "food.txt" + "~")
            with open("food.txt", "w+") as dest:
                with open("food.txt" + "~", "r+") as src:
                    n = 0
                    for line in src:
                        if not re.match(r'^\s*$', line):
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
            self.bag_of_food_removed_from_inventory.place(relx=.4, rely=.9325)
        except Exception as e:
            self.food_file_error_label.place(relx=.75, rely=.60)
            print("error in lower inventory " + str(e))

    # =====================================================================================
    #                                                     REGISTRATION
    # =====================================================================================

    # registration validation
    def register_user(self):
        # deleting entry boxes
        self.username_info = self.username_verify.get()
        self.password_info = self.password_verify.get()
        # TODO : add password verify compare here
        self.clear_registration_errors()
        self.clear_login_info_error()
        self.ready_to_register = True
        __username_length = 8
        __password_length = 8
        __max_password_length = 20
        __max_username_length = 20

        # plug into regex101.com for a clear explanation
        # (?=.*[a-z]) positive lookahead for a-z
        regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
        pattern = re.compile(regex)

        # TODO: change these x y values once changing main login page

        # check for username too short
        if len(self.username_info) < __username_length:
            self.registration_error("Username must be atleast 8 letters", .68, .4)

        # check for non chars in username
        elif re.search("[^a-zA-Z]", self.username_info):
            self.registration_error("Only use letters a-z for username", .68, .4)

        # check if password too short
        elif len(self.password_info) < __password_length:
            self.registration_error("Password must be atleast 8 characters", .68, .455)

        # limit password & username length
        elif len(self.password_info) > __max_password_length:  # or
            self.registration_error("Password must be LESS than\n"
                                    "{} characters".format(__max_password_length), .68, .455)
        elif len(self.username_info) > __max_username_length:
            self.registration_error("Username must be LESS than \n"
                                    "{} characters".format(__max_username_length), .68, .455)

        # check password objects used a-z !@#$%^&*
        elif not re.search(pattern, self.password_info):
            self.registration_error("Password must contain atleast\n"
                                    "one uppercase, one lowercase\n"
                                    "one number, and one\n"
                                    "special character @$!#%*?&", .68, .455)
        # check passwords match
        elif self.password_verify.get == self.password_compare_verify.get:
            self.registration_error("passwords must match", .68, .455)

        # check if username to register already exists
        else:
            try:
                with open('username_password_file.txt', "r+") as readf:
                    readf.seek(0, os.SEEK_SET)
                    for line in readf:
                        tokens = re.split(" ", line.strip())
                        if tokens[0] == self.username_info:
                            self.registration_error("username already exists", .68, .4)
                            break
            except Exception as e:
                print("error in open: register user if username already exists: " + str(e))

        # username is a new user, and password is ok, REGISTER THE USER
        if self.ready_to_register:
            # hash the password
            self.hash = pbkdf2_sha256.hash(self.password_info)

            # add username to the username file
            try:
                with open('username_password_file.txt', "a+") as writef:
                    writef.write(self.username_info + " ")
                    writef.write(self.hash + "\n")
            except Exception as e:
                print("error in open: write username/pw to file: " + str(e))

            # successfully registered
            self.user_register_success.place(relx=.46, rely=.64)
            # testing added clear login screen
            self.eyeball_button.place_forget()
            self.password_compare_entry.place_forget()
            self.clear_login_screen()
            self.clear_verify()
            # print("cleared login screen READY TO REGISER TRUE,
            # registered and loading login screen")
            self.login_screen()

    # ===============================================================================
    #                                              LOGIN VERIFICATION
    # ===============================================================================

    def login_verify(self):
        # TODO: i think the following lines can be removed - test them
        self.clear_registration_errors()
        self.clear_registration_success()
        self.backup_button.place_forget()

        # self.clear_login_screen()  # test
        self.username_info = self.username_verify.get()
        self.password_info = self.password_verify.get()

        # check username and hashed password
        self.ready_to_login = False
        try:
            with open('username_password_file.txt', "a+") as readf:
                readf.seek(0, os.SEEK_SET)
                for line in readf:
                    tokens = re.split(" ", line.strip())
                    if tokens[0] == self.username_info and len(tokens[0]) > 7 and pbkdf2_sha256.verify(
                            self.password_info, tokens[1]):
                        self.ready_to_login = True
                        # print("confirmed password")
                        break
        except Exception as e:
            print("error in open: login verify: " + str(e))

        self.clear_verify()

        # TODO: uncomment next few lines to skip login
        # TODO: comment out the screen you don't want --- remove both for login verification
        # self.user_screen()
        self.admin_screen()

        '''
        # TODO: commnted out if/else to skip login steps while building program,
        #  put back in for finished product
        if self.ready_to_login:
            self.clear_verify()
            self.clear_login_screen()
            self.username_for_event_log.configure(text=str(tokens[0]))
            place_object(self.username_for_event_log, .02, .85)
            if tokens[0] == 'adminarmy':
                self.admin_screen()
            else:
                self.user_screen()
        else:
            self.login_failure("username & password invalid", .65, .4)
            self.clear_verify()
            self.login_info_screen()
        '''


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

    # universal entry box palce function
    # self.object-to-be-placed, relx, rely, True(optional, default is false)


def place_object(box, x, y, focus=False):
    box.place(relx=x, rely=y)
    if focus is not False:
        box.focus()


# ----------------------------------------------------------------------
# everything above this line
# ----------------------------------------------------------------------
if __name__ == '__main__':
    StartGui().mainloop()
from tkinter import *
import tkinter as tk
import re
from passlib.hash import pbkdf2_sha256
from time import *
import shutil
from shutil import copyfile
import yagmail
import os
import difflib
import sys
from winsound import *


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
        # self.resizable(0, 0)  # TODO: don't allow resizing, DISABLE ON MAC DUE TO 'zoomed' not working
        self.resizable(1, 1)  # TODO: don't allow resizing, DISABLE ON MAC DUE TO 'zoomed' not working
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)
        self.title("Salvation Army Pantry Inventory")  # app title
        self.iconbitmap(r'salogo_YMx_icon.ico')  # icon
        self._bgcolor = 'white'
        self._activebgcolor = '#e4fcdc'
        self._font = "Helvetica"
        self._font_big = 26
        self._font_big_big = 40
        self._font_medium = 22
        self._font_small = 18
        self._fgcolor = '#ff9194'
        self._fgcolor2 = '#ac73fb'
        # make a dict
        self.d = {}
        self.make_dict(self.d)
        # fixed some weirdness
        self.notFound = []
        # list of unknown barcodes
        self.isBarcode = False
        # does unknown barcode exist
        self.isModifying = "as_user"
        self.isPassingBarcode = "default"
        self.login_time = tk.StringVar()
        self.logout_time = tk.StringVar()
        self.logged_in = tk.BooleanVar()
        self.list_l = []
        self.list_k = []

        # ============================================================================================
        #                                              buttons - INIT
        # ============================================================================================
        # exit program button
        self.exitButton = tk.Button(self, text="Exit",
                                    background=self._bgcolor, font=(self._font, self._font_big),
                                    command=lambda: self.exit_program())
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
                                                     command=lambda: self.backup_button_with_d(self.d,
                                                                                               self.previous_view))
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

        # bag photo
        self.food_bag_photo = tk.PhotoImage(file="foodbag.png").subsample(2, 2)

        self.food_bag_photo_label = tk.Label(self, text="Ffooouwudd", font=(self._font, self._font_big),
                                             image=self.food_bag_photo)

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
                                                        'Barcodes'))
        self.barcode_scanner_add_button.configure(activebackground=self._activebgcolor, padx=29)

        # go to add or remove items screen using barcode
        self.barcode_scanner_remove_button = tk.Button(self, text="Remove items",
                                                       background=self._fgcolor, font=(self._font, self._font_medium),
                                                       command=lambda: self.barcode_scanner_add_remove_button_cmd(
                                                           'Barcodes '))
        self.barcode_scanner_remove_button.configure(activebackground=self._activebgcolor)

        # add_barcode_to_existing function
        self.add_barcode_to_existing_button = tk.Button(self, text="Add Barcode(s) to inventory",
                                                        background=self._fgcolor, font=(self._font, self._font_medium),
                                                        command=lambda: self.add_barcode_to_existing())
        self.add_barcode_to_existing_button.configure(activebackground=self._activebgcolor)

        # append barcode function
        self.append_barcode_button = tk.Button(self, text="Add barcode to item",
                                               background=self._fgcolor, font=(self._font, self._font_medium),
                                               command=lambda: self.append_barcode())
        self.append_barcode_button.configure(activebackground=self._activebgcolor)

        # added barcode function
        self.added_barcode_button = tk.Button(self, text="Submit",
                                              background=self._fgcolor, font=(self._font, self._font_medium),
                                              command=lambda: self.added_barcode())
        self.added_barcode_button.configure(activebackground=self._activebgcolor)

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
                                                       command=lambda: self.display_inventory_user_button_cmd('middle'))
        self.display_inventory_user_button.configure(activebackground=self._activebgcolor, padx=16)

        # view inventory as one list
        self.display_inventory_left_side_button = tk.Button(self, text="View Inventory",
                                                            font=(self._font, self._font_medium),
                                                            background=self._fgcolor,
                                                            command=lambda: self.swap_inventory_button('left'))
        self.display_inventory_left_side_button.configure(activebackground=self._activebgcolor, padx=14)
        # ========================================================================
        #                    Admin screen buttons
        # ========================================================================

        # view inventory in 3 boxes, high low out of stockbutton
        self.display_inventory_high_low_outofstock_button = tk.Button(self, text="View Inventory",
                                                                      font=(self._font, self._font_medium),
                                                                      background=self._fgcolor,
                                                                      command=lambda: self.swap_inventory_button('all'))
        self.display_inventory_high_low_outofstock_button.configure(activebackground=self._activebgcolor, padx=14)

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

        # choose item to delete 'admin'
        self.choose_an_item_to_delete_button = tk.Button(self, text="Delete This Item!",
                                                         background=self._fgcolor, font=(self._font, self._font_medium),
                                                         command=lambda: self.choose_an_item_to_delete_button_cmd(
                                                             self.d))
        self.choose_an_item_to_delete_button.configure(activebackground=self._activebgcolor, padx=47)

        # confirm delete calls deleteItem
        self.deleteItem_button = tk.Button(self, text="Confirm Deletion",
                                           background=self._fgcolor, font=(self._font, self._font_medium),
                                           command=lambda: self.deleteItem(self.delete_confirm.get()))
        self.deleteItem_button.configure(activebackground=self._activebgcolor)

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

        # make csv for excel
        self.make_csv_button = tk.Button(self, background=self._fgcolor, font=(self._font, self._font_medium),
                                         command=lambda: self.make_csv())
        self.make_csv_button.configure(activebackground=self._activebgcolor)

        # =============================================================================
        #                 END Admin screen buttons
        # =============================================================================

        # remove bag button after logging in
        self.make_bag_screen_button = tk.Button(self, text="Make A New Bag",
                                                background=self._fgcolor, font=(self._font, self._font_medium),
                                                command=lambda: self.make_bag_screen())
        self.make_bag_screen_button.configure(activebackground=self._activebgcolor)

        # make many bags button
        self.make_many_bags_button = tk.Button(self, text="Make Food bag(s)",
                                               background=self._fgcolor, font=(self._font, self._font_medium),
                                               command=lambda: self.made_a_bag_screen(self.d))
        self.make_many_bags_button.configure(activebackground=self._activebgcolor)

        # many bags entry box
        self.many_bags = tk.StringVar()
        self.many_bags_entry = tk.Entry(self, font=(self._font, self._font_big),
                                        textvariable=self.many_bags, width=20)

        # make theoretical bags
        self.make_theoretical_bags_button = tk.Button(self, text="Calculate",
                                                      background=self._fgcolor, font=(self._font, self._font_medium),
                                                      command=lambda: self.make_theoretical_bags())
        self.make_theoretical_bags_button.configure(activebackground=self._activebgcolor)

        # make_theoretical_bags entry box
        self.theoretical_bags = tk.StringVar()
        self.theoretical_bags_entry = tk.Entry(self, font=(self._font, self._font_big),
                                               textvariable=self.theoretical_bags, width=10)

        # make ANOTHER bag
        self.make_another_bag_button = tk.Button(self, text="Make more bags",
                                                 background=self._fgcolor, font=(self._font, self._font_medium),
                                                 command=lambda: self.back_button_func(self.previous_view))
        self.make_another_bag_button.configure(activebackground=self._activebgcolor, padx=10)

        # assign substitution of items
        self.substitute_foods_screen_button = tk.Button(self, text="Start substitution of food",
                                                        background=self._fgcolor, font=(self._font, self._font_medium),
                                                        command=lambda: self.substitute_foods_screen())
        self.substitute_foods_screen_button.configure(activebackground=self._activebgcolor, padx=10)

        self.substitute_foods_screen_submit_button = tk.Button(self, text="Submit",
                                                               background=self._fgcolor,
                                                               font=(self._font, self._font_medium),
                                                               command=lambda: self.substitute_foods_submit())
        self.substitute_foods_screen_submit_button.configure(activebackground=self._activebgcolor, padx=10)

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
        self.to_many_missing_items = tk.Label(self, font=(self._font, self._font_small),
                                              text="To many missing items")
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
        self.create_new_item_itemsperbag = tk.Label(self, font=(self._font, self._font_small),
                                                    text="Items per bag: ")
        self.create_new_item_barcode = tk.Label(self, font=(self._font, self._font_small),
                                                text="Barcode: ")
        self.create_new_submit_error = tk.Label(self, font=(self._font, self._font_small),
                                                text="All boxes need to be filled")
        self.create_new_submit_error_alpha = tk.Label(self, font=(self._font, self._font_small),
                                                      text="Name needs to be letters and spaces only")
        self.create_new_submit_error_num = tk.Label(self, font=(self._font, self._font_small),
                                                    text="Amount, Low level, Itemsperbag, and Barcode\nall need to be numbers only")
        self.exceeds_barcode_length = tk.Label(self, font=(self._font, self._font_small),
                                               text="Exceeds maximum number of barcodes holdable\nfor this item")
        self.exist_already_label = tk.Label(self, font=(self._font, self._font_small),
                                            text="Already Exist")
        self.barcode_exist_error = tk.Label(self, font=(self._font, self._font_small),
                                            text="Barcode Already Exist")

        self.create_new_added = tk.Label(self, font=(self._font, self._font_small),
                                         text="Added item")

        # notFound barcode list
        self.notFound_label = tk.Label(self, font=(self._font, self._font_small), fg='blue')

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
        self.delete_label = tk.Label(self, font=(self._font, self._font_big), fg='red')

        self.substitute_foods_screen_label_1 = tk.Label(self, text="Too low for full bag",
                                                        font=(self._font, self._font_big))
        self.substitute_foods_screen_label_2 = tk.Label(self,
                                                        text="Select what will replace them\nThe number amount above the food picture is the\namount you need to add in additionally to the normal amount",
                                                        font=(self._font, self._font_big))
        self.substitute_foods_screen_label_3 = tk.Label(self, font=(self._font, self._font_medium))
        self.substitute_foods_screen_label_4 = tk.Label(self, font=(self._font, self._font_medium))

        self.make_theoretical_bags_label = tk.Label(self,
                                                    text="To calculate\ninventory needed \nto make x number \nof theoretical bags",
                                                    font=(self._font, self._font_small))

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

        # barcode scanner amount entry box
        self.barcode_scanner_amount = tk.StringVar()
        self.barcode_scanner_amount_entry = tk.Entry(self, font=(self._font, self._font_big),
                                                     textvariable=self.barcode_scanner_amount, width=4)

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

        self.create_new_item_input_itemsperbag = tk.StringVar()
        self.create_new_item_input_itemsperbag_entry = tk.Entry(self, font=(self._font, self._font_big),
                                                                textvariable=self.create_new_item_input_itemsperbag,
                                                                width=20)

        self.create_new_item_input_barcode = tk.StringVar()
        self.create_new_item_input_barcode_entry = tk.Entry(self, font=(self._font, self._font_big),
                                                            textvariable=self.create_new_item_input_barcode, width=20)

        # Delete confirm box
        self.delete_confirm = tk.StringVar()
        self.delete_confirm_entry = tk.Entry(self, font=(self._font, self._font_big),
                                             textvariable=self.delete_confirm, width=20)

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

        # starting program at the login screen
        self.logged_in = False
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
        elif words == "admin_edit_main":
            self.clear_create_new_item(d)
            self.clear_admin_screen()
            self.clear_to_login()
            self.invalid_entry_error_label.place_forget()
            self.edit_inventory_button_cmd(d)
            self.deleteItem_button.place_forget()
        elif words == "admin_screen":
            self.invalid_entry_error_label.place_forget()
            self.create_new_added.place_forget()
            self.admin_screen()
            self.clear_list_box()
            self.list_box_2.place_forget()
            self.list_box_2_label.place_forget()
            self.choose_an_item_to_edit_button.place_forget()
            self.choose_an_item_to_delete_button.place_forget()
            self.backup_button_with_d_button.place_forget()
            self.delete_label.place_forget()
            self.create_new_item_button.place_forget()

    def logout_with_d(self, d, words):
        # This is for removing labels from create new item that pass d with logout button
        if words == "user_screen":
            self.backup_button_with_d(d, "user_screen")
        elif words == "login_screen":
            self.backup_button_with_d(d, "admin_screen")
        self.logoutButton_with_d.place_forget()
        self.delete_confirm_entry.place_forget()
        self.deleteItem_button.place_forget()
        self.delete_label.place_forget()
        self.login_screen()

    def back_button_func(self, words):
        # goes back to user screen
        if words == "user_screen":
            self.clear_makebag_screen()
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
            self.list_box_2_label.place_forget()
            self.invalid_entry_error_label.place_forget()
            self.display_inventory_left_side_button.place_forget()
            self.food_bag_photo_label.place_forget()
            self.append_barcode_button.place_forget()
            self.clear_add_barcode_to_existing()
            self.clear_append_barcode()
            self.user_screen()

        # goes back to make a bag screen
        elif words == "make_bag_screen":
            self.make_bag_screen()
            self.clear_todo_label()
            self.clear_list_box()
            self.make_another_bag_button.place_forget()
            self.food_file_error_label.place_forget()
            self.bag_of_food_removed_from_inventory.place_forget()
            self.invalid_entry_error_label.place_forget()
            self.clear_substitutions_page()
        elif words == "login_screen":
            self.clear_login_info_screen()
            self.clear_login_info_error()
            self.clear_registration_errors()
            self.clear_registration_success()
            self.login_screen()
            self.eyeball_button.place_forget()
            self.invalid_entry_error_label.place_forget()
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
            self.invalid_entry_error_label.place_forget()
        elif words == "choose_item_screen":
            self.item_to_be_changed_label_2.place_forget()
            self.adjust_item_quantity_button_cmd(self.d)
            self.choose_new_item.place_forget()
            self.adjust_inventory_entry.place_forget()
            self.add_button.place_forget()
            self.subtract_button.place_forget()
            self.invalid_entry_error_label.place_forget()
            self.confirm_inventory_manual_button.place_forget()
            self.cancel_inventory_manual_button.place_forget()
            self.invalid_entry_error_label.place_forget()
        elif words == "add_barcode_to_existing":
            # self.clear_add_barcode_to_existing()
            self.add_barcode_to_existing()
            self.clear_append_barcode()

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
        if self.logged_in:
            self.snapshot_comparison_on_logout("food.txt")
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
        # backup_button_with_d
        self.backup_button_with_d_button.place_forget()

    def admin_screen(self):
        self.clear_login_screen()
        self.logout_button_place()
        self.clear_login_info_error()
        self.army_image_place()
        self.eyeball_button.place_forget()
        place_object(self.admin_email_inventory_button, .845, .835)
        place_object(self.display_inventory_high_low_outofstock_button, .845, .77)
        place_object(self.display_users_button, .845, .705)
        place_object(self.edit_inventory_button, .845, .64)
        # add export to csv button
        self.make_csv_button.configure(text="Make Excel .csv", padx=3)
        place_object(self.make_csv_button, .845, .575)

    def user_screen(self):
        self.isModifying = "as_user"
        self.isPassingBarcode = "is_passing_false"
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
        self.isBarcode = False
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
        if str(self.many_bags.get()).isnumeric() == True and int(self.many_bags.get()) <= int(self.lowestRatio) and int(
                self.many_bags.get()) > 0:
            self.numberofBags = int(self.many_bags.get())
            self.many_bags.set("")

            '''n = self.numberofBags
            while n > 0:
                n -= 1
                self.lower_inventory(d)'''

            self.lower_inventory_new()

            self.clear_makebag_screen()
            self.previous_view = "make_bag_screen"
            self.make_another_bag_button.place(relx=.8, rely=.3)
            self.view_inventory_3_list_boxes(d)
        else:
            self.make_bag_screen()
            self.delete_label.configure(text="Enter number > 0\nand needs to be less than bags left")
            self.delete_label.place(relx=.75, rely=.3, anchor="center")
            self.many_bags.set("")

    def lower_inventory_new(self):
        count = 0
        try:
            totalLines = len(open("food.txt").readlines())
            with open('food.txt', 'w') as f:
                print("item, amount, lowlevel, itemsperbag, barcode", file=f)
                for p_id, p_info in self.d.items():
                    self.d[p_id]['amount'] -= self.d[p_id]['itemsperbag'] * self.numberofBags
                    self.beautifulString(str(p_id))
                    if count < totalLines - 2:
                        self.beautiful_string = str(self.beautiful_string) + '\n'
                    f.write(str(self.beautiful_string))
                    count += 1
            self.bag_of_food_removed_from_inventory.configure(text=f"{int(self.numberofBags)} bag(s) of food removed")
            self.bag_of_food_removed_from_inventory.place(relx=.4, rely=.9325)
            self.d = {}
            self.make_dict(self.d)
        except Exception as e:
            print("error in opening food.txt : lower_inventory_new" + str(e))

    # make bag screen
    def make_bag_screen(self):
        self.clear_user_screen()

        # calculate max number of bag that can be made now
        # get the lowest ratio (amount / itmesperbag)
        self.calculate_max_bags()
        self.numberofBags = 1

        self.food_bag_photo_label.place(relx=0.15, rely=0.25)
        # entry box for many bags
        self.make_many_bags_button.place(relx=.75, rely=.4, anchor="center")
        self.many_bags.set('1')
        self.many_bags_entry.place(relx=.75, rely=.47, anchor="center")
        self.make_theoretical_bags_button.place(relx=.075, rely=.4, anchor="center")
        self.theoretical_bags_entry.place(relx=.075, rely=.47, anchor="center")
        self.theoretical_bags.set('')
        self.make_theoretical_bags_label.configure(
            text="To calculate\ninventory needed \nto make x number \nof theoretical bags", fg="black")
        self.make_theoretical_bags_label.place(relx=.075, rely=.30, anchor="center")
        if int(self.lowestRatio) > 0:
            self.checkbutton_label.configure(
                text=f"Enter number of Bags to make\n\n\n{int(self.lowestRatio)} Full bag(s) left\n\n\n{str(self.nameofLowest).upper()}: is the bottleneck")
        else:
            self.checkbutton_label.configure(
                text=f"Full bags can't be made\n\n\n{str(self.nameofLowest).upper()}: is the bottleneck")
            # TODO: decide what to do with partial bags
            # place substitution button page here
            self.substitute_foods_screen_button.place(relx=.75, rely=.7, anchor="center")

        self.checkbutton_label.place(relx=.75, rely=.6, anchor="center")

        self.backup_place()
        self.previous_view = "user_screen"

    def make_theoretical_bags(self):
        if self.theoretical_bags.get().isnumeric():
            if int(self.theoretical_bags.get()) > 0 and int(self.theoretical_bags.get()) <= 999999999999:
                self.previous_view = "make_bag_screen"
                self.clear_makebag_screen()

                d_calc = {}
                d_calc = self.d
                d_needed = {}

                for key, value in d_calc.items():
                    d_calc[key]['amount'] -= d_calc[key]['itemsperbag'] * int(self.theoretical_bags.get())
                    if d_calc[key]['amount'] < 0:
                        d_needed[key] = -1 * d_calc[key]['amount']

                self.clear_list_box()
                self.list_box_1.place(x=.4 * 1920, y=.3 * 1080, relwidth=.2, relheight=.6)
                self.list_box_1_label.configure(
                    text=f"What will be needed for {int(self.theoretical_bags.get())} bags\n including current stock",
                    fg="black")
                self.list_box_1_label.place(relx=.5, rely=.25, anchor='center')
                self.list_box_2_label.configure(text=f"If it is blank then you have enough\n in stock to make "
                                                     f"{int(self.theoretical_bags.get())} bags\n\n\n\n\nElse it will show the\nfood and number "
                                                     f"needed to buy\nfor {int(self.theoretical_bags.get())} bags\n\n\n\nAlso, theoretical.txt\n has a copy of this info",
                                                fg="black")
                self.list_box_2_label.place(relx=.75, rely=.5, anchor='center')

                box1count = 0
                for item_id, item_info in d_needed.items():
                    box1count += 1
                    self.list_box_1.insert(box1count, item_id + ' : ' + str(item_info))
                try:
                    with open('theoretical.txt', 'w') as f:
                        print(
                            f"Amount and items needed for {int(self.theoretical_bags.get())} bags\nThis is after current stocks goes to zero\nitem: amount",
                            file=f)
                        for p_id, p_info in d_needed.items():
                            print(f"{str(p_id)}: {d_needed[p_id]}", file=f)
                except Exception as e:
                    print("error in writing theoretical.txt: make_theoretical_bags : " + str(e))
            else:
                self.make_theoretical_bags_label.configure(text="Enter number\nbetween 0 and 9999", fg='red')
                self.theoretical_bags.set('')
        else:
            self.make_theoretical_bags_label.configure(text="Enter number\nbetween 0 and 9999", fg='red')
            self.theoretical_bags.set('')

    def calculate_max_bags(self):
        self.make_dict(self.d)
        self.lowestRatio = 9999.9
        self.nameofLowest = ""
        try:
            with open("food.txt", "r+") as src:
                n = 0
                for line in src:
                    if not re.match(r'^\s*$', line):
                        if n == 0:
                            n += 1
                        else:
                            words = line.split(", ")
                            if int(words[3]) != 0:
                                if (int(words[1]) / int(words[3])) < self.lowestRatio:
                                    self.lowestRatio = int(words[1]) / int(words[3])
                                    self.nameofLowest = words[0]
        except Exception as e:
            print("error in reading food.txt: calculate_max_bags : " + str(e))

    def substitute_foods_screen(self):
        self.d = {}
        self.make_dict(self.d)
        # force reset/ update of dict. Really only need it if directly editing the txt
        self.clear_makebag_screen()
        self.previous_view = "make_bag_screen"
        # Needs labels and a submit button
        self.substitute_foods_screen_label_1.place(relx=.025, rely=.26)
        self.substitute_foods_screen_label_2.place(relx=.25, rely=.225)
        self.substitute_foods_screen_label_4.configure(text="When ready hit submit", fg='black')
        self.substitute_foods_screen_label_4.place(relx=.81, rely=.55)
        self.substitute_foods_screen_submit_button.place(relx=.85, rely=.6)

        self.d_outofstock = {}
        self.d_instock = {}

        self.d_photos = {}
        for key, value in self.d.items():
            try:
                self.d_photos[self.d[key]['item']] = tk.PhotoImage(file=f"images/{self.d[key]['item']}.png").subsample(
                    4, 4)
            except Exception:
                # all make a bag items without a picture will have a ? picture so it can still work
                self.d_photos[self.d[key]['item']] = tk.PhotoImage(file=f"images/unknown.png").subsample(4, 4)

        outofstock = []
        instock = []
        self.stock = []

        for key, value in self.d.items():
            if self.d[key]['amount'] < self.d[key]['itemsperbag']:
                outofstock.append(self.d[key]['item'])
            elif self.d[key]['itemsperbag'] == 0:
                pass
            elif self.d[key]['amount'] >= self.d[key]['itemsperbag'] * 2:
                instock.append(self.d[key]['item'])
            # make sure it is eligible to be a sub/ don't want negatives after subtituiting
            if self.d[key]['amount'] >= self.d[key]['itemsperbag']:
                self.stock.append(self.d[key]['item'])
        if outofstock.__len__() > 3:
            # print("To many missing items")
            self.clear_substitutions_page()
            self.make_bag_screen()
            # self.to_many_missing_items.place()
            self.substitute_foods_screen_label_3.configure(text="To many missing items", fg='red')
            self.substitute_foods_screen_label_3.place(relx=.655, rely=.75)
            return

        index = 0
        for i in outofstock:
            # checkbox value stored at foodname
            self.d_outofstock[i] = IntVar()

            l = Checkbutton(text="    " + str(i).upper() + ":   \n" + str(self.d[i]['amount']),
                            variable=self.d_outofstock[i], image=self.d_photos[f'{i}'], compound='bottom',
                            state=DISABLED)
            self.list_l.append(l)

            self.d_outofstock[i].set(1)

            l.place(relx=0.05, rely=0.15 * index + 0.35)
            # Max is 4, they should never have more than 4 (out of stock/ less than itemsperbag) anyway
            index += 1

        index = 0
        offset_y = [0, 0, 0, 0]
        x = 0.105
        for j in instock:
            # checkbox value stored at foodname
            self.d_instock[j] = IntVar()

            k = Checkbutton(text="    " + str(j).upper() + ":   " + str(self.d[j]['itemsperbag']),
                            variable=self.d_instock[j], image=self.d_photos[f'{j}'], compound='bottom')
            self.list_k.append(k)

            if index > 3:
                offset_x = x
                offset_y[0] += 1
                if index > 7:
                    offset_y[0] = 0
                    offset_y[1] += 1
                    offset_x = x * 2
                    if index > 11:
                        offset_y[1] = 0
                        offset_y[2] += 1
                        offset_x = x * 3
                        if index > 15:
                            # At this point it should never happen, but just in case
                            offset_y[2] = 0
                            offset_y[3] += 1
                            offset_x = x * 4

                k.place(relx=0.25 + offset_x,
                        rely=0.15 * (offset_y[0] + offset_y[1] + offset_y[2] + offset_y[3]) + 0.20)
            else:
                k.place(relx=0.25, rely=0.15 * index + 0.35)
            index += 1

    def substitute_foods_submit(self):
        self.previous_view = "make_bag_screen"
        # Need to make it modify txt, probably fake admin
        # but this is the logic
        notevenOne = True
        try:
            totalLines = len(open("food.txt").readlines())
        except Exception as e:
            print("error in reading food.txt: substitute_foods_submit : total lines : " + str(e))
        count = 0
        for key, value in self.d_outofstock.items():
            if self.d_outofstock[key].get() == 1:
                self.d[key]['amount'] = 0

        for key, value in self.d_instock.items():
            if self.d_instock[key].get() == 1:
                self.d[key]['amount'] -= self.d[key]['itemsperbag'] * 2
                notevenOne = False
                self.stock.remove(key)

        for key in self.stock:
            self.d[key]['amount'] -= self.d[key]['itemsperbag']
            # the in between stock

        if notevenOne == True:
            self.previous_view = "make_bag_screen"
            self.back_button_func(self.previous_view)
            self.substitute_foods_screen_label_3.configure(text="No substitutes were selected", fg='red')
            self.substitute_foods_screen_label_3.place(relx=.655, rely=.75)
            # Force back button press
        else:
            try:
                with open('food.txt', 'w') as f:
                    print("item, amount, lowlevel, itemsperbag, barcode", file=f)
                    for p_id, p_info in self.d.items():
                        self.beautifulString(str(p_id))
                        if count < totalLines - 2:
                            self.beautiful_string = str(self.beautiful_string) + '\n'
                        f.write(str(self.beautiful_string))
                        count += 1
            except Exception as e:
                print("error writing food.txt : substitute_foods_submit : beautiful string : " + str(e))

            self.d = {}
            self.make_dict(self.d)
            # most easy way to do it

            self.back_button_func(self.previous_view)
            # Force back button press
            self.substitute_foods_screen_label_3.configure(text="Made bag with substitutes", fg='blue')
            self.substitute_foods_screen_label_3.place(relx=.66, rely=.75)

    def make_csv(self):
        import csv
        count = 0
        try:
            totalLines = len(open("food.txt").readlines())
            fieldnames = ['item', 'amount', 'lowlevel', 'itemsperbag', 'barcodes']
            with open("food.csv", "w") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                print(
                    "'Name of food', 'Current Amount', 'Low Level Threshold', 'Items per food bag', 'List of Barcodes'\n",
                    file=f)
                for p_id, p_info in self.d.items():
                    self.beautifulString(str(p_id))
                    if count < totalLines - 2:
                        self.beautiful_string = str(self.beautiful_string) + '\n'
                    f.write(str(self.beautiful_string))
                    count += 1
            self.make_csv_button.configure(text="Made food.csv", padx=13)
        except Exception:
            print("error in reading food.txt make_csv : " + str(e))

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
        # place_object(self.display_inventory_left_side_button, .8, .84)
        self.view_inventory_one_list_box(self.d, 'left')

        self.list_of_items_words = 'Inventory Changes\n'
        self.list_of_items_label.config(text=self.list_of_items_words)

    def barcode_scanner_add_remove_button_cmd(self, direction):
        # TODO: add barcode & qty columns
        self.previous_view = "user_screen"
        self.clear_barcode_screen()
        place_object(self.list_box_2_label, .08, .25)
        self.invalid_entry_error_label.place_forget()
        self.barcode_scanner_label.configure(text=direction + '    \t\tEnter amount')
        place_object(self.barcode_scanner_label, .3, .25)
        place_object(self.barcode_scanner_input_entry, .3, .3, True)
        place_object(self.barcode_scanner_amount_entry, .55, .3)
        place_object(self.list_of_items_label, .7, .3)
        self.barcode_scanner_input.set("")
        self.barcode_scanner_amount.set(1)
        self.bind('<Tab>', lambda x: self.bind_tab_to_scanner_input_entry())
        self.bind('<Return>', lambda x: self.search_for_item_in_food_file(
            direction, self.barcode_scanner_input.get(),
            self.barcode_scanner_amount.get()))
        if self.notFound.__len__() > 0:
            #self.add_barcode_to_existing_button.place(relx=.35, rely=.5)
            self.add_barcode_to_existing()

    def bind_tab_to_scanner_input_entry(self):
        self.barcode_scanner_input_entry.place_forget()
        place_object(self.barcode_scanner_input_entry, .3, .3, True)

    def unbind_return_func(self):
        self.unbind('<Return>')
        self.unbind('<Tab>')

    def search_for_item_in_food_file(self, direction, item_to_find, qty):
        # TODO: add barcode & qty columns
        # TODO: limit size of list_of_items_words so its doesn't go over inventory button
        # TODO: I suggest to always show inventory box and update every scan instead of needing to toggle to update the box
        try:
            self.invalid_entry_error_label.place_forget()
            intcheck = int(qty)
            intcheck = int(item_to_find)
            try:
                totalLines = len(open("food.txt").readlines())
                shutil.move("food.txt", "food.txt" + "~")
                with open("food.txt", "w+") as dest:
                    dest.seek(0, os.SEEK_SET)
                    with open("food.txt" + "~", "r+") as src:
                        src.seek(0, os.SEEK_SET)
                        newitem = True
                        count = 0
                        for line in src:
                            count += 1
                            if not re.match(r'^\s*$', line):  # skips blank lines
                                found = False
                                tokens = re.split(", ", line.strip())
                                for ndex in range(len(tokens))[4:]:
                                    if str(tokens[ndex].strip()) == str(item_to_find):
                                        if direction == 'Barcodes':
                                            if str(self.list_of_items_words).count('\n') > 20:
                                                self.list_of_items_words = ''
                                            tokens[1] = str(int(tokens[1]) + int(self.barcode_scanner_amount.get()))
                                            self.list_of_items_words = self.list_of_items_words + \
                                                                       'added ' + \
                                                                       str(self.barcode_scanner_amount.get()) + \
                                                                       " to '" + tokens[0] + "' " + \
                                                                       str(item_to_find) + ' New Qty: ' + \
                                                                       tokens[1] + '\n'
                                            self.list_of_items_label.config(text=self.list_of_items_words)

                                        if direction == 'Barcodes ':
                                            if str(self.list_of_items_words).count('\n') > 20:
                                                self.list_of_items_words = ''
                                            tokens[1] = str(int(tokens[1]) - int(self.barcode_scanner_amount.get()))
                                            self.list_of_items_words = self.list_of_items_words + \
                                                                       'removed ' + \
                                                                       str(self.barcode_scanner_amount.get()) + \
                                                                       " from '" + tokens[0] + "' " + \
                                                                       str(item_to_find) + ' New Qty: ' + \
                                                                       tokens[1] + '\n'

                                            self.list_of_items_label.config(text=self.list_of_items_words)
                                        found = True
                                        newitem = False
                                        if count < totalLines:
                                            dest.write(", ".join(tokens) + '\n')
                                        else:
                                            dest.write(", ".join(tokens))
                                if found is False:
                                    dest.write(line)
                        if newitem:
                            self.list_of_items_words = self.list_of_items_words + \
                                                       ' not found : ' + str(item_to_find) + '\n'
                            self.list_of_items_label.config(text=self.list_of_items_words)
                            if (str(item_to_find) in self.notFound) == False:
                                self.notFound.append(str(item_to_find))
                            # place add_barcode_to_existing button
                            # self.add_barcode_to_existing()
                            #self.add_barcode_to_existing_button.place(relx=.02, rely=.5)

                            '''# TODO : probably call new item screen here
                            print("new item need to add it to the inventory")
                            print("new plan?  save items not found to a new list")
                            print("place a new item screen button")
                            print("display new item list on the new item screen until back button pushed")
                            # addition to plan, make a "append barcode to existing fooditem" page instead of assuming it is
                            # a brand new fooditem every time, ask if it would fall under any foods already in the dict
                            # if not then they can make a new item'''

                self.barcode_scanner_add_remove_button_cmd(direction)
                self.view_inventory_one_list_box(self.d, 'left')
                self.clear_list_box()
                self.view_inventory_one_list_box(self.d, 'left')
                if self.notFound.__len__()>0:
                    self.add_barcode_to_existing()
                    PlaySound("Wilhelm_Scream.wav", SND_FILENAME)
            except Exception as e:
                print("error writing to food file : " + str(e))
        except Exception as e:
            # input a non int value, show error label to user
            self.invalid_entry_error_label.config(text='Enter numbers only')
            place_object(self.invalid_entry_error_label, .8, .25)
            self.barcode_scanner_input.set("")
            self.barcode_scanner_amount.set(1)

    def barcode_exist(self, code):
        for key, value in self.d.items():
            if code in self.d[key]['barcodes']:
                return True
        return False

    def add_barcode_to_existing(self):
        # pulls up list of notfound
        # lets user select from box for which item to add barcode to
        # if new item needs to be made then createnewitem screen passing notfound?
        self.previous_view = "user_screen"
        self.clear_barcode_screen()
        self.display_inventory_left_side_button.place_forget()

        self.list_box_2.delete(0, tk.END)
        box2count = 0
        for item_id, item_info in self.d.items():
            box2count += 1
            self.list_box_2.insert(box2count, str(item_info['item']))

        self.isPassingBarcode = "is_passing_true"

        self.list_box_2.place(relx=.02, rely=.3, relwidth=.125, relheight=.55)
        self.list_box_2_label.configure(font=(self._font, self._font_big_big),
                                        text="If item falls under one from the list\nselect from the list\n\n\nIf not, then create a new item,\nthe barcode(s) will carry over",
                                        fg='red')
        self.list_box_2_label.place(x=1050, y=600, anchor="center")

        self.isBarcode = True
        # place create new item button
        self.create_new_item_button.place(x=1700, y=600, anchor="center")
        # place append_barcode button
        self.append_barcode_button.place(x=450, y=600, anchor="center")

    def append_barcode(self):
        self.selected_item_to_be_changed = self.list_box_2.curselection()
        if self.selected_item_to_be_changed != ():
            self.previous_view = "add_barcode_to_existing"
            self.clear_add_barcode_to_existing()

            self.change_inventory_by_this_much.set(0)
            self.item_to_be_changed = self.list_box_2.get(self.selected_item_to_be_changed)
            self.invalid_entry_error_label.place_forget()

            # self.item_to_be_changed for the name of item

            self.list_box_3.delete(0, tk.END)
            box3count = 0
            for bar in self.notFound:
                box3count += 1
                self.list_box_3.insert(box3count, str(bar))

            self.list_box_3.place(relx=.02, rely=.3, relwidth=.125, relheight=.55)
            self.list_box_3_label.configure(font=(self._font, self._font_big),
                                            text=f"Now select which barcode to add to {str(self.item_to_be_changed).upper()}")
            self.list_box_3_label.place(x=960, y=400, anchor="center")

            # place added_barcode button
            self.added_barcode_button.place(x=450, y=600, anchor="center")

        else:
            self.invalid_entry_error_label.place_forget()
            self.invalid_entry_error_label.config(text="Choose an Item")
            place_object(self.invalid_entry_error_label, .17, .45)

    def added_barcode(self):
        self.selected_item_to_be_changed = self.list_box_3.curselection()
        if self.selected_item_to_be_changed != ():
            # self.previous_view = "added_barcode" need to add this

            self.change_inventory_by_this_much.set(0)
            self.barcode_to_be_added = self.list_box_3.get(self.selected_item_to_be_changed)
            self.invalid_entry_error_label.place_forget()

            # everything else
            self.invalid_entry_error_label.config(text=f"Added {self.barcode_to_be_added} to {self.item_to_be_changed}",
                                                  fg='blue')
            self.invalid_entry_error_label.place(x=1050, y=320, anchor="center")

            # do the appending
            self.beautifulString(self.item_to_be_changed)
            try:
                s = open("food.txt").read()
                s = s.replace(self.beautiful_string, self.beautiful_string + ", " + str(self.barcode_to_be_added))
                f = open("food.txt", 'w')
                f.write(s)
                f.close()
            except Exception:
                print("error in opening food.txt added_barcode : " + str(e))

            # clear only the item from self.notfound selected
            self.notFound.remove(str(self.barcode_to_be_added))

            # Force a back press
            self.back_button_func(self.previous_view)

        else:
            self.invalid_entry_error_label.config(text="Choose an Item")
            place_object(self.invalid_entry_error_label, .17, .45)

    def clear_add_barcode_to_existing(self):
        self.list_box_2.place_forget()
        self.list_box_2_label.place_forget()
        self.create_new_item_button.place_forget()
        self.append_barcode_button.place_forget()

    def clear_append_barcode(self):
        self.list_box_3.place_forget()
        self.list_box_3_label.place_forget()
        self.added_barcode_button.place_forget()

    def clear_substitutions_page(self):
        for i in self.list_l:
            i.place_forget()
        for j in self.list_k:
            j.place_forget()
        self.substitute_foods_screen_label_1.place_forget()
        self.substitute_foods_screen_label_2.place_forget()
        self.substitute_foods_screen_submit_button.place_forget()
        self.substitute_foods_screen_label_4.place_forget()

    # ===================================================================
    #               New items screen and functions
    # ==================================================================

    def create_new_item_screen(self, d):
        # creates blank screen
        self.invalid_entry_error_label.place_forget()
        self.clear_add_barcode_to_existing()
        self.clear_user_screen()
        self.logoutButton.place_forget()
        self.logout_button_place_with_d(d, "user_screen")

        if self.isModifying == "is_admin_modifying_with_check":
            self.is_modifying_3_clears()

        if self.isBarcode == True:
            self.codeList = ''
            for codes in self.notFound:
                self.codeList = self.codeList + "\n" + codes
            self.notFound_label.configure(text="BARCODES\n" + self.codeList)
            self.notFound_label.place(relx=.05, rely=.3)

        self.previous_view = "user_screen"
        self.backup_place_with_d()

        self.create_new_item.place(relx=.4, rely=.23)

        self.create_new_item_name.place(relx=.2, rely=.3)
        self.create_new_item_amount.place(relx=.2, rely=.4)
        self.create_new_item_low_level.place(relx=.2, rely=.5)
        self.create_new_item_itemsperbag.place(relx=.2, rely=.6)
        self.create_new_item_barcode.place(relx=.2, rely=.7)

        self.create_new_item_input_amount.set(1)
        self.create_new_item_input_low_level.set(20)
        self.create_new_item_input_itemsperbag.set(0)
        self.create_new_item_input_barcode.set('')

        if self.isPassingBarcode == "is_passing_true":
            if self.notFound.__len__() > 0:
                self.create_new_item_input_barcode.set(str(self.notFound[0]))
        # prefilling defaults for new item, user can set different values if they want

        place_object(self.create_new_item_submit_button, .7, .5)
        place_object(self.create_new_item_input_entry, .4, .3, True)
        place_object(self.create_new_item_input_amount_entry, .4, .4)
        place_object(self.create_new_item_input_low_level_entry, .4, .5)
        place_object(self.create_new_item_input_itemsperbag_entry, .4, .6)
        place_object(self.create_new_item_input_barcode_entry, .4, .7)

    def create_new_item_submit_button_cmd(self, d):
        self.newItem = self.create_new_item_input.get() + ", " + \
                       str(self.create_new_item_input_amount.get()) + ", " + \
                       str(self.create_new_item_input_low_level.get()) + ", " + \
                       str(self.create_new_item_input_itemsperbag.get()) + ", " + \
                       str(self.create_new_item_input_barcode.get())

        if self.isModifying == "is_admin":
            self.create_new_item_screen(d)
            self.auto_fill_edit_item()

            self.toDelete = str(self.words[0])
            self.isModifying = "is_admin_modifying"
        else:
            allFilled = self.isAllFilled(self.newItem)
            if allFilled == 0:
                self.create_new_item_input.set("")
                self.create_new_item_input_amount.set(1)
                self.create_new_item_input_low_level.set(20)
                self.create_new_item_input_itemsperbag.set(0)
                self.create_new_item_input_barcode.set("")

                if self.isPassingBarcode == "is_passing_true":
                    if self.notFound.__len__() > 0:
                        self.create_new_item_input_barcode.set(int(self.notFound[0]))

                self.create_new_item_screen(d)
                self.create_new_item.place_forget()

                if self.isModifying == "is_admin_modifying":
                    self.auto_fill_edit_item()
            else:
                self.append_food(d, self.newItem)
                self.create_new_item_input.set("")
                self.create_new_item_input_amount.set(1)
                self.create_new_item_input_low_level.set(20)
                self.create_new_item_input_itemsperbag.set(0)
                self.create_new_item_input_barcode.set("")

                if self.isPassingBarcode == "is_passing_true":
                    if self.notFound.__len__() > 0:
                        self.create_new_item_input_barcode.set(int(self.notFound[0]))

    def auto_fill_edit_item(self):
        self.words = self.beautiful_string.split(", ")

        self.create_new_item_input.set(self.words[0])
        self.create_new_item_input_amount.set(self.words[1])
        self.create_new_item_input_low_level.set(self.words[2])
        self.create_new_item_input_itemsperbag.set(self.words[3])

        n = 4
        self.barcodeList = ""
        while n < self.words.__len__():
            self.barcodeList += self.words[n] + ", "
            n += 1
        self.create_new_item_input_barcode.set(self.barcodeList[:self.barcodeList.__len__() - 2])

    def isAllFilled(self, d):
        self.make_dict(self.d)
        if (self.create_new_item_input.get() == "" or
                str(self.create_new_item_input_amount.get()) == "" or
                str(self.create_new_item_input_low_level.get()) == "" or
                str(self.create_new_item_input_itemsperbag.get()) == "" or
                str(self.create_new_item_input_barcode.get()) == ""):
            place_object(self.create_new_submit_error, .692, .6)

            self.create_new_submit_error_alpha.place_forget()
            self.create_new_submit_error_num.place_forget()
            self.create_new_added.place_forget()
            self.exceeds_barcode_length.place_forget()
            self.exist_already_label.place_forget()
            self.barcode_exist_error.place_forget()
            return 0
        elif ((str(self.create_new_item_input.get()) in self.d) == True and self.isModifying == "as_user") or \
                (self.isModifying == "is_admin_modifying_with_check" and (
                        str(self.create_new_item_input.get()) in self.d) == True):
            place_object(self.exist_already_label, .725, .6)
            self.create_new_submit_error_alpha.place_forget()
            self.create_new_submit_error.place_forget()
            self.create_new_added.place_forget()
            self.exceeds_barcode_length.place_forget()
            self.barcode_exist_error.place_forget()
            return 0
        elif re.search("[^a-zA-Z\s]", self.create_new_item_input.get()) != None or \
                str(self.create_new_item_input.get()).count("  ") > 0 or str(self.create_new_item_input.get()).endswith(
            " "):
            # names of items can now have spaces *fixed I didnt use None
            # checks for invalid spaces
            place_object(self.create_new_submit_error_alpha, .68, .6)

            self.create_new_submit_error.place_forget()
            self.create_new_submit_error_num.place_forget()
            self.create_new_added.place_forget()
            self.exceeds_barcode_length.place_forget()
            self.exist_already_label.place_forget()
            self.barcode_exist_error.place_forget()
            return 0
        elif (str(self.create_new_item_input_amount.get()).isnumeric() == False or
              str(self.create_new_item_input_low_level.get().isnumeric()) == False or
              str(self.create_new_item_input_itemsperbag.get()).isnumeric() == False or
              re.search("[^0-9\s,]", str(self.create_new_item_input_barcode.get())) != None or
              str(self.create_new_item_input_barcode.get()).count(",,") > 0 or
              str(self.create_new_item_input_barcode.get()).count(", ,") > 0 or
              str(self.create_new_item_input_barcode.get()).endswith(",") or
              str(self.create_new_item_input_barcode.get()).endswith(" ") or
              str(self.create_new_item_input_barcode.get()).count("  ") > 0):
            # can have numbers, commas, and spaces for barcodes only, others are nums only
            # ,, check to see if it is invalid use of commas/ spaces
            place_object(self.create_new_submit_error_num, .655, .6)

            self.create_new_submit_error_alpha.place_forget()
            self.create_new_submit_error.place_forget()
            self.create_new_added.place_forget()
            self.exceeds_barcode_length.place_forget()
            self.exist_already_label.place_forget()
            self.barcode_exist_error.place_forget()
            return 0
        else:
            if int(self.newItem.count(",")) > int(self.barcodesLenght - 2):
                place_object(self.exceeds_barcode_length, .655, .6)
                return 0
            # check to see if barcode limit is reached via comma count

            # need loop to check every barcode split by comma
            barcodes_to_check = str(self.create_new_item_input_barcode.get()).split(", ")
            for i in barcodes_to_check:
                if self.barcode_exist(
                        int(i)) == True and self.isModifying == "is_admin_modifying_with_check" or self.barcode_exist(
                        int(i)) == True and self.isModifying == "as_user":
                    place_object(self.barcode_exist_error, .7, .6)
                    return 0

            for index in range(str(self.newItem).find(","), len(self.newItem) - 1):
                if self.newItem[index] == ',' and self.newItem[index + 1] != " ":
                    self.newItem = self.newItem[:index] + ", " + self.newItem[index + 1:]
                if self.newItem[index] == ' ' and self.newItem[index - 1] != ",":
                    self.newItem = self.newItem[:index] + ", " + self.newItem[index + 1:]
            # fixes non spaced commas in barcode
            # fixes non comma'd spaces in barcode

            # remove all other error labels
            self.create_new_submit_error.place_forget()
            self.create_new_submit_error_alpha.place_forget()
            self.create_new_submit_error_num.place_forget()
            self.create_new_added.place_forget()
            self.exceeds_barcode_length.place_forget()
            self.exist_already_label.place_forget()
            self.barcode_exist_error.place_forget()
            place_object(self.create_new_added, .73, .6)
            return 1

    def is_modifying_3_clears(self):
        self.previous_view = "admin_screen"
        self.choose_an_item_to_edit_button.place_forget()
        self.choose_an_item_to_delete_button.place_forget()
        self.list_box_2_label.place_forget()
        self.list_box_2.place_forget()
        self.delete_label.place_forget()
        self.create_new_added.place_forget()
        self.create_new_added.configure(text="Item added")
        self.create_new_item.place(relx=.4, rely=.23)
        self.create_new_item_input.set('')
        self.create_new_item_input_amount.set('')
        self.create_new_item_input_low_level.set('')
        self.create_new_item_input_itemsperbag.set('')
        self.create_new_item_input_barcode.set("")
        self.backup_button_with_d_button.place_forget()
        self.backup_place()

    def manual_entry_screen(self):
        # self.clear_adjust_inventory_screen()
        self.clear_user_screen()
        # self.backup_place()
        # self.view_inventory_3_list_boxes(self.d)
        # self.previous_view = "user_screen"
        # place_object(self.adjust_item_quantity_button, .8, .835)

        self.adjust_item_quantity_button_cmd(self.d)
        self.previous_view = "user_screen"
        self.backup_place()

    # =================================================================================
    #                                             Place functions
    # =================================================================================
    def backup_place(self):
        self.backup_button.place(relx=.02, rely=.9)

    # TODO: new:
    def backup_place_with_d(self):
        if self.isModifying == "as_user":
            self.backup_button_with_d_button.place(relx=.02, rely=.9)
            self.previous_view = "user_screen"
        else:  # self.isModifying != 0:
            self.backup_button_with_d_button.configure(text="Back to Choose")
            self.backup_button_with_d_button.place(relx=.02, rely=.9)
            self.previous_view = "admin_edit_main"

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
        self.create_new_item_itemsperbag.place_forget()
        self.create_new_item_barcode.place_forget()

        self.create_new_item_submit_button.place_forget()
        self.create_new_item_input_entry.place_forget()
        self.create_new_item_input_amount_entry.place_forget()
        self.create_new_item_input_low_level_entry.place_forget()
        self.create_new_item_input_itemsperbag_entry.place_forget()
        self.create_new_item_input_barcode_entry.place_forget()

        self.create_new_submit_error.place_forget()
        self.create_new_submit_error_alpha.place_forget()
        self.create_new_submit_error_num.place_forget()
        self.exist_already_label.place_forget()
        self.exceeds_barcode_length.place_forget()
        self.create_new_added.place_forget()

        self.back_button_func("user_screen")
        self.backup_button_with_d_button.place_forget()

        self.notFound_label.place_forget()
        self.barcode_exist_error.place_forget()

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
        self.display_inventory_high_low_outofstock_button.place_forget()
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
        self.choose_an_item_to_delete_button.place_forget()
        self.choose_new_item.place_forget()
        self.adjust_inventory_entry.place_forget()
        self.confirm_inventory_manual_button.place_forget()
        self.cancel_inventory_manual_button.place_forget()
        self.unbind_return_func()
        self.list_of_items_label.place_forget()
        self.display_inventory_left_side_button.place_forget()
        self.clear_append_barcode()
        self.clear_add_barcode_to_existing()
        self.clear_substitutions_page()
        self.clear_admin_screen()

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
        self.checkbutton_label.place_forget()

        self.many_bags_entry.place_forget()
        self.make_many_bags_button.place_forget()
        self.delete_label.place_forget()

        self.food_bag_photo_label.place_forget()
        self.substitute_foods_screen_button.place_forget()
        self.substitute_foods_screen_label_3.place_forget()
        self.make_theoretical_bags_button.place_forget()
        self.theoretical_bags_entry.place_forget()
        self.make_theoretical_bags_label.place_forget()

    # clears user screen
    def clear_user_screen(self):
        # self.adjust_inventory_button.place_forget()
        self.make_bag_screen_button.place_forget()
        self.manual_entry_button.place_forget()
        self.barcode_scanner_button.place_forget()
        self.display_inventory_user_button.place_forget()
        self.create_new_item_button.place_forget()

    def clear_admin_screen(self):
        # self.admin_button.place_forget()
        self.admin_email_inventory_button.place_forget()
        self.display_inventory_high_low_outofstock_button.place_forget()
        self.display_users_button.place_forget()
        self.edit_inventory_button.place_forget()
        self.delete_user_button.place_forget()
        self.create_new_item_button.place_forget()
        self.enter_email_add_label.place_forget()
        self.enter_email_add_entry.place_forget()
        self.admin_email_send_button.place_forget()
        self.make_csv_button.place_forget()

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
        self.barcode_scanner_amount_entry.place_forget()
        self.clear_todo_label()
        self.list_of_items_label.place_forget()
        self.list_box_2_label.place_forget()
        self.add_barcode_to_existing_button.place_forget()

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
                        itemsperbag = int(words[3])
                        barcodes = [''] * 100
                        self.barcodesLenght = barcodes.__len__()
                        # could use None but '' looks better
                        d[item] = {}
                        d[item]['item'] = item
                        d[item]['amount'] = amount
                        d[item]['lowlevel'] = lowlevel
                        d[item]['itemsperbag'] = itemsperbag
                        number_of_barcodes = len(words) - 4
                        n = 1
                        while n <= number_of_barcodes:
                            barcodes[n - 1] = int(words[3 + n])
                            n += 1
                        d[item]['barcodes'] = barcodes
        except Exception as e:
            self.food_file_error_label.place(relx=.75, rely=.60)
            print("error in open: make dict : " + str(e))

    def print_dict(self, d):
        for item_id, item_info in d.items():
            print('\n')
            for key in item_info:
                print(key + " : " + str(item_info[key]))

    def append_food(self, d, newItem):
        if (str(self.create_new_item_input_barcode.get()) in self.notFound) == True:
            self.notFound.remove(str(self.create_new_item_input_barcode.get()))

            if self.isBarcode == True:
                self.codeList = ''
                for codes in self.notFound:
                    self.codeList = self.codeList + "\n" + codes
                self.notFound_label.configure(text="BARCODES\n" + self.codeList)
                self.notFound_label.place(relx=.05, rely=.3)

        if self.isModifying == "is_admin_modifying":
            # 'fix' this later
            try:
                s = open("food.txt").read()
                s = s.replace(self.beautiful_string, newItem)
                f = open("food.txt", 'w')
                f.write(s)
                f.close()
            except Exception as e:
                print("error in opening food.txt : append food : replace" + str(e))
            # forces a back button press on success
            self.previous_view = "admin_edit_main"
            self.backup_button_with_d(d, self.previous_view)
            del self.d[self.toDelete]

            self.edit_inventory_button_cmd(d)
            self.create_new_added.configure(text="Item Modified")
            self.create_new_added.place_forget()
            place_object(self.create_new_added, .74, .58)

        else:
            try:
                with open("food.txt", "a") as f:
                    f.write("\n" + newItem)
            except Exception:
                print("error in appending food.txt with open : " + str(e))

    # =============================================================================
    #                Display inventory - user mode
    # =============================================================================

    # display full inventory, just to view
    def display_inventory_user_button_cmd(self, side):
        # self.clear_adjust_inventory_screen()
        self.clear_user_screen()
        self.backup_place()
        # self.view_inventory_one_list_box(self.d, side)
        self.view_inventory_3_list_boxes(self.d)
        self.previous_view = "user_screen"

    # =============================================================================
    #                Change Log
    # =============================================================================

    def snapshot_of_file_on_login(self, file):
        copyfile(file, file + "_login")
        printlocaltime = localtime(time())
        monthday = str(printlocaltime.tm_mon) + "/" + str(printlocaltime.tm_mday) + " "
        currenttime = monthday + str(printlocaltime.tm_hour) + ":" + str(printlocaltime.tm_min)
        self.login_time = currenttime
        self.logged_in = True
        print(self.username_for_event_log.cget("text") + " logging in " + str(self.login_time))

    def snapshot_comparison_on_logout(self, file):
        copyfile(file, file + "_logout")
        self.compare_files(file + "_login", file + "_logout")
        printlocaltime = localtime(time())
        monthday = str(printlocaltime.tm_mon) + "/" + str(printlocaltime.tm_mday) + " "
        currenttime = monthday + str(printlocaltime.tm_hour) + ":" + str(printlocaltime.tm_min)
        self.logout_time = currenttime
        self.logged_in = False
        print(self.username_for_event_log.cget("text") + " logging out " + str(self.logout_time))

    def compare_files(self, file_one, file_two):
        try:
            with open(file_one, 'r') as file1, open(file_two, 'r') as file2:
                line_form = '{:3d} {}'.format
                file1_lines = [line_form(i, line) for i, line in enumerate(file1, 1)]
                file2_lines = [line_form(i, line) for i, line in enumerate(file2, 1)]
                results = difflib.Differ().compare(file1_lines, file2_lines)
                for line in results:
                    if line[0] == '+' or line[0] == '-':
                        print(line)
                print("\ncomparing files : " + str(file_one) + " " + str(file_two))
        except Exception as e:
            print("error in compare_files : " + str(e))

    def exit_program(self):
        if self.logged_in:
            self.snapshot_comparison_on_logout("food.txt")
        self.destroy()

    # ===================================================================================
    #                   View and/or change Inventory & users
    #                  TODO: split these into 2-3 sections for easier viewing
    # ===================================================================================
    # adjust inventory manually
    def adjust_item_quantity_button_cmd(self, d):
        self.view_inventory_one_list_box(d, 'middle')
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
        # self.previous_view = "manual_entry_screen"
        self.previous_view = "user_screen"

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

            self.item_to_be_changed_label_2.place(x=960, y=275, anchor="center")
            # New, use anchor to force the label to remain at same center regardless of length

            string_key = re.split(" :", self.item_to_be_changed.strip())[0]

            self.beautifulString(string_key)

            self.admin_modify_inventory_screen(d)
            self.item_to_be_changed_label_2.configure(text="Currently:\n" + self.beautiful_string)
            self.create_new_added.place_forget()

        else:
            self.invalid_entry_error_label.config(text="Choose an Item")
            self.create_new_added.place_forget()
            place_object(self.invalid_entry_error_label, .715, .4)

    def beautifulString(self, string_key):
        # turn into string with commas (pre-modified)
        pre_beautiful_string = str(self.d[str(self.d[string_key]['item'])].values())
        pre_beautiful_string = str(re.split("dict_values", pre_beautiful_string))
        pre_beautiful_string = pre_beautiful_string.replace("[\'\', \"([", '')
        pre_beautiful_string = pre_beautiful_string.replace('])"]', '')
        pre_beautiful_string = pre_beautiful_string.replace("'", '')
        pre_beautiful_string = pre_beautiful_string.replace("[", '')
        pre_beautiful_string = pre_beautiful_string.replace("]", '')
        # to delete list brackets
        pre_beautiful_string = pre_beautiful_string.replace(", ,", '')
        pre_beautiful_string = pre_beautiful_string.replace(" , ", '')
        pre_beautiful_string = pre_beautiful_string.replace("   ", '')
        pre_beautiful_string = pre_beautiful_string.replace("  ", '')
        # deletes bad commas/spaces
        if pre_beautiful_string.endswith(" ") or pre_beautiful_string.endswith(","):
            pre_beautiful_string = pre_beautiful_string[:pre_beautiful_string.__len__() - 1]
        # gets rid of all the empty values in barcodes[]
        self.beautiful_string = pre_beautiful_string

    def choose_an_item_to_delete_button_cmd(self, d):
        self.logout_button_place_with_d(d, "admin_edit_main")
        self.selected_item_to_be_changed = self.list_box_2.curselection()
        if self.selected_item_to_be_changed != ():
            self.change_inventory_by_this_much.set(0)
            self.item_to_be_changed = self.list_box_2.get(self.selected_item_to_be_changed)
            self.invalid_entry_error_label.place_forget()
            self.create_new_item_button.place_forget()
            self.previous_view = "admin_edit_main"
            self.backup_button_with_d_button.configure(text="Back to choose")

            self.list_box_2_label.configure(font=(self._font, self._font_big),
                                            text=f"Are you sure you want to delete\n{str(re.split(' :', self.item_to_be_changed.strip())[0]).upper()}?\n\n\n\n"
                                                 f"Enter YES to delete\n{str(re.split(' :', self.item_to_be_changed.strip())[0]).upper()}")
            place_object(self.delete_confirm_entry, .435, .5)
            self.deleteItem_button.place(relx=.47, rely=.55)
            self.delete_label.place_forget()

            self.choose_an_item_to_edit_button.place_forget()
            self.choose_an_item_to_delete_button.place_forget()
            self.list_box_2.place_forget()
            self.create_new_added.place_forget()
        else:
            self.invalid_entry_error_label.config(text="Choose an Item")
            self.create_new_added.place_forget()
            place_object(self.invalid_entry_error_label, .175, .4)

    def deleteItem(self, testWord):
        string_key = re.split(' :', self.item_to_be_changed.strip())[0]
        self.delete_confirm.set("")
        if testWord == "YES":
            self.beautifulString(string_key)
            try:
                s = open("food.txt").read()
                s = s.replace(self.beautiful_string, '')
                s = s.replace("\n\n", '\n')
                f = open("food.txt", 'w')
                f.write(s)
                f.close()
            except Exception:
                print("error in opening food.txt delete item : " + str(e))

            self.delete_label.configure(text=f"{str(string_key).upper()}\nWas Deleted")
            del self.d[string_key]
        else:
            self.delete_label.configure(text="Not Deleted\nType YES to delete")

        # jump to last page with message
        self.backup_button_with_d(self.d, self.previous_view)
        self.delete_label.place(relx=.24, rely=.6, anchor="center")

    def admin_modify_inventory_screen(self, d):
        self.isModifying = "is_admin"
        self.create_new_submit_error_num.configure(
            text="Amount, Low level, Itemsperbag\nall need to be numbers only\n\n Barcode can have\nspaces, commas, and numbers only")
        # clears last screen
        self.choose_an_item_to_edit_button.place_forget()
        self.choose_an_item_to_delete_button.place_forget()
        self.list_box_2_label.place_forget()
        self.list_box_2.place_forget()
        # reusing inputs and checks screen passing beautiful/ iteminfo
        self.create_new_item_submit_button_cmd(d)
        self.create_new_item_submit_button.configure(text="Submit Edit")
        self.create_new_item.place_forget()

        # forgets unneeded reused labels/buttons
        self.create_new_submit_error.place_forget()
        self.delete_label.place_forget()

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
                        description = 'increased by '
                        self.new_inventory_amount = (int(original_inventory_amount) +
                                                     int(self.change_inventory_by_this_much.get()))
                except Exception as e:
                    print("bad input 2 : " + str(e))

                try:
                    if direction == 'down':
                        description = 'reduced by '
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
                self.item_to_be_changed_label_2.configure(text=str(parsed_name_to_be_changed).upper() + description
                                                               + str(self.change_inventory_by_this_much.get()).upper()
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
            totalLines = len(open("food.txt").readlines())
            shutil.move("food.txt", "food.txt" + "~")
            with open("food.txt", "w+") as dest:
                dest.seek(0, os.SEEK_SET)
                with open("food.txt" + "~", "r+") as src:
                    src.seek(0, os.SEEK_SET)
                    count = 0
                    for line in src:
                        count += 1
                        if not re.match(r'^\s*$', line):
                            tokens = re.split(",", line.strip())
                            if tokens[0] == parsed_name_to_be_changed.strip():
                                tokens[1] = ' ' + str(self.new_inventory_amount)
                                if count < totalLines:
                                    dest.write(",".join(tokens) + '\n')
                                else:
                                    dest.write(",".join(tokens))
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
            self.item_to_be_changed_label_2.configure(text=str(self.item_to_be_changed).upper())
            place_object(self.item_to_be_changed_label_1, .42, .25)
            # place_object(self.item_to_be_changed_label_2, .4, .3)
            self.item_to_be_changed_label_2.place(x=950, y=350, anchor="center")
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
            # self.previous_view = "choose_item_screen"
            self.previous_view = "manual_entry_screen"
            # self.backup_button.place_forget()

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
    # TODO: shows inventory button, not forgetting, fix this
    def swap_inventory_button(self, choice):
        # inventory_button_for_three_boxes_text = self.display_inventory_high_low_outofstock_button.cget('text')
        # inventory_button_for_one_box_text = self.display_inventory_left_side_button.cget('text')
        if choice == 'all':
            if self.display_inventory_high_low_outofstock_button.cget('text') == 'View Inventory':
                self.display_inventory_high_low_outofstock_button.config(text="Hide Inventory")
                self.display_users_button.config(text="View Users")
                self.delete_user_button.place_forget()
                self.view_inventory_3_list_boxes(self.d)
            else:
                self.display_inventory_high_low_outofstock_button.config(text="View Inventory")
                self.clear_list_box()
        if choice == 'left':
            if self.display_inventory_left_side_button.cget('text') == 'View Inventory':
                self.display_inventory_left_side_button.config(text="Hide Inventory")
                self.view_inventory_one_list_box(self.d, choice)
            else:
                self.display_inventory_left_side_button.config(text="View Inventory")
                self.clear_list_box()

    # show/hide users
    def swap_display_users_button(self):
        users_button_text = self.display_users_button.cget('text')
        if users_button_text == 'View Users':
            self.display_users_button.config(text="Hide Users")
            self.display_inventory_high_low_outofstock_button.config(text="View Inventory")
            place_object(self.delete_user_button, .845, .640)
            self.view_users()
        else:
            self.display_users_button.config(text="View Users")
            self.delete_user_button.place_forget()
            self.clear_list_box()

    def edit_inventory_button_cmd(self, d):
        self.previous_view = "admin_screen"
        self.backup_button_with_d_button.place(relx=.02, rely=.9)
        self.clear_admin_screen()
        # Jump to modify screen and be able to modify and delete items
        self.modify_inventory(d)

    def modify_inventory(self, d):
        # reuse select item code from manual entry
        self.view_inventory_one_list_box(d, 'middle')
        self.create_new_added.place_forget()
        self.list_box_2.place_forget()
        self.list_box_2_label.place_forget()
        self.delete_confirm_entry.place_forget()
        self.isModifying = "is_admin_modifying_with_check"
        place_object(self.create_new_item_button, .715, .625)

        self.list_box_2_label.configure(font=(self._font, self._font_big_big), text="\\\ Select Here! //")
        place_object(self.list_box_2_label, .41, .23)
        self.list_box_2.place(relx=.44, rely=.3, relwidth=.15, relheight=.55)

        self.choose_an_item_to_edit_button.configure(text="Edit This Item")
        place_object(self.choose_an_item_to_edit_button, .7, .5)
        # New add delete button/ screen
        place_object(self.choose_an_item_to_delete_button, .15, .5)
        self.backup_button_with_d_button.configure(text="Back")

    # displays users in a box
    def view_users(self):
        self.clear_list_box()
        self.list_box_2.place(relx=.39, rely=.3, relwidth=.14)
        self.list_box_2_label.place(relx=.42, rely=.25)
        self.list_box_2_label.config(font=(self._font, self._font_medium), text="USERS", fg='black')
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

    # TODO: do side stuff, left, center for now
    # display inventory in 1 list box
    def view_inventory_one_list_box(self, d, side):
        self.make_dict(d)
        self.clear_list_box()
        if side == 'middle':
            place_object(self.list_box_2, .39, .3)
            place_object(self.list_box_2_label, .39, .25)
        if side == 'left':
            place_object(self.list_box_2, .07, .3)
            place_object(self.list_box_2_label, .08, .25)
        self.list_box_2_label.configure(font=(self._font, self._font_medium), text="Inventory", fg='black')
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
        self.list_box_3_label.configure(font=(self._font, self._font_medium), fg='black', text="INVENTORY")
        self.list_box_2_label.config(font=(self._font, self._font_medium), text="LOW INVENTORY")
        self.list_box_1_label.configure(text="OUT OF STOCK")
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

    # TODO: [Done] new decreases by 'itemsperbag' var from dict
    def lower_inventory(self, d):
        try:
            self.make_dict(d)
            totalLines = len(open("food.txt").readlines())
            shutil.move("food.txt", "food.txt" + "~")
            with open("food.txt", "w+") as dest:
                with open("food.txt" + "~", "r+") as src:
                    n = 0
                    count = 0
                    for line in src:
                        count += 1
                        if not re.match(r'^\s*$', line):
                            if n == 0:
                                dest.write(line)
                                n += 1
                            else:  # decrease amount by 'itemsperbag'
                                line = line.strip()
                                words = line.split(", ")
                                words[1] = str(int(words[1]) - int(words[3]))
                                line = ", ".join(words)
                                line.strip()
                                if count <= totalLines - 1:
                                    line = line + '\n'
                                dest.write(line)
            self.bag_of_food_removed_from_inventory.configure(text=f"{int(self.numberofBags)} bag(s) of food removed")
            self.bag_of_food_removed_from_inventory.place(relx=.4, rely=.9325)
            # [fixed] the \n at the end of txt file, would leave gaps when bag was made then createnewitem appended
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
        self.user_screen()
        # self.admin_screen()

        # TODO: commnted out if/else to skip login steps while building program,
        #  put back in for finished product
        '''if self.ready_to_login:
            self.clear_verify()
            self.clear_login_screen()
            self.username_for_event_log.configure(text=str(tokens[0]))
            place_object(self.username_for_event_log, .02, .85)
            # logging in,
            # snapshot of inventory on login - timestamp, username_for_event_log
            # check that logged in
            # on logout :
            # snapshot of inventory on logout - timestamp
            # compare snapshots
            # append changes from snapshot to changelog
            # email changelog button simliar to email inventory
            self.snapshot_of_file_on_login("food.txt")                                                                  
            if tokens[0] == 'adminarmy':
                self.admin_screen()
            else:
                self.user_screen()
        else:
            self.login_failure("username & password invalid", .65, .4)
            self.clear_verify()
            self.login_info_screen()'''


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

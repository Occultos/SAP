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
import os.path
from os import path
import textwrap
import smtplib
import imaplib
import email
import datetime
from datetime import datetime


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
        self.iconbitmap(r'images/salogo_YMx_icon.ico')  # icon
        self._bgcolor = 'white'
        self._activebgcolor = '#e4fcdc'
        self._font = "Helvetica"
        self._font_big = 26
        self._font_big_big = 40
        self._font_medium = 22
        self._font_smallish = 20
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
        self.changelog_text = tk.StringVar()
        self.changelog_text = ''
        self.bags_made_per_login = tk.IntVar()
        self.partial_bags_made_per_login = tk.IntVar()
        self.inventory_comparison_before = tk.StringVar()
        self.inventory_comparison_before = ''
        self.inventory_comparison_after = tk.StringVar()
        self.inventory_comparison_after = ''
        self.comparison = tk.StringVar
        self.comparison = ''
        self.list_l = []
        self.list_k = []
        self.from_add_subtract = ''
        self.from_admin_message = False
        self.admin_message = ''
        self.set_default_times()

        # moved to login screen
        # self.default_admin_message()
        # self.admin_message = '\n'.join(textwrap.wrap(self.admin_message, 64))

        # ============================================================================================
        #                                    Universal Buttons
        # ============================================================================================

        self.Button_1 = tk.Button(self, background=self._bgcolor, font=(self._font, self._font_big),
                                  activebackground=self._activebgcolor)

        self.Button_2 = tk.Button(self, background=self._bgcolor, font=(self._font, self._font_big),
                                  activebackground=self._activebgcolor)

        self.Button_3 = tk.Button(self, background=self._bgcolor, font=(self._font, self._font_big),
                                  activebackground=self._activebgcolor)

        self.Button_4 = tk.Button(self, background=self._bgcolor, font=(self._font, self._font_big),
                                  activebackground=self._activebgcolor)

        self.Button_5 = tk.Button(self, background=self._bgcolor, font=(self._font, self._font_big),
                                  activebackground=self._activebgcolor)

        # ============================================================================================
        #                                    Universal Labels
        # ============================================================================================

        self.Label_1 = tk.Label(self, font=(self._font, self._font_medium), fg='black')

        self.Label_2 = tk.Label(self, font=(self._font, self._font_medium), fg='black')

        self.Label_3 = tk.Label(self, font=(self._font, self._font_medium), fg='black')

        self.Label_4 = tk.Label(self, font=(self._font, self._font_medium), fg='black')

        self.Label_5 = tk.Label(self, font=(self._font, self._font_medium), fg='black')

        # ============================================================================================
        #                                    Universal Entries
        # ============================================================================================

        self.Entry_var_1 = tk.StringVar()
        self.Entry_1 = tk.Entry(self, font=(self._font, self._font_big), textvariable=self.Entry_var_1, width=20)

        self.Entry_var_2 = tk.StringVar()
        self.Entry_2 = tk.Entry(self, font=(self._font, self._font_big), textvariable=self.Entry_var_2, width=20)

        self.Entry_var_3 = tk.StringVar()
        self.Entry_3 = tk.Entry(self, font=(self._font, self._font_big), textvariable=self.Entry_var_3, width=20)

        self.Entry_var_4 = tk.StringVar()
        self.Entry_4 = tk.Entry(self, font=(self._font, self._font_big), textvariable=self.Entry_var_4, width=20)

        self.Entry_var_5 = tk.StringVar()
        self.Entry_5 = tk.Entry(self, font=(self._font, self._font_big), textvariable=self.Entry_var_5, width=20)

        self.admin_create_new_clear()

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
                                     command=lambda: self.login_load_screen())
        self.loginbutton.configure(activebackground=self._activebgcolor, padx=66)

        # back button to return to previous screen
        self.backup_button = tk.Button(self, text="Back",
                                       background=self._bgcolor, font=(self._font, self._font_big),
                                       command=lambda: self.back_button_func(self.previous_view))
        self.backup_button.configure(activebackground=self._activebgcolor, padx=25)

        # logoutButton
        self.logoutButton = tk.Button(self, text="Logout",
                                      background=self._bgcolor, font=(self._font, self._font_big),
                                      command=lambda: self.login_screen())
        self.logoutButton.configure(activebackground=self._activebgcolor, padx=25)

        # register account button
        self.registerbutton = tk.Button(self, text="Register",
                                        background=self._fgcolor, font=(self._font, self._font_big),
                                        command=lambda: self.register_user())

        self.registerbutton.configure(activebackground=self._activebgcolor, padx=45)

        # eyeball to show/hide passwords
        self.eyeball_closed_photo = tk.PhotoImage(file="images/closedeye.png").subsample(9, 9)
        self.eyeball_open_photo = tk.PhotoImage(file="images/openeye.png").subsample(9, 9)

        self.eyeball_button = tk.Button(self, image=self.eyeball_closed_photo, text='closed',
                                        command=lambda: self.swap_eyeball())
        # bag photo
        self.food_bag_photo = tk.PhotoImage(file="images/foodbag.png").subsample(2, 2)

        # =================================================================================
        # buttons in user add items screen
        # ==================================================================================
        # choose an item
        self.choose_an_item_button = tk.Button(self, text="Choose An Item",
                                               background=self._fgcolor, font=(self._font, self._font_medium),
                                               command=lambda: self.choose_an_item_to_change_cmd())
        self.choose_an_item_button.configure(activebackground=self._activebgcolor, padx=47)

        # choose a different item
        self.choose_new_item = tk.Button(self, text="Choose a New Item",
                                         background=self._fgcolor, font=(self._font, self._font_medium),
                                         command=lambda: self.adjust_item_quantity_button_cmd())
        self.choose_new_item.configure(activebackground=self._activebgcolor, padx=24)

        # manual entry button
        self.manual_entry_button = tk.Button(self, text="Manual Entry",
                                             background=self._fgcolor, font=(self._font, self._font_medium),
                                             command=lambda: self.manual_entry_screen())
        self.manual_entry_button.configure(activebackground=self._activebgcolor, padx=25)

        # button inside manual entry screen
        self.adjust_item_quantity_button = tk.Button(self, text="Adjust Item Quantity",
                                                     font=(self._font, self._font_medium), background=self._fgcolor,
                                                     command=lambda: self.adjust_item_quantity_button_cmd())
        self.adjust_item_quantity_button.configure(activebackground=self._activebgcolor, padx=20)

        # change value of items, currently in manual entry screen
        self.change_value_button = tk.Button(self, text="Change Value",
                                             font=(self._font, self._font_medium), background=self._fgcolor,
                                             command=lambda: self.change_value_of_item_chosen())
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
                                                        'Barcodes for Adding'))
        self.barcode_scanner_add_button.configure(activebackground=self._activebgcolor, padx=29)

        # go to add or remove items screen using barcode
        self.barcode_scanner_remove_button = tk.Button(self, text="Remove items",
                                                       background=self._fgcolor, font=(self._font, self._font_medium),
                                                       command=lambda: self.barcode_scanner_add_remove_button_cmd(
                                                           'Barcodes for Subtracting'))
        self.barcode_scanner_remove_button.configure(activebackground=self._activebgcolor)

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
                                               command=lambda: self.edit_inventory_button_cmd())
        self.edit_inventory_button.configure(activebackground=self._activebgcolor, padx=20)

        # delete users : in admin screen
        self.delete_user_button = tk.Button(self, text="Delete User", font=(self._font, self._font_medium),
                                            background=self._fgcolor2,
                                            command=lambda: self.remove_username_func())
        self.delete_user_button.config(activebackground=self._activebgcolor, padx=29)

        # open email entry
        self.admin_email_inventory_button = tk.Button(self, text="Email inventory", background=self._fgcolor,
                                                      font=(self._font, self._font_medium),
                                                      command=lambda: self.email_entry(self.d))
        self.admin_email_inventory_button.configure(activebackground=self._activebgcolor, padx=8)

        # send email
        self.admin_email_send_button = tk.Button(self, text="Send", background=self._fgcolor,
                                                 font=(self._font, self._font_medium),
                                                 command=lambda: self.admin_email_inventory(self.d))
        self.admin_email_send_button.configure(activebackground=self._activebgcolor)

        # admin_email_partners_button
        self.admin_email_partners_button = tk.Button(self, text="Email Partners", background=self._fgcolor,
                                                     font=(self._font, self._font_medium),
                                                     command=lambda: self.email_partners())
        self.admin_email_partners_button.configure(activebackground=self._activebgcolor, padx=10)

        # make csv for excel
        self.make_csv_button = tk.Button(self, background=self._fgcolor, font=(self._font, self._font_medium),
                                         command=lambda: self.make_csv())
        self.make_csv_button.configure(activebackground=self._activebgcolor)

        # view changelog
        self.view_changelog_text = tk.Text(self, wrap=WORD)
        self.view_changelog_button = tk.Button(self, text="View Changelog", background=self._fgcolor,
                                               font=(self._font, self._font_smallish),
                                               command=lambda: self.view_changelog())
        self.view_changelog_button.configure(activebackground=self._activebgcolor, padx=10)

        # email changelog
        self.email_changelog_button = tk.Button(self, text="Email Changelog", background=self._fgcolor,
                                                font=(self._font, self._font_smallish),
                                                command=lambda: self.email_changelog_entry())
        self.email_changelog_button.configure(activebackground=self._activebgcolor, padx=5)

        # volunteer instructions
        self.volunteer_instructions_button = tk.Button(self, text="Volunteer\nInstructions", background=self._fgcolor,
                                                       font=(self._font, self._font_smallish),
                                                       command=lambda: self.volunteer_instructions_screen())
        self.volunteer_instructions_button.configure(activebackground=self._activebgcolor, padx=36)

        self.textBox = tk.Text(self, wrap=WORD, height=14, width=64, font=(self._font, self._font_big))
        # =============================================================================
        #                 END Admin screen buttons
        # =============================================================================

        # =======================================================================================
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

        self.volunteer_instructions_label = tk.Label(self, text="Volunteer Instructions",
                                                     background='#c1bcf5', font=(self._font, self._font_medium))
        self.volunteer_instructions_label.configure(padx=20, pady=15)
        self.food_bag_contents_title = tk.Label(self, text="What is in a Bag",
                                                background='#c1bcf5', font=(self._font, self._font_medium))

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
        self.login_army_logo = tk.PhotoImage(file="images/SA_doing_the_most_good.png").subsample(3, 3)
        self.login_army_label = tk.Label(self, image=self.login_army_logo)
        self.image = self.login_army_logo  # save a reference through garbarge pickup

        # =======================================================================================
        #                                           TOOLTIP - INIT
        # =======================================================================================

        ToolTip(self.volunteer_instructions_label, self._font, self.admin_message, delay=0.0)

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

    def set_default_times(self):
        self.updated_time = '2020-01-01 00:00:00'
        self.updated_time = datetime.strptime(self.updated_time, '%Y-%m-%d %H:%M:%S')

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

    def back_button_func(self, words):
        # goes back to user screen
        if words == "user_screen":
            self.clear_create_new_item()
            self.clear_makebag_screen()
            self.clear_todo_label()
            self.clear_list_box()
            self.adjust_item_quantity_button.place_forget()
            self.choose_an_item_button.place_forget()
            self.clear_barcode_screen()
            self.unbind_return_func()
            self.list_of_items_words = ''
            self.list_of_items_label.place_forget()
            self.list_box_2_label.place_forget()
            self.invalid_entry_error_label.place_forget()
            self.display_inventory_left_side_button.place_forget()
            self.clear_add_barcode_to_existing()
            self.textBox.place_forget()
            self.clear_volunteer_instructions_screen()

            self.user_screen()
        elif words == "volunteer_instructions_screen":
            self.clear_admin_message_configure()
            self.volunteer_instructions_screen()

        elif words == "admin_message_configure":
            self.clear_modify_inventory()
            self.list_box_2_label.place_forget()
            self.list_box_2.place_forget()
            self.admin_message_configure()

        # goes back to make a bag screen
        elif words == "make_bag_screen":
            self.make_bag_screen()
            self.clear_todo_label()
            self.clear_list_box()
            self.food_file_error_label.place_forget()
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
            self.adjust_item_quantity_button_cmd()
            self.choose_new_item.place_forget()
            self.adjust_inventory_entry.place_forget()
            self.add_button.place_forget()
            self.subtract_button.place_forget()
            self.invalid_entry_error_label.place_forget()
            self.confirm_inventory_manual_button.place_forget()
            self.cancel_inventory_manual_button.place_forget()
            self.invalid_entry_error_label.place_forget()
        elif words == "add_barcode_to_existing":
            self.clear_create_new_item()
            self.add_barcode_to_existing()
        elif words == 'barcode_scanner_screen':
            self.clear_barcode_screen()
            self.barcode_scanner_screen()
            self.Label_4.place_forget()
        elif words == "admin_edit_main":
            self.clear_create_new_item()
            self.clear_admin_screen()
            self.clear_to_login()
            self.logout_button_place()
            self.invalid_entry_error_label.place_forget()
            self.edit_inventory_button_cmd()
        elif words == "admin_screen":
            self.admin_screen()
            self.clear_list_box()
            self.list_box_2.place_forget()
            self.list_box_2_label.place_forget()
            self.backup_button.place_forget()
            self.clear_volunteer_instructions_screen()
            self.clear_email_partners()
            self.clear_email_entry_inventory()
            self.unbind_return_func()

            self.Label_1.place_forget()
            self.Label_2.place_forget()
            self.Label_3.place_forget()
            self.Label_4.place_forget()

            self.Button_1.place_forget()
            self.Button_2.place_forget()
            self.Button_3.place_forget()

            self.display_users_button.config(text="View Users")
            self.display_inventory_high_low_outofstock_button.config(text="View Inventory")

    # ====================================================================================
    #                                   EMAIL Functions
    # ===================================================================================

    def read_email(self):
        try:
            ORG_EMAIL = "@gmail.com"
            FROM_EMAIL = "volunteerinstructions" + ORG_EMAIL
            FROM_PWD = "1qaz!QAZ1qaz!QAZ"
            SMTP_SERVER = "imap.gmail.com"
            SMTP_PORT = 993
            mail = imaplib.IMAP4_SSL(SMTP_SERVER)
            mail.login(FROM_EMAIL, FROM_PWD)
            mail.select('inbox')
            typ, data = mail.search(None, 'ALL')
            mail_ids = data[0]
            id_list = mail_ids.split()
            first_email_id = int(id_list[0])
            latest_email_id = id_list[-1]
            typ, data = mail.fetch(latest_email_id, '(RFC822)')

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1].decode('utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    self.email_time = msg['Date']
                    self.email_msg = ''
                    self.email_msg = 'Date: ' + str(self.email_time) + '\n' + 'From: ' + str(email_from) + '\n' + \
                                     'Subject : ' + str(email_subject) + '\n' + '\n'

                    # email date & time of most recent email
                    self.email_datetime = self.email_time[:-6]
                    self.email_date_time = datetime.strptime(self.email_datetime, '%a, %d %b %Y %H:%M:%S')
                    # just the day of email
                    self.email_day = str(self.email_date_time).split(" ")[0]
                    self.email_day = datetime.strptime(self.email_day, '%Y-%m-%d')

                    if msg.is_multipart():
                        for payload in msg.get_payload():
                            if payload.get_payload()[0] == '<':
                                continue
                            self.email_msg = self.email_msg + payload.get_payload()
                    else:
                        print("Does this else statment do anything?")
                        print(msg.get_payload())


        except Exception as e:
            print("Error in reading email : vars : " + str(e))

    def set_instructions(self):
        pass

    def email_changelog_entry(self):
        self.make_dict(self.d)
        self.clear_volunteer_instructions_screen()
        self.display_users_button.config(text="View Users")
        self.delete_user_button.place_forget()
        self.clear_list_box()
        self.display_inventory_high_low_outofstock_button.config(text="View Inventory")

        self.admin_email_label.place_forget()
        self.enter_email_add_label.configure(text='Enter Email Address\nto send changelog',
                                             font=(self._font, self._font_big))
        place_object(self.enter_email_add_label, .2, .9175)
        place_object(self.enter_email_add_entry, .3675, .92, True)
        self.admin_email_send_button.configure(command=lambda: self.admin_email_changelog(self.d))
        place_object(self.admin_email_send_button, .73, .9125)
        self.bind('<Return>', lambda x: self.admin_email_changelog(self.d))

    def admin_email_changelog(self, d):
        self.unbind_return_func()
        self.print_dict_to_file(d)
        self.admin_email_label.configure(text="Changelog Email Sent")
        place_object(self.admin_email_label, .58, .9275)

        try:
            if not os.path.isfile("text/changelog.txt"):
                with open("text/changelog.txt", "a+") as f:
                    f.write("Change Log" + '\n==============================================================\n')
        except Exception as e:
            print("error creating changelog " + str(e))
        try:
            if os.path.isfile("text/changelog.txt"):
                with open("text/changelog.txt", "a+") as f:
                    f.write(self.changelog_text)
                    f.write('==============================================================\n')
        except Exception as e:
            print("error updating changelog " + str(e))

        emailpw = self.password_info
        try:
            yag = yagmail.SMTP('sanantoniopantrynoreply@gmail.com', emailpw)
            contents = [
                "Sent via SAP inventory program. Do not reply",
                "You can find current changelog attached.", 'text/changelog.txt']
            yag.send(self.email_add.get(), 'Food Inventory', contents)
            self.changelog_text = self.changelog_text + '\tEmail sent to : ' + \
                                  self.email_add.get() + ' : changelog status\n'
        # Alternatively, with a simple one-liner:
        # yagmail.SMTP('mygmailusername').send('to@someone.com', 'subject', contents)
        except Exception as e:
            # print("error " + str(e))
            self.admin_email_label.configure(text="Email error", font=(self._font, self._font_big))
            self.unbind_return_func()
        self.email_add.set('')
        self.clear_changelog()

    def email_entry(self, d):
        self.clear_volunteer_instructions_screen()
        self.admin_email_label.place_forget()
        self.clear_changelog()

        self.enter_email_add_label.configure(text='Enter Email Address\nto send inventory',
                                             font=(self._font, self._font_big))
        place_object(self.enter_email_add_label, .2, .9175)
        place_object(self.enter_email_add_entry, .3675, .92, True)
        self.admin_email_send_button.configure(command=lambda: self.admin_email_inventory(self.d))
        place_object(self.admin_email_send_button, .73, .9125)
        self.bind('<Return>', lambda x: self.admin_email_inventory(self.d))
        self.email_box_update()
        self.list_box_2.bind("<Double-Button-1>", self.on_double)
        self.previous_view = "admin_screen"
        self.backup_place()

    def email_partners(self):
        self.clear_admin_screen()
        self.clear_list_box()
        self.clear_volunteer_instructions_screen()
        self.previous_view = "admin_screen"
        self.backup_button.place(relx=.02, rely=.9)
        self.already_exist = False
        self.Label_2.place_forget()
        self.Label_2.place(relx=.6, rely=.3, anchor='center')
        self.Label_2.configure(text='Modify Email Partners List', fg='Black')

        self.email_box_update()

        self.email_to_be_changed = self.list_box_2.curselection()
        self.Entry_1.configure(width=30)
        self.Entry_1.place(relx=.45, rely=.5)
        self.Entry_var_1.set('')
        self.list_box_2.bind("<Double-Button-1>", self.on_double)

        self.button_select = ''
        self.Button_1.configure(text="Edit Email", background=self._fgcolor, font=(self._font, self._font_medium),
                                command=lambda *args: self.button_select_cmd("Edit"),
                                activebackground=self._activebgcolor, padx=0)
        place_object(self.Button_1, .45, .4)

        self.Button_2.configure(text="Delete Email", background=self._fgcolor, font=(self._font, self._font_medium),
                                command=lambda *args: self.button_select_cmd("Delete"),
                                activebackground=self._activebgcolor, padx=0)
        place_object(self.Button_2, .55, .4)

        self.Button_3.configure(text="Add Email", background=self._fgcolor, font=(self._font, self._font_medium),
                                command=lambda *args: self.button_select_cmd("Add"),
                                activebackground=self._activebgcolor, padx=0)
        place_object(self.Button_3, .67, .4)

    def email_box_update(self):
        self.list_box_2.place_forget()
        self.list_box_2_label.place_forget()
        self.list_box_2.delete(0, tk.END)
        box2count = 0
        with open('text/food_partners.txt') as food_partners:
            for line in food_partners:
                box2count += 1
                self.list_box_2.insert(box2count, str(line).replace('\n', ''))
        self.list_box_2.place(relx=.15, rely=.3, relwidth=.25, relheight=.6)

        self.list_box_2_label.configure(text='            Double click to select', font=(self._font, self._font_medium))
        self.list_box_2_label.place(relx=.15, rely=.25)

    def button_select_cmd(self, words):
        self.Label_2.place_forget()
        self.Label_2.place(relx=.6, rely=.3, anchor='center')

        if self.email_to_be_changed != () or words == "Add":
            self.button_select = words
            if self.button_select == "Edit":
                try:
                    with open("text/food_partners.txt", "r") as f:
                        lines = f.readlines()
                    with open("text/food_partners.txt", "w") as f:
                        for line in lines:
                            if line.strip("\n") != self.email_to_be_changed:
                                f.write(line)
                            else:
                                f.write(str(self.Entry_var_1.get() + '\n'))
                except Exception as e:
                    print("error in opening food_partners.txt : delete email : replace" + str(e))
                if str(self.Entry_var_1.get()) == '':
                    self.Label_2.configure(text='Select or Enter Email', fg='red')
                else:
                    self.Label_2.configure(
                        text=f'Edited Email: {str(self.email_to_be_changed)}\n to {str(self.Entry_var_1.get())}',
                        fg='blue')
                self.Entry_var_1.set('')

            elif self.button_select == "Delete":
                try:
                    with open("text/food_partners.txt", "r") as f:
                        lines = f.readlines()
                    with open("text/food_partners.txt", "w") as f:
                        for line in lines:
                            if line.strip("\n") != str(self.Entry_var_1.get()):
                                f.write(line)
                except Exception as e:
                    print("error in opening food_partners.txt : delete email : replace" + str(e))
                if str(self.Entry_var_1.get()) == '':
                    self.Label_2.configure(text='Select or Enter Email', fg='red')
                else:
                    self.Label_2.configure(text=f'Deleted Email: {str(self.Entry_var_1.get())}', fg='blue')
                self.Entry_var_1.set('')

            elif self.button_select == "Add":
                try:
                    with open('text/food_partners.txt') as food_partners:
                        for line in food_partners:
                            if str(self.Entry_var_1.get()).replace('\n', '') == str(line).replace('\n', ''):
                                self.already_exist = True
                except Exception as e:
                    print('add email' + str(e))

                if str(self.Entry_var_1.get()) == '':
                    self.Label_2.configure(text='Select or Enter Email', fg='red')
                elif self.already_exist:
                    self.Label_2.configure(text='Already exist', fg='red')
                    self.already_exist = False
                else:
                    with open('text/food_partners.txt', 'a+') as food_partners:
                        food_partners.write('\n' + str(self.Entry_var_1.get()))
                        self.Label_2.configure(text=f'Added Email: {str(self.Entry_var_1.get())}', fg='blue')
                        self.Entry_var_1.set('')
        else:
            self.Label_2.configure(text='Select or Enter Email', fg='red')
        self.email_box_update()

    def on_double(self, event):
        try:
            widget = event.widget
            self.email_to_be_changed = widget.get(widget.curselection()[0])
            self.Entry_var_1.set(str(self.email_to_be_changed))
            self.email_add.set(str(self.email_to_be_changed))
            self.Label_2.place_forget()
            self.unbind('<Double-Button-1>')
        except Exception as e:
            print("on_double  " + str(e))

    def clear_email_partners(self):
        self.backup_button.place_forget()
        self.list_box_2.place_forget()
        self.Entry_1.place_forget()
        self.list_box_2_label.place_forget()
        self.Button_1.place_forget()
        self.Button_2.place_forget()

    def admin_email_inventory(self, d):
        self.unbind_return_func()
        self.print_dict_to_file(d)
        self.admin_email_label.configure(text="Inventory Email Sent")
        place_object(self.admin_email_label, .58, .9275)
        emailpw = self.password_info
        try:
            yag = yagmail.SMTP('sanantoniopantrynoreply@gmail.com', emailpw)
            contents = [
                "Sent via SAP inventory program. Do not reply",
                "You can find current inventory status attached.", 'text/food_status.txt']
            yag.send(self.email_add.get(), 'Food Inventory', contents)
            self.changelog_text = self.changelog_text + '\tEmail sent to : ' + \
                                  self.email_add.get() + ' : inventory levels\n'
        # Alternatively, with a simple one-liner:
        # yagmail.SMTP('mygmailusername').send('to@someone.com', 'subject', contents)
        except Exception as e:
            # print("error " + str(e))
            self.admin_email_label.configure(text="Email error", font=(self._font, self._font_big))
            self.unbind_return_func()
        self.email_add.set('')
        self.clear_changelog()

    # ===================================================================================
    #                                                 SCREENS
    # ===================================================================================

    # main login screen
    def login_screen(self):
        if self.logged_in:
            self.snapshot_on_logout()
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
        # backup_button_
        self.backup_button.place_forget()

    def admin_screen(self):
        self.unbind_return_func()
        self.clear_login_screen()
        self.logout_button_place()
        self.clear_login_info_error()
        self.army_image_place()
        self.eyeball_button.place_forget()
        self.from_admin_message = False
        self.volunteer_instructions_label.place_forget()

        place_object(self.view_changelog_button, .845, .835)  # view changelog
        place_object(self.display_inventory_high_low_outofstock_button, .845, .77)  # show inventory
        place_object(self.display_users_button, .845, .705)  # show users
        place_object(self.edit_inventory_button, .845, .64)  # edit inventory
        place_object(self.email_changelog_button, .845, .51)  # email changelog
        place_object(self.admin_email_inventory_button, .845, .44)  # email inventory
        place_object(self.admin_email_partners_button, .845, .37)  # email_partners_button

        # add export to csv button
        self.make_csv_button.configure(text="Make Excel .csv", padx=3)
        place_object(self.make_csv_button, .845, .575)

        # volunteer instructions
        place_object(self.volunteer_instructions_button, .845, .275)

    def user_screen(self):
        '''
        Button_1 : calls make_bag_screen
        Button_2 : calls display_inventory_user_button_cmd
        Button_3 : calls barcode_scanner_screen
        Button_4 : calls manual_entry_screen
        Button_5 : calls create_new_item_screen
        '''
        self.unbind_return_func()
        self.isModifying = "as_user"
        self.isPassingBarcode = "is_passing_false"
        self.clear_login_screen()
        self.logout_button_place()
        self.clear_login_info_error()
        self.backup_button.place_forget()
        self.eyeball_button.place_forget()
        self.army_image_place()
        self.Entry_1.config(show='')
        self.volunteer_instructions_label.place(relx=.01, rely=.05)
        self.volunteer_instructions_ToolTip_update()

        # place_object(self.volunteer_instructions_button, .458, .3)

        self.Button_1.configure(text="Make A New Bag", background=self._fgcolor, font=(self._font, self._font_medium),
                                command=lambda: self.make_bag_screen(), activebackground=self._activebgcolor, padx=0)
        place_object(self.Button_1, .47, .4)

        self.Button_2.configure(text="View Inventory", font=(self._font, self._font_medium), background=self._fgcolor,
                                command=lambda: self.display_inventory_user_button_cmd('middle'),
                                activebackground=self._activebgcolor, padx=16)
        place_object(self.Button_2, .47, .5)

        self.Button_3.configure(text="Barcode Scan", background=self._fgcolor, font=(self._font, self._font_medium),
                                command=lambda: self.barcode_scanner_screen(), activebackground=self._activebgcolor,
                                padx=18)
        place_object(self.Button_3, .47, .6)

        self.Button_4.configure(text="Manual Entry", background=self._fgcolor, font=(self._font, self._font_medium),
                                command=lambda: self.manual_entry_screen(), activebackground=self._activebgcolor,
                                padx=25)
        place_object(self.Button_4, .47, .7)

        self.Button_5.configure(text="Create New Item", font=(self._font, self._font_medium), background=self._fgcolor,
                                command=lambda: self.create_new_item_screen(), activebackground=self._activebgcolor,
                                padx=0)
        place_object(self.Button_5, .47, .8)

        self.isBarcode = False
        self.Label_3.configure(text='')

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
        self.bind('<Tab>', lambda x: self.bind_tab_to_User_Name_entry())
        self.bind('<Return>', lambda x: self.login_load_screen())
        self.backup_place()
        self.previous_view = "login_screen"

    def bind_tab_to_User_Name_entry(self):
        self.username_entry.place_forget()
        place_object(self.username_entry, .430, .4, True)

    def unbind_return_func(self):
        self.unbind('<Return>')
        self.unbind('<Tab>')

    # load registration screen
    def registration_info_screen(self):
        self.unbind_return_func()
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

    def default_admin_message(self):
        # check email / if else to thisu
        self.read_email()

        # current time
        self.current_time = datetime.now()
        self.current_time = str(self.current_time).split(".")[0]
        self.current_time = datetime.strptime(self.current_time, '%Y-%m-%d %H:%M:%S')
        # current day
        self.current_day = str(self.current_time).split(" ")[0]
        self.current_day = datetime.strptime(self.current_day, '%Y-%m-%d')

        # update admin msg
        if self.email_day == self.current_day and self.email_date_time > self.updated_time:
            self.admin_message = self.email_msg
        else:
            try:
                with open('text/admin_message.txt', 'r+') as file:
                    self.admin_message = file.read()
            except Exception as e:
                print("admin_message read" + str(e))

        self.volunteer_instructions_ToolTip_update()

    def volunteer_instructions_screen(self):
        self.clear_volunteer_instructions_screen()
        self.previous_view = "admin_screen"
        self.textBox.delete('1.0', END)
        self.textBox.insert(INSERT, self.admin_message)
        self.textBox.place(relx=0.05, rely=0.30)
        self.textBox.config(state=DISABLED)

        self.Button_1.place_forget()
        self.Button_1.configure(text="Edit Message", background=self._fgcolor,
                                font=(self._font, self._font_medium),
                                command=lambda: self.admin_message_configure(),
                                activebackground=self._activebgcolor, padx=30)
        self.Button_1.place(relx=0.2, rely=0.875)

        self.display_users_button.config(text="View Users")
        self.delete_user_button.place_forget()
        self.clear_list_box()
        self.display_inventory_high_low_outofstock_button.config(text="View Inventory")
        self.clear_email_entry_inventory()
        self.clear_changelog()

    # TODO: check email in user screen

    def clear_volunteer_instructions_screen(self):
        self.Button_1.place_forget()
        self.textBox.place_forget()
        self.Label_1.place_forget()
        self.Label_2.place_forget()
        self.Label_3.place_forget()
#TODO: remove tooltip

    def clear_email_entry_inventory(self):
        self.enter_email_add_label.place_forget()
        self.enter_email_add_entry.place_forget()
        self.admin_email_send_button.place_forget()

    def admin_message_configure(self):
        self.Label_3.place_forget()

        # TODO: Danny, is this next line neccessary?
        self.Entry_var_1.set('')

        self.Label_1.configure(text="Enter new message", font=(self._font, self._font_big), image='')
        self.Label_1.place(relx=0.05, rely=0.25)

        self.textBox.focus_set()
        self.textBox.delete('1.0', END)
        self.textBox.insert(INSERT, self.admin_message)
        self.textBox.place(relx=0.05, rely=0.30)
        self.textBox.config(state='normal')

        self.Button_1.place_forget()
        self.Button_1.configure(text="Update Message", background=self._fgcolor,
                                font=(self._font, self._font_medium),
                                command=lambda: self.retrieve_input(),
                                activebackground=self._activebgcolor, padx=10)

        self.Button_1.place(relx=0.2, rely=0.875)

    def clear_admin_message_configure(self):
        self.Label_1.place_forget()
        self.Label_2.place_forget()
        self.Label_3.place_forget()
        self.textBox.place_forget()
        self.Button_1.place_forget()
        self.edit_inventory_button.place_forget()

    def retrieve_input(self):
        self.Label_3.place_forget()
        self.inputValue = self.textBox.get("1.0", END)
        '''x_list = self.inputValue.split("\n")
        for str in x_list:
            if len(str) > 75:
                self.Label_3.configure(text="Don't let words hit end of box!", fg='red')
                self.Label_3.place(relx=0.73, rely=0.3)
                return'''
        try:
            with open('text/admin_message.txt', 'w+') as file:
                file.write(self.inputValue)
        except Exception as e:
            print("admin_message write" + str(e))

        #time when msg was manually updated
        self.updated_time = datetime.now()
        self.updated_time = str(self.updated_time).split(".")[0]
        self.updated_time = datetime.strptime(self.updated_time, '%Y-%m-%d %H:%M:%S')

        self.admin_message = self.inputValue
        self.clear_admin_message_configure()
        self.back_button_func(self.previous_view)
        self.volunteer_instructions_screen()
        self.Label_3.configure(text="Message updated", fg='blue')
        self.Label_3.place(relx=0.05, rely=0.25)


    def volunteer_instructions_ToolTip_update(self):
        self.volunteer_instructions_label.destroy()
        self.volunteer_instructions_label = tk.Label(self, text="Volunteer Instructions",
                                                     background='#c1bcf5', font=(self._font, self._font_medium))
        self.volunteer_instructions_label.configure(padx=20, pady=15)
        self.volunteer_instructions_label.place(relx=.01, rely=.05)
        ToolTip(self.volunteer_instructions_label, self._font, self.admin_message, delay=0.0)

    # made a bag
    def made_a_bag_screen(self):
        '''
        //// This page is what you see after successful bag making ////
        Entry_var_1 : number of bags to be made
        Button_1 : Make more bags/ goes back
        Label_4 : Error label
        '''
        # Checks if int is entered, then checks if it is in bounds calculated in calculate_max_bags
        if str(self.Entry_var_1.get()).isnumeric() == True and int(self.Entry_var_1.get()) <= int(
                self.lowestRatio) and int(
            self.Entry_var_1.get()) > 0:
            self.numberofBags = int(self.Entry_var_1.get())
            self.Entry_var_1.set("")
            # lowers inventory by Entry_var_1/self.numberofBags full food bags
            self.lower_inventory_new()

            self.clear_makebag_screen()
            self.previous_view = "make_bag_screen"

            self.Button_1.configure(text="Make more bags", background=self._fgcolor,
                                    font=(self._font, self._font_medium),
                                    command=lambda: self.back_button_func(self.previous_view),
                                    activebackground=self._activebgcolor, padx=10)
            self.Button_1.place(relx=.8, rely=.3)
            self.view_inventory_3_list_boxes(self.d)
        else:
            self.make_bag_screen()
            self.Label_4.configure(font=(self._font, self._font_big), fg='red',
                                   text="Enter number > 0\nand needs to be less than bags left")
            self.Label_4.place(relx=.75, rely=.3, anchor="center")
            self.Entry_var_1.set("")

    def lower_inventory_new(self):
        '''
        lowers inventory by subtracting 'itemsperbag' * self.numberofBags from 'amount' for each item in self.d
        Turned 0(n^2) into O(1), since the bag will almost always be around 20 unique items
        Label_5 : info label
        '''
        count = 0
        try:
            totalLines = len(open("text/food.txt").readlines())
            with open('text/food.txt', 'w') as f:
                print("item, amount, lowlevel, itemsperbag, barcode", file=f)
                for p_id, p_info in self.d.items():
                    self.d[p_id]['amount'] -= self.d[p_id]['itemsperbag'] * self.numberofBags
                    self.beautifulString(str(p_id))
                    if count < totalLines - 2:
                        self.beautiful_string = str(self.beautiful_string) + '\n'
                    f.write(str(self.beautiful_string))
                    count += 1

            self.Label_5.configure(font=(self._font, self._font_small),
                                   text=f"{int(self.numberofBags)} bag(s) of food removed", fg='black')
            self.Label_5.place(relx=.4, rely=.9325)
            self.bags_made_per_login = self.bags_made_per_login + int(self.numberofBags)
            self.d = {}
            self.make_dict(self.d)
        except Exception as e:
            print("error in opening food.txt : lower_inventory_new " + str(e))

    def food_bag_contents_title_ToolTip_update(self):
        self.food_bag_contents_title.destroy()
        self.food_bag_contents_title = tk.Label(self, text="What is in a Bag",
                                                background='#c1bcf5', font=(self._font, self._font_medium))
        self.food_bag_contents_title.configure(padx=20, pady=15)
        self.food_bag_contents_title.place(relx=.01, rely=.5)

        self.food_bag_contents = ''
        for key, value in self.d.items():
            if self.d[key]['itemsperbag'] > 0:
                self.food_bag_contents += str(self.d[key]['item']) + ': ' + str(self.d[key]['itemsperbag']) + '\n'

        ToolTip(self.food_bag_contents_title, self._font, self.food_bag_contents, delay=0.0)

    # make bag screen
    def make_bag_screen(self):
        '''
        //// Main screen for making food bags/ calculating Theoretical bags ////
        Label_1 : Food bag photo
        Label_2 : Theoretical bags info
        Label_3 : Make bags info
        Button_1 : Make food bags
        Button_2 : Make Theoretical bags/ calculate
        Button_3 : Substitution page when no more full food bags can be made
        Entry_1 : Number of bags to make, with Entry_var_1 default value of 1
        Entry_2 : Number of Theoretical bags to calculate, with Entry_var_2 default value of ''
        '''
        self.clear_user_screen()
        self.food_bag_contents_title_ToolTip_update()

        # calculate max number of bag that can be made now
        # get the lowest ratio (amount / itmesperbag)
        self.calculate_max_bags()
        self.numberofBags = 1

        self.Label_1.configure(image=self.food_bag_photo)
        self.Label_1.place(relx=0.15, rely=0.25)
        # entry box for many bags
        self.Button_1.configure(text="Make Food bag(s)", background=self._fgcolor, font=(self._font, self._font_medium),
                                command=lambda: self.made_a_bag_screen(), activebackground=self._activebgcolor)
        self.Button_1.place(relx=.75, rely=.4, anchor="center")

        self.Entry_var_1.set(1)
        self.Entry_1.configure(font=(self._font, self._font_big), textvariable=self.Entry_var_1, width=20)
        self.Entry_1.place(relx=.75, rely=.47, anchor="center")

        self.Button_2.configure(text="Calculate", background=self._fgcolor, font=(self._font, self._font_medium),
                                command=lambda: self.make_theoretical_bags(), activebackground=self._activebgcolor)
        self.Button_2.place(relx=.075, rely=.4, anchor="center")

        self.Entry_2.configure(font=(self._font, self._font_big), textvariable=self.Entry_var_2, width=10)
        self.Entry_2.place(relx=.075, rely=.47, anchor="center")
        self.Entry_var_2.set('')

        self.Label_2.configure(
            text="To calculate\ninventory needed \nto make x number \nof theoretical bags", fg="black",
            font=(self._font, self._font_small))
        self.Label_2.place(relx=.075, rely=.30, anchor="center")

        if int(self.lowestRatio) > 0:
            self.Label_3.configure(
                text=f"Enter number of Bags to make\n\n\n{int(self.lowestRatio)} Full bag(s) left\n\n\n{str(self.nameofLowest).upper()}: is the bottleneck",
                font=(self._font, self._font_medium), fg='black')
        else:
            self.Label_3.configure(
                text=f"Full bags can't be made\n\n\n{str(self.nameofLowest).upper()}: is the bottleneck", fg='black')
            # place substitution button page here
            self.Button_3.configure(text="Start substitution of food", background=self._fgcolor,
                                    font=(self._font, self._font_medium),
                                    command=lambda: self.substitute_foods_screen(),
                                    activebackground=self._activebgcolor, padx=10)
            self.Button_3.place(relx=.75, rely=.7, anchor="center")
        self.Label_3.place(relx=.75, rely=.6, anchor="center")

        self.backup_place()
        self.previous_view = "user_screen"

    def make_theoretical_bags(self):
        '''
        //// Where the theoretical bags are calculated/ list box is shown/ theoretical.txt is writen ////
        Entry_var_2 : number of Theoretical bags to make/ calculate
        Label_2 : Theoretical bags info/ error label
        '''
        if self.Entry_var_2.get().isnumeric():
            # checking if input is an int, then checking if value is in bounds
            if int(self.Entry_var_2.get()) > 0 and int(self.Entry_var_2.get()) <= 99999:
                self.previous_view = "make_bag_screen"
                self.clear_makebag_screen()

                d_calc = self.d
                d_needed = {}
                # If food's amount value goes negative after calculation, it is added to d_needed.
                # That is, a negative number means the current inventory can't handle Entry_var_2 bags being made
                for key, value in d_calc.items():
                    d_calc[key]['amount'] -= d_calc[key]['itemsperbag'] * int(self.Entry_var_2.get())
                    if d_calc[key]['amount'] < 0:
                        d_needed[key] = -1 * d_calc[key]['amount']

                # labels with info about Theoretical bags made, read them for details
                self.clear_list_box()
                self.list_box_1.place(x=.4 * 1920, y=.3 * 1080, relwidth=.2, relheight=.6)
                self.list_box_1_label.configure(
                    text=f"What will be needed for {int(self.Entry_var_2.get())} bags\n including current stock",
                    fg="black")
                self.list_box_1_label.place(relx=.5, rely=.25, anchor='center')
                self.list_box_2_label.configure(text=f"If it is blank then you have enough\n in stock to make "
                                                     f"{int(self.Entry_var_2.get())} bags\n\n\n\n\nElse it will show the\nfood and number "
                                                     f"needed to buy\nfor {int(self.Entry_var_2.get())} bags\n\n\n\nAlso, theoretical.txt\n has a copy of this info",
                                                fg="black", font=(self._font, self._font_medium))
                self.list_box_2_label.place(relx=.75, rely=.6, anchor='center')

                # Populating list_box_1 with d_needed items and amount needed for Entry_var_2 bags to be made
                box1count = 0
                for item_id, item_info in d_needed.items():
                    box1count += 1
                    self.list_box_1.insert(box1count, item_id + ' : ' + str(item_info))
                try:
                    # Printing to a text file for a 'hard' copy, rewrites to same file every submit
                    with open('text/theoretical.txt', 'w') as f:
                        print(
                            f"Amount and items needed for {int(self.Entry_var_2.get())} bags\nThis is after current stocks goes to zero\nitem: amount\n",
                            file=f)
                        for p_id, p_info in d_needed.items():
                            print(f"{str(p_id)}: {d_needed[p_id]}", file=f)
                except Exception as e:
                    print("error in writing theoretical.txt: make_theoretical_bags : " + str(e))
            else:
                self.Label_2.configure(text="Enter number\nbetween 0 and 99999", fg='red')
                self.Entry_var_2.set('')
        else:
            self.Label_2.configure(text="Enter number\nbetween 0 and 99999", fg='red')
            self.Entry_var_2.set('')

    def calculate_max_bags(self):
        '''
        Uses worse ratio between 'amount' and 'itemsperbag' variables to find max full bags possible
        Saves the ratio and the name of worst
        '''
        self.make_dict(self.d)
        self.lowestRatio = 9999.9
        self.nameofLowest = ""

        for key, value in self.d.items():
            if self.d[key]['itemsperbag'] != 0:
                if float(self.d[key]['amount'] / self.d[key]['itemsperbag']) <= self.lowestRatio:
                    self.lowestRatio = float(self.d[key]['amount'] / self.d[key]['itemsperbag'])
                    self.nameofLowest = self.d[key]['item']

    def substitute_foods_screen(self):
        '''
        //// The fanciest page that will never be seen (⌣́_⌣̀) ////
        //// dynamically creates checkboxes with text and images as needed ////
        Label_1 : Too low for full bag
        Label_2 : instructions
        Label_3 : submit reminder
        Label_4 : error label
        Button_1 : submit, calls substitute_foods_submit
        '''
        self.d = {}
        self.make_dict(self.d)
        # force reset/ update of dict. Really only needed if directly editing the txt
        self.clear_makebag_screen()
        self.previous_view = "make_bag_screen"
        # labels and a submit button
        self.Label_1.configure(text="Too low for full bag", font=(self._font, self._font_big), image='', fg='black')
        self.Label_1.place(relx=.025, rely=.26)
        self.Label_2.configure(
            text="Select what will replace them\nThe number amount above the food picture is the\namount you need to add in additionally to the normal amount",
            font=(self._font, self._font_big), fg='black')
        self.Label_2.place(relx=.25, rely=.225)

        self.Label_3.configure(font=(self._font, self._font_medium), text="When ready hit submit", fg='black')
        self.Label_3.place(relx=.81, rely=.55)

        self.Button_1.configure(text="Submit", background=self._fgcolor, font=(self._font, self._font_medium),
                                command=lambda: self.substitute_foods_submit(), activebackground=self._activebgcolor,
                                padx=10)
        self.Button_1.place(relx=.85, rely=.6)

        # creates d for outofstock and 'instock', however 'instock' really means items that have at least two times its own 'itemsperbag' var
        self.d_outofstock = {}
        self.d_instock = {}

        # Creating a d of item:photos using the item's name for direction, if picture is not found for said item's name it defaults to unknown.png
        self.d_photos = {}
        for key, value in self.d.items():
            try:
                self.d_photos[self.d[key]['item']] = tk.PhotoImage(file=f"images/{self.d[key]['item']}.png").subsample(
                    4, 4)
            except Exception:
                # all make a bag items without a picture will have a ? picture so it can still work
                self.d_photos[self.d[key]['item']] = tk.PhotoImage(file=f"images/unknown.png").subsample(4, 4)

        # list of item names under each category
        outofstock = []
        instock = []
        # self.stock is items between outofstock/instock, again instock are items with at least two times their own 'itemsperbag' var
        self.stock = []

        # Assigns items to appropriate lists
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

        # When too many items are below their own 'itemsperbag' var, doesn't allow any more substitute bags
        if outofstock.__len__() > 3:
            self.clear_substitutions_page()
            self.make_bag_screen()
            self.Label_4.configure(font=(self._font, self._font_medium), text="Too many missing items", fg='red')
            self.Label_4.place(relx=.665, rely=.75)
            PlaySound("audio/Wilhelm_Scream.wav", SND_FILENAME)
            return

        # Creates the needed amount of checkboxes with text, image, and checkbox variable for d_outofstock
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
        # Creates the needed amount of checkboxes with text, image, and checkbox variable for d_instock
        # Also has coordinate offsets for checkboxes, could be better
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
        '''
        //// When substitutions submit is pressed, check and stuff ////
        //// Looks at values of checkbox ////
        Label_4 : error label
        '''
        self.previous_view = "make_bag_screen"
        notevenOne = True
        # notevenOne is for detecting if at least one checkbox was selected on submit

        try:
            totalLines = len(open("text/food.txt").readlines())
            count = 0
        except Exception as e:
            print("error in reading food.txt: substitute_foods_submit : total lines : " + str(e))

        for key, value in self.d_outofstock.items():
            if self.d_outofstock[key].get() == 1:
                self.d[key]['amount'] = 0

        for key, value in self.d_instock.items():
            if self.d_instock[key].get() == 1:
                self.d[key]['amount'] -= self.d[key]['itemsperbag'] * 2
                # when at least one d_instock checkbox is selected set notevenOne to False
                notevenOne = False
                self.stock.remove(key)

        for key in self.stock:
            self.d[key]['amount'] -= self.d[key]['itemsperbag']
            # the in between stock

        if notevenOne == True:
            # Force back button press if no checkboxes were selected
            self.previous_view = "make_bag_screen"
            self.back_button_func(self.previous_view)
            self.Label_4.configure(text="No substitutes were selected", fg='red')
            self.Label_4.place(relx=.655, rely=.75)

        else:
            try:
                # Updates food.txt after making the substitute bag
                with open('text/food.txt', 'w') as f:
                    print("item, amount, lowlevel, itemsperbag, barcode", file=f)
                    for p_id, p_info in self.d.items():
                        self.beautifulString(str(p_id))
                        if count < totalLines - 2:
                            self.beautiful_string = str(self.beautiful_string) + '\n'
                        f.write(str(self.beautiful_string))
                        count += 1
                    self.partial_bags_made_per_login = self.partial_bags_made_per_login + 1
            except Exception as e:
                print("error writing food.txt : substitute_foods_submit : beautiful string : " + str(e))

            self.d = {}
            self.make_dict(self.d)
            # most easy way to do it

            self.back_button_func(self.previous_view)
            # Force back button press
            self.Label_4.configure(text="Made bag with substitutes", fg='blue')
            self.Label_4.place(relx=.66, rely=.75)

    def make_csv(self):
        self.clear_changelog()
        self.clear_volunteer_instructions_screen()
        self.admin_email_label.place_forget()
        # makes excel csv for viewing, some barcodes can end up in si
        count = 0
        try:
            totalLines = len(open("text/food.txt").readlines())
            with open("food.csv", "w") as f:
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
        except Exception as e:
            print("error in reading food.txt make_csv : " + str(e))

    def make_food_txt(self):
        count = 0
        try:
            totalLines = len(open("text/food.txt").readlines())
            if self.Entry_var_1.get() == 'YES':
                totalLines -= 1
            with open("text/food.txt", "w") as f:
                print("item, amount, lowlevel, itemsperbag, barcode", file=f)
                for p_id, p_info in self.d.items():
                    self.beautifulString(str(p_id))
                    if count < totalLines - 2:
                        self.beautiful_string = str(self.beautiful_string) + '\n'
                    f.write(str(self.beautiful_string))
                    count += 1
        except Exception as e:
            print("error in reading food.txt make_food_txt : " + str(e))
        self.d = {}
        self.make_dict(self.d)

    # ========================================================
    #                 barcode screen functions
    # =======================================================
    # in barcode scanner screen
    def barcode_scanner_screen(self):
        self.clear_user_screen()
        self.backup_place()
        self.previous_view = "user_screen"
        place_object(self.barcode_scanner_add_button, .47, .4)
        place_object(self.barcode_scanner_remove_button, .47, .5)
        self.view_inventory_one_list_box(self.d, 'left')
        self.list_of_items_words = 'Inventory Changes\n'
        self.list_of_items_words = 'Inventory Changes\n\n'
        self.list_of_items_label.config(text=self.list_of_items_words)
        self.Label_3.place_forget()

    def barcode_scanner_add_remove_button_cmd(self, direction):
        # TODO: add barcode & qty columns
        self.previous_view = "barcode_scanner_screen"
        self.clear_barcode_screen()
        place_object(self.list_box_2_label, .08, .25)
        self.invalid_entry_error_label.place_forget()
        self.barcode_scanner_label.configure(text=direction + '  \tEnter amount')
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
            self.add_barcode_to_existing()

    def bind_tab_to_scanner_input_entry(self):
        self.barcode_scanner_input_entry.place_forget()
        place_object(self.barcode_scanner_input_entry, .3, .3, True)

    def unbind_return_func(self):
        self.unbind('<Return>')
        self.unbind('<Tab>')

    def search_for_item_in_food_file(self, direction, item_to_find, qty):
        # TODO: add barcode & qty columns
        try:
            self.Label_4.place_forget()
            if direction == 'Barcodes for Adding':
                self.from_add_subtract = 'add'
            else:
                self.from_add_subtract = 'subtract'
            self.invalid_entry_error_label.place_forget()
            intcheck = int(qty)
            intcheck = int(item_to_find)
            if qty.isnumeric() and item_to_find.isnumeric():
                try:
                    totalLines = len(open("text/food.txt").readlines())
                    shutil.move("text/food.txt", "text/food.txt" + "~")
                    with open("text/food.txt", "w+") as dest:
                        dest.seek(0, os.SEEK_SET)
                        with open("text/food.txt" + "~", "r+") as src:
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
                                            if direction == 'Barcodes for Adding':
                                                if str(self.list_of_items_words).count('\n') > 20:
                                                    self.list_of_items_words = 'Inventory Changes\n\n'
                                                tokens[1] = str(int(tokens[1]) + int(self.barcode_scanner_amount.get()))
                                                self.changelog_text = self.changelog_text + \
                                                                      '\tadded ' + \
                                                                      str(self.barcode_scanner_amount.get()) + \
                                                                      " to '" + tokens[0] + "' barcode: " + \
                                                                      str(item_to_find) + ' New Qty: ' + \
                                                                      tokens[1] + '\n'
                                                self.list_of_items_words = self.list_of_items_words + \
                                                                           'Added ' + \
                                                                           str(self.barcode_scanner_amount.get()) + \
                                                                           " to '" + tokens[0] + "' \n" + \
                                                                           str(item_to_find) + ' New Qty: ' + \
                                                                           tokens[1] + '\n'
                                                self.list_of_items_label.config(text=self.list_of_items_words)

                                            if direction == 'Barcodes for Subtracting':
                                                if str(self.list_of_items_words).count('\n') > 20:
                                                    self.list_of_items_words = 'Inventory Changes\n\n'
                                                if int(self.barcode_scanner_amount.get()) > int(tokens[1]):
                                                    self.Label_3.config(
                                                        text=f'Cannot subtract past {int(tokens[1])} for {tokens[0]}',
                                                        fg='red')
                                                    place_object(self.Label_3, .67, .25)
                                                else:
                                                    self.Label_3.place_forget()
                                                    tokens[1] = str(
                                                        int(tokens[1]) - int(self.barcode_scanner_amount.get()))
                                                    self.changelog_text = self.changelog_text + \
                                                                          '\tremoved ' + \
                                                                          str(self.barcode_scanner_amount.get()) + \
                                                                          " from '" + tokens[0] + "' " + \
                                                                          str(item_to_find) + ' New Qty: ' + \
                                                                          tokens[1] + '\n'
                                                    self.list_of_items_words = self.list_of_items_words + \
                                                                               'Removed ' + \
                                                                               str(self.barcode_scanner_amount.get()) + \
                                                                               " from '" + tokens[0] + "' \n" + \
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

                    self.barcode_scanner_add_remove_button_cmd(direction)
                    # to update inventory box every scan
                    self.view_inventory_one_list_box(self.d, 'left')
                    self.clear_list_box()
                    self.view_inventory_one_list_box(self.d, 'left')
                    if self.notFound.__len__() > 0:
                        self.add_barcode_to_existing()
                        PlaySound("audio/bcNotfound1.wav", SND_FILENAME)
                except Exception as e:
                    print("error writing to food file : " + str(e))
            else:
                self.invalid_entry_error_label.config(text='Enter positive numbers only')
                place_object(self.invalid_entry_error_label, .67, .25)
                self.barcode_scanner_input.set("")
                self.barcode_scanner_amount.set(1)
        except Exception:
            # input a non int value, show error label to user
            self.invalid_entry_error_label.config(text='Enter numbers only')
            place_object(self.invalid_entry_error_label, .8, .25)
            self.barcode_scanner_input.set("")
            self.barcode_scanner_amount.set(1)

    def barcode_exist(self, code):
        # quick easy check to see if barcode exist
        for key, value in self.d.items():
            if code in self.d[key]['barcodes']:
                return True
        return False

    def add_barcode_to_existing(self):
        '''
        //// Main screen for assigning new barcode to food ////
        Button_1 : create_new_item_screen
        Button_2 : append_barcode
        '''
        self.Label_4.place_forget()
        self.unbind_return_func()
        self.previous_view = "barcode_scanner_screen"
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
                                        text=f"BARCODE: {self.notFound[0]}\n\nNOT FOUND \n\nSelect from the list\n\n\nOr create a new item\n\nBarcode will be remembered",
                                        fg='red')
        self.list_box_2_label.place(x=1050, y=600, anchor="center")

        self.isBarcode = True
        # place create new item button
        self.Button_1.configure(text="Create New Item", font=(self._font, self._font_medium), background=self._fgcolor,
                                command=lambda: self.create_new_item_screen(), activebackground=self._activebgcolor)

        self.Button_1.place_forget()
        self.Button_1.place(x=1700, y=600, anchor="center")
        # place append_barcode button
        self.Button_2.configure(text="Add barcode to item", background=self._fgcolor,
                                font=(self._font, self._font_medium), command=lambda: self.append_barcode(),
                                activebackground=self._activebgcolor)
        self.Button_2.place(x=450, y=600, anchor="center")

    def append_barcode(self):
        '''
        /// for appending barcode to existing food item ////
        Label_1 : confirmed/ error
        '''
        # self.make_food_txt()
        self.print_dict_to_file(self.d)
        self.selected_item_to_be_changed = self.list_box_2.curselection()
        if self.selected_item_to_be_changed != ():
            self.previous_view = "user_screen"

            self.change_inventory_by_this_much.set(0)
            self.item_to_be_changed = self.list_box_2.get(self.selected_item_to_be_changed)
            self.Label_1.place_forget()

            pre_beautiful_string = str(self.notFound)
            pre_beautiful_string = pre_beautiful_string.replace("'", '')
            pre_beautiful_string = pre_beautiful_string.replace("[", '')
            pre_beautiful_string = pre_beautiful_string.replace("]", '')
            self.barcode_to_be_added = pre_beautiful_string

            # do the appending
            self.beautifulString(self.item_to_be_changed)
            try:
                s = open("text/food.txt").read()
                s = s.replace(self.beautiful_string, self.beautiful_string + ", " + str(self.barcode_to_be_added))
                f = open("text/food.txt", 'w')
                f.write(s)
                self.changelog_text = self.changelog_text + '\tBarcode: ' + \
                                      str(self.barcode_to_be_added) + ' associated with ' + \
                                      "'" + str(self.item_to_be_changed) + "'" + '\n'
                f.close()
            except Exception as e:
                print("error in opening food.txt added_barcode : " + str(e))

            self.notFound = []
            self.back_button_func(self.previous_view)
            self.barcode_scanner_screen()

            self.Label_1.configure(font=(self._font, self._font_big), text=f"Added {self.barcode_to_be_added} to "
                                                                           f"{self.item_to_be_changed}", fg='blue',
                                   image='')
            self.Label_1.place(x=1000, y=320, anchor="center")
            if self.from_add_subtract == "add":
                self.barcode_scanner_add_remove_button_cmd('Barcodes for Adding')
            else:
                self.barcode_scanner_add_remove_button_cmd('Barcodes for Subtracting')

            self.Label_4.configure(font=(self._font, self._font_big), text=f"Added {self.barcode_to_be_added}\nto "
                                                                           f"{str(self.item_to_be_changed).upper()}",
                                   fg='blue', image='')
            self.Label_4.place(relx=.4, rely=.4, anchor='center')
        else:
            self.Label_1.place_forget()
            self.Label_1.config(text="Choose an Item", fg='red', image='')
            place_object(self.Label_1, .17, .45)

    def clear_add_barcode_to_existing(self):
        self.list_box_2.place_forget()
        self.list_box_2_label.place_forget()

    def clear_substitutions_page(self):
        for i in self.list_l:
            i.place_forget()
        for j in self.list_k:
            j.place_forget()

    # ===================================================================
    #               New items screen and functions
    # ==================================================================

    def create_new_item_screen(self):
        '''
        /// The main create new item page ////
        Label_1 : Title
        Label_2 : Entry boxes descriptions
        Label_3 : label from admin modify view
        Entry_1 / Entry_var_1 : item name
        Entry_2 / Entry_var_2 : amount
        Entry_3 / Entry_var_3 : lowlevel
        Entry_3 / Entry_var_4 : itemsperbag
        Entry_5 / Entry_var_5 : barcodes
        Button_1 : Submit
        '''
        self.invalid_entry_error_label.place_forget()
        self.clear_add_barcode_to_existing()
        self.clear_user_screen()
        # creates blank screen
        self.backup_place()
        if self.Label_3.cget("text") == "Item Modified" or self.Label_3.cget("text") == "Added item":
            self.Label_3.configure(text='')
        self.Label_4.place_forget()

        if self.isModifying == "as_user":
            self.previous_view = "user_screen"
        else:
            self.previous_view = "admin_edit_main"

        if self.isModifying == "is_admin_modifying_with_check":
            self.is_modifying_3_clears()

        if self.isBarcode == True:
            self.codeList = ''
            for codes in self.notFound:
                self.codeList = self.codeList + "\n" + codes
            self.Label_4.configure(font=(self._font, self._font_small), fg='blue', text="BARCODES\n" + self.codeList)
            self.Label_4.place(relx=.05, rely=.3)

        self.Label_1.configure(font=(self._font, self._font_big),
                               text="Create new item screen", image='', fg='black')
        if self.isModifying != "is_admin_modifying":
            self.Label_1.place(relx=.4, rely=.23)

        self.Label_2.place_forget()
        self.Label_2.configure(font=(self._font, self._font_small), fg='black',
                               text="Item Name: \n\n\n\nCurrent amount: \n\n\n\nLow amount warning at: \n\n\n\nItems per bag: \n\n\n\nBarcode(s): ")
        self.Label_2.place(relx=.2, rely=.3)

        if self.isModifying == "as_user":
            self.user_create_new_clear()

        if self.isPassingBarcode == "is_passing_true":
            if self.notFound.__len__() > 0:
                self.previous_view = "add_barcode_to_existing"
                self.Entry_var_5.set(str(self.notFound[0]))
        # prefilling defaults for new item, user can set different values if they want

        self.Button_1.configure(text="Submit New Item", background=self._fgcolor, font=(self._font, self._font_medium),
                                command=lambda: self.create_new_item_submit_button_cmd(),
                                activebackground=self._activebgcolor)
        place_object(self.Button_1, .7, .5)

        self.Entry_2.configure(width=20)
        place_object(self.Entry_1, .4, .3, True)
        place_object(self.Entry_2, .4, .4)
        place_object(self.Entry_3, .4, .5)
        place_object(self.Entry_4, .4, .6)
        place_object(self.Entry_5, .4, .7)
        if len(str(self.Label_3.cget('text'))) > 30:
            self.Label_3.place(relx=.765, rely=.67, anchor="center")
        else:
            self.Label_3.place(relx=.765, rely=.6, anchor="center")

    def create_new_item_submit_button_cmd(self):
        '''
        //// When submit in create_new_item is hit ////
        Entry_var_1 : item name
        Entry_var_2 : amount
        Entry_var_3 : lowlevel
        Entry_var_4 : itemsperbag
        Entry_var_5 : barcodes
        '''
        self.newItem = self.Entry_var_1.get() + ", " + \
                       str(self.Entry_var_2.get()) + ", " + \
                       str(self.Entry_var_3.get()) + ", " + \
                       str(self.Entry_var_4.get()) + ", " + \
                       str(self.Entry_var_5.get())

        try:
            self.newItem = self.Entry_var_1.get() + ", " + \
                           str(int(self.Entry_var_2.get())) + ", " + \
                           str(int(self.Entry_var_3.get())) + ", " + \
                           str(int(self.Entry_var_4.get())) + ", " + \
                           str(self.Entry_var_5.get())
        except Exception as e:
            print(" '' cant be casted " + str(e))

        if self.isModifying == "is_admin":
            self.create_new_item_screen()
            self.auto_fill_edit_item()
            self.toDelete = str(self.words[0])
            self.isModifying = "is_admin_modifying"
        else:
            allFilled = self.isAllFilled()
            if allFilled == 0:
                self.user_create_new_clear()

                if self.isPassingBarcode == "is_passing_true":
                    if self.notFound.__len__() > 0:
                        self.Entry_var_5.set(str(self.notFound[0]))

                self.create_new_item_screen()

                if self.isModifying == "is_admin_modifying":
                    self.auto_fill_edit_item()
            else:
                self.append_food(self.newItem)
                if self.isModifying == "as_user":
                    self.user_create_new_clear()
                else:
                    self.admin_create_new_clear()

                if self.isPassingBarcode == "is_passing_true":
                    if self.notFound.__len__() > 0:
                        self.Entry_var_5.set(str(self.notFound[0]))

    def user_create_new_clear(self):
        self.Entry_var_1.set('')
        self.Entry_var_2.set(1)
        self.Entry_var_3.set(20)
        self.Entry_var_4.set(0)
        self.Entry_var_5.set('')

    def admin_create_new_clear(self):
        self.Entry_var_1.set('')
        self.Entry_var_2.set('')
        self.Entry_var_3.set('')
        self.Entry_var_4.set('')
        self.Entry_var_5.set('')

    def auto_fill_edit_item(self):
        '''
        //// admin auto-fill on select and on fail when modifying ////
        Entry_var_1 : item name
        Entry_var_2 : amount
        Entry_var_3 : lowlevel
        Entry_var_4 : itemsperbag
        Entry_var_5 : barcodes
        '''
        self.words = self.beautiful_string.split(", ")

        self.Entry_var_1.set(self.words[0])
        self.Entry_var_2.set(self.words[1])
        self.Entry_var_3.set(self.words[2])
        self.Entry_var_4.set(self.words[3])

        n = 4
        self.barcodeList = ""
        while n < self.words.__len__():
            self.barcodeList += self.words[n] + ", "
            n += 1
        self.Entry_var_5.set(self.barcodeList[:self.barcodeList.__len__() - 2])

    def isAllFilled(self):
        '''
        //// Checks all the Entry inputs starting with if they are all filled ////
        Entry_var_1 : item name
        Entry_var_2 : amount
        Entry_var_3 : lowlevel
        Entry_var_4 : itemsperbag
        Entry_var_5 : barcodes
        Label_3 : universal label for all errors/ notifications for create_new_item
        '''
        self.make_dict(self.d)
        if (self.Entry_var_1.get() == "" or
                str(self.Entry_var_2.get()) == "" or
                str(self.Entry_var_3.get()) == "" or
                str(self.Entry_var_4.get()) == "" or
                str(self.Entry_var_5.get()) == ""):

            self.Label_3.configure(text="All boxes need to be filled", fg='black')
            return 0
        elif ((str(self.Entry_var_1.get()) in self.d) == True and self.isModifying == "as_user") or \
                (self.isModifying == "is_admin_modifying_with_check" and (
                        str(self.Entry_var_1.get()) in self.d) == True):

            self.Label_3.configure(text="Already Exist", fg='black')
            return 0
        elif re.search("[^a-zA-Z\s]", self.Entry_var_1.get()) != None or \
                str(self.Entry_var_1.get()).count("  ") > 0 or str(self.Entry_var_1.get()).endswith(
            " "):
            # checks for invalid spaces
            self.Label_3.configure(text="Name needs to be letters and spaces only", fg='black')
            return 0
        elif (str(self.Entry_var_2.get()).isnumeric() == False or
              str(self.Entry_var_3.get()).isnumeric() == False or
              str(self.Entry_var_4.get()).isnumeric() == False or
              re.search("[^0-9\s,]", str(self.Entry_var_5.get())) != None or
              str(self.Entry_var_5.get()).count(",,") > 0 or
              str(self.Entry_var_5.get()).count(", ,") > 0 or
              str(self.Entry_var_5.get()).endswith(",") or
              str(self.Entry_var_5.get()).endswith(" ") or
              str(self.Entry_var_5.get()).count("  ") > 0):
            # can have numbers, commas, and spaces for barcodes only, others are nums only
            # ,, check to see if it is invalid use of commas/ spaces
            self.Label_3.configure(
                text="Amount, Low level, and Itemsperbag\nall need to be numbers only\n\n\nBarcodes are \nnumbers/spaces/commas only",
                fg='black')
            return 0
        else:
            try:
                if int(self.newItem.count(",")) > int(self.barcodesLenght - 2):
                    place_object(self.exceeds_barcode_length, .655, .6)
                    return 0
            except Exception as e:
                print("barcodesLenght to short " + str(e))
            # check to see if barcode limit is reached via comma count

            barcodes_to_check = str(self.Entry_var_5.get()).split(", ")
            for i in barcodes_to_check:
                if self.barcode_exist(
                        i) == True and self.isModifying == "is_admin_modifying_with_check" or self.barcode_exist(
                    i) == True and self.isModifying == "as_user":
                    self.Label_3.configure(text="Barcode Already Exist", fg='black')
                    return 0

            for index in range(str(self.newItem).find(","), len(self.newItem) - 1):
                if self.newItem[index] == ',' and self.newItem[index + 1] != " ":
                    self.newItem = self.newItem[:index] + ", " + self.newItem[index + 1:]
                if self.newItem[index] == ' ' and self.newItem[index - 1] != ",":
                    self.newItem = self.newItem[:index] + ", " + self.newItem[index + 1:]
            # fixes non spaced commas in barcode
            # fixes non comma'd spaces in barcode

            # remove all other error labels
            self.Label_3.configure(text="Added item", fg='black')
            return 1

    def is_modifying_3_clears(self):
        self.previous_view = "admin_edit_main"
        self.list_box_2_label.place_forget()
        self.list_box_2.place_forget()
        self.admin_create_new_clear()

    def manual_entry_screen(self):
        # self.clear_adjust_inventory_screen()
        self.clear_user_screen()
        # self.backup_place()
        # self.view_inventory_3_list_boxes(self.d)
        # self.previous_view = "user_screen"
        # place_object(self.adjust_item_quantity_button, .8, .835)

        self.adjust_item_quantity_button_cmd()
        self.previous_view = "user_screen"
        self.backup_place()

    # =================================================================================
    #                                             Place functions
    # =================================================================================
    def backup_place(self):
        self.backup_button.place(relx=.02, rely=.9)

    def todo_label_place(self):
        self.todo_label.place(relx=.300, rely=.450)

    def logout_button_place(self):
        self.logoutButton.place(relx=.8, rely=.9)

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

    def clear_create_new_item(self):
        self.Label_1.place_forget()
        self.Label_2.place_forget()
        self.Label_3.place_forget()
        self.Label_4.place_forget()

        self.Entry_1.place_forget()
        self.Entry_2.place_forget()
        self.Entry_3.place_forget()
        self.Entry_4.place_forget()
        self.Entry_5.place_forget()

    # clear everything back to login screen
    def clear_to_login(self):
        self.clear_create_new_item()
        self.username_for_event_log.place_forget()
        self.logoutButton.place_forget()
        # self.remove_items_button.place_forget()
        # self.adjust_inventory_button.place_forget()
        # self.admin_button.place_forget()
        self.admin_email_inventory_button.place_forget()
        self.admin_email_label.place_forget()
        self.food_file_error_label.place_forget()
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
        self.clear_email_entry_inventory()
        # self.enter_email_add_label.place_forget()
        # self.enter_email_add_entry.place_forget()

        self.list_box_2_label.place_forget()
        self.list_box_2.place_forget()
        # self.admin_email_send_button.place_forget()
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
        self.choose_new_item.place_forget()
        self.adjust_inventory_entry.place_forget()
        self.confirm_inventory_manual_button.place_forget()
        self.cancel_inventory_manual_button.place_forget()
        self.unbind_return_func()
        self.list_of_items_label.place_forget()
        self.display_inventory_left_side_button.place_forget()
        self.clear_add_barcode_to_existing()
        self.clear_substitutions_page()
        self.clear_admin_screen()
        self.clear_admin_message_configure()
        self.volunteer_instructions_label.place_forget()

    # clear list boxes
    def clear_list_box(self):
        self.list_box_1.delete(0, tk.END)
        self.list_box_2.delete(0, tk.END)
        self.list_box_3.delete(0, tk.END)
        self.list_box_1.place_forget()
        self.list_box_2.place_forget()
        self.list_box_3.place_forget()
        self.list_box_1_label.place_forget()
        self.list_box_2_label.place_forget()
        self.list_box_3_label.place_forget()

    # clear check buttons
    def clear_makebag_screen(self):

        self.Label_1.place_forget()
        self.Label_2.place_forget()
        self.Label_3.place_forget()
        self.Label_4.place_forget()

        self.Button_1.place_forget()
        self.Button_2.place_forget()
        self.Button_3.place_forget()

        self.Entry_1.place_forget()
        self.Entry_2.place_forget()
        self.food_bag_contents_title.place_forget()

    # clears user screen
    def clear_user_screen(self):
        self.volunteer_instructions_button.place_forget()
        self.Button_1.place_forget()
        self.Button_2.place_forget()
        self.Button_3.place_forget()
        self.Button_4.place_forget()
        self.Button_5.place_forget()

        self.Label_5.place_forget()

    def clear_admin_screen(self):
        self.volunteer_instructions_button.place_forget()
        # self.admin_button.place_forget()
        self.email_add.set('')
        self.list_box_2_label.place_forget()
        self.list_box_2.place_forget()
        self.admin_email_inventory_button.place_forget()
        self.display_inventory_high_low_outofstock_button.place_forget()
        self.display_users_button.place_forget()
        self.edit_inventory_button.place_forget()
        self.delete_user_button.place_forget()
        self.clear_email_entry_inventory()
        # self.enter_email_add_label.place_forget()
        # self.enter_email_add_entry.place_forget()
        # self.admin_email_send_button.place_forget()
        self.make_csv_button.place_forget()
        self.view_changelog_text.place_forget()
        self.email_changelog_button.place_forget()
        self.view_changelog_button.place_forget()
        self.admin_email_label.place_forget()
        self.admin_email_partners_button.place_forget()
        self.clear_changelog()

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
        self.Label_1.place_forget()
        self.invalid_entry_error_label.place_forget()

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
            with open("text/food_status.txt", "w") as dest:
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
        try:
            with open("text/food.txt", "r+") as f:
                f.seek(0, os.SEEK_SET)
                next(f)
                for line in f:
                    if not re.match(r'^\s*$', line):
                        words = line.split(",")
                        item = words[0]
                        amount = int(words[1])
                        lowlevel = int(words[2])
                        itemsperbag = int(words[3])
                        barcodes = [''] * 20
                        self.barcodesLenght = barcodes.__len__()
                        # could use None but '' looks better
                        d[item] = {}
                        d[item]['item'] = item
                        d[item]['amount'] = amount
                        d[item]['lowlevel'] = lowlevel
                        d[item]['itemsperbag'] = int(itemsperbag)
                        number_of_barcodes = len(words) - 4
                        n = 1
                        while n <= number_of_barcodes:
                            barcodes[n - 1] = str(words[3 + n]).replace(" ", '').replace("\n", "")
                            n += 1
                        d[item]['barcodes'] = barcodes
        except Exception as e:
            self.food_file_error_label.place(relx=.75, rely=.60)
            print("error in open: make dict : " + str(e))

    '''def print_dict(self, d):
        for item_id, item_info in d.items():
            print('\n')
            for key in item_info:
                print(key + " : " + str(item_info[key]))'''

    def append_food(self, newItem):
        '''
        //// Adds newly created item to end of food.txt ////
        //// also where modifying existing item happens ////
        '''

        # when admin is modifying existing item
        if self.isModifying == "is_admin_modifying":
            try:
                s = open("text/food.txt").read()
                s = s.replace(self.beautiful_string, newItem)
                f = open("text/food.txt", 'w')
                f.write(s)
                self.inventory_comparison_after = str(newItem)
                self.compare_before_after_changes_admin()
                f.close()
            except Exception as e:
                print("error in opening food.txt : append food : replace" + str(e))
            # forces a back button press on success
            self.previous_view = "admin_edit_main"
            self.back_button_func(self.previous_view)
            del self.d[self.toDelete]
            # deletes old version of item from dict
            self.edit_inventory_button_cmd()
            self.Label_3.configure(text="Item Modified", fg='black')
            place_object(self.Label_3, .73, .57)

        else:
            # Basic add new item after all checks pass
            try:
                with open("text/food.txt", "a") as f:
                    f.write("\n" + newItem)
                    self.changelog_text = self.changelog_text + '\tnew item: name, amount, lowlevel, itemsperbag, barcode\n'
                    self.changelog_text = self.changelog_text + '\t\t' + \
                                          str(newItem) + '\n'
            except Exception as e:
                print("error in appending food.txt with open : " + str(e))

            # if the barcode entered (it is prefilled by default) is the unknown one, remove it from unknown barcodes
            if (str(self.Entry_var_5.get()) in self.notFound) == True:
                self.notFound.remove(str(self.Entry_var_5.get()))
            elif self.isBarcode == True:
                self.clear_create_new_item()
                self.barcode_scanner_screen()
                self.Label_4.configure(
                    text=f"Added {self.Entry_var_5.get()}\n to {str(self.Entry_var_1.get()).upper()} \n\nHowever, that was not the barcode passed!",
                    font=(self._font, self._font_big), fg='orange')
                self.Label_4.place(relx=.53, rely=.7, anchor='center')
                self.Label_3.configure(text='')
                return

            # A label that has a list of all unknown barcodes (now one unknown is the max, but still works for multiple)
            if self.isBarcode == True:
                self.codeList = ''
                for codes in self.notFound:
                    self.codeList = self.codeList + "\n" + codes
                self.Label_4.configure(text="BARCODES\n" + self.codeList, font=(self._font, self._font_small),
                                       fg='blue')
                self.Label_4.place(relx=.05, rely=.3)
                self.clear_create_new_item()
                self.barcode_scanner_screen()
                self.Label_4.configure(
                    text=f"Added {self.Entry_var_5.get()}\n to {str(self.Entry_var_1.get()).upper()}",
                    font=(self._font, self._font_big), fg='blue')
                self.Label_4.place(relx=.4, rely=.4, anchor='center')
                if self.from_add_subtract == "add":
                    self.barcode_scanner_add_remove_button_cmd('Barcodes for Adding')
                else:
                    self.barcode_scanner_add_remove_button_cmd('Barcodes for Subtracting')

                self.view_inventory_one_list_box(self.d, 'left')
                self.clear_list_box()
                self.view_inventory_one_list_box(self.d, 'left')
                # to update list box right after a new item is added
        self.d = {}
        self.make_dict(self.d)

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
    def view_changelog(self):
        # self.admin_email_label.place_forget()
        self.clear_email_entry_inventory()
        self.clear_volunteer_instructions_screen()
        self.display_users_button.config(text="View Users")
        self.display_inventory_high_low_outofstock_button.config(text="View Inventory")
        self.delete_user_button.place_forget()
        self.list_box_2.place_forget()
        self.list_box_2_label.place_forget()
        self.clear_list_box()
        self.view_changelog_text.delete('1.0', END)
        try:
            with open("text/changelog.txt", 'r') as f:
                self.view_changelog_text.insert(INSERT, f.read())
        except Exception as e:
            print("error viewing changelog : " + str(e))
        place_object(self.view_changelog_text, .3, .3)

    def write_changelog(self):
        # print(self.inventory_comparison_before)
        # print(self.inventory_comparison_after)
        try:
            if not os.path.isfile("text/changelog.txt"):
                with open("changelog.txt", "a+") as f:
                    f.write("Change Log" + '\n==============================================================\n')
        except Exception as e:
            print("error creating changelog " + str(e))
        try:
            if os.path.isfile("text/changelog.txt"):
                with open("text/changelog.txt", "a+") as f:
                    f.write(self.changelog_text)
                    f.write('==============================================================\n')
        except Exception as e:
            print("error updating changelog " + str(e))

        print(self.changelog_text)

    def compare_before_after_changes_admin(self):
        self.comparison = '\tadmin inventory changes:\n'
        before = re.split(",", self.inventory_comparison_before.strip())
        after = re.split(",", self.inventory_comparison_after.strip())
        try:
            before_barcodes = [''] * (before.__len__() - 4)
            before_barcodes = self.barcode_arr(before)
            after_barcodes = [''] * (after.__len__() - 4)
            after_barcodes = self.barcode_arr(after)
        except Exception as e:
            print("barcodes error : " + str(e))

        if before[0] != after[0]:
            self.comparison = self.comparison + '\t New Name : ' + str(after[0]) + \
                              ' Old Name : ' + str(before[0]) + '\n'
        if before[1] != after[1]:
            self.comparison = self.comparison + '\t New Amount : ' + str(after[1]) + \
                              ' Old Amount : ' + str(before[1]) + '\n'
        if before[2] != after[2]:
            self.comparison = self.comparison + '\t New low level : ' + str(after[2]) + \
                              ' Old low level : ' + str(before[2]) + '\n'
        if before[3] != after[3]:
            self.comparison = self.comparison + '\t New items per bag : ' + str(after[3]) + \
                              ' Old items per bag : ' + str(before[3]) + '\n'
        self.changelog_text = self.changelog_text + self.comparison

        diff_list = [i for i in before_barcodes + after_barcodes if i not in after_barcodes]
        if len(diff_list) > 0:
            self.comparison = self.comparison + '\tDeleted barcodes : ' + \
                              str(diff_list) + '\n'
        diff_list = [i for i in before_barcodes + after_barcodes if i not in before_barcodes]
        if len(diff_list) > 0:
            self.comparison = self.comparison + '\tAdded barcodes : ' + \
                              str(diff_list) + '\n'

    def barcode_arr(self, arr):
        barcodes = [''] * (arr.__len__() - 4)
        number_of_barcodes = len(arr) - 4
        n = 1
        while n <= number_of_barcodes:
            barcodes[n - 1] = int(arr[3 + n])
            n += 1
        return barcodes

    def change_log_new_user(self, username):
        try:
            printlocaltime = localtime(time())
            monthday = str(printlocaltime.tm_mon) + "/" + str(printlocaltime.tm_mday) + " "
            currenttime = monthday + str(printlocaltime.tm_hour) + ":" + str(printlocaltime.tm_min)
            try:
                self.changelog_text = self.changelog_text + '- Registered new user: ' + \
                                      str(username) + 'at ' + str(currenttime) + '\n'
            except Exception as e:
                print("error updating changelog text " + str(e))
            try:
                self.write_changelog()
            except Exception as e:
                print("error writing to changelog wih new user : change_log_new_user : " + str(e))
        except Exception as e:
            print("error registering user: changelog new user: " + str(e))

    def snapshot_on_login(self):
        printlocaltime = localtime(time())
        monthday = str(printlocaltime.tm_mon) + "/" + str(printlocaltime.tm_mday) + " "
        currenttime = monthday + str(printlocaltime.tm_hour) + ":" + str(printlocaltime.tm_min)
        self.login_time = currenttime
        self.logged_in = True
        self.changelog_text = ''
        self.bags_made_per_login = 0
        self.partial_bags_made_per_login = 0
        self.changelog_text = self.username_for_event_log.cget("text") + " logging in  " + str(self.login_time) + '\n'

    def snapshot_on_logout(self):
        # copyfile(file, file + "_logout")
        self.change_log()  # show changes
        printlocaltime = localtime(time())
        monthday = str(printlocaltime.tm_mon) + "/" + str(printlocaltime.tm_mday) + " "
        currenttime = monthday + str(printlocaltime.tm_hour) + ":" + str(printlocaltime.tm_min)
        self.logout_time = currenttime
        self.logged_in = False
        self.bags_made_per_login = 0
        self.partial_bags_made_per_login = 0
        self.changelog_text = self.changelog_text + self.username_for_event_log.cget("text") + \
                              " logging out " + str(self.logout_time) + '\n'
        self.write_changelog()
        self.changelog_text = ''

    def change_log(self):
        try:
            # user
            # done: 'make a new bag' -> 'make food bag(s)' with entry box -> changelog
            # done: 'make a new bag' -> 'start substitution of food' -> 'submit' -> changelog
            # done: 'barcode scan' -> add/remove items -> enter button (exists) -> changelog
            # done: 'barcode scan' -> add/remove items -> enter button (does not exist) -> 'add barcode to item' -> changelog
            # done: 'barcode scan' -> add/remove items -> enter button (does not exist) -> 'create new item' -> 'submit new item' -> changelog
            # done: 'manual entry' -> 'choose an item' -> add/subtract -> 'confirm' -> changelog
            # done: 'create new item' -> 'submit new item' -> changelog
            # done: 'register' -> 'register' -> changelog
            # admin
            # done: 'edit inventory' -> 'delete this item' -> 'confirm deletion' -> changelog
            # show comparisons: 'edit inventory' -> 'edit this item' -> 'submit edit' -> changelog
            # done: 'edit inventory' -> 'create new item' -> 'submit new item' -> changlog
            # done: 'view users' -> 'delete user' -> changelog
            # done: 'email inventory' -> 'send' -> changelog
            if self.bags_made_per_login > 0:
                self.changelog_text = self.changelog_text + '\t' + str(self.bags_made_per_login) + \
                                      ' bags of food made\n'
            if self.partial_bags_made_per_login > 0:
                self.changelog_text = self.changelog_text + '\t' + str(self.partial_bags_made_per_login) + \
                                      ' partial bags of food made\n'
        except Exception as e:
            print("error in compare_files : " + str(e))

    def exit_program(self):
        if self.logged_in:
            self.snapshot_on_logout()
        self.destroy()

    # ===================================================================================
    #                   View and/or change Inventory & users
    #                  TODO: split these into 2-3 sections for easier viewing
    # ===================================================================================
    # adjust inventory manually
    def adjust_item_quantity_button_cmd(self):
        self.view_inventory_one_list_box(self.d, 'middle')
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

    def choose_an_item_to_change_cmd(self):
        try:
            self.selected_item_to_be_changed = self.list_box_2.curselection()
            if self.selected_item_to_be_changed != ():
                self.change_inventory_by_this_much.set(0)
                self.item_to_be_changed = self.list_box_2.get(self.selected_item_to_be_changed)
                self.invalid_entry_error_label.place_forget()
                self.change_value_of_item_chosen()
            else:
                self.Label_4.configure()
                self.invalid_entry_error_label.config(text="Choose an Item")
                place_object(self.invalid_entry_error_label, .8, .4)
        # TODO: change to pass
        except Exception as e:
            print("Change to pass")
            print("Error inside choose_an_item_to_change_cmd : " + str(e))

    def choose_an_item_to_edit_button_cmd(self):
        self.selected_item_to_be_changed = self.list_box_2.curselection()
        if self.selected_item_to_be_changed != ():
            self.change_inventory_by_this_much.set(0)
            self.item_to_be_changed = self.list_box_2.get(self.selected_item_to_be_changed)
            self.invalid_entry_error_label.place_forget()

            self.item_to_be_changed_label_2.place(x=960, y=275, anchor="center")
            # New, use anchor to force the label to remain at same center regardless of length
            string_key = re.split(" :", self.item_to_be_changed.strip())[0]
            self.beautifulString(string_key)
            self.admin_modify_inventory_screen()
            self.item_to_be_changed_label_2.configure(text="Currently:\n" + self.beautiful_string,
                                                      font=(self._font, self._font_medium))
            self.inventory_comparison_before = str(self.beautiful_string)
            self.Label_1.place_forget()
        else:
            self.Label_4.configure(font=(self._font, self._font_big), fg='red', text="Choose an Item")
            place_object(self.Label_4, .715, .4)

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

    def choose_an_item_to_delete_button_cmd(self):
        '''
        //// Delete item confirm screen, requires the admin to enter 'YES' and reminds them what they are deleting ////
        Label_4 : error label
        Entry_1 : delete confirm entry, where admin enters 'YES' to confirm
        Button_1 : deleteItem submit
        '''
        self.selected_item_to_be_changed = self.list_box_2.curselection()
        if self.selected_item_to_be_changed != ():
            self.change_inventory_by_this_much.set(0)
            self.item_to_be_changed = self.list_box_2.get(self.selected_item_to_be_changed)

            # clear last page
            self.clear_modify_inventory()
            self.Entry_var_1.set('')
            self.previous_view = "admin_edit_main"

            self.list_box_2_label.configure(font=(self._font, self._font_big),
                                            text=f"Are you sure you want to delete\n{str(re.split(' :', self.item_to_be_changed.strip())[0]).upper()}?\n\n\n\n"
                                                 f"Enter YES to delete\n{str(re.split(' :', self.item_to_be_changed.strip())[0]).upper()}")

            self.Entry_1.configure(font=(self._font, self._font_big), textvariable=self.Entry_var_1, width=20, )
            place_object(self.Entry_1, .435, .5, True)

            self.Button_1.configure(text="Confirm Deletion", background=self._fgcolor,
                                    font=(self._font, self._font_medium),
                                    command=lambda: self.deleteItem(), activebackground=self._activebgcolor)
            self.Button_1.place(relx=.47, rely=.55)

            self.list_box_2.place_forget()
        else:
            self.Label_4.configure(font=(self._font, self._font_big), fg='red', image='', text="Choose an Item")
            place_object(self.Label_4, .175, .4)

    def deleteItem(self):
        '''
        //// Does the deletion ////
        Label_2 : confirmation / error
        '''
        string_key = re.split(' :', self.item_to_be_changed.strip())[0]

        if self.Entry_var_1.get() == "YES":
            del self.d[string_key]
            self.changelog_text = self.changelog_text + '\t' + str(string_key) + ' deleted from inventory\n'
            self.make_food_txt()

            self.Label_2.configure(font=(self._font, self._font_big), fg='red',
                                   text=f"{str(string_key).upper()}\nWas Deleted")
        else:
            self.Label_2.configure(font=(self._font, self._font_big), text="Not Deleted\nType YES to delete", fg='red',
                                   anchor="center")
        self.Entry_var_1.set("")
        # jump to last page with message
        self.back_button_func(self.previous_view)
        self.Label_2.place(relx=.24, rely=.6, anchor="center")

    def admin_modify_inventory_screen(self):
        self.isModifying = "is_admin"
        self.Label_3.configure(text='')
        # clears last screen
        self.list_box_2_label.place_forget()
        self.list_box_2.place_forget()
        # reusing inputs and checks screen passing beautiful/ iteminfo
        self.create_new_item_submit_button_cmd()
        self.Button_1.configure(text="Submit Edit", background=self._fgcolor, font=(self._font, self._font_medium),
                                command=lambda: self.create_new_item_submit_button_cmd(),
                                activebackground=self._activebgcolor)

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
                # print("is instance error : " + str(e))
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
                    # print("bad input 1 : " + str(e))
                    # print(int(self.change_inventory_by_this_much.get()))
                    if int(self.change_inventory_by_this_much.get()) < 0:
                        self.catch_exception_bad_input()
                        return

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
            # print("bottom exception:")
            self.catch_exception_bad_input()

    def catch_exception_bad_input(self):
        self.invalid_entry_error_label.config(text="Only Positive \nNumbers allowed")
        place_object(self.invalid_entry_error_label, .8, .4)
        place_object(self.adjust_inventory_entry, .5, .45)
        place_object(self.add_button, .4, .4)
        place_object(self.subtract_button, .4, .5)
        self.change_inventory_by_this_much.set(0)

    def confirm_inventory_manual_button_cmd(self):
        try:
            parsed_name_to_be_changed = re.split(":", self.item_to_be_changed.strip())[0]
            totalLines = len(open("text/food.txt").readlines())
            shutil.move("text/food.txt", "text/food.txt" + "~")
            with open("text/food.txt", "w+") as dest:
                dest.seek(0, os.SEEK_SET)
                with open("text/food.txt" + "~", "r+") as src:
                    src.seek(0, os.SEEK_SET)
                    count = 0
                    for line in src:
                        count += 1
                        if not re.match(r'^\s*$', line):
                            tokens = re.split(",", line.strip())
                            if tokens[0] == parsed_name_to_be_changed.strip():
                                tokens[1] = ' ' + str(self.new_inventory_amount)
                                self.changelog_text = self.changelog_text + \
                                                      '\t' + self.item_to_be_changed_label_2.cget('text') + '\n'
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
    def change_value_of_item_chosen(self):
        try:
            self.item_to_be_changed_label_1.configure(text="Item to be changed")
            self.item_to_be_changed_label_2.configure(text=str(self.item_to_be_changed).upper())
            place_object(self.item_to_be_changed_label_1, .42, .25)
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
        self.admin_email_label.place_forget()
        try:
            sel = self.list_box_2.curselection()
            user_to_be_deleted = self.list_box_2.get(sel)
            self.list_box_2.delete(sel)
            try:
                shutil.move("text/username_password_file.txt", "text/username_password_file.txt" + "~")
                with open("text/username_password_file.txt", "w+") as dest:
                    dest.seek(0, os.SEEK_SET)
                    with open("text/username_password_file.txt" + "~", "r+") as src:
                        src.seek(0, os.SEEK_SET)
                        for line in src:
                            if not re.match(r'^\s*$', line):
                                tokens = re.split(" ", line.strip())
                                if tokens[0] != "adminarmy" and tokens[0] == user_to_be_deleted:
                                    self.changelog_text = self.changelog_text + '\tDeleted User : ' + \
                                                          user_to_be_deleted + '\n'
                                if tokens[0] != user_to_be_deleted or tokens[0] == "adminarmy":
                                    dest.write(line)
            # TODO: change exceptions to pass
            except Exception as e:
                print("exception in remove_func : writing file : " + str(e))
        except Exception as e:
            pass

    def clear_changelog(self):
        self.view_changelog_text.place_forget()
        self.clear_email_entry_inventory()
        # self.enter_email_add_label.place_forget()
        # self.enter_email_add_entry.place_forget()
        self.list_box_2_label.place_forget()
        self.list_box_2.place_forget()
        # self.admin_email_send_button.place_forget()

    # swap display inventory button
    # TODO: shows inventory button, not forgetting, fix this
    def swap_inventory_button(self, choice):
        self.clear_changelog()
        # self.admin_email_label.place_forget()
        self.clear_email_entry_inventory()
        self.clear_volunteer_instructions_screen()
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
        self.clear_changelog()
        self.clear_volunteer_instructions_screen()
        self.admin_email_label.place_forget()
        users_button_text = self.display_users_button.cget('text')
        if users_button_text == 'View Users':
            self.display_users_button.config(text="Hide Users")
            self.display_inventory_high_low_outofstock_button.config(text="View Inventory")
            place_object(self.delete_user_button, .71, .705)
            self.view_users()
        else:
            self.display_users_button.config(text="View Users")
            self.delete_user_button.place_forget()
            self.clear_list_box()

    def edit_inventory_button_cmd(self):
        self.clear_changelog()
        self.clear_volunteer_instructions_screen()
        self.admin_email_label.place_forget()

        # TODO: Danny, i dont think this is neccessary now
        if self.from_admin_message == True:
            self.clear_admin_message_configure()
            self.previous_view = "admin_message_configure"
        else:
            self.previous_view = "admin_screen"
        self.backup_button.place(relx=.02, rely=.9)
        self.clear_admin_screen()
        self.clear_volunteer_instructions_screen()
        # Jump to modify screen and be able to modify and delete items
        self.modify_inventory()

    def modify_inventory(self):
        '''
        //// Admin selects what item you want to modify/ delete then selects appropriate button ////
        Button_1 : create_new_item_screen
        Button_2 : choose_an_item_to_edit_button_cmd
        Button_3 : choose_an_item_to_delete_button_cmd
        '''
        # reuse select item code from manual entry
        self.volunteer_instructions_label.place_forget()
        self.view_inventory_one_list_box(self.d, 'middle')
        self.list_box_2.place_forget()
        self.list_box_2_label.place_forget()
        self.isModifying = "is_admin_modifying_with_check"

        self.Button_1.configure(text="Create New Item", font=(self._font, self._font_medium), background=self._fgcolor,
                                command=lambda: self.create_new_item_screen(), activebackground=self._activebgcolor)
        place_object(self.Button_1, .71, .625)

        self.list_box_2_label.configure(font=(self._font, self._font_big_big), text="\\\ Select Here! //")
        self.Label_3.configure(text='')
        place_object(self.list_box_2_label, .41, .23)
        self.list_box_2.place(relx=.44, rely=.3, relwidth=.15, relheight=.55)

        self.Button_2.configure(background=self._fgcolor, font=(self._font, self._font_medium),
                                command=lambda: self.choose_an_item_to_edit_button_cmd(),
                                activebackground=self._activebgcolor, padx=47, text="Edit This Item")
        place_object(self.Button_2, .7, .5)
        # New add delete button/ screen

        self.Button_3.configure(text="Delete This Item!", background=self._fgcolor,
                                font=(self._font, self._font_medium),
                                command=lambda: self.choose_an_item_to_delete_button_cmd(),
                                activebackground=self._activebgcolor, padx=47)
        place_object(self.Button_3, .15, .5)

        self.backup_button.configure(text="Back")

    def clear_modify_inventory(self):
        self.Label_2.place_forget()
        self.Label_3.place_forget()
        self.Label_4.place_forget()
        self.Button_2.place_forget()
        self.Button_3.place_forget()

    # displays users in a box
    def view_users(self):
        self.clear_list_box()
        self.list_box_2.place(relx=.39, rely=.3, relwidth=.14)
        self.list_box_2_label.place(relx=.42, rely=.25)
        self.list_box_2_label.config(font=(self._font, self._font_medium), text="USERS", fg='black')
        box2count = 0
        try:
            with open('text/username_password_file.txt', "r+") as readf:
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
        maxboxheight = .55
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
        elif self.password_verify.get() != self.password_compare_verify.get():
            self.registration_error("passwords must match", .68, .455)

        # check if username to register already exists
        else:
            try:
                with open('text/username_password_file.txt', "r+") as readf:
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
                with open('text/username_password_file.txt', "a+") as writef:
                    writef.write(self.username_info + " ")
                    writef.write(self.hash + "\n")
                    try:
                        self.change_log_new_user(self.username_info)
                    except Exception as e:
                        print("error change log new user" + str(e))

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

    def login_load_screen(self):
        self.clear_registration_errors()
        self.clear_registration_success()
        self.backup_button.place_forget()
        self.login_verify()

    def login_verify(self):
        # TODO: i think the following lines can be removed - test them
        # self.clear_registration_errors()
        # self.clear_registration_success()
        # self.backup_button.place_forget()

        # self.clear_login_screen()  # test
        self.username_info = self.username_verify.get()
        self.password_info = self.password_verify.get()

        # check username and hashed password
        self.ready_to_login = False
        try:
            with open('text/username_password_file.txt', "a+") as readf:
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

        # TODO: change login to 1, 2, or 3
        login = 3
        if login == 1:
            self.default_admin_message()
            self.user_screen()
        elif login == 2:
            self.default_admin_message()
            self.admin_screen()
        elif login == 3:
            if self.ready_to_login:
                self.default_admin_message()
                self.clear_verify()
                self.clear_login_screen()
                self.username_for_event_log.configure(text=str(tokens[0]))
                place_object(self.username_for_event_log, .02, .85)
                self.snapshot_on_login()
                if tokens[0] == 'adminarmy':
                    self.admin_screen()
                else:
                    self.user_screen()
            else:
                self.login_failure("username & password invalid", .65, .4)
                self.clear_verify()
                self.login_info_screen()


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
        self.geometry('+%i+%i' % (event.x_root + 10, event.y_root))
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

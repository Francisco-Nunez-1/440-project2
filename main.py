# TO DO
# center the login window
# add the database
# screen for after one logs in
# screen for creating a new user, in this have to ask if mentor or mentee, myers briggs code,...
# ...link to myers briggs website, and idk what else will be asked in this page
# back-end functionality after that.


# # Imports to run Qt5
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QLabel, QComboBox, QLineEdit
from PyQt5 import *
import sqlite3
import webbrowser
import mysql.connector
from mysql.connector import Error


# Show the welcome_screen, created class that will have objects,
# and objects have variables like labels we created in Qt5 app and let pyqt5 do it behind the scenes
class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        # load the gui to our python code
        loadUi("welcome_screen.ui", self)
        # this will command to go to gotoLogin function when the button is clicked
        self.loginbtn.clicked.connect(self.goto_login)
        # this will command to go to gotocreateAccount function when the button is clicked
        self.createAccountbtn.clicked.connect(self.goto_CreateAccount)

    def goto_login(self):
        # this will open the new login window in the current window by calling the .ui class
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goto_CreateAccount(self):
        # this will open the new create account window in the current window by calling the .ui class
        create_account = CreateAccountScreen()
        widget.addWidget(create_account)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        # load the gui to our python code
        loadUi("login.ui", self)
        # This line will hide the password as its type in
        self.password_textbx.setEchoMode(QtWidgets.QLineEdit.Password)
        # connect to function to do next after login button is clicked
        self.loginbtn.clicked.connect(self.login_function)

    def login_function(self):
        # extracting the user and password
        typed_user = self.username_textbx.text()
        typed_password = self.password_textbx.text()

        # check fields arent blank
        if len(typed_user) == 0 or len(typed_password) == 0:
            self.error_lbl.setText("Fields can't be blank, \nPlease fill in all fields ")

        # *********************************** NEEDS WORK DONE TO IT **********************************************
        # *******************************************************************************************************
        # validate if user and password match
        else:
            conn = sqlite3.connect("DATABASE NAME HERE")
            # this execute the query's
            cur = conn.cursor()
            query = 'SELECT password_COLUMN_HERE FROM TABLE_NAME_HERE WHERE username_COLUMN_NAME =\'' + typed_user + "\'"
            cur.execute(query)
            # save to result_pass this will get the password from db and check it matches
            # with what they typed in
            result_password = cur.fetchone()
            if result_password == typed_password:
                print("Successfully logged in")
                self.error_lbl.setText("")
            else:
                # tried to be funny
                self.error_lbl.setText("Invalid Username or Password \nor Both go figure it out!!!!")


# *********************************** END OF NEEDS WORK DONE TO IT **********************************************
# ***************************************************************************************************************

# def nextpage_function():
#     # this will open the SecondCreateAccountScreen window in the current window by calling the .ui class
#     second_page_create_account = SecondCreateAccountScreen()
#     widget.addWidget(second_page_create_account)
#     widget.setCurrentIndex(widget.currentIndex() + 1)


    # # extracting the user and password
    # typed_fname = self.fname_textbx.text()
    # typed_lname = self.lname_textbx.text()
    # typed_user = self.username_textbx.text()
    # typed_password = self.password_textbx.text()
    # retyped_password = self.confirmPassword_textbx.text()
    # typed_email = self.email_textbx.text()
    # typed_phonenumber = self.phonenumber_textbx.text()
    #
    # # check fields arent blank
    # if len(typed_fname) == 0 or len(typed_lname) == 0 or len(typed_user) == 0 or len(typed_password) == 0 \
    #         or len(retyped_password) == 0 or len(typed_email) == 0 or len(typed_phonenumber) == 0:
    #     self.error_lbl.setText("Fields can't be blank, \nPlease fill in all fields ")
    #
    # else:
    #     # this will command to go to gotocreateAccount function when the button is clicked
    #     self.nextbtn.clicked.connect(self.SecondCreateAccountScreen)


class CreateAccountScreen(QDialog):
    def __init__(self, parent=None):
        super(CreateAccountScreen, self).__init__()
        # load the gui to our python code
        loadUi("create_account_both.ui", self)

        # This line will hide the password as its type in
        self.password_textbx.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmPassword_textbx.setEchoMode(QtWidgets.QLineEdit.Password)

        # when next button is clicked it will go to nextpage_funtion
        self.nextbtn.clicked.connect(self.nextpage_function)

    def nextpage_function(self):
        # this will open the SecondCreateAccountScreen window in the current window by calling the .ui class

        # firstname = self.fname_textbx.text()
        # print(firstname)

        # Get user input from create_account_both.ui
        fname = self.fname_textbx.text()
        lname = self.lname_textbx.text()
        userdata = (fname, lname)
        print(userdata)

        second_page_create_account = SecondCreateAccountScreen()
        widget.addWidget(second_page_create_account)
        widget.setCurrentIndex(widget.currentIndex() + 1)


# this is for link
class HyperlinkLabel(QLabel):
    # def __init__(self, parent=None):
    def __init__(self, parent=None):
        super(HyperlinkLabel, self).__init__()
        # self.setStyleSheet('font-size: 35px')
        self.setOpenExternalLinks(True)
        self.setParent(parent)


class SecondCreateAccountScreen(QDialog):
    def __init__(self):
        super(SecondCreateAccountScreen, self).__init__()

        # load the gui to our python code
        loadUi("second_create_account.ui", self)

        # this is for link/ place holders should be available
        # https://learndataanalysis.org/create-hyperlinks-pyqt5-tutorial/
        linkTemplate = '<a href={0}>{1}</a>'

        linklbl = HyperlinkLabel(self)
        # self.linklbl.setText(linkTemplate.format('https://google.com', 'Google.com'))
        self.linklbl.setText(linkTemplate.format('https://google.com', 'Google.com'))

        self.createAccountbtn.clicked.connect(self.connectdatabase)

    def connectdatabase(self):
        try:
            # Gets input from the form
            # Only able to get input from second_create_account.ui

            # From create_account_both.ui
            # Ends the program when ran
            # fname = self.fname_textbx.text()
            # print(fname)

            # From second_create_account.ui
            department = self.department_comboBox.currentText()
            print(department)

            connection = mysql.connector.connect(host='107.180.1.16',
                                                 database='cis440fall2021group1',
                                                 user='fall2021group1',
                                                 password='fall2021group1')

            if connection.is_connected():
                db_info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_info)
                cursor = connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)


                # # Insert data to the database
                # Only work with inputs from second_create_account.ui
                # sql = "INSERT INTO Employees (FName, Department) VALUES (%s, %s)"
                # val = (fname, department)
                # cursor.execute(sql, val)
                # connection.commit()
                #
                # print(cursor.rowcount, "record inserted.")

        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")



# Connect to a mysql database (hard coded data)
# class ConnectDatabase:
#     def __init__(self):
#         try:
#             connection = mysql.connector.connect(host='107.180.1.16',
#                                                  database='cis440fall2021group1',
#                                                  user='fall2021group1',
#                                                  password='fall2021group1')
#
#             if connection.is_connected():
#                 db_info = connection.get_server_info()
#                 print("Connected to MySQL Server version ", db_info)
#                 cursor = connection.cursor()
#                 cursor.execute("select database();")
#                 record = cursor.fetchone()
#                 print("You're connected to database: ", record)
#
#                 # # Insert data to the database
#                 # sql = "INSERT INTO Employees (FName, LName, AdvisingRole, Department) VALUES (%s, %s, %s, %s)"
#                 # val = ("John", "Doe", "Mentee", "IT")
#                 # cursor.execute(sql, val)
#                 # connection.commit()
#                 #
#                 # print(cursor.rowcount, "record inserted.")
#
#                 # Insert data to the database
#                 department
#
#                 sql = "INSERT INTO Employees (Department) VALUES (%s)"
#                 val = department
#                 cursor.execute(sql, val)
#                 connection.commit()
#
#                 print(cursor.rowcount, "record inserted.")
#
#
#         except Error as e:
#             print("Error while connecting to MySQL", e)
#         finally:
#             if connection.is_connected():
#                 cursor.close()
#                 connection.close()
#                 print("MySQL connection is closed")





# main
# show gui
app = QApplication(sys.argv)
welcome = WelcomeScreen()
# this will stack many widgets on top of each other so we can move between screens
widget = QStackedWidget()
# pass in the screen
widget.addWidget(welcome)
widget.setFixedHeight(900)
widget.setFixedWidth(1400)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")

# TO DO
# functionality for back button
# add numbers to the slider as its slides

# # Imports to run Qt5
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QLabel, QComboBox, QLineEdit
from PyQt5 import *

import sqlite3
import webbrowser
import mysql.connector


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


# Show the login screen
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
class CreateAccountScreen(QDialog):

    # def __init__(self, parent=None):

    def __init__(self):
        super(CreateAccountScreen, self).__init__()
        # load the gui to our python code
        loadUi("create_account_both.ui", self)

        # This line will hide the password as its type in
        self.password_textbx.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmPassword_textbx.setEchoMode(QtWidgets.QLineEdit.Password)

        # when next button is clicked it will go to nextpage_funtion
        self.nextbtn.clicked.connect(self.nextpage_function)

    def nextpage_function(self):
        # Get user input from create_account_both.ui
        fname = self.fname_textbx.text()
        lname = self.lname_textbx.text()
        email = self.email_textbx.text()
        password = self.password_textbx.text()
        number = self.phonenumber_textbx.text()
        userDataPage1 = {"fname": fname, "lname": lname, "email": email, "password": password, "phoneNumber": number}
        # print(userDataPage1)

        # this will open the SecondCreateAccountScreen window in the current window by calling the .ui class
        second_page_create_account = SecondCreateAccountScreen(userDataPage1)
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
    def __init__(self, userData):
        super(SecondCreateAccountScreen, self).__init__()
        self.userData = userData
        # print(self.userData)
        # load the gui to our python code
        loadUi("second_create_account.ui", self)

        # this is for link/ place holders should be available
        linkTemplate = "<a href='https://www.16personalities.com/free-personality-test'>'Myers–Briggs'</a>"

        linklbl = HyperlinkLabel(self)
        # self.linklbl.setText(linkTemplate.format('https://google.com', 'Google.com'))
        self.linklbl.setText(linkTemplate.format('https://google.com', 'Google.com'))

        self.createAccountbtn.clicked.connect(self.connectdatabase)

    def connectdatabase(self):
        try:
            department = self.department_comboBox.currentText()
            jobPosition = self.jobPosition_comboBox.currentText()
            myersBriggs = self.myersBriggs_comboBox.currentText()

            if self.mentee_rdbtn.isChecked():
                advisingRole = "Mentee"
            elif self.mentor_rdbtn.isChecked():
                advisingRole = "Mentor"

            else:
                self.error_lbl.setText("Please select if you are a\nMentor or Mentee ")

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


                sql = "INSERT INTO Employees (FName, LName, Phone, Email, Password, AdvisingRole, MBType, LoginCount," \
                      "Department,JobPosition) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                val = (self.userData['fname'], self.userData['lname'], self.userData['phoneNumber'],
                       self.userData['email'], self.userData['password'],
                       advisingRole, myersBriggs, '0', department, jobPosition)

                cursor.execute(sql, val)
                connection.commit()

                print(cursor.rowcount, "record inserted.")

        except Exception as e:
            print("Error while connecting to MySQL", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
                self.check()


    def check(self):
        if self.mentor_rdbtn.isChecked():
            print('mentor is checked')
            self.mentorPg1_function()
        elif self.mentee_rdbtn.isChecked():
            print('mentee is checked')
            self.goto_login()
        else:
            self.error_lbl.setText("Please select if you are a\nMentor or Mentee ")

    def mentorPg1_function(self):
        # this will open the MentorQuestionsPg1 window in the current window by calling the .ui class
        mentor_pg1 = MentorQuestionsPg1()
        widget.addWidget(mentor_pg1)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goto_login(self):
        # this will open the new login window in the current window by calling the .ui class
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class MentorQuestionsPg1(QDialog):
    def __init__(self):
        super(MentorQuestionsPg1, self).__init__()
        # load the gui to our python code
        loadUi("mentor_questions_pg1.ui", self)

        # when next button is clicked it will go to nextpage_funtion
        self.nextbtn.clicked.connect(self.nextpage_function)

        # # when next button is clicked it will go back to the previous page
        self.backbtn.clicked.connect(self.backpage_function)

    # go to MentorQuestionsPg2
    def nextpage_function(self):
        # this will open the SecondCreateAccountScreen window in the current window by calling the .ui class
        mentor_pg2 = MentorQuestionsPg2()
        widget.addWidget(mentor_pg2)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    # go back to SecondAccountScreen
    def backpage_function(self):
        second_page_create_account = SecondCreateAccountScreen()
        widget.addWidget(second_page_create_account)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class MentorQuestionsPg2(QDialog):
    def __init__(self):
        super(MentorQuestionsPg2, self).__init__()
        # load the gui to our python code
        loadUi("mentor_questions_pg2.ui", self)

        # # when next button is clicked it will go back to the previous page
        self.backbtn.clicked.connect(self.backpage_function)

    # go back to MentorQuestionsPg1
    def backpage_function(self):
        mentor_pg1 = MentorQuestionsPg1()
        widget.addWidget(mentor_pg1)
        widget.setCurrentIndex(widget.currentIndex() + 1)


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

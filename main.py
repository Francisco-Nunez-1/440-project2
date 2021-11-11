# TO DO
# functionality for back button
# mentor page 1 fix if else on the checkboxes, currently it goes to next page if more than 3
# Create Account Button in second_create_account needs to be changed to Next
# Next Button in Mentor_questions_pg1 needs to be changed to create account
# Next Button in Mentor_questions_pg2 needs to be changed to create account
# Disable the check boxes and the next button unless only 3 check boxes are checked
# Try to call the mentee checkboxes to the already established function in mentor page 1
# Pulling from data base to log in into login landing page
# Matching algorithm
# Pull and display info in login landing page

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
        confirmPassword = self.confirmPassword_textbx.text()
        userDataPage1 = {"fname": fname, "lname": lname, "email": email, "password": password, "phoneNumber": number}
        # print(userDataPage1)

        # check fields arent blank and password matches before going to next page
        if len(fname) == 0 or len(lname) == 0 or len(email) == 0 or len(password) == 0 or len(number) == 0:
            self.error_lbl.setText("Fields can't be blank, \nPlease fill in all fields ")
        elif password != confirmPassword:
            self.error_lbl.setText("Password Does\n Not Match ")
        else:
            # this will open the SecondCreateAccountScreen window in the current window by calling the .ui class
            second_page_create_account = SecondCreateAccountScreen(userDataPage1)
            widget.addWidget(second_page_create_account)
            widget.setCurrentIndex(widget.currentIndex() + 1)

        # second_page_create_account = SecondCreateAccountScreen(userDataPage1)
        # widget.addWidget(second_page_create_account)
        # widget.setCurrentIndex(widget.currentIndex() + 1)


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
            self.menteePg1_function()
        else:
            self.error_lbl.setText("Please select if you are a\nMentor or Mentee ")

    def mentorPg1_function(self):
        # this will open the MentorQuestionsPg1 window in the current window by calling the .ui class
        mentor_pg1 = MentorQuestionsPg1()
        widget.addWidget(mentor_pg1)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def menteePg1_function(self):
        # this will open the new login window in the current window by calling the .ui class
        mentee_Pg1 = MenteeQuestionsPg1()
        widget.addWidget(mentee_Pg1)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class MentorQuestionsPg1(QDialog):
    def __init__(self):
        super(MentorQuestionsPg1, self).__init__()
        # load the gui to our python code
        loadUi("mentor_questions_pg1.ui", self)

        # check boxes functionality

        # This lines of code will check if the checkboxes are checked with (stateChanged) and...
        # ...then it goes into function checked_checkbox

        # programming_checkBox
        self.programming_checkBox.stateChanged.connect(lambda: self.checked_checkbox())
        # sql_checkBox
        self.sql_checkBox.stateChanged.connect(lambda: self.checked_checkbox())
        # databaseAdmin_checkBox
        self.databaseAdmin_checkBox.stateChanged.connect(lambda: self.checked_checkbox())
        # mvvm_checkBox
        self.mvvm_checkBox.stateChanged.connect(lambda: self.checked_checkbox())

        # htmlCssJs_checkBox
        self.htmlCssJs_checkBox.stateChanged.connect(lambda: self.checked_checkbox())
        # networkAdmin_checkBox
        self.networkAdmin_checkBox.stateChanged.connect(lambda: self.checked_checkbox())
        # databaseManger_checkBox
        self.databaseManger_checkBox.stateChanged.connect(lambda: self.checked_checkbox())
        # git_checkBox
        self.git_checkBox.stateChanged.connect(lambda: self.checked_checkbox())

        # cSharpNet_checkBox
        self.cSharpNet_checkBox.stateChanged.connect(lambda: self.checked_checkbox())
        # qualityAssurance_checkBox
        self.qualityAssurance_checkBox.stateChanged.connect(lambda: self.checked_checkbox())
        # databaseQuerying_checkBox
        self.databaseQuerying_checkBox.stateChanged.connect(lambda: self.checked_checkbox())
        # azure_checkBox
        self.azure_checkBox.stateChanged.connect(lambda: self.checked_checkbox())

        # c_checkBox
        self.c_checkBox.stateChanged.connect(lambda: self.checked_checkbox())
        # automatedTesting_checkBox
        self.automatedTesting_checkBox.stateChanged.connect(lambda: self.checked_checkbox())
        # reactJs_checkBox
        self.reactJs_checkBox.stateChanged.connect(lambda: self.checked_checkbox())
        # ios_checkBox
        self.ios_checkBox.stateChanged.connect(lambda: self.checked_checkbox())

        # swift_checkBox
        self.swift_checkBox.stateChanged.connect(lambda: self.checked_checkbox())
        # cloudAdmin_checkBox
        self.cloudAdmin_checkBox.stateChanged.connect(lambda: self.checked_checkbox())
        # wpf_checkBox
        self.wpf_checkBox.stateChanged.connect(lambda: self.checked_checkbox())
        # androidDev_checkBox
        self.androidDev_checkBox.stateChanged.connect(lambda: self.checked_checkbox())

    # Function to verify if checked to display name or not
    def checked_checkbox(self):

        # list for check boxes to be stored
        checkbox_list = []

        # programming
        if self.programming_checkBox.isChecked():
            self.programming = "Programming  "
            checkbox_list.append(self.programming)
        else:
            self.programming = ''
        # SQL
        if self.sql_checkBox.isChecked():
            self.SQL = "SQL  "
            checkbox_list.append(self.SQL)
        else:
            self.SQL = ''
        # databaseAdmin
        if self.databaseAdmin_checkBox.isChecked():
            self.databaseAdmin = "Database Admin  "
            checkbox_list.append(self.databaseAdmin)
        else:
            self.databaseAdmin = ''
        # mvvm_checkBox
        if self.mvvm_checkBox.isChecked():
            self.mvvm = "MVVM  "
            checkbox_list.append(self.mvvm)
        else:
            self.mvvm = ''
        # htmlCssJs_checkBox
        if self.htmlCssJs_checkBox.isChecked():
            self.htmlCssJs = "html/Css/Js  "
            checkbox_list.append(self.htmlCssJs)
        else:
            self.htmlCssJs = ''
        # networkAdmin_checkBox
        if self.networkAdmin_checkBox.isChecked():
            self.networkAdmin = "Network Admin  "
            checkbox_list.append(self.networkAdmin)
        else:
            self.networkAdmin = ''
        # databaseManger_checkBox
        if self.databaseManger_checkBox.isChecked():
            self.databaseManger = "Database Manger  "
            checkbox_list.append(self.databaseManger)
        else:
            self.databaseManger = ''
        # git_checkBox
        if self.git_checkBox.isChecked():
            self.git = "Git  "
            checkbox_list.append(self.git)
        else:
            self.git = ''
        # cSharpNet_checkBox ********************************************
        if self.cSharpNet_checkBox.isChecked():
            self.cSharpNet = "C#/Net  "
            checkbox_list.append(self.cSharpNet)
        else:
            self.cSharpNet = ''
        # qualityAssurance_checkBox
        if self.qualityAssurance_checkBox.isChecked():
            self.qualityAssurance = "Quality Assurance  "
            checkbox_list.append(self.qualityAssurance)
        else:
            self.qualityAssurance = ''
        # databaseQuerying_checkBox
        if self.databaseQuerying_checkBox.isChecked():
            self.databaseQuerying = "Database Querying  "
            checkbox_list.append(self.databaseQuerying)
        else:
            self.databaseQuerying = ''
        # azure_checkBox
        if self.azure_checkBox.isChecked():
            self.azure = "Azure  "
            checkbox_list.append(self.azure)
        else:
            self.azure = ''
        # c_checkBox # ****************************************
        if self.c_checkBox.isChecked():
            self.c = "C  "
            checkbox_list.append(self.c)
        else:
            self.c = ''
        # automatedTesting_checkBox
        if self.automatedTesting_checkBox.isChecked():
            self.automatedTesting = "Automated Testing  "
            checkbox_list.append(self.automatedTesting)
        else:
            self.automatedTesting = ''
        # reactJs_checkBox
        if self.reactJs_checkBox.isChecked():
            self.reactJs = "ReactJs  "
            checkbox_list.append(self.reactJs)
        else:
            self.reactJs = ''
        # ios_checkBox
        if self.ios_checkBox.isChecked():
            self.ios = "IOS  "
            checkbox_list.append(self.ios)
        else:
            self.ios = ''
        print(checkbox_list)
        # swift_checkBox # **************************************
        if self.swift_checkBox.isChecked():
            self.swift = "Swift  "
            checkbox_list.append(self.swift)
        else:
            self.swift = ''
        # cloudAdmin_checkBox
        if self.cloudAdmin_checkBox.isChecked():
            self.cloudAdmin = "Cloud Admin  "
            checkbox_list.append(self.cloudAdmin)
        else:
            self.cloudAdmin = ''
        # wpf_checkBox
        if self.wpf_checkBox.isChecked():
            self.wpf = "WPF  "
            checkbox_list.append(self.wpf)
        else:
            self.wpf = ''
        # androidDev_checkBox
        if self.androidDev_checkBox.isChecked():
            self.androidDev = "Android Dev.  "
            checkbox_list.append(self.androidDev)
        else:
            self.androidDev = ''

        # print the names of the check boxes that were checked
        print(checkbox_list)
        num_in_list = (len(checkbox_list))
        print(num_in_list)

        # Display the names of the check boxes that were checked on to the GUI
        self.specialties_strengthslbl.setText(f'{self.programming}{self.SQL}{self.databaseAdmin}{self.mvvm}'
                                              f'{self.htmlCssJs}{self.networkAdmin}{self.databaseManger}{self.git}'
                                              f'{self.cSharpNet}{self.qualityAssurance}{self.databaseQuerying}{self.azure}'
                                              f'{self.c}{self.automatedTesting}{self.reactJs}{self.ios}'
                                              f'{self.swift}{self.cloudAdmin}{self.wpf}{self.androidDev}')

        yearsinIndustry = self.yearsinIndustry_textbx.text()
        yearsWithCompany = self.yearsWithCompany_textbx.text()

        print(yearsinIndustry)
        print(yearsWithCompany)

        # check fields arent blank and password matches before going to next page
        if len(yearsinIndustry) == 0 and len(yearsWithCompany) == 0:
            self.error_lbl.setText("Fields can't be blank, \nPlease fill in all fields ")
        elif num_in_list < 3:
            self.error_lbl.setText("Can't choose less than 3\n allowed 3 only ")
        elif num_in_list > 3:
            self.error_lbl.setText("Can't choose more than 3\n allowed 3 only")
        else:
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


class MenteeQuestionsPg1(QDialog):
    def __init__(self):
        super(MenteeQuestionsPg1, self).__init__()
        # load the gui to our python code
        loadUi("mentee_questions_pg1.ui", self)
        # this will command to go to gotoLogin function when the button is clicked
        # self.createAccountbtn.clicked.connect(self.)


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

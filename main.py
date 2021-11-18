# TO DO
# Done - functionality for back button
# mentor page 1 fix if else on the checkboxes, currently it goes to next page if more than 3
# Create Account Button in second_create_account needs to be changed to Next
# Next Button in Mentor_questions_pg1 needs to be changed to create account
# Next Button in Mentor_questions_pg2 needs to be changed to create account
# Disable the check boxes and the next button unless only 3 check boxes are checked
# Try to call the mentee checkboxes to the already established function in mentor page 1
# Pulling from data base to log in into login landing page
# Matching algorithm
# Pull and display info in login landing page
# check if class mentore page 2 questions checks that fields are field before continuing and call the spinbox
# check if class mente questions checks that checkboxes are only 3 before continuing

# # Imports to run Qt5
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QLabel, QComboBox, QLineEdit
from PyQt5 import *

import sqlite3
import webbrowser
import mysql.connector


# Credentials to connect to the database
def mysqlconnect():
    credentials = mysql.connector.connect(host='107.180.1.16',
                                          database='cis440fall2021group1',
                                          user='fall2021group1',
                                          password='fall2021group1')
    return credentials


# Loads the Login screen (login.ui) in the same window
def goto_login():
    # this will open the new login window in the current window by calling the .ui class
    login = LoginScreen()
    widget.addWidget(login)
    widget.setCurrentIndex(widget.currentIndex() + 1)


# Work on this if there is time
# def backpage_function(className):
#     widget.addWidget(className)
#     widget.setCurrentIndex(widget.currentIndex() + 1)


# Show the welcome_screen, created class that will have objects,
# and objects have variables like labels we created in Qt5 app and let pyqt5 do it behind the scenes
class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        # load the gui to our python code
        loadUi("welcome_screen.ui", self)
        # this will command to go to gotoLogin function when the button is clicked
        # self.loginbtn.clicked.connect(self.goto_login)
        self.loginbtn.clicked.connect(goto_login)
        # this will command to go to gotocreateAccount function when the button is clicked
        self.createAccountbtn.clicked.connect(self.goto_CreateAccount)

    # def goto_login(self):
    #     # this will open the new login window in the current window by calling the .ui class
    #     login = LoginScreen()
    #     widget.addWidget(login)
    #     widget.setCurrentIndex(widget.currentIndex() + 1)

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
        self.backbtn.clicked.connect(self.backpage_function)

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
            # conn = sqlite3.connect("DATABASE NAME HERE")
            connection = mysqlconnect()
            cursor = connection.cursor()
            # this execute the query's
            # cur = conn.cursor()
            # query = 'SELECT password_COLUMN_HERE FROM TABLE_NAME_HERE WHERE username_COLUMN_NAME =\'' + typed_user + "\'"



            # Check validity of the username
            # query = 'SELECT Email FROM Employees WHERE Email =\'' + typed_user + "\'"
            # cursor.execute(query)
            #
            # result_username = str(cursor.fetchone()[0])
            # print(result_username)


            query = 'SELECT Password FROM Employees WHERE Email =\'' + typed_user + "\'"
            cursor.execute(query)

            # save to result_pass this will get the password from db and check it matches
            # with what they typed in
            # result_password = cursor.fetchone()
            result_password = str(cursor.fetchone()[0])
            print(result_password)

            # if result_username == typed_user and result_password == typed_password:
            if result_password == typed_password:
                print("Successfully logged in")
                self.error_lbl.setText("")
                query = 'SELECT AdvisingRole FROM Employees WHERE Email =\'' + typed_user + "\'"
                cursor.execute(query)
                result_role = str(cursor.fetchone()[0])
                print(result_role)
                self.path(result_role, typed_user)
            else:
                self.error_lbl.setText("Invalid Username or Password")

            cursor.close()
            connection.close()

    # go back to the login page
    def backpage_function(self):
        welcome_pg = WelcomeScreen()
        widget.addWidget(welcome_pg)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    # Loads the corresponding landing page depending on the advising role of the user
    def path(self, role, user):
        if role == "Mentor":
            mentor_login = MentorLanding(user)
            widget.addWidget(mentor_login)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        elif role == "Mentee":
            mentee_login = MenteeLanding(user)
            widget.addWidget(mentee_login)
            widget.setCurrentIndex(widget.currentIndex() + 1)


# Still a working progress
# Displays the mentee matches to the mentor
class MentorLanding(QDialog):
    def __init__(self, user):
        super(MentorLanding, self).__init__()
        loadUi("mentor_landing_pg.ui", self)

        self.user = user
        connection = mysqlconnect()
        cursor = connection.cursor()

        # AOK1 AOK2 AOK3 from mentor
        query1 = f"SELECT AOK1, AOK2, AOK3 FROM Employees WHERE Email = '{self.user}'"
        cursor.execute(query1)
        for value in cursor.fetchall():
            aok1 = str(value[0])
            aok2 = str(value[1])
            aok3 = str(value[2])

        # For Mentee1
        query2 = f"Select FName, LName, Email FROM Employees WHERE '{aok1}' IN(AOK1,AOK2,AOK3) " \
                 f"AND '{aok2}' IN(AOK1,AOK2,AOK3) AND '{aok3}' IN(AOK1,AOK2,AOK3) AND AdvisingRole='Mentee'"
        print(query2)
        cursor.execute(query2)

        matches = cursor.fetchmany(size=5)
        print(matches)
        try:
            if matches:
                if matches[0]:
                    self.mentee1_lbl.setText(matches[0][0] + " " + matches[0][1])
                    self.mentee1_email_lbl.setText(matches[0][2])

                if matches[1]:
                    self.mentee2_lbl.setText(matches[1][0] + " " + matches[1][1])
                    self.mentee2_email_lbl.setText(matches[1][2])

                if matches[2]:
                    self.mentee3_lbl.setText(matches[2][0] + " " + matches[2][1])
                    self.mentee3_email_lbl.setText(matches[2][2])

                if matches[3]:
                    self.mentee4_lbl.setText(matches[3][0] + " " + matches[3][1])
                    self.mentee4_email_lbl.setText(matches[3][2])

                if matches[4]:
                    self.mentee5_lbl.setText(matches[4][0] + " " + matches[4][1])
                    self.mentee5_email_lbl.setText(matches[4][2])
            else:
                # Maybe set all labels to blank to begin with
                print('in else')
                self.mentee1_lbl.setText("No matches are found")
                self.mentee1_email_lbl.setText("")
                #
                # self.mentee2_lbl.setText("")
                # self.mentee2_email_lbl.setText("")
                #
                # self.mentee3_lbl.setText("")
                # self.mentee3_email_lbl.setText("")
                #
                # self.mentee3_lbl.setText("")
                # self.mentee3_email_lbl.setText("")
                #
                # self.mentee4_lbl.setText("")
                # self.mentee4_email_lbl.setText("")
                #
                # self.mentee5_lbl.setText("")
                # self.mentee5_email_lbl.setText("")
        except IndexError:
            print("There are no matches.")
            self.mentee1_lbl.setText("No matches are found")
            # self.mentee1_lbl.setText("")
            # self.mentee1_email_lbl.setText("")
            #
            # self.mentee2_lbl.setText("")
            # self.mentee2_email_lbl.setText("")
            #
            # self.mentee3_lbl.setText("")
            # self.mentee3_email_lbl.setText("")
            #
            # self.mentee3_lbl.setText("")
            # self.mentee3_email_lbl.setText("")
            #
            # self.mentee4_lbl.setText("")
            # self.mentee4_email_lbl.setText("")
            #
            # self.mentee5_lbl.setText("")
            # self.mentee5_email_lbl.setText("")

        self.logout_btn.clicked.connect(goto_login)


# Displays the mentee matches to the mentor
class MenteeLanding(QDialog):
    def __init__(self, user):
        super(MenteeLanding, self).__init__()
        loadUi("mentee_landing_pg.ui", self)

        self.user = user
        connection = mysqlconnect()
        cursor = connection.cursor()

        # AOK1 AOK2 AOK3 from mentor
        query1 = f"SELECT AOK1, AOK2, AOK3 FROM Employees WHERE Email = '{self.user}'"
        cursor.execute(query1)
        for value in cursor.fetchall():
            aok1 = str(value[0])
            aok2 = str(value[1])
            aok3 = str(value[2])

        query2 = f"Select FName, LName, MBType, JobPosition, AbScore, Email FROM Employees " \
                 f"WHERE '{aok1}' IN(AOK1,AOK2,AOK3) AND " \
                 f"'{aok2}' IN(AOK1,AOK2,AOK3) AND " \
                 f"'{aok3}' IN(AOK1,AOK2,AOK3) AND " \
                 f"AdvisingRole='Mentor'"
        cursor.execute(query2)

        matches = cursor.fetchmany(size=2)
        print(matches)
        try:
            if matches:
                if matches[0]:
                    self.mentor1_name_lbl.setText(matches[0][0] + " " + matches[0][1])
                    self.myers_briggs_1.setText(matches[0][2])
                    self.mentor1_job_lbl.setText(matches[0][3])
                    self.mentor1_abscore_lbl.setText(str(matches[0][4]))
                    self.mentor1_email_lbl.setText(matches[0][5])

                if matches[1]:
                    self.mentor2_name_lbl.setText(matches[1][0] + " " + matches[1][1])
                    self.myers_briggs_2.setText(matches[1][2])
                    self.mentor2_job_lbl.setText(matches[1][3])
                    self.mentor2_abscore_lbl.setText(str(matches[1][4]))
                    self.mentor2_email_lbl.setText(matches[1][5])

        except IndexError:
            print("Error Found")

        self.add1_btn.clicked.connect(self.add_mentor_one)
        self.add2_btn.clicked.connect(self.add_mentor_two)
        self.selc_delete_btn.clicked.connect(self.delete_mentor)

        self.logout_btn.clicked.connect(goto_login)

    def add_mentor_one(self):
        self.selc_mentor_name_lbl.setText(self.mentor1_name_lbl.text())
        self.selc_job_lbl.setText(self.mentor1_job_lbl.text())
        self.selc_myers_lbl.setText(self.myers_briggs_1.text())
        self.selc_abscore_lbl.setText('Teaching ability: ' + self.mentor1_abscore_lbl.text())
        self.selc_email_lbl.setText(self.mentor1_email_lbl.text())

    def add_mentor_two(self):
        self.selc_mentor_name_lbl.setText(self.mentor2_name_lbl.text())
        self.selc_job_lbl.setText(self.mentor2_job_lbl.text())
        self.selc_myers_lbl.setText(self.myers_briggs_2.text())
        self.selc_abscore_lbl.setText('Teaching ability: ' +self.mentor2_abscore_lbl.text())
        self.selc_email_lbl.setText(self.mentor2_email_lbl.text())

    def delete_mentor(self):
        self.selc_mentor_name_lbl.setText("Selected Mentor Name")
        self.selc_job_lbl.setText('Position')
        self.selc_myers_lbl.setText('Myers-Briggs')
        self.selc_abscore_lbl.setText('Teaching Ability')
        self.selc_email_lbl.setText('Email')


class CreateAccountScreen(QDialog):


    def __init__(self):
        super(CreateAccountScreen, self).__init__()
        # load the gui to our python code
        loadUi("create_account_both.ui", self)

        # This line will hide the password as its type in
        self.password_textbx.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmPassword_textbx.setEchoMode(QtWidgets.QLineEdit.Password)

        # when next button is clicked it will go to nextpage_funtion
        self.nextbtn.clicked.connect(self.nextpage_function)

        # when the back button is clicked it will go back to the LoginScreen
        self.backbtn.clicked.connect(self.backpage_function)

    def nextpage_function(self):
        # Get user input from create_account_both.ui
        fname = self.fname_textbx.text()
        lname = self.lname_textbx.text()
        email = self.email_textbx.text()
        password = self.password_textbx.text()
        number = self.phonenumber_textbx.text()
        confirmPassword = self.confirmPassword_textbx.text()
        userDataPage1 = {"fname": fname, "lname": lname, "email": email, "password": password, "phoneNumber": number}
        # userDataPage1 = {"fname": fname, "lname": lname, "email": email, "password": password, "phoneNumber": number,
        #                  "department": [], "jobPosition": [], "myersBriggs": []}
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

    # go back to the welcome screen
    def backpage_function(self):
        welcome_pg = WelcomeScreen()
        widget.addWidget(welcome_pg)
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
        self.linklbl.setText(linkTemplate.format('URL', 'Description'))

        self.nextbtn.clicked.connect(self.save_pg1)
        self.backbtn.clicked.connect(self.backpage_function)

    # go back to the first CreateAccountScreen
    def backpage_function(self):
        create_account_pg = CreateAccountScreen()
        widget.addWidget(create_account_pg)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def save_pg1(self):
        # try:
        department = self.department_comboBox.currentText()
        jobPosition = self.jobPosition_comboBox.currentText()
        myersBriggs = self.myersBriggs_comboBox.currentText()

        self.userData.update({"department": department})
        self.userData.update({"jobPosition": jobPosition})
        self.userData.update({"myersBriggs": myersBriggs})

        if self.mentee_rdbtn.isChecked():
            advisingRole = "Mentee"
            self.userData.update({"advisingRole": advisingRole})
        elif self.mentor_rdbtn.isChecked():
            advisingRole = "Mentor"
            self.userData.update({"advisingRole": advisingRole})
        else:
            self.error_lbl.setText("Please select if you are a\nMentor or Mentee ")

            # connection = mysql.connector.connect(host='107.180.1.16',
            #                                      database='cis440fall2021group1',
            #                                      user='fall2021group1',
            #                                      password='fall2021group1')

            # connection = mysqlconnect()

            # if connection.is_connected():
            #     db_info = connection.get_server_info()
            #     print("Connected to MySQL Server version ", db_info)
            #     cursor = connection.cursor()
            #     cursor.execute("select database();")
            #     record = cursor.fetchone()
            #     print("You're connected to database: ", record)

            # Check if any of the fields are empty
        blank = ''
        if blank in self.userData.values():
            self.error_lbl.setText("Please fill in all fields")
            print("A field is empty")
        else:
            # sql = "INSERT INTO Employees (FName, LName, Phone, Email, Password, AdvisingRole, MBType," \
            #       "Department, JobPosition) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            #
            # val = (self.userData['fname'], self.userData['lname'], self.userData['phoneNumber'],
            #        self.userData['email'], self.userData['password'],
            #        advisingRole, myersBriggs, '0', department, jobPosition)
            #
            # cursor.execute(sql, val)
            # connection.commit()
            #
            # print(cursor.rowcount, "record inserted.")
            self.check()

        # except Exception as e:
        #     print("Error while connecting to MySQL", e)

        # finally:
        #     if connection.is_connected():
        #         cursor.close()
        #         connection.close()
        #         print("MySQL connection is closed")

    # Loads the corresponding form page depending on which advising role is selected
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
        mentor_pg1 = MentorQuestionsPg1(self.userData)
        widget.addWidget(mentor_pg1)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def menteePg1_function(self):
        # this will open the MenteeQuestionsPg1 window in the current window by calling the .ui class
        mentee_Pg1 = MenteeQuestionsPg1(self.userData)
        widget.addWidget(mentee_Pg1)
        widget.setCurrentIndex(widget.currentIndex() + 1)


# Questions for Mentors
class MentorQuestionsPg1(QDialog):
    def __init__(self, userData):
        super(MentorQuestionsPg1, self).__init__()
        # load the gui to our python code
        loadUi("mentor_questions_pg1.ui", self)

        self.userData = userData

        # when the back button is clicked it will go back to the previous page
        self.backbtn.clicked.connect(self.backpage_function)

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

        yearsWithCompany = self.yearsWithCompany_textbx.text()
        yearsinIndustry = self.yearsinIndustry_textbx.text()

        # programming
        if self.programming_checkBox.isChecked():
            self.programming = "Programming"
            checkbox_list.append(self.programming)
        else:
            self.programming = ''
        # SQL
        if self.sql_checkBox.isChecked():
            self.SQL = "SQL"
            checkbox_list.append(self.SQL)
        else:
            self.SQL = ''
        # databaseAdmin
        if self.databaseAdmin_checkBox.isChecked():
            self.databaseAdmin = "Database Admin"
            checkbox_list.append(self.databaseAdmin)
        else:
            self.databaseAdmin = ''
        # mvvm_checkBox
        if self.mvvm_checkBox.isChecked():
            self.mvvm = "MVVM"
            checkbox_list.append(self.mvvm)
        else:
            self.mvvm = ''
        # htmlCssJs_checkBox
        if self.htmlCssJs_checkBox.isChecked():
            self.htmlCssJs = "HTML/CSS/JS"
            checkbox_list.append(self.htmlCssJs)
        else:
            self.htmlCssJs = ''
        # networkAdmin_checkBox
        if self.networkAdmin_checkBox.isChecked():
            self.networkAdmin = "Network Admin"
            checkbox_list.append(self.networkAdmin)
        else:
            self.networkAdmin = ''
        # databaseManger_checkBox
        if self.databaseManger_checkBox.isChecked():
            self.databaseManger = "Database Manager"
            checkbox_list.append(self.databaseManger)
        else:
            self.databaseManger = ''
        # git_checkBox
        if self.git_checkBox.isChecked():
            self.git = "Git"
            checkbox_list.append(self.git)
        else:
            self.git = ''
        # cSharpNet_checkBox ********************************************
        if self.cSharpNet_checkBox.isChecked():
            self.cSharpNet = "C#/.NET"
            checkbox_list.append(self.cSharpNet)
        else:
            self.cSharpNet = ''
        # qualityAssurance_checkBox
        if self.qualityAssurance_checkBox.isChecked():
            self.qualityAssurance = "Quality Assurance"
            checkbox_list.append(self.qualityAssurance)
        else:
            self.qualityAssurance = ''
        # databaseQuerying_checkBox
        if self.databaseQuerying_checkBox.isChecked():
            self.databaseQuerying = "Database Querying"
            checkbox_list.append(self.databaseQuerying)
        else:
            self.databaseQuerying = ''
        # azure_checkBox
        if self.azure_checkBox.isChecked():
            self.azure = "Azure"
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
            self.automatedTesting = "Automated Testing"
            checkbox_list.append(self.automatedTesting)
        else:
            self.automatedTesting = ''
        # reactJs_checkBox
        if self.reactJs_checkBox.isChecked():
            self.reactJs = "ReactJS"
            checkbox_list.append(self.reactJs)
        else:
            self.reactJs = ''
        # ios_checkBox
        if self.ios_checkBox.isChecked():
            self.ios = "IOS"
            checkbox_list.append(self.ios)
        else:
            self.ios = ''
        # swift_checkBox # **************************************
        if self.swift_checkBox.isChecked():
            self.swift = "Swift"
            checkbox_list.append(self.swift)
        else:
            self.swift = ''
        # cloudAdmin_checkBox
        if self.cloudAdmin_checkBox.isChecked():
            self.cloudAdmin = "Cloud Admin"
            checkbox_list.append(self.cloudAdmin)
        else:
            self.cloudAdmin = ''
        # wpf_checkBox
        if self.wpf_checkBox.isChecked():
            self.wpf = "WPF"
            checkbox_list.append(self.wpf)
        else:
            self.wpf = ''
        # androidDev_checkBox
        if self.androidDev_checkBox.isChecked():
            self.androidDev = "Android Dev."
            checkbox_list.append(self.androidDev)
        else:
            self.androidDev = ''

        num_in_list = (len(checkbox_list))
        # print(checkbox_list)
        # print(num_in_list)

        if num_in_list < 4:
            # Display the names of the check boxes that were checked on to the GUI
            self.specialties_strengthslbl.setText(f' {self.programming} {self.SQL} {self.databaseAdmin} {self.mvvm}'
                                                  f' {self.htmlCssJs} {self.networkAdmin} {self.databaseManger} {self.git}'
                                                  f' {self.cSharpNet} {self.qualityAssurance} {self.databaseQuerying} {self.azure}'
                                                  f' {self.c} {self.automatedTesting} {self.reactJs} {self.ios}'
                                                  f' {self.swift} {self.cloudAdmin} {self.wpf} {self.androidDev}')

        # check fields arent blank and password matches before going to next page
        if num_in_list > 3:
            self.error_lbl.setText("Must choose 3.")
        elif num_in_list == 3:
            self.userData.update({"yearsWithCompany": yearsWithCompany})
            self.userData.update({"yearsInIndustry": yearsinIndustry})
            self.userData.update({"AOK1": checkbox_list[0]})
            self.userData.update({"AOK2": checkbox_list[1]})
            self.userData.update({"AOK3": checkbox_list[2]})

        if yearsWithCompany and yearsinIndustry:
            self.nextbtn.clicked.connect(self.nextpage_function)

        self.backbtn.clicked.connect(self.backpage_function)

        return checkbox_list

    # go to MentorQuestionsPg2
    def nextpage_function(self):
        strengths_list = self.checked_checkbox()
        if len(strengths_list) == 3:
            mentor_pg2 = MentorQuestionsPg2(self.userData)
            widget.addWidget(mentor_pg2)
            widget.setCurrentIndex(widget.currentIndex() + 1)

    # go back to SecondAccountScreen
    def backpage_function(self):
        second_page_create_account = SecondCreateAccountScreen(self.userData)
        widget.addWidget(second_page_create_account)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class MentorQuestionsPg2(QDialog):
    def __init__(self, userData):
        super(MentorQuestionsPg2, self).__init__()
        # load the gui to our python code
        loadUi("mentor_questions_pg2.ui", self)

        self.userData = userData
        self.backbtn.clicked.connect(self.backpage_function)
        # When create account button is clicked it will go to validate function
        self.createAccountbtn.clicked.connect(self.validate)

    # This function will validate that no fields are left empty
    def validate(self):
        ability_num = self.spinBox.value()
        hobby1 = self.hobby1_textbx.text()
        hobby2 = self.hobby2_textbx.text()
        hobby3 = self.hobby3_textbx.text()
        bio = self.bio_textbx.toPlainText()

        # check fields arent blank before recording to database and going to the login page
        if len(hobby1) == 0 or len(hobby2) == 0 or len(hobby3) == 0 or len(bio) == 0:
            self.error_lbl.setText("Fields can't be blank, \nPlease fill in all fields ")
        else:
            print(f'num = {ability_num}')
            print(f'h1 = {hobby1}')
            print(f'h1 = {hobby2}')
            print(f'h1 = {hobby3}')
            print(f'bio = {bio}')
            # go to connectdatabase function so it can save data in database
            self.connectdatabase()

    # # Insert data into the database
    def connectdatabase(self):
        try:
            connection = mysqlconnect()
            self.createAccountbtn.setEnabled(False)
            if connection.is_connected():
                db_info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_info)
                cursor = connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)

                sql = "INSERT INTO Employees (FName, LName, Phone, Email, Password, AdvisingRole, MBType, Department," \
                      "JobPosition, YearsCo, YearsInd, AOK1, AOK2, AOK3, Hobby1, Hobby2, Hobby3, AbScore, Bio)" \
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                val = (self.userData['fname'], self.userData['lname'], self.userData['phoneNumber'],
                       self.userData['email'], self.userData['password'], self.userData['advisingRole'],
                       self.userData['myersBriggs'], self.userData['department'], self.userData['jobPosition'],
                       self.userData['yearsWithCompany'], self.userData['yearsInIndustry'],
                       self.userData['AOK1'], self.userData['AOK2'], self.userData['AOK3'], self.hobby1_textbx.text(),
                       self.hobby2_textbx.text(), self.hobby3_textbx.text(), self.spinBox.text(),
                       self.bio_textbx.toPlainText())

                cursor.execute(sql, val)
                connection.commit()

                print(cursor.rowcount, "record inserted.")

        except Exception as e:
            print("Error while connecting to MySQL", e)
            self.createAccountbtn.clicked.connect(self.connectdatabase)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
                goto_login()

    # go back to MentorQuestionsPg1
    def backpage_function(self):
        mentor_pg1 = MentorQuestionsPg1(self.userData)
        widget.addWidget(mentor_pg1)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class MenteeQuestionsPg1(QDialog):
    def __init__(self, userData):
        super(MenteeQuestionsPg1, self).__init__()
        # load the gui to our python code
        loadUi("mentee_questions_pg1.ui", self)

        # when next button is clicked it will go back to the previous page
        self.backbtn.clicked.connect(self.backpage_function)

        self.userData = userData
        # self.createAccountbtn.clicked.connect(self.connectdatabase)

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
            self.programming = "Programming"
            checkbox_list.append(self.programming)
        else:
            self.programming = ''
        # SQL
        if self.sql_checkBox.isChecked():
            self.SQL = "SQL"
            checkbox_list.append(self.SQL)
        else:
            self.SQL = ''
        # databaseAdmin
        if self.databaseAdmin_checkBox.isChecked():
            self.databaseAdmin = "Database Admin"
            checkbox_list.append(self.databaseAdmin)
        else:
            self.databaseAdmin = ''
        # mvvm_checkBox
        if self.mvvm_checkBox.isChecked():
            self.mvvm = "MVVM"
            checkbox_list.append(self.mvvm)
        else:
            self.mvvm = ''
        # htmlCssJs_checkBox
        if self.htmlCssJs_checkBox.isChecked():
            self.htmlCssJs = "HTML/CSS/JS"
            checkbox_list.append(self.htmlCssJs)
        else:
            self.htmlCssJs = ''
        # networkAdmin_checkBox
        if self.networkAdmin_checkBox.isChecked():
            self.networkAdmin = "Network Admin"
            checkbox_list.append(self.networkAdmin)
        else:
            self.networkAdmin = ''
        # databaseManger_checkBox
        if self.databaseManger_checkBox.isChecked():
            self.databaseManger = "Database Manager"
            checkbox_list.append(self.databaseManger)
        else:
            self.databaseManger = ''
        # git_checkBox
        if self.git_checkBox.isChecked():
            self.git = "Git"
            checkbox_list.append(self.git)
        else:
            self.git = ''
        # cSharpNet_checkBox ********************************************
        if self.cSharpNet_checkBox.isChecked():
            self.cSharpNet = "C#/.NET"
            checkbox_list.append(self.cSharpNet)
        else:
            self.cSharpNet = ''
        # qualityAssurance_checkBox
        if self.qualityAssurance_checkBox.isChecked():
            self.qualityAssurance = "Quality Assurance"
            checkbox_list.append(self.qualityAssurance)
        else:
            self.qualityAssurance = ''
        # databaseQuerying_checkBox
        if self.databaseQuerying_checkBox.isChecked():
            self.databaseQuerying = "Database Querying"
            checkbox_list.append(self.databaseQuerying)
        else:
            self.databaseQuerying = ''
        # azure_checkBox
        if self.azure_checkBox.isChecked():
            self.azure = "Azure"
            checkbox_list.append(self.azure)
        else:
            self.azure = ''
        # c_checkBox # ****************************************
        if self.c_checkBox.isChecked():
            self.c = "C"
            checkbox_list.append(self.c)
        else:
            self.c = ''
        # automatedTesting_checkBox
        if self.automatedTesting_checkBox.isChecked():
            self.automatedTesting = "Automated Testing"
            checkbox_list.append(self.automatedTesting)
        else:
            self.automatedTesting = ''
        # reactJs_checkBox
        if self.reactJs_checkBox.isChecked():
            self.reactJs = "ReactJS"
            checkbox_list.append(self.reactJs)
        else:
            self.reactJs = ''
        # ios_checkBox
        if self.ios_checkBox.isChecked():
            self.ios = "iOS"
            checkbox_list.append(self.ios)
        else:
            self.ios = ''

        # swift_checkBox # **************************************
        if self.swift_checkBox.isChecked():
            self.swift = "Swift"
            checkbox_list.append(self.swift)
        else:
            self.swift = ''
        # cloudAdmin_checkBox
        if self.cloudAdmin_checkBox.isChecked():
            self.cloudAdmin = "Cloud Admin"
            checkbox_list.append(self.cloudAdmin)
        else:
            self.cloudAdmin = ''
        # wpf_checkBox
        if self.wpf_checkBox.isChecked():
            self.wpf = "WPF"
            checkbox_list.append(self.wpf)
        else:
            self.wpf = ''
        # androidDev_checkBox
        if self.androidDev_checkBox.isChecked():
            self.androidDev = "Android Dev."
            checkbox_list.append(self.androidDev)
        else:
            self.androidDev = ''

        # print the names of the check boxes that were checked
        print(checkbox_list)
        num_in_list = (len(checkbox_list))
        print(num_in_list)

        # Display the names of the check boxes that were checked on to the GUI
        if num_in_list < 4:
            self.specialties_strengthslbl.setText(f' {self.programming} {self.SQL} {self.databaseAdmin} {self.mvvm}'
                                                  f' {self.htmlCssJs} {self.networkAdmin} {self.databaseManger} {self.git}'
                                                  f' {self.cSharpNet} {self.qualityAssurance} {self.databaseQuerying} {self.azure}'
                                                  f' {self.c} {self.automatedTesting} {self.reactJs} {self.ios}'
                                                  f' {self.swift} {self.cloudAdmin} {self.wpf} {self.androidDev}')

        if num_in_list > 3:
            self.error_lbl.setText("Must choose 3.")
        elif num_in_list == 3:
            self.userData.update({"AOK1": checkbox_list[0]})
            self.userData.update({"AOK2": checkbox_list[1]})
            self.userData.update({"AOK3": checkbox_list[2]})
            self.createAccountbtn.clicked.connect(self.connectdatabase)

        return checkbox_list

    def connectdatabase(self):
        print('connecting')

        strengths_list = self.checked_checkbox()

        if len(strengths_list) == 3:
            self.createAccountbtn.setEnabled(False)

            try:
                connection = mysqlconnect()

                if connection.is_connected():
                    db_info = connection.get_server_info()
                    print("Connected to MySQL Server version ", db_info)
                    cursor = connection.cursor()
                    cursor.execute("select database();")
                    record = cursor.fetchone()
                    print("You're connected to database: ", record)

                    sql = "INSERT INTO Employees (FName, LName, Phone, Email, Password, AdvisingRole, MBType, Department," \
                          "JobPosition, AOK1, AOK2, AOK3)" \
                          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                    val = (self.userData['fname'], self.userData['lname'], self.userData['phoneNumber'],
                           self.userData['email'], self.userData['password'], self.userData['advisingRole'],
                           self.userData['myersBriggs'], self.userData['department'], self.userData['jobPosition'],
                           self.userData['AOK1'], self.userData['AOK2'], self.userData['AOK3'])

                    cursor.execute(sql, val)
                    connection.commit()

                    print(cursor.rowcount, "record inserted.")

            except Exception as e:
                print("Error while connecting to MySQL", e)
                self.createAccountbtn.clicked.connect(self.connectdatabase)

            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("MySQL connection is closed")
                    goto_login()

    # go back to SecondAccountScreen
    def backpage_function(self):
        second_page_create_account = SecondCreateAccountScreen(self.userData)
        widget.addWidget(second_page_create_account)
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
widget.setWindowTitle('COBOLT')
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")

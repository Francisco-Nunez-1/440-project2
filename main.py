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
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QLabel
import sqlite3
import webbrowser


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

def nextpage_function():
    # this will open the SecondCreateAccountScreen window in the current window by calling the .ui class
    second_page_create_account = SecondCreateAccountScreen()
    widget.addWidget(second_page_create_account)
    widget.setCurrentIndex(widget.currentIndex() + 1)

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
    def __init__(self):
        super(CreateAccountScreen, self).__init__()
        # load the gui to our python code
        loadUi("create_account_both.ui", self)

        # This line will hide the password as its type in
        self.password_textbx.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmPassword_textbx.setEchoMode(QtWidgets.QLineEdit.Password)

        # when next button is clicked it will go to nextpage_funtion
        self.nextbtn.clicked.connect(nextpage_function)


# this is for link
class HyperlinkLabel(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setStyleSheet('font-size: 35px')
        self.setOpenExternalLinks(True)
        self.setParent(parent)


class SecondCreateAccountScreen(QDialog):
    def __init__(self):
        super(SecondCreateAccountScreen, self).__init__()
        # load the gui to our python code
        loadUi("second_create_account.ui", self)

        # this is for link/ place holders should be available
        # https://learndataanalysis.org/create-hyperlinks-pyqt5-tutorial/
        linkTemplate = "<a href='https://www.16personalities.com/free-personality-test'>'Myers–Briggs'</a>"

        # linklbl = HyperlinkLabel(self)
        self.linklbl.setText(linkTemplate)


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

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
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget
import sqlite3


# Show the welcome_screen, created class that will have objects,
# and objects have variables like labels we created in Qt5 app and let pyqt5 do it behind the scenes
class welcome_screen(QDialog):
    def __init__(self):
        super(welcome_screen, self).__init__()
        # load the gui to our python code
        loadUi("welcome_screen.ui", self)
        # this will command to go to login screen when button clicked
        self.login.clicked.connect(self.gotologin)

    def gotologin(self):
        # this will open the new window in the current window
        login = Login_screen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Login_screen(QDialog):
    def __init__(self):
        super(Login_screen, self).__init__()
        # load the gui to our python code
        loadUi("login.ui", self)
        # This line will hide the password as its type in
        self.password_textbx.setEchoMode(QtWidgets.QLineEdit.Password)
        # connect to function to do next after login button is clicked
        self.login.clicked.connect(self.loginfunction)

    def loginfunction(self):
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
# *******************************************************************************************************

# main
app = QApplication(sys.argv)
welcome = welcome_screen()
# this will stack many widgets on top of eachother so we can move between screens
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

from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, \
    QVBoxLayout, QLineEdit, QMainWindow, \
    QAction, QTextEdit, QLabel, QHBoxLayout, QScrollArea, QGroupBox, QCheckBox
from PyQt5.QtGui import QColor, QPalette, QIcon
from PyQt5.QtCore import Qt, QSize
import sys
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import imaplib
import email


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.id = ""
        self.password = ""
        self.init_ui()

    def init_ui(self):
        self.mail_address = QLineEdit()
        self.send_button = QPushButton("Send!")
        self.mail_text = QTextEdit()
        self.mail_subject = QLineEdit()
        self.label_to = QLabel("To:")
        self.label_subject = QLabel("Subject:")
        self.label_text = QLabel("Text:")
        self.label_text.setFixedWidth(50)
        self.warning_label = QLabel("")
        self.warning_label_head = QLabel("")
        self.hidden_inbox_button = QPushButton("<")
        self.hidden_inbox_button.setFixedSize(30, 70)

        v_box1 = QVBoxLayout()
        v_box1.addWidget(self.label_to)
        v_box1.addWidget(self.label_subject)

        v_box2 = QVBoxLayout()
        v_box2.addWidget(self.mail_address)
        v_box2.addWidget(self.mail_subject)

        h_box1 = QHBoxLayout()
        h_box1.addLayout(v_box1)
        h_box1.addLayout(v_box2)

        h_box2 = QHBoxLayout()
        h_box2.addWidget(self.label_text)
        h_box2.addWidget(self.mail_text)

        v_box = QVBoxLayout()
        v_box.addLayout(h_box1)
        v_box.addLayout(h_box2)
        v_box.addWidget(self.warning_label_head)
        v_box.addWidget(self.warning_label)
        v_box.addWidget(self.send_button, 10)

        h_box5 = QHBoxLayout()
        h_box5.addLayout(v_box)
        self.setLayout(h_box5)
        self.send_button.clicked.connect(self.send)

    def send(self):
        to = self.mail_address.text()
        subject = self.mail_subject.text()
        text = self.mail_text.toPlainText()
        mail = MailSettings(to, subject, text, self.id, self.password)
        warnings = mail.mail_info()
        warning = "\n".join(warnings)
        self.warning_label_head.setText("Invalid e-mail addresses:\n")
        self.warning_label_head.setStyleSheet("color: red; border: 2px solid red; border-radius: 5px")
        self.warning_label.setText(warning)


class LoginUI(QWidget):
    def __init__(self):
        super().__init__()
        self.login()

    def login(self):
        self.id = QLineEdit("")
        self.password = QLineEdit("")
        self.password.setEchoMode(QLineEdit.Password)
        self.sign_in = QPushButton("Sign In", self)
        id_label = QLabel("ID:", self)
        password_label = QLabel("Password:", self)

        inp_box = QVBoxLayout()
        inp_box.addStretch()
        inp_box.addWidget(self.id)
        inp_box.addWidget(self.password)

        v_box = QVBoxLayout()
        v_box.addStretch()
        v_box.addWidget(id_label)
        v_box.addWidget(password_label)

        h_box = QHBoxLayout()
        h_box.addLayout(v_box)
        h_box.addLayout(inp_box)

        gen_box = QVBoxLayout()
        gen_box.addLayout(h_box)
        gen_box.addWidget(self.sign_in)
        gen_box.addStretch()

        gen2_box = QHBoxLayout()
        gen2_box.addStretch()
        gen2_box.addLayout(gen_box)
        gen2_box.addStretch()

        self.setLayout(gen2_box)


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("E-Mapp")
        self.setWindowIcon(QIcon('email_sender_icon.png'))
        self.main_ui()
        self.window = Window()
        self.login = LoginUI()
        self.setFixedSize(400, 300)
        self.setCentralWidget(self.login)
        menubar = self.menuBar()
        file = menubar.addMenu("File")
        file.addAction(QAction("Open", self))
        self.login.sign_in.clicked.connect(self.enter_system)

    def enter_system(self):
        self.setFixedSize(800, 600)
        self.window.id = self.login.id.text()
        self.window.password = self.login.password.text()
        self.setCentralWidget(self.window)

    def main_ui(self):
        top, bottom, width, height = 300, 500, 600, 400
        self.setGeometry(top, bottom, width, height)
        self.show()


class MailSettings:
    def __init__(self, to=None, subject="No Subject", text=None, user_id=None, user_pass=None):
        self.to = to.split(",")
        self.subject = subject
        self.text = text
        self.user_id = user_id
        self.user_pass = user_pass

    def mail_info(self):
        send_fails = []
        for person in self.to:
            message = MIMEMultipart()
            person = person.strip(" ")
            message["To"] = "{}".format(person)
            message["From"] = "{}".format(self.user_id)
            message["Subject"] = self.subject
            self.text += "\n\nThis email was sent via E-Mapp.\nE-Mapp Source Code: https://github.com/MERTULAS/E-Mapp"
            content = MIMEText(self.text, "plain")
            message.attach(content)
            try:
                mail = SMTP("smtp.gmail.com", 587)
                mail.ehlo()
                mail.starttls()
                mail.login(self.user_id, self.user_pass)
                mail.sendmail(message["From"], message["To"], message.as_string())
                mail.close()

            except:
                send_fails.append("-" + person)
        return send_fails


if __name__ == '__main__':
    app = QApplication(sys.argv)

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.Base, QColor(0, 0, 30))
    palette.setColor(QPalette.Text, QColor(200, 200, 200))
    app.setPalette(palette)

    menu = Menu()
    sys.exit(app.exec_())

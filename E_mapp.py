from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, \
    QVBoxLayout, QLineEdit, QMainWindow, \
    QAction, QTextEdit, QLabel, QHBoxLayout, QScrollArea, QGroupBox, QCheckBox
from PyQt5.QtGui import QColor, QPalette, QMouseEvent
from PyQt5.QtCore import Qt, QSize
import sys
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import imaplib
import email
from email.header import decode_header


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.id = ""
        self.password = ""
        self.inbox = ""
        self.init_ui()

    def inbox_mails(self,mail):
        self.incoming_mail = QGroupBox()
        self.incoming_mail_group = QVBoxLayout(self.incoming_mail)
        self.inbox_subject = QLabel("Subject: " + mail[0])
        self.inbox_from = QLabel("From: " + mail[1])
        self.incoming_mail_group.addWidget(self.inbox_subject)
        self.incoming_mail_group.addWidget(self.inbox_from)
        self.box_palette = QPalette()
        self.box_palette.setColor(QPalette.Background, QColor(100, 100, 100))
        self.setPalette(self.box_palette)
        return self.incoming_mail

    def inbox_container(self):
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setMaximumWidth(250)
        self.scrollArea.setMinimumWidth(100)
        self.scrollArea.setWidgetResizable(True)
        self.widget = QWidget()
        self.scrollArea.setWidget(self.widget)
        self.layoutScrollArea = QVBoxLayout()
        self.inbox = MailSettings.inbox_getter()
        for index, mail_in_inbox in enumerate(self.inbox):
            self.layoutScrollArea.addWidget(self.inbox_mails(mail_in_inbox))
        self.widget.setLayout(self.layoutScrollArea)

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
        self.hidden_inbox_button = QPushButton("<", self)
        self.hidden_inbox_button.setFixedSize(30, 70)

        self.hidden_inbox_button.clicked.connect(self.hidden_inbox)

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

        self.v_box = QVBoxLayout()
        self.v_box.addLayout(h_box1)
        self.v_box.addLayout(h_box2)
        self.v_box.addWidget(self.warning_label_head)
        self.v_box.addWidget(self.warning_label)
        self.v_box.addWidget(self.send_button, 10)

        self.inbox_container()
        h_box4 = QHBoxLayout()
        h_box4.addWidget(self.scrollArea)
        h_box4.addWidget(self.hidden_inbox_button)

        h_box5 = QHBoxLayout()
        h_box5.addLayout(h_box4)
        h_box5.addLayout(self.v_box)
        self.setLayout(h_box5)
        self.send_button.clicked.connect(self.send)

    def send(self):
        to = self.mail_address.text()
        subject = self.mail_subject.text()
        text = self.mail_text.toPlainText()
        mail = MailSettings(to, subject, text, self.id, self.password)
        warnings = mail.mail_sender()
        warning = "\n".join(warnings)
        self.warning_label_head.setText("Invalid e-mail addresses:\n")
        self.warning_label_head.setStyleSheet("color: red; border: 2px solid red; border-radius: 5px")
        self.warning_label.setText(warning)

    def hidden_inbox(self):
        if self.scrollArea.isHidden():
            self.scrollArea.show()
            #self.incoming_mail.show()
            self.hidden_inbox_button.setText("<")
            self.setGeometry(self.x() + 1, self.y() + 1, self.width() + 1, self.height() + 1)
            self.update()
        else:
            self.scrollArea.hide()
            #self.incoming_mail.hide()
            self.hidden_inbox_button.setText(">")
            self.resize(self.width() - 1, self.height() - 1)


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
        self.main_ui()
        self.window = Window()
        self.login = LoginUI()
        self.setFixedSize(400, 300)
        self.setCentralWidget(self.login)
        self.login.resize(300, 200)
        self.login.sign_in.clicked.connect(self.enter_system)

    def enter_system(self):
        self.setFixedSize(900, 600)
        self.window.id = self.login.id.text()
        self.window.password = self.login.password.text()
        self.setCentralWidget(self.window)

    def main_ui(self):
        self.menubar = self.menuBar()
        self.file = self.menubar.addMenu("File")
        # self.open_ = QAction("Open", self)
        # self.file.addAction(self.open_)
        self.edit = self.menubar.addMenu("Edit")
        self.dark_mode = QAction("Dark Mode: On/Off", self, checkable=True)
        self.dark_mode.setChecked(True)
        self.edit.addAction(self.dark_mode)
        self.dark_mode.triggered.connect(self.theme_mode)
        self.show()

    @staticmethod
    def theme_mode(action):
        theme = QPalette()
        if action:
            theme.setColor(QPalette.Window, QColor(53, 53, 53))
            theme.setColor(QPalette.Base, QColor(10, 10, 15))
            theme.setColor(QPalette.Text, QColor(200, 200, 200))
            app.setPalette(theme)
        else:
            theme.setColor(QPalette.Window, QColor(210, 210, 210))
            theme.setColor(QPalette.Base, QColor(190, 190, 190))
            theme.setColor(QPalette.Text, QColor(0, 0, 0))
            theme.setColor(QPalette.ToolTipText, QColor(255, 0, 0))
            app.setPalette(theme)


class MailSettings:
    def __init__(self, to=None, subject="No Subject", text=None, user_id="", user_pass=""):
        if to:
            self.to = to.split(",")
        self.subject = subject
        self.text = text
        self.user_id = user_id
        self.user_pass = user_pass

    def mail_sender(self):
        send_fails = []
        for person in self.to:
            message = MIMEMultipart()
            person = person.strip(" ")
            message["To"] = "{}".format(person)
            message["From"] = "{}".format(self.user_id)
            message["Subject"] = self.subject
            content_text = self.text + "\n\nThis email was sent via E-Mapp.\nE-Mapp Source Code: https://github.com/MERTULAS/E-Mapp"
            content = MIMEText(content_text, "plain")
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

    @staticmethod
    def inbox_getter():
        inbox = []
        mail_inbox = imaplib.IMAP4_SSL("imap.gmail.com")
        mail_inbox.login("h.mert.ulas@gmail.com", "hmfb342244oyun")
        status, messages = mail_inbox.select("INBOX")
        messages = int(messages[0])
        for i in range(messages, messages - 10, -1):
            res, msg = mail_inbox.fetch(str(i), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    subject = decode_header(msg["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        try:
                            subject = subject.decode("utf-8")
                        except UnicodeDecodeError:
                            pass
                    from_ = msg.get("From")
                    if msg.is_multipart():ü
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                body_ = body
                    else:
                        content_type = msg.get_content_type()
                        body = msg.get_payload(decode=True).decode()
                        if content_type == "text/plain":
                            body_ = body
                    inbox.append([subject, from_, body_])
        return inbox


if __name__ == '__main__':
    app = QApplication(sys.argv)
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.Base, QColor(10, 10, 15))
    palette.setColor(QPalette.Text, QColor(200, 200, 200))
    app.setPalette(palette)
    menu = Menu()
    sys.exit(app.exec_())

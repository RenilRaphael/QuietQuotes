from PyQt6.QtWidgets import QDialog, QFormLayout, QComboBox, QPushButton, QFontComboBox, QSpinBox, QColorDialog, QWidget, QVBoxLayout, QLabel, QApplication
from PyQt6.QtCore import Qt, pyqtSignal,QTimer
import quotespicker as qp

class Settings_window(QDialog):
    settings_saved = pyqtSignal(dict)
    def __init__(self, mainw):
        super().__init__()
        self.main_screen=mainw
        self.setGeometry(300,100,500,250)
        fbox = QFormLayout()
        
        self.qfont_size = QComboBox()
        self.qfont_size.addItems([str(x) for x in range(15,41)])
        self.qfont_cb = QPushButton("Select quote's font colour")
        self.qfont_select=QFontComboBox()
        self.qfont_select.setFontFilters(QFontComboBox.FontFilter.ScalableFonts)

        self.afont_size = QComboBox()
        self.afont_size.addItems([str(x) for x in range(15,41)])
        self.afont_cb = QPushButton("Select author's font colour")
        self.afont_select=QFontComboBox()
        self.afont_select.setFontFilters(QFontComboBox.FontFilter.ScalableFonts)
        self.timeset = QSpinBox()
        try:
            self.qfont_size.setCurrentText(self.main_screen.current_settings["qfonts"])
            self.qfont_select.setCurrentText(self.main_screen.current_settings["qfontf"])
            self.afont_size.setCurrentText(self.main_screen.current_settings["afonts"])
            self.afont_select.setCurrentText(self.main_screen.current_settings["afontf"])
            self.qcolour=self.main_screen.current_settings["qfontc"]
            self.acolour=self.main_screen.current_settings["afontc"]
            self.timeset.setValue(self.main_screen.current_settings["duration"])
        except KeyError:
                pass
        self.timeset.setRange(1,120)
        self.resetdef = QPushButton("Reset to defaults")
        fbox.addRow("Quote Font:", self.qfont_select)
        fbox.addRow("Quote Font size:",self.qfont_size)
        fbox.addRow(self.qfont_cb)
        fbox.addRow("Author Font:", self.afont_select)
        fbox.addRow("Author Font size:",self.afont_size)
        fbox.addRow(self.afont_cb)
        fbox.addRow("Set duration:",self.timeset)
        fbox.addRow(self.resetdef)
        self.qfont_cb.clicked.connect(lambda: self.colourP(1))
        self.afont_cb.clicked.connect(lambda: self.colourP(0))
        self.resetdef.clicked.connect(lambda: self.save_f(1))

        self.save_button=QPushButton("Save",self)
        self.close_button=QPushButton("Close QuietQuotes",self)
        fbox.addWidget(self.save_button)

        self.cancel=QPushButton("Cancel",self)
        fbox.addWidget(self.cancel)
        fbox.addWidget(self.close_button)
        self.save_button.clicked.connect(self.save_f)
        self.cancel.clicked.connect(self.close)
        self.close_button.clicked.connect(self.close_A)

        self.setLayout(fbox)
        self.show()
    
    def save_f(self,flg=0):
        if flg==0:
            changes= {
            "qfonts":self.qfont_size.currentText(),
            "qfontf":self.qfont_select.currentText(),
            "afonts":self.afont_size.currentText(),
            "afontf":self.afont_select.currentText(),
            "qfontc":self.qcolour,
            "afontc":self.acolour,
            "duration":self.timeset.value()
            }
        else:
            changes= {
            "qfonts":"25",
            "qfontf":"Times New Roman",
            "afonts":"25",
            "afontf":"Times New Roman",
            "qfontc":"white",
            "afontc":"white",
            "duration":30
        }
        self.settings_saved.emit(changes)
        self.accept()

    def close_A(self):
        self.main_screen.close()
        self.close()

    def colourP(self,flgs):
        col_p=QColorDialog(self)
        col_p.show()
        if col_p.exec():
            if flgs==1:
                self.qfont_cb.setStyleSheet("background-color: %s;" % col_p.currentColor().name())
                self.qcolour= col_p.currentColor().name()
            else:
                self.afont_cb.setStyleSheet("background-color: %s;" % col_p.currentColor().name())
                self.acolour= col_p.currentColor().name()


class M_window(QWidget):
    def __init__(self):
        super().__init__()
        self.get_Settings()
        self.setGeometry(1000,100,600,250)
        self.setFixedWidth(500)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        vbox=QVBoxLayout()

        quote=qp.getQuote()
        self.quote=QLabel(quote["quote"])
        self.author=QLabel(f"-{quote["author"]}")
        vbox.addStretch()
        vbox.addWidget(self.quote)
        self.quote.setWordWrap(True)
        self.quote.setStyleSheet(f"font-size:{self.current_settings["qfonts"]}px;font-family:{self.current_settings["qfontf"]};color:{self.current_settings["qfontc"]}")
        self.author.setWordWrap(True)
        self.author.setStyleSheet(f"font-size:{self.current_settings["afonts"]}px;font-family:{self.current_settings["afontf"]};color:{self.current_settings["afontc"]};")
        
        vbox.addWidget(self.author)
        vbox.addStretch()
        vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.quote.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.author.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setLayout(vbox)
        
        self.button1=QPushButton("Settings",self)
        self.button1.setGeometry(400,0,70,25)
        self.button1.clicked.connect(self.openSettings)
        
        self.q_countdown= QTimer()
        self.q_countdown.setInterval(self.current_settings["duration"]*60000)
        self.q_countdown.timeout.connect(self.setQuote)

        self.q_countdown.start()
        
        self.show()
    
    def setQuote(self):
        quote=qp.getQuote()
        self.quote.setText(quote["quote"])
        self.author.setText(quote["author"])
    
    def openSettings(self):
        self.button1.setDisabled(True)
        sw=Settings_window(self)
        sw.settings_saved.connect(self.applyS)
        sw.exec()
        self.button1.setDisabled(False)
    
    def applyS(self,s):
        self.current_settings=s
        self.quote.setStyleSheet(f"font-size:{self.current_settings["qfonts"]}px;font-family:{self.current_settings["qfontf"]};color:{self.current_settings["qfontc"]}")
        self.author.setStyleSheet(f"font-size:{self.current_settings["afonts"]}px;font-family:{self.current_settings["afontf"]};color:{self.current_settings["afontc"]};")
        self.q_countdown.setInterval(self.current_settings["duration"]*60000)

        self.save_Settings()
    
    def get_Settings(self):
        try:
            with open("settings.json","r+",encoding='utf-8') as file:
                self.current_settings=qp.json.load(file)
        except FileNotFoundError:
            with open('settings.json', 'w') as file:
                self.current_settings={"qfonts":"25",
                               "qfontf":"Times New Roman",
                               "afonts":"25",
                               "afontf":"Times New Roman",
                               "qfontc":"white",
                               "afontc":"white",
                               "duration":30
                               }
                qp.json.dump(self.current_settings,file)
                
    def save_Settings(self):
        with open("settings.json","w",encoding='utf-8') as file:
                qp.json.dump(self.current_settings,file)

app= QApplication([])
main_window=M_window()

app.exec()





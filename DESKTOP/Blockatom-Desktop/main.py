# |---------------------------------------------CODED BY @SENSORDS---------------------------------------------|

import sqlite3

import bit
import clipboard
import qrcode as qrcode
import requests
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from bs4 import BeautifulSoup
from pywallet import wallet
from pywallet.utils import *


class LoginScreen(QMainWindow):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("GUI/atom.ui",self)
        self.passwordline.setEchoMode(QtWidgets.QLineEdit.Password)
        self.registrnow.clicked.connect(self.gotoReg)
        self.Loginone.clicked.connect(self.loginfunction)

    def gotoReg(self):
        Reg = RegScreen()
        widget.addWidget(Reg)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def loginfunction(self):
        password = self.passwordline.text()
        if len(password) == 0:
            self.error.setText("Please input all fields.")
        else:
            db = sqlite3.connect("wallet.db")
            curs = db.cursor()
            curs.execute(f"SELECT * FROM users WHERE Password = '{password}'")
            if not curs.fetchone():
                self.error.setText("Incorrect password")
            else:
                fillprofile = Profile()
                widget.addWidget(fillprofile)
                widget.setCurrentIndex(widget.currentIndex() + 1)

class Profile(QDialog):
    def __init__(self):
        super(Profile, self).__init__()
        loadUi("GUI/main.ui", self)
        self.btcpricee()
        self.balanceuser()
        self.logout.clicked.connect(self.loginout)
        self.receive.clicked.connect(self.receivebtcaddress)
        self.receive_2.clicked.connect(self.receivebtcaddress)
        self.walletbutton.clicked.connect(self.walletent)
        self.sendd.clicked.connect(self.sendbtc)
        self.sendd_2.clicked.connect(self.sendbtc)
        self.settings.clicked.connect(self.settinges)

    def balanceuser(self):
        try:
            db = sqlite3.connect("wallet.db")
            curs = db.cursor()
            sss = "SELECT btc_address FROM users"
            curs.execute(sss)
            adres = curs.fetchone()
            url = f'https://www.blockchain.com/btc/address/{adres[0]}'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'}
            Response = requests.get(url, headers=headers)
            wallet = BeautifulSoup(Response.content, 'html.parser')
            convert = wallet.findAll("span", {"class": "sc-16b9dsl-1","class": "ZwupP", "class": "u3ufsr-0", "class": "eQTRKC"})
            rx = convert[6].text
            self.balance.setText(str(rx))
            response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
            data = response.json()
            x = data["bpi"]["USD"]["rate_float"]
            xx = rx.rstrip('BTC')
            us = (x * float(xx))
            self.usdbalance.setText(str(us))
        except:
            self.balance.setText(str('Loading...'))
            self.usdbalance.setText(str('---'))

    def btcpricee(self):
        response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
        data = response.json()
        btc = data["bpi"]["USD"]["rate_float"]
        self.btcprice.setText(str(int(btc)))
        return btc

    def loginout(self):
        Log = LoginScreen()
        widget.addWidget(Log)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def receivebtcaddress(self):
        receivebtc2 = receivebtc()
        widget.addWidget(receivebtc2)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def walletent(self):
        wallets = Wallets()
        widget.addWidget(wallets)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def sendbtc(self):
        sends = sending()
        widget.addWidget(sends)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def settinges(self):
        set = settingss()
        widget.addWidget(set)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class receivebtc(QDialog):
    def __init__(self):
        super(receivebtc, self).__init__()
        loadUi("GUI/receive.ui", self)
        self.logout.clicked.connect(self.loginout)
        self.home.clicked.connect(self.profilee)
        self.walletbutton.clicked.connect(self.walletent)
        self.receive()
        self.sendd.clicked.connect(self.sendbtc)
        self.settings.clicked.connect(self.settinges)
        self.copy.clicked.connect(self.copy_address)

    def profilee(self):
        fillprofile = Profile()
        widget.addWidget(fillprofile)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def walletent(self):
        wallets = Wallets()
        widget.addWidget(wallets)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def loginout(self):
        Log = LoginScreen()
        widget.addWidget(Log)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def receive(self):
        db = sqlite3.connect("wallet.db")
        curs = db.cursor()
        curs.execute("SELECT btc_address FROM users")
        adr = curs.fetchone()
        self.btcaddress.setText(str(adr[0]))

    def copy_address(self):
        adress = self.btcaddress.text()
        clipboard.copy(adress)
        self.copied.setText('Copied!')

    def sendbtc(self):
        sends = sending()
        widget.addWidget(sends)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def settinges(self):
        set = settingss()
        widget.addWidget(set)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class sending(QDialog):
    def __init__(self):
        super(sending, self).__init__()
        loadUi("GUI/send.ui", self)
        self.logout.clicked.connect(self.loginout)
        self.home.clicked.connect(self.profilee)
        self.receive_2.clicked.connect(self.receivee)
        self.walletbutton.clicked.connect(self.walletent)
        self.addressfrom()
        self.settings.clicked.connect(self.settinges)
        self.send_button.clicked.connect(self.seend)

    def seend(self):
        try:
            db = sqlite3.connect("wallet.db")
            curs = db.cursor()
            curs.execute("SELECT wif FROM users")
            wif = curs.fetchone()[0]
            # wifstr = str(wif, encoding='utf-8')
            if self.minimalfee.isChecked():
                fee=2000
                where = self.sendto.text()
                if len(where) == 0:
                    self.fielderror.setText("You have not filled out this field")
                else:
                    amount = self.amountbtc.value()
                    sss = "SELECT btc_address FROM users"
                    curs.execute(sss)
                    adres = curs.fetchone()
                    url = f'https://www.blockchain.com/btc/address/{adres[0]}'
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'}
                    Response = requests.get(url, headers=headers)
                    wallet = BeautifulSoup(Response.content, 'html.parser')
                    convert = wallet.findAll("span", {"class": "sc-16b9dsl-1", "class": "ZwupP", "class": "u3ufsr-0","class": "eQTRKC"})
                    rx = convert[6].text
                    xx = rx.rstrip('BTC')
                    if amount + 0.00002000 <= float(xx):
                        try:
                            wif_key = bit.PrivateKey(wif=wif)
                            tx_hash = wif_key.create_transaction([(where, float(amount), 'btc')], fee=fee, absolute_fee=True)
                            url = 'https://blockchain.info/pushtx'
                            x = requests.post(url, data={'tx': tx_hash})
                            result = x.text
                            self.conf.setText(result)
                        except Exception:
                            self.not_2.setText('An error occurred while executing a transaction')
                    else:
                        self.notenou.setText('Not enought coins')
            elif self.priorityfee.isChecked():
                fee=20000
                where = self.sendto.text()
                # wifstr = str(wif, encoding='utf-8')
                if len(where) == 0:
                    self.fielderror.setText("You have not filled out this field")
                else:
                    amount = self.amountbtc.value()
                    sss = "SELECT btc_address FROM users"
                    curs.execute(sss)
                    adres = curs.fetchone()
                    url = f'https://www.blockchain.com/btc/address/{adres[0]}'
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'}
                    Response = requests.get(url, headers=headers)
                    wallet = BeautifulSoup(Response.content, 'html.parser')
                    convert = wallet.findAll("span", {"class": "sc-16b9dsl-1", "class": "ZwupP", "class": "u3ufsr-0","class": "eQTRKC"})
                    rx = convert[6].text
                    xx = rx.rstrip('BTC')
                    if amount + 4000 <= float(xx) / 100000000:
                        try:
                            wif_key = bit.PrivateKey(wif=wif)
                            tx_hash = wif_key.create_transaction([(where, float(amount), 'btc')], fee=fee, absolute_fee=True)
                            url = 'https://blockchain.info/pushtx'
                            x = requests.post(url, data={'tx': tx_hash})
                            result = x.text
                            self.conf.setText(result)
                        except Exception:
                            self.not_2.setText('An error occurred while executing a transaction')
                    else:
                        self.notenou.setText('Not enought coins')
            else:
                self.selfees.setText('Select fees')
        except ValueError:
            self.notenou.setText('Amount entered incorrectly')

    def walletent(self):
        wallets = Wallets()
        widget.addWidget(wallets)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def profilee(self):
        fillprofile = Profile()
        widget.addWidget(fillprofile)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def loginout(self):
        Log = LoginScreen()
        widget.addWidget(Log)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def addressfrom(self):
        db = sqlite3.connect("wallet.db")
        curs = db.cursor()
        curs.execute("SELECT btc_address FROM users")
        adr = curs.fetchone()
        self.btcaddress.setText(str(adr[0]))

    def receivee(self):
        rec = receivebtc()
        widget.addWidget(rec)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def settinges(self):
        set = settingss()
        widget.addWidget(set)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class settingss(QDialog):
    def __init__(self):
        super(settingss, self).__init__()
        loadUi("GUI/settings.ui", self)
        self.logout.clicked.connect(self.loginout)
        self.home.clicked.connect(self.profilee)
        self.receive_2.clicked.connect(self.receivee)
        self.walletbutton.clicked.connect(self.walletent)
        self.sendd.clicked.connect(self.sendbtc)
        self.changepass.clicked.connect(self.chng)
        self.deletewallet.clicked.connect(self.sure)

    def chng(self):
        new_pass = self.newpass.text()
        repl_pass = self.newpass2.text()
        if new_pass != repl_pass:
            self.er.setText("Password does not match")
        else:
            if len(new_pass) == 0:
                self.field.setText("To change password, you need to fill in all the fields")
            elif len(new_pass) < 8:
                self.er.setText('Minimum 8 charsets')
            else:
                db = sqlite3.connect("wallet.db")
                curs = db.cursor()
                curs.execute(f"UPDATE users SET Password = '{new_pass}'")
                db.commit()
                self.changed.setText('Changed!')
    def sure(self):
        sures = DeleteWallet()
        widget.addWidget(sures)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def walletent(self):
        wallets = Wallets()
        widget.addWidget(wallets)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def profilee(self):
        fillprofile = Profile()
        widget.addWidget(fillprofile)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def loginout(self):
        Log = LoginScreen()
        widget.addWidget(Log)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def receivee(self):
        rec = receivebtc()
        widget.addWidget(rec)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def sendbtc(self):
        sends = sending()
        widget.addWidget(sends)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class Wallets(QDialog):
    def __init__(self):
        super(Wallets, self).__init__()
        loadUi("GUI/wallet.ui", self)
        self.balanceuser()
        self.logout.clicked.connect(self.loginout)
        self.home.clicked.connect(self.profilee)
        self.receive_2.clicked.connect(self.receivee)
        self.receive_3.clicked.connect(self.receivee)
        self.sendd.clicked.connect(self.sendbtc)
        self.settings.clicked.connect(self.settinges)

    def settinges(self):
        set = settingss()
        widget.addWidget(set)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def balanceuser(self):
        try:
            db = sqlite3.connect("wallet.db")
            curs = db.cursor()
            sss = "SELECT btc_address FROM users"
            curs.execute(sss)
            adres = curs.fetchone()
            url = f'https://www.blockchain.com/btc/address/{adres[0]}'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'}
            Response = requests.get(url, headers=headers)
            wallet = BeautifulSoup(Response.content, 'html.parser')
            convert = wallet.findAll("span", {"class": "sc-16b9dsl-1", "class": "ZwupP", "class": "u3ufsr-0","class": "eQTRKC"})
            rx = convert[6].text
            TS = convert[5].text
            TR = convert[4].text
            xx = rx.rstrip('BTC')
            self.balance.setText(str(xx))
            response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
            data = response.json()
            x = data["bpi"]["USD"]["rate_float"]
            us = (x * float(xx))
            self.totalrec.setText(str(TR))
            self.totalsend.setText(str(TS))
            self.balance_usd.setText(str(float(us)))
        except:
            self.balance.setText(str('Loading...'))
            self.balance_usd.setText(str('---'))

    def profilee(self):
        fillprofile = Profile()
        widget.addWidget(fillprofile)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def loginout(self):
        Log = LoginScreen()
        widget.addWidget(Log)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def receivee(self):
        rec = receivebtc()
        widget.addWidget(rec)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def sendbtc(self):
        sends = sending()
        widget.addWidget(sends)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class DeleteWallet(QDialog):
    def __init__(self):
        super(DeleteWallet, self).__init__()
        loadUi("GUI/sure.ui",self)
        self.YES.clicked.connect(self.YESs)
        self.NO.clicked.connect(self.NOo)

    def YESs(self):
        db = sqlite3.connect("wallet.db")
        curs = db.cursor()
        curs.execute("DROP TABLE users ")
        Reg = RegScreen()
        widget.addWidget(Reg)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def NOo(self):
        set = settingss()
        widget.addWidget(set)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class RegScreen(QDialog):
    def __init__(self):
        super(RegScreen, self).__init__()
        loadUi("GUI/reg.ui",self)
        self.loginperehod.clicked.connect(self.gotoLogin)
        self.signupreg.clicked.connect(self.registrationfunction)

    def gotoLogin(self):
        Log = LoginScreen()
        widget.addWidget(Log)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def registrationfunction(self):
        password_reg = self.passwordreg.text()
        repl_password = self.relacepasswordreg.text()
        if repl_password != password_reg:
            self.errorreg1_2.setText("Password does not match")
        else:
            if len(password_reg) == 0:
                self.errorreg1.setText("To register, you need to fill in all the fields")
            elif len(password_reg) < 8:
                self.passerror.setText('Password cannot be less than 8 characters')
            else:
                db = sqlite3.connect('wallet.db')
                curs = db.cursor()

                curs.execute('''CREATE TABLE IF NOT EXISTS users (
                                            Password TEXT,
                                            balance INTEGER,
                                            btc_address,
                                            wif TEXT,
                                            btc_send TEXT
                                            )''')

                db.commit()
                curs.execute("SELECT Password FROM users")
                if curs.fetchone() is None:
                    index = 0
                    seed = ''
                    master_key = wallet.HDPrivateKey.master_key_from_mnemonic(seed)
                    root_keys = wallet.HDKey.from_path(master_key, "m/44'/0'/0'/0")[-1].public_key.to_b58check()
                    xpublic_key = (root_keys)
                    address = Wallet.deserialize(xpublic_key, network='BTC').get_child(index,is_prime=False).to_address()
                    rootkeys_wif = wallet.HDKey.from_path(master_key, f"m/44'/0'/0'/0/{index}")[-1]
                    xprivatekey = rootkeys_wif.to_b58check()
                    wif = Wallet.deserialize(xprivatekey, network='BTC').export_to_wif()
                    curs.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (password_reg, 0, address, wif, 0))
                    img = qrcode.make(address)
                    img.save('GUI/qr.png')
                    db.commit()
                    self.successreg.setText("You have successfully registered!")
                else:
                    error = QMessageBox()
                    error.setWindowTitle('Big request to create an account')
                    error.setText('Sorry, you cannot create another account.')
                    error.setIcon(QMessageBox.Warning)
                    error.setDefaultButton(QMessageBox.Ok)
                    error.exec_()
                    exit()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    welcome = LoginScreen()
    widget = QtWidgets.QStackedWidget()
    widget.setWindowTitle('Blockatom V.1')
    widget.setWindowIcon(QIcon('images/logo.png'))
    widget.addWidget(welcome)
    widget.show()
    sys.exit(app.exec_())

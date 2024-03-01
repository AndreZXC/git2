from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.Qt import QIntValidator, QTableView
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
import sqlite3
import sys


class Coffe(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.loadtable()
        self.addcoffee.clicked.connect(self.add)
        self.table.doubleClicked.connect(self.change)

    def loadtable(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('coffee.sqlite')
        db.open()

        model = QSqlTableModel(self, db)
        model.setTable('Coffee')
        model.select()

        self.table.setModel(model)

    def add(self):
        self.form = AddCoffee(self)
        self.form.show()

    def change(self):
        index = self.table.currentIndex().row()
        self.form = EditCoffee(self, index)
        self.form.show()



class AddCoffee(QWidget):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.price.setValidator(QIntValidator())
        self.volume.setValidator(QIntValidator())
        self.pushButton.clicked.connect(self.add)
        self.con = sqlite3.connect('coffee.sqlite')
        self.parent = parent

    def add(self):
        cur = self.con.cursor()
        gr = "yes" if self.grains.checkState() else "no"
        exc = ('INSERT INTO Coffee(name,"degree of roasting",taste,"in grains?",price,volume) '
               'VALUES (?,?,?,?,?,?)')
        if self.price.text():
            if self.volume.text():
                cur.execute(exc, (self.name.text(), self.degree.text(), self.taste.text(), gr,
                                  int(self.price.text()), int(self.volume.text())))
                self.con.commit()
                self.close()
            else:
                self.pushButton.setText('Укажите объём')
        else:
            self.pushButton.setText('Укажите цену')

    def closeEvent(self, event):
        self.parent.loadtable()


class EditCoffee(QWidget):
    def __init__(self, parent, row):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.price.setValidator(QIntValidator())
        self.volume.setValidator(QIntValidator())
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()
        row += 1
        res = self.cur.execute('SELECT * FROM Coffee WHERE id=?', (row,)).fetchone()
        self.row = row
        self.name.setText(res[1])
        self.degree.setText(res[2])
        self.taste.setText(res[3])
        self.grains.setCheckState(res[4] == 'yes')
        self.price.setText(str(res[5]))
        self.volume.setText(str(res[6]))
        self.pushButton.clicked.connect(self.edit)
        self.parent = parent

    def edit(self):
        gr = "yes" if self.grains.checkState() else "no"
        exc = ('UPDATE Coffee SET '
               'name = ?, '
               '"degree of roasting" = ?, '
               'taste = ?, '
               '"in grains?" = ?, '
               'price = ?, '
               'volume = ? '
               'WHERE id = ?')
        if self.price.text():
            if self.volume.text():
                self.cur.execute(exc, (self.name.text(), self.degree.text(), self.taste.text(), gr,
                                       int(self.price.text()), int(self.volume.text()), self.row))
                self.con.commit()
                self.close()
            else:
                self.pushButton.setText('Укажите объём')
        else:
            self.pushButton.setText('Укажите цену')

    def closeEvent(self, event):
        self.parent.loadtable()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffe()
    ex.show()
    sys.exit(app.exec())
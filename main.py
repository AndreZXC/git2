from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
import sys


class Coffe(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.loadtable()

    def loadtable(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('coffee.sqlite')
        db.open()

        model = QSqlTableModel(self, db)
        model.setTable('Coffee')
        model.select()

        self.table.setModel(model)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffe()
    ex.show()
    sys.exit(app.exec())
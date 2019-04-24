import sys
import csv
import os
from itertools import cycle
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class DragTable(QTableWidget):
    def __init__(self, int, int_, name, parent):
        super().__init__(int, int_, parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setColumnWidth(0,500)
        self.verticalHeader().setDefaultSectionSize(31)
        self.name = name

    def dragEnterEvent(self,e):
        e.accept()

    def dragMoveEvent(self, e):
        e.accept()    

    def dropEvent(self, e):
        sw = e.source()
        dw = e.pos()

        if e.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            if sw.item(sw.currentRow(),0):
                self.setItem(self.indexAt(dw).row(), 0, QTableWidgetItem(sw.item(sw.currentRow(),0).text()))
                sw.setItem(sw.currentRow(), 0, QTableWidgetItem(''))
        else:
            self.setItem(self.indexAt(dw).row(), 0, QTableWidgetItem(e.mimeData().text()))
        
class MyLabel(QWidget):
    def __init__(self, x, y, text, parent):
        super().__init__(parent)       
        self.x = x
        self.y = y
        self.text = text

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.begin(self)
        painter.setPen(Qt.black)
        self.setGeometry(self.x,self.y,100,100)
        painter.translate(20,70)
        painter.rotate(-90)       
        painter.drawText(0, 0, self.text)
        painter.end()

class Fenster(QWidget):
    def __init__(self):
        super().__init__()
        self.init_fenster()

    def init_fenster(self):

        dirname = os.getcwd()
        self.csvfilename = os.path.join(dirname, 'tables.csv')

        self.setGeometry(50,50,1050,590)

        self.label_info = QLabel(self)
        self.label_info.setText('MyIke V0.1')
        self.label_info.resize(100,20)
        self.label_info.move(10,10)

        self.label_error = QLabel(self)
        self.label_error.setText('')
                        
        label_wichtig = MyLabel(0,145,'Wichtig',self)
        label_unwichtig = MyLabel(0,415,'Nicht Wichtig',self)

        label_dringend = QLabel(self)
        label_dringend.setText('Dringend')
        label_dringend.move(290,20)

        label_ndringend = QLabel(self)
        label_ndringend.setText('Nicht Dringend')
        label_ndringend.move(790,20)

        self.tb = DragTable(8,1,'tb',self)
        self.tb.setAcceptDrops(True)
        self.tb.setDragEnabled(True)
        self.tb.move(50,50)
        self.tb.resize(500,270)
        item = QTableWidgetItem('Sofort selbst erledigen')
        item.setBackground(QColor(0, 255, 0))
        self.tb.setHorizontalHeaderItem(0,item)

        self.tb2 = DragTable(8,1,'tb2',self)
        self.tb2.setAcceptDrops(True)
        self.tb2.move(50,320)
        self.tb2.resize(500,270)
        item = QTableWidgetItem('Delegieren')
        item.setBackground(QColor(255, 200, 100))
        self.tb2.setHorizontalHeaderItem(0,item)     

        self.tb3 = DragTable(8,1,'tb3',self)
        self.tb3.setAcceptDrops(True)
        self.tb3.move(550,50)
        self.tb3.resize(500,270)
        item = QTableWidgetItem('Einplanen')
        item.setBackground(QColor(0, 100, 255))
        self.tb3.setHorizontalHeaderItem(0,item)         

        self.tb4 = DragTable(8,1,'tb4',self)
        self.tb4.setAcceptDrops(True)
        self.tb4.move(550,320)
        self.tb4.resize(500,270)
        item = QTableWidgetItem('Papierkorb')
        item.setBackground(QColor(255, 0, 0))
        self.tb4.setHorizontalHeaderItem(0,item)

        self.deserialize(self.csvfilename)      
        self.show()

    def closeEvent(self, event):
        self.serialize(self.csvfilename)
    
    def serialize(self, csvfile):
        try:
            with open(csvfile, mode='w', newline='') as csvDataFile:
                csv_writer = csv.writer(csvDataFile, delimiter=';')
                for j in [self.tb, self.tb2, self.tb3, self.tb4]:
                    for i in range(0,7):
                        if j.item(i,0):
                            if j.item(i,0).text():
                                csv_writer.writerow([j.item(i, 0).text()])
                    csv_writer.writerow(['-**-'])
        except:
            self.label_error.setText('Fehler CSV speichern')
            self.label_error.resize(100,20)
            self.label_error.move(10,30)
 
    def deserialize(self, csvfile):
        try:
            with open(self.csvfilename) as csvDataFile:
                csvReader = csv.reader(csvDataFile, delimiter=';')
                tab_row = 0
                ltable = [self.tb, self.tb2, self.tb3, self.tb4]
                ctable = cycle(ltable)
                table = next(ctable)
                for row in csvReader:
                    if row[0] == '-**-':
                        table = next(ctable)
                        tab_row = 0
                        continue

                    table.setItem(tab_row, 0, QTableWidgetItem(row[0]))
                    tab_row+=1
        except:
            self.label_error.setText('Fehler CSV laden')
            self.label_error.resize(100,20)
            self.label_error.move(10,30)

app = QApplication(sys.argv)
app.setStyle(QStyleFactory.create('Fusion'))
w = Fenster()
w.setWindowTitle("MyIke")
sys.exit(app.exec())
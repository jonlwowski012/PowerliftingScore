import sys
import csv
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
from pl_form import Ui_MainWindow
 
class MyDialog(QtGui.QMainWindow):
	def __init__(self, filename, parent=None):
		QtGui.QWidget.__init__(self, parent)

		### Store CSV into Table
		self.filename = filename
		self.model = QtGui.QStandardItemModel(self)

		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
	
		self.ui.LoadDataButton.clicked.connect(self.LoadDataButton)
		self.ui.GoodButton.clicked.connect(self.GoodButton)
		self.ui.BadButton.clicked.connect(self.BadButton)
		self.connect(self.ui.LiftSelected, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.LiftSelected)
		self.connect(self.ui.FlightSelected, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.FlightSelected)
		self.connect(self.ui.tableWidget, QtCore.SIGNAL("cellClicked(int,int)"), self.CellClicked)
	def CellClicked(self,row,col):
		if col == 1:
			self.CurrentLifter = row-1
			self.next_lifter()
	def FlightSelected(self):
		flight_selected = self.ui.FlightSelected.currentText()
		for i in range(self.ui.tableWidget.rowCount()):
			if self.ui.tableWidget.item(i,0).text().toUpper()!= flight_selected:
				self.ui.tableWidget.setRowHidden(i, True)
			else:
				self.ui.tableWidget.setRowHidden(i, False)
	def LiftSelected(self):
		lift_selected = self.ui.LiftSelected.currentText()
		if lift_selected == "Squat 1":
			self.rack_index = 7
			self.lift_index = 8
			self.SortTable(8)
		elif lift_selected == "Squat 2":
			self.rack_index = 7
			self.lift_index = 9
			self.SortTable(9)
		elif lift_selected == "Squat 3":
			self.rack_index = 7
			self.lift_index = 10
			self.SortTable(10)
		elif lift_selected == "Bench 1":
			self.rack_index = 12
			self.lift_index = 13
			self.SortTable(13)
		elif lift_selected == "Bench 2":
			self.rack_index = 12
			self.lift_index = 14
			self.SortTable(14)
		elif lift_selected == "Bench 3":
			self.rack_index = 12
			self.lift_index = 15
			self.SortTable(15)
		elif lift_selected == "Deadlift 1":
			self.lift_index = 18
			self.SortTable(18)
		elif lift_selected == "Deadlift 2":
			self.lift_index = 19
			self.SortTable(19)
		elif lift_selected == "Deadlift 3":
			self.lift_index = 20
			self.SortTable(20)
		self.CurrentLifter = 0
		self.ui.LifterNameLabel.setText(self.ui.tableWidget.item(self.CurrentLifter,1).text())
		self.ui.RackLabel.setText("Rack " + self.ui.tableWidget.item(self.CurrentLifter,self.rack_index).text())
	def loadCsv(self, fileName):
		#try:
			with open(fileName, "rb") as fileInput:
				for row in csv.reader(fileInput):
					if row[0].lower() != 'flt':  
						currentRowCount = self.ui.tableWidget.rowCount()  
						self.ui.tableWidget.insertRow(currentRowCount)
						col_count = 0
						for index, element in enumerate(row):
							while col_count in (9,10,11,14,15,16,17,19,20,21,22):
								self.ui.tableWidget.setItem(currentRowCount , col_count, QtGui.QTableWidgetItem("0"))
								col_count += 1
							for i in range(19,23):
								self.ui.tableWidget.setItem(currentRowCount , i, QtGui.QTableWidgetItem("0"))
								
							self.ui.tableWidget.setItem(currentRowCount , col_count, QtGui.QTableWidgetItem(element))
							col_count += 1

		#except: 
			#print "Please store data as data.csv"

	def LoadDataButton(self):
    		self.loadCsv(self.filename)
		for r in range(self.ui.tableWidget.rowCount() ):
				for c in range(self.ui.tableWidget.columnCount()):
					if c == 1:
				    		self.ui.tableWidget.item(r,c).setFlags(QtCore.Qt.ItemIsSelectable)
						self.ui.tableWidget.item(r,c).setForeground(QtGui.QColor(0,0,0))
		self.SortTable(8)
		self.CurrentLifter = 0
		self.lift_index = 8
		self.rack_index = 7
		self.ui.LifterNameLabel.setText(self.ui.tableWidget.item(self.CurrentLifter,1).text())
		self.ui.Weight_kg.setText(self.ui.tableWidget.item(self.CurrentLifter,self.lift_index).text()+"kg")
		self.ui.Weight_lb.setText(str(int(round(int(self.ui.tableWidget.item(self.CurrentLifter,self.lift_index).text())*2.204)))+"lb")
		self.ui.RackLabel.setText("Rack " + self.ui.tableWidget.item(self.CurrentLifter,self.rack_index).text())
		self.calculateLoading(int(self.ui.tableWidget.item(self.CurrentLifter,self.lift_index).text()))

	def GoodButton(self):
		self.ui.tableWidget.item(self.CurrentLifter,self.lift_index).setBackground(QtGui.QColor(0,255,0))
		self.next_lifter()
		self.bestSquat()
		self.bestBench()
		self.bestDeadlift()
		self.calculateTotal()
		self.calculatesubTotal()

	def BadButton(self):
		self.ui.tableWidget.item(self.CurrentLifter,self.lift_index).setBackground(QtGui.QColor(255,0,0))
		self.next_lifter()
		self.bestSquat()
		self.bestBench()
		self.bestDeadlift()
		self.calculateTotal()
		self.calculatesubTotal()

	def SortTable(self, index):
		self.ui.tableWidget.setSortingEnabled(True)
		self.ui.tableWidget.sortItems(index,Qt.AscendingOrder)
		self.ui.tableWidget.setSortingEnabled(False)
	def next_lifter(self):
		self.CurrentLifter = (self.CurrentLifter + 1) % self.ui.tableWidget.rowCount()
		self.ui.LifterNameLabel.setText(self.ui.tableWidget.item(self.CurrentLifter,1).text())
		self.ui.Weight_kg.setText(self.ui.tableWidget.item(self.CurrentLifter,self.lift_index).text()+"kg")
		self.ui.Weight_lb.setText(str(int(round(int(self.ui.tableWidget.item(self.CurrentLifter,self.lift_index).text())*2.204)))+"lb")
		self.ui.RackLabel.setText("Rack " + self.ui.tableWidget.item(self.CurrentLifter,self.rack_index).text())
		self.calculateLoading(int(self.ui.tableWidget.item(self.CurrentLifter,self.lift_index).text()))
	def bestSquat(self):
		for i in range(self.ui.tableWidget.rowCount()):
			if self.ui.tableWidget.item(i,10).background().color().green() > 100:
				self.ui.tableWidget.setItem(i,11,QtGui.QTableWidgetItem(self.ui.tableWidget.item(i,10)))
			elif self.ui.tableWidget.item(i,9).background().color().green() > 100:
				self.ui.tableWidget.setItem(i,11,QtGui.QTableWidgetItem(self.ui.tableWidget.item(i,9)))
			elif self.ui.tableWidget.item(i,8).background().color().green() > 100:
				self.ui.tableWidget.setItem(i,11,QtGui.QTableWidgetItem(self.ui.tableWidget.item(i,8)))
			else:
				self.ui.tableWidget.setItem(i,11,QtGui.QTableWidgetItem("0"))
	def bestBench(self):
		for i in range(self.ui.tableWidget.rowCount()):
			if self.ui.tableWidget.item(i,15).background().color().green() > 100:
				self.ui.tableWidget.setItem(i,16,QtGui.QTableWidgetItem(self.ui.tableWidget.item(i,15)))
			elif self.ui.tableWidget.item(i,14).background().color().green() > 100:
				self.ui.tableWidget.setItem(i,16,QtGui.QTableWidgetItem(self.ui.tableWidget.item(i,14)))
			elif self.ui.tableWidget.item(i,13).background().color().green() > 100:
				self.ui.tableWidget.setItem(i,16,QtGui.QTableWidgetItem(self.ui.tableWidget.item(i,13)))
			else:
				self.ui.tableWidget.setItem(i,16,QtGui.QTableWidgetItem("0"))

	def bestDeadlift(self):
		for i in range(self.ui.tableWidget.rowCount()):
			if self.ui.tableWidget.item(i,20).background().color().green() > 100:
				self.ui.tableWidget.setItem(i,21,QtGui.QTableWidgetItem(self.ui.tableWidget.item(i,20)))
			elif self.ui.tableWidget.item(i,19).background().color().green() > 100:
				self.ui.tableWidget.setItem(i,21,QtGui.QTableWidgetItem(self.ui.tableWidget.item(i,19)))
			elif self.ui.tableWidget.item(i,18).background().color().green() > 100:
				self.ui.tableWidget.setItem(i,21,QtGui.QTableWidgetItem(self.ui.tableWidget.item(i,18)))
			else:
				self.ui.tableWidget.setItem(i,21,QtGui.QTableWidgetItem("0"))

	def calculateTotal(self):
		for i in range(self.ui.tableWidget.rowCount()):
			sum = float(self.ui.tableWidget.item(i,21).text()) + float(self.ui.tableWidget.item(i,16).text()) + float(self.ui.tableWidget.item(i,11).text())
			self.ui.tableWidget.setItem(i,22,QtGui.QTableWidgetItem(str(sum)))
	def calculatesubTotal(self):
		for i in range(self.ui.tableWidget.rowCount()):
			sum = float(self.ui.tableWidget.item(i,16).text()) + float(self.ui.tableWidget.item(i,11).text())
			self.ui.tableWidget.setItem(i,17,QtGui.QTableWidgetItem(str(sum)))

	def calculateLoading(self, weight):
		weight -= 25
		p25kg = 0
		p20kg = 0
		p15kg = 0
		p10kg = 0
		p5kg = 0
		p2kg = 0
		p1kg = 0
		while(weight-50 >= 0):
			p25kg += 1
			weight -= 50 
		while(weight-40 >= 0):
			p20kg += 1
			weight -= 40
		while(weight-30 >= 0):
			p15kg += 1
			weight -= 30
		while(weight-20 >= 0):
			p10kg += 1
			weight -= 20
		while(weight-10 >= 0):
			p5kg += 1
			weight -= 10
		while(weight-5 >= 0):
			p2kg += 1
			weight -= 5
		while(weight-2.5 >= 0):
			p1kg += 1
			weight -= 2.5
		self.ui.kg25.setText("25kg: " + str(int(p25kg)))
		self.ui.kg20.setText("20kg: " + str(int(p20kg)))
		self.ui.kg15.setText("15kg: " + str(int(p15kg)))
		self.ui.kg10.setText("10kg: " + str(int(p10kg)))
		self.ui.kg5.setText("5kg: " + str(int(p5kg)))
		self.ui.kg2.setText("2.5kg: " + str(int(p2kg)))
		self.ui.kg1.setText("1.25kg: " + str(int(p1kg)))
 
if __name__ == "__main__":
        app = QtGui.QApplication(sys.argv)
        myapp = MyDialog("data.csv")
        myapp.show()
        sys.exit(app.exec_())
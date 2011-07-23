#!/usr/bin/env python
#
#    Football Match Result Database (FMRD)
#    Desktop-based data entry tool
#
#    Contains classes that implement entry forms to administrative tables of FMRD.
#    These tables are pre-loaded when the database is initially set up, so they do not 
#    need to be changed by the user.  With exception of About window, these 
#    modules would be incorporated into an administration version of the tool.
# 
#    Copyright (C) 2010-2011, Howard Hamilton
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from FmrdAdmin import *
from FmrdLib import Constants
from FmrdLib.CustomDelegates import *

# Class: AboutDlg
# Inherits: Ui_AboutDlg (ui_aboutwindow)
#
# Displays About box.  Just a simple dialog window.
class AboutDlg(QDialog, ui_aboutwindow.Ui_AboutDlg):
    
    def __init__(self, parent=None):
        super(AboutDlg, self).__init__(parent)
        self.setupUi(self)
        
        # configure signal/slot
        QObject.connect(self.pushButton, SIGNAL("clicked()"), self, SLOT("close()"))

# Class: cardSetupDlg
# Inherits: Ui_cardSetupDlg (ui_cardsetup)
#
# Implements user interface to Disciplinary Card table.
class cardSetupDlg(QDialog, ui_cardsetup.Ui_cardSetupDlg):
 
    FIRST,  PREV,  NEXT,  LAST = range(4)
    ID,  DESC = range(2)
    
    def __init__(self, parent=None):
        super(cardSetupDlg, self).__init__(parent)
        self.setupUi(self)
        
        # define model
        # underlying database model
        self.model = QSqlTableModel(self)
        self.model.setTable("tbl_cards")
        self.model.setSort(cardSetupDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.cardID_display, cardSetupDlg.ID)
        self.mapper.addMapping(self.cardtypeEdit, cardSetupDlg.DESC)
        self.mapper.toFirst()
        
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)        
        
        # configure signal/slot
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(cardSetupDlg.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(cardSetupDlg.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(cardSetupDlg.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(cardSetupDlg.LAST))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)

    # accept: Submit changes to database, and then close window
    def accept(self):
        self.mapper.submit()
        QDialog.accept(self)
    
    # saveRecord: Submit changes to database,
    #                     advance to next record 
    #                     apply conditions if at first/last record
    def saveRecord(self, where):
        row = self.mapper.currentIndex()
        self.mapper.submit()
        if where == cardSetupDlg.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == cardSetupDlg.PREV:
            if row <= 1:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
                row = 0
            else:
                if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)                    
                row -= 1
        elif where == cardSetupDlg.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row >= self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
                row = self.model.rowCount() - 1
        elif where == cardSetupDlg.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)
        
    # addRecord: add new record at end of entry list
    #                    set focus to edit line    
    def addRecord(self):
        
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            self.mapper.submit()
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(card_id) FROM tbl_cards"))
        if query.next():
            maxCardID= query.value(0).toInt()[0]
            if not maxCardID:
                card_id = Constants.MinCardID
            else:
                self.mapper.submit()
                card_id = QString()
                card_id.setNum(maxCardID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to cardID field
        self.cardID_display.setText(card_id)
        
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)        
        self.cardtypeEdit.setFocus()
    
    # deleteRecord: delete record from database
    #                        ask user to confirm deletion
    def deleteRecord(self):
        if QMessageBox.question(self, QString("Delete Record"), 
                                QString("Delete current record?"), 
                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
            return
        row = self.mapper.currentIndex()
        self.model.removeRow(row)
        self.model.submitAll()
        if row + 1 >= self.model.rowCount():
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row) 
        
# Class: foulSetupDlg
# Inherits: Ui_foulSetupDlg (ui_foulsetup)
#
# Implements user interface to Fouls table.
class foulSetupDlg(QDialog, ui_foulsetup.Ui_foulSetupDlg):

    FIRST,  PREV,  NEXT,  LAST = range(4)
    ID,  DESC = range(2)
 
    def __init__(self, parent=None):
        super(foulSetupDlg, self).__init__(parent)
        self.setupUi(self)
 
        # define model
        # underlying database model
        self.model = QSqlTableModel(self)
        self.model.setTable("tbl_fouls")
        self.model.setSort(foulSetupDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.foulID_display, foulSetupDlg.ID)
        self.mapper.addMapping(self.foulDescEdit, foulSetupDlg.DESC)
        self.mapper.toFirst()
        
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)
        
        # configure signal/slot
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(foulSetupDlg.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(foulSetupDlg.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(foulSetupDlg.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(foulSetupDlg.LAST))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)

    # accept: Submit changes to database, and then close window
    def accept(self):
        self.mapper.submit()
        QDialog.accept(self)
    
    # saveRecord: Submit changes to database,
    #                     advance to next record 
    #                     apply conditions if at first/last record
    def saveRecord(self, where):
        row = self.mapper.currentIndex()
        self.mapper.submit()
        if where == foulSetupDlg.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == foulSetupDlg.PREV:
            if row <= 1:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
                row = 0
            else:
                if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)                    
                row -= 1
        elif where == foulSetupDlg.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row >= self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
                row = self.model.rowCount() - 1
        elif where == foulSetupDlg.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)
        
    # addRecord: add new record at end of entry list
    #                    set focus to edit line    
    def addRecord(self):
        
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            self.mapper.submit()
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(foul_id) FROM tbl_fouls"))
        if query.next():
            maxFoulID= query.value(0).toInt()[0]
            if not maxFoulID:
                foul_id = Constants.MinFoulID
            else:
                self.mapper.submit()
                foul_id = QString()
                foul_id.setNum(maxFoulID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to foulID field
        self.foulID_display.setText(foul_id)
        
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)
        self.foulDescEdit.setFocus()
    
    # deleteRecord: delete record from database
    #                        ask user to confirm deletion
    def deleteRecord(self):
        if QMessageBox.question(self, QString("Delete Record"), 
                                QString("Delete current record?"), 
                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
            return
        row = self.mapper.currentIndex()
        self.model.removeRow(row)
        self.model.submitAll()
        if row + 1 >= self.model.rowCount():
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)  
        
# Class: penSetupDlg
# Inherits: Ui_penSetupDlg (ui_penoutcomesetup)
# 
# Implements user interface to Penalty Outcomes table.
class penSetupDlg(QDialog, ui_penoutcomesetup.Ui_penSetupDlg):
 
    FIRST,  PREV,  NEXT,  LAST = range(4)
    ID,  DESC = range(2)
 
    def __init__(self, parent=None):
        super(penSetupDlg, self).__init__(parent)
        self.setupUi(self)
        
        # define model
        # underlying database model
        self.model = QSqlTableModel(self)
        self.model.setTable("tbl_penoutcomes")
        self.model.setSort(penSetupDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.penoutcomeID_display, penSetupDlg.ID)
        self.mapper.addMapping(self.penOutcomeEdit, penSetupDlg.DESC)
        self.mapper.toFirst()
        
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)
        
        # configure signal/slot
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(penSetupDlg.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(penSetupDlg.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(penSetupDlg.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(penSetupDlg.LAST))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)

    # accept: Submit changes to database, and then close window
    def accept(self):
        self.mapper.submit()
        QDialog.accept(self)
    
    # saveRecord: Submit changes to database,
    #                     advance to next record 
    #                     apply conditions if at first/last record
    def saveRecord(self, where):
        row = self.mapper.currentIndex()
        self.mapper.submit()
        if where == penSetupDlg.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == penSetupDlg.PREV:
            if row <= 1:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
                row = 0
            else:
                if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)                    
                row -= 1
        elif where == penSetupDlg.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row >= self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
                row = self.model.rowCount() - 1
        elif where == penSetupDlg.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)
        
    # addRecord: add new record at end of entry list
    #                    set focus to edit line    
    def addRecord(self):
        
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            self.mapper.submit()
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(penoutcome_id) FROM tbl_penoutcomes"))
        if query.next():
            maxPenOutcomeID = query.value(0).toInt()[0]
            if not maxPenOutcomeID:
                outcome_id = Constants.MinPenOutcomeID
            else:
                self.mapper.submit()
                outcome_id = QString()
                outcome_id.setNum(maxPenOutcomeID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to penOutcomeID field
        self.penoutcomeID_display.setText(outcome_id)
        
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)
        self.penOutcomeEdit.setFocus()
    
    # deleteRecord: delete record from database
    #                        ask user to confirm deletion
    def deleteRecord(self):
        if QMessageBox.question(self, QString("Delete Record"), 
                                QString("Delete current record?"), 
                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
            return
        row = self.mapper.currentIndex()
        self.model.removeRow(row)
        self.model.submitAll()
        if row + 1 >= self.model.rowCount():
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)

# Class: goaleventSetupDlg
# Inherits: Ui_goaleventSetupDlg (ui_goaleventsetup)
#
# Implements user interface to Goal Events table.
class goaleventSetupDlg(QDialog, ui_goaleventsetup.Ui_goaleventSetupDlg):

    FIRST,  PREV,  NEXT,  LAST = range(4)
    ID,  DESC = range(2)
 
    def __init__(self, parent=None):
        super(goaleventSetupDlg, self).__init__(parent)
        self.setupUi(self)
        
        # define model
        # underlying database model
        self.model = QSqlTableModel(self)
        self.model.setTable("tbl_goalevents")
        self.model.setSort(goaleventSetupDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.goaleventID_display, goaleventSetupDlg.ID)
        self.mapper.addMapping(self.goaleventEdit, goaleventSetupDlg.DESC)
        self.mapper.toFirst()
        
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)
        
        # configure signal/slot
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(goaleventSetupDlg.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(goaleventSetupDlg.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(goaleventSetupDlg.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(goaleventSetupDlg.LAST))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)

    # accept: Submit changes to database, and then close window
    def accept(self):
        self.mapper.submit()
        QDialog.accept(self)
    
    # saveRecord: Submit changes to database,
    #                     advance to next record 
    #                     apply conditions if at first/last record
    def saveRecord(self, where):
        row = self.mapper.currentIndex()
        self.mapper.submit()
        if where == goaleventSetupDlg.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == goaleventSetupDlg.PREV:
            if row <= 1:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
                row = 0
            else:
                if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)                    
                row -= 1
        elif where == goaleventSetupDlg.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row >= self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
                row = self.model.rowCount() - 1
        elif where == goaleventSetupDlg.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)
        
    # addRecord: add new record at end of entry list
    #                    set focus to edit line    
    def addRecord(self):
        
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            self.mapper.submit()
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(gtetype_id) FROM tbl_goalevents"))
        if query.next():
            maxGoalEventID= query.value(0).toInt()[0]
            if not maxGoalEventID:
                event_id = Constants.MinGoalEventID
            else:
                self.mapper.submit()
                event_id = QString()
                event_id.setNum(maxGoalEventID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to GoalEventID field
        self.goaleventID_display.setText(event_id)
        
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)
        self.goaleventEdit.setFocus()
    
    # deleteRecord: delete record from database
    #                        ask user to confirm deletion
    def deleteRecord(self):
        if QMessageBox.question(self, QString("Delete Record"), 
                                QString("Delete current record?"), 
                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
            return
        row = self.mapper.currentIndex()
        self.model.removeRow(row)
        self.model.submitAll()
        if row + 1 >= self.model.rowCount():
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)

# Class: goalstrikeSetupDlg
# Inherits: Ui_goalstrikeSetupDlg (ui_goalstrikesetup)
#
# Implements user interface to Goal Strikes table.
class goalstrikeSetupDlg(QDialog, ui_goalstrikesetup.Ui_goalstrikeSetupDlg):

    FIRST,  PREV,  NEXT,  LAST = range(4)
    ID,  DESC = range(2)
 
    def __init__(self, parent=None):
        super(goalstrikeSetupDlg, self).__init__(parent)
        self.setupUi(self)
        
        # define model
        # underlying database model
        self.model = QSqlTableModel(self)
        self.model.setTable("tbl_goalstrikes")
        self.model.setSort(goalstrikeSetupDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.goalstrikeID_display, goalstrikeSetupDlg.ID)
        self.mapper.addMapping(self.goalstrikeEdit, goalstrikeSetupDlg.DESC)
        self.mapper.toFirst()
        
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)
        
        # configure signal/slot
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(goalstrikeSetupDlg.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(goalstrikeSetupDlg.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(goalstrikeSetupDlg.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(goalstrikeSetupDlg.LAST))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)

    # accept: Submit changes to database, and then close window
    def accept(self):
        self.mapper.submit()
        QDialog.accept(self)
    
    # saveRecord: Submit changes to database,
    #                     advance to next record 
    #                     apply conditions if at first/last record
    def saveRecord(self, where):
        row = self.mapper.currentIndex()
        self.mapper.submit()
        if where == goalstrikeSetupDlg.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == goalstrikeSetupDlg.PREV:
            if row <= 1:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
                row = 0
            else:
                if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)                    
                row -= 1
        elif where == goalstrikeSetupDlg.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row >= self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
                row = self.model.rowCount() - 1
        elif where == goalstrikeSetupDlg.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)
        
    # addRecord: add new record at end of entry list
    #                    set focus to edit line    
    def addRecord(self):
        
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            self.mapper.submit()
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(gtstype_id) FROM tbl_goalstrikes"))
        if query.next():
            maxGoalStrikeID= query.value(0).toInt()[0]
            if not maxGoalStrikeID:
                strike_id = Constants.MinGoalStrikeID
            else:
                self.mapper.submit()
                strike_id = QString()
                strike_id.setNum(maxGoalStrikeID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to goalStrikeID field
        self.goalstrikeID_display.setText(strike_id)
        
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)
        self.goalstrikeEdit.setFocus()
    
    # deleteRecord: delete record from database
    #                        ask user to confirm deletion
    def deleteRecord(self):
        if QMessageBox.question(self, QString("Delete Record"), 
                                QString("Delete current record?"), 
                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
            return
        row = self.mapper.currentIndex()
        self.model.removeRow(row)
        self.model.submitAll()
        if row + 1 >= self.model.rowCount():
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)
        
# Class: fieldposSetupDlg
# Inherits: Ui_fieldposSetupDlg (ui_fieldpossetup)
#
# Implements user interface to Field Position table.
class fieldposSetupDlg(QDialog, ui_fieldpossetup.Ui_fieldposSetupDlg):

    FIRST,  PREV,  NEXT,  LAST = range(4)
    ID,  DESC = range(2)
 
    def __init__(self, parent=None):
        super(fieldposSetupDlg, self).__init__(parent)
        self.setupUi(self)

        # define model
        # underlying database model
        self.model = QSqlTableModel(self)
        self.model.setTable("tbl_fieldnames")
        self.model.setSort(fieldposSetupDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.fieldposID_display, fieldposSetupDlg.ID)
        self.mapper.addMapping(self.fieldposEdit, fieldposSetupDlg.DESC)
        self.mapper.toFirst()
        
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)
        
        # configure signal/slot
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(fieldposSetupDlg.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(fieldposSetupDlg.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(fieldposSetupDlg.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(fieldposSetupDlg.LAST))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)

    # accept: Submit changes to database, and then close window
    def accept(self):
        self.mapper.submit()
        QDialog.accept(self)
    
    # saveRecord: Submit changes to database,
    #                     advance to next record 
    #                     apply conditions if at first/last record
    def saveRecord(self, where):
        row = self.mapper.currentIndex()
        self.mapper.submit()
        if where == fieldposSetupDlg.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == fieldposSetupDlg.PREV:
            if row <= 1:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
                row = 0
            else:
                if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)                    
                row -= 1
        elif where == fieldposSetupDlg.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row >= self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
                row = self.model.rowCount() - 1
        elif where == fieldposSetupDlg.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)
        
    # addRecord: add new record at end of entry list
    #                    set focus to edit line    
    def addRecord(self):
        
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            self.mapper.submit()
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(posfield_id) FROM tbl_fieldnames"))
        if query.next():
            maxFieldID= query.value(0).toInt()[0]
            if not maxFieldID:
                field_id = Constants.MinFieldID
            else:
                self.mapper.submit()
                field_id = QString()
                field_id.setNum(maxFieldID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to fieldposID field
        self.fieldposID_display.setText(field_id)
        
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)
        self.fieldposEdit.setFocus()
    
    # deleteRecord: delete record from database
    #                        ask user to confirm deletion
    def deleteRecord(self):
        if QMessageBox.question(self, QString("Delete Record"), 
                                QString("Delete current record?"), 
                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
            return
        row = self.mapper.currentIndex()
        self.model.removeRow(row)
        self.model.submitAll()
        if row + 1 >= self.model.rowCount():
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)
        
# Class: flankposSetupDlg
# Inherits: Ui_flankposSetupDlg (ui_flankpossetup)
#
# Implements user interface to Flank Position table.
class flankposSetupDlg(QDialog, ui_flankpossetup.Ui_flankposSetupDlg):

    FIRST,  PREV,  NEXT,  LAST = range(4)
    ID,  DESC = range(2)
 
    def __init__(self, parent=None):
        super(flankposSetupDlg, self).__init__(parent)
        self.setupUi(self)

        # define model
        # underlying database model
        self.model = QSqlTableModel(self)
        self.model.setTable("tbl_flanknames")
        self.model.setSort(flankposSetupDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        localDelegate = GenericDelegate(self)
        localDelegate.insertColumnDelegate(flankposSetupDlg.DESC, NullLineEditDelegate())
        self.mapper.setItemDelegate(localDelegate)        
        self.mapper.addMapping(self.flankposID_display, flankposSetupDlg.ID)
        self.mapper.addMapping(self.flankposEdit, flankposSetupDlg.DESC)
        self.mapper.toFirst()
        
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)
        
        # configure signal/slot
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(flankposSetupDlg.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(flankposSetupDlg.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(flankposSetupDlg.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(flankposSetupDlg.LAST))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)

    # accept: Submit changes to database, and then close window
    def accept(self):
        self.mapper.submit()
        QDialog.accept(self)
    
    # saveRecord: Submit changes to database,
    #                     advance to next record 
    #                     apply conditions if at first/last record
    def saveRecord(self, where):
        row = self.mapper.currentIndex()
        self.mapper.submit()
        if where == flankposSetupDlg.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == flankposSetupDlg.PREV:
            if row <= 1:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
                row = 0
            else:
                if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)                    
                row -= 1
        elif where == flankposSetupDlg.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row >= self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
                row = self.model.rowCount() - 1
        elif where == flankposSetupDlg.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)
        
    # addRecord: add new record at end of entry list
    #                    set focus to edit line    
    def addRecord(self):
        
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            self.mapper.submit()
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(posflank_id) FROM tbl_flanknames"))
        if query.next():
            maxFlankID= query.value(0).toInt()[0]
            if not maxFlankID:
                flank_id = Constants.MinFlankID
            else:
                self.mapper.submit()
                flank_id = QString()
                flank_id.setNum(maxFlankID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to flankposID field
        self.flankposID_display.setText(flank_id)
        
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)
        self.flankposEdit.setFocus()
    
    # deleteRecord: delete record from database
    #                        ask user to confirm deletion
    def deleteRecord(self):
        if QMessageBox.question(self, QString("Delete Record"), 
                                QString("Delete current record?"), 
                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
            return
        row = self.mapper.currentIndex()
        self.model.removeRow(row)
        self.model.submitAll()
        if row + 1 >= self.model.rowCount():
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)

        
# Class: posSetupDlg
# Inherits: Ui_posSetupDlg (ui_positionsetup)
# 
# Implements user interface to Position table, which links to Flank Position and Field Position tables.
class posSetupDlg(QDialog, ui_positionsetup.Ui_posSetupDlg):

    FIRST,  PREV,  NEXT,  LAST = range(4)
    POS_ID,  FIELD_ID,  FLANK_ID = range(3)    

    def __init__(self, parent=None):
        super(posSetupDlg, self).__init__(parent)
        self.setupUi(self)
        
        # define model
        # underlying database model
        self.model = QSqlRelationalTableModel(self)
        self.model.setTable("tbl_positions")
        self.model.setRelation(posSetupDlg.FIELD_ID, QSqlRelation("tbl_fieldnames", "posfield_id", "posfield_name"))
        self.model.setRelation(posSetupDlg.FLANK_ID, QSqlRelation("tbl_flanknames", "posflank_id", "posflank_name"))        
        self.model.setSort(posSetupDlg.POS_ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.setItemDelegate(QSqlRelationalDelegate(self))
        self.mapper.addMapping(self.positionID_display, posSetupDlg.POS_ID)
        # set up Field Position combobox that links to tbl_fieldnames
        fieldrelationModel = self.model.relationModel(posSetupDlg.FIELD_ID)
        self.fieldposSelect.setModel(fieldrelationModel)
        self.fieldposSelect.setModelColumn(fieldrelationModel.fieldIndex("posfield_name"))        
        self.mapper.addMapping(self.fieldposSelect, posSetupDlg.FIELD_ID)        
         # set up Flank Position combobox that links to tbl_flanknames
        flankrelationModel = self.model.relationModel(posSetupDlg.FLANK_ID)
        self.flankposSelect.setModel(flankrelationModel)
        self.flankposSelect.setModelColumn(flankrelationModel.fieldIndex("posflank_name"))
        self.mapper.addMapping(self.flankposSelect, posSetupDlg.FLANK_ID)        
        self.mapper.toFirst()         
        
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)
        
        # configure signal/slot
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(posSetupDlg.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(posSetupDlg.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(posSetupDlg.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(posSetupDlg.LAST))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)
        
    def accept(self):
        self.mapper.submit()
        QDialog.accept(self)
        
    def saveRecord(self, where):
        row = self.mapper.currentIndex()
        self.mapper.submit()
        if where == posSetupDlg.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == posSetupDlg.PREV:
            if row <= 1:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
                row = 0
            else:
                if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)                    
                row -= 1
        elif where == posSetupDlg.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row >= self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
                row = self.model.rowCount() - 1
        elif where == posSetupDlg.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)
        
    def addRecord(self):
        
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            self.mapper.submit()
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(position_id) FROM tbl_positions"))
        if query.next():
            maxPositionID = query.value(0).toInt()[0]
            if not maxPositionID:
                position_id = Constants.MinPositionID
            else:
                self.mapper.submit()
                position_id = QString()
                position_id.setNum(maxPositionID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to PositionID field
        self.positionID_display.setText(position_id)
        
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)        
        self.countryEdit.setFocus()
        self.confedSelect.setCurrentIndex(-1)
        
    def deleteRecord(self):
        if QMessageBox.question(self, QString("Delete Record"), 
                                QString("Delete current record?"), 
                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
            return
        row = self.mapper.currentIndex()
        self.model.removeRow(row)
        self.model.submitAll()
        if row + 1 >= self.model.rowCount():
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)

# Class: countrySetupDlg
# Inherits: Ui_countrySetupDlg (ui_countrysetup)
#
# Implements user interface to Country table, which links to Confederation table.
class countrySetupDlg(QDialog, ui_countrysetup.Ui_countrySetupDlg):
    
    FIRST,  PREV,  NEXT,  LAST = range(4)
    ID,  REGION_ID,  NAME = range(3)    
    
    def __init__(self, parent=None):
        super(countrySetupDlg, self).__init__(parent)
        self.setupUi(self)         
        
        # define model
        # underlying database model
        self.model = QSqlRelationalTableModel(self)
        self.model.setTable("tbl_countries")
        self.model.setRelation(countrySetupDlg.REGION_ID, QSqlRelation("tbl_confederations", "confed_id", "confed_name"))
        self.model.setSort(countrySetupDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.setItemDelegate(QSqlRelationalDelegate(self))
        self.mapper.addMapping(self.countryID_display, countrySetupDlg.ID)
        self.mapper.addMapping(self.countryEdit, countrySetupDlg.NAME)        
         # set up combobox that links to foreign table
        relationModel = self.model.relationModel(countrySetupDlg.REGION_ID)
        self.confedSelect.setModel(relationModel)
        self.confedSelect.setModelColumn(relationModel.fieldIndex("confed_name"))
        self.mapper.addMapping(self.confedSelect, countrySetupDlg.REGION_ID)        
        self.mapper.toFirst()        
       
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)

        # configure signal/slot
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(countrySetupDlg.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(countrySetupDlg.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(countrySetupDlg.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(countrySetupDlg.LAST))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)
        
    def accept(self):
        self.mapper.submit()
        QDialog.accept(self)
        
    def saveRecord(self, where):
        row = self.mapper.currentIndex()
        self.mapper.submit()
        if where == countrySetupDlg.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == countrySetupDlg.PREV:
            if row <= 1:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
                row = 0
            else:
                if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)                    
                row -= 1
        elif where == countrySetupDlg.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row >= self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
                row = self.model.rowCount() - 1
        elif where == countrySetupDlg.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)
        
    def addRecord(self):
        
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            self.mapper.submit()
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(country_id) FROM tbl_countries"))
        if query.next():
            maxCountryID= query.value(0).toInt()[0]
            if not maxCountryID:
                country_id = Constants.MinCountryID
            else:
                self.mapper.submit()
                country_id = QString()
                country_id.setNum(maxCountryID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to countryID field
        self.countryID_display.setText(country_id)
        
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)        
        self.countryEdit.setFocus()
        self.confedSelect.setCurrentIndex(-1)
        
    def deleteRecord(self):
        if QMessageBox.question(self, QString("Delete Record"), 
                                QString("Delete current record?"), 
                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
            return
        row = self.mapper.currentIndex()
        self.model.removeRow(row)
        self.model.submitAll()
        if row + 1 >= self.model.rowCount():
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)
        

# Class: confedSetupDlg
# Inherits: Ui_confedSetupDlg (ui_confederationsetup)
# 
# Implements user interface to Confederation table.
class confedSetupDlg(QDialog, ui_confederationsetup.Ui_confedSetupDlg):
    
    FIRST,  PREV,  NEXT,  LAST = range(4)
    ID,  NAME = range(2)
    
    def __init__(self, parent=None):
        super(confedSetupDlg, self).__init__(parent)
        self.setupUi(self)
        
        # define model
        # underlying database model
        self.model = QSqlTableModel(self)
        self.model.setTable("tbl_confederations")
        self.model.setSort(confedSetupDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.confedID_display, confedSetupDlg.ID)
        self.mapper.addMapping(self.confederationEdit, confedSetupDlg.NAME)
        self.mapper.toFirst()
        
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)
        
        # configure signal/slot
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(confedSetupDlg.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(confedSetupDlg.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(confedSetupDlg.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(confedSetupDlg.LAST))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)

    def accept(self):
        self.mapper.submit()
        QDialog.accept(self)
        
    def saveRecord(self, where):
        row = self.mapper.currentIndex()
        self.mapper.submit()
        if where == confedSetupDlg.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == confedSetupDlg.PREV:
            if row <= 1:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
                row = 0
            else:
                if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)                    
                row -= 1
        elif where == confedSetupDlg.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row >= self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
                row = self.model.rowCount() - 1
        elif where == confedSetupDlg.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)
        
    # addRecord: add new record at end of entry list
    #                    set focus to edit line    
    def addRecord(self):
        
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            self.mapper.submit()
        
        # move to end of table and insert new record
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(confed_id) FROM tbl_confederations"))
        if query.next():
            maxConfedID= query.value(0).toInt()[0]
            if not maxConfedID:
                confed_id = Constants.MinConfedID
            else:
                self.mapper.submit()
                confed_id = QString()
                confed_id.setNum(maxConfedID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to confedID field
        self.confedID_display.setText(confed_id)
        
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)
        self.confederationEdit.setFocus()
        
    def deleteRecord(self):
        if QMessageBox.question(self, QString("Delete Record"), 
                                QString("Delete current record?"), 
                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
            return
        row = self.mapper.currentIndex()
        self.model.removeRow(row)
        self.model.submitAll()
        if row + 1 >= self.model.rowCount():
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)

# Class: roundSetupDlg
# Inherits: Ui_roundSetupDlg (ui_roundsetup)
#
# Implements user interface to Rounds table.
class roundSetupDlg(QDialog, ui_roundsetup.Ui_roundSetupDlg):
 
    FIRST,  PREV,  NEXT,  LAST = range(4)
    ID,  DESC = range(2)
    
    def __init__(self, parent=None):
        super(roundSetupDlg, self).__init__(parent)
        self.setupUi(self)
        
        # define model
        # underlying database model
        self.model = QSqlTableModel(self)
        self.model.setTable("tbl_rounds")
        self.model.setSort(roundSetupDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.roundID_display, roundSetupDlg.ID)
        self.mapper.addMapping(self.rounddescEdit, roundSetupDlg.DESC)
        self.mapper.toFirst()
        
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)
        
        # configure signal/slot
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(roundSetupDlg.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(roundSetupDlg.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(roundSetupDlg.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(roundSetupDlg.LAST))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)
    
    # accept: Submit changes to database, and then close window
    def accept(self):
        self.mapper.submit()
        QDialog.accept(self)
    
    # saveRecord: Submit changes to database,
    #                     advance to next record 
    #                     apply conditions if at first/last record
    def saveRecord(self, where):
        row = self.mapper.currentIndex()
        self.mapper.submit()
        if where == roundSetupDlg.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == roundSetupDlg.PREV:
            if row <= 1:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
                row = 0
            else:
                if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)                    
                row -= 1
        elif where == roundSetupDlg.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row >= self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
                row = self.model.rowCount() - 1
        elif where == roundSetupDlg.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)
        
    # addRecord: add new record at end of entry list
    #                    set focus to edit line    
    def addRecord(self):
        
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            self.mapper.submit()
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(round_id) FROM tbl_rounds"))
        if query.next():
            maxRoundID = query.value(0).toInt()[0]
            if not maxRoundID:
                round_id = Constants.MinRoundID
            else:
                self.mapper.submit()
                round_id = QString()
                round_id.setNum(maxRoundID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to RoundID field
        self.roundID_display.setText(round_id)
        
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)        
        self.rounddescEdit.setFocus()
    
    # deleteRecord: delete record from database
    #                        ask user to confirm deletion
    def deleteRecord(self):
        if QMessageBox.question(self, QString("Delete Record"), 
                                QString("Delete current record?"), 
                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
            return
        row = self.mapper.currentIndex()
        self.model.removeRow(row)
        self.model.submitAll()
        if row + 1 >= self.model.rowCount():
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)    
            
# Class: wxcondSetupDlg
# Inherits: Ui_wxcondSetupDlg (ui_weathersetup)
#
# Implements user interface to Weather Conditions table.
class wxcondSetupDlg(QDialog, ui_weathersetup.Ui_wxcondSetupDlg):
 
    FIRST,  PREV,  NEXT,  LAST = range(4)
    ID,  DESC = range(2)
    
    def __init__(self, parent=None):
        super(wxcondSetupDlg, self).__init__(parent)
        self.setupUi(self)
 
        # define model
        # underlying database model
        self.model = QSqlTableModel(self)
        self.model.setTable("tbl_weather")
        self.model.setSort(wxcondSetupDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.weatherID_display, wxcondSetupDlg.ID)
        self.mapper.addMapping(self.wxcondEdit, wxcondSetupDlg.DESC)
        self.mapper.toFirst()
        
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)
        
        # configure signal/slot
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(wxcondSetupDlg.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(wxcondSetupDlg.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(wxcondSetupDlg.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(wxcondSetupDlg.LAST))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)

    # accept: Submit changes to database, and then close window
    def accept(self):
        self.mapper.submit()
        QDialog.accept(self)
    
    # saveRecord: Submit changes to database,
    #                     advance to next record 
    #                     apply conditions if at first/last record
    def saveRecord(self, where):

        row = self.mapper.currentIndex()
        self.mapper.submit()
        if where == wxcondSetupDlg.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == wxcondSetupDlg.PREV:
            if row <= 1:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
                row = 0
            else:
                if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)                    
                row -= 1
        elif where == wxcondSetupDlg.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row >= self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
                row = self.model.rowCount() - 1
        elif where == wxcondSetupDlg.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)
        
    # addRecord: add new record at end of entry list
    #                    set focus to edit line    
    def addRecord(self):
        
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            self.mapper.submit()
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(weather_id) FROM tbl_weather"))
        if query.next():
            maxWeatherID = query.value(0).toInt()[0]
            if not maxWeatherID:
                weather_id = Constants.MinWeatherID
            else:
                self.mapper.submit()
                weather_id = QString()
                weather_id.setNum(maxWeatherID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to WeatherID field
        self.weatherID_display.setText(weather_id)
        
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)
        self.wxcondEdit.setFocus()
    
    # deleteRecord: delete record from database
    #                        ask user to confirm deletion
    def deleteRecord(self):
        if QMessageBox.question(self, QString("Delete Record"), 
                                QString("Delete current record?"), 
                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
            return
        row = self.mapper.currentIndex()
        self.model.removeRow(row)
        self.model.submitAll()
        if row + 1 >= self.model.rowCount():
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row) 

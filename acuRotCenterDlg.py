from    qt import   *
import  acuIcon
import  sys

#----------------------------------------------------------------------
#
#----------------------------------------------------------------------

class AcuRotCenterDlg(QDialog):

#----------------------------------------------------------------------
#
#----------------------------------------------------------------------

    def __init__( self, parent      =       None,
                        caption     =       "Rotation Center",
                        icon        =       None ):

        QDialog.__init__(           self,          parent               )
        self.setCaption(            caption                             )
        if icon==None:
            self.setIcon(           acuIcon.getIcon('logored')          )
        else:
            self.setIcon(           acuIcon.getIcon(icon)               )

        self.parent     = parent

        self.point = (0., 0., 0.)

        #---text fields group

        inpGBox         = QFrame(               self                    )
        inpLayout       = QHBoxLayout(          inpGBox                 )

        #---make main text fields
        self.centerTextLbl  =    QLabel("Center of rotation:",  inpGBox )
        self.xLEdit         =    QLineEdit ("0.",  "",          inpGBox )
        self.yLEdit         =    QLineEdit ("0.",  "",          inpGBox )
        self.zLEdit         =    QLineEdit ("0.",  "",          inpGBox )

        #---add main text fields
        inpLayout.addStretch(        2                                  )
        inpLayout.addWidget(        self.centerTextLbl                  )
        inpLayout.addStretch(        1                                  )
        inpLayout.addSpacing(10                                         )
        inpLayout.addWidget(        self.xLEdit                         )
        inpLayout.addStretch(        1                                  )
        inpLayout.addWidget(        self.yLEdit                         )
        inpLayout.addStretch(        1                                  )
        inpLayout.addWidget(        self.zLEdit                         )
        inpLayout.addStretch(        2                                  )

        #---button group

        btnGBox         = QFrame(               self                    )
        btnLayout       = QHBoxLayout(          btnGBox                 )

        #---make main button
        self.okBtn              =    QPushButton("OK",      btnGBox     )
        self.cancelBtn          =    QPushButton("Cancel",  btnGBox     )
        self.helpBtn            =    QPushButton("Help",    btnGBox     )

        #---add main buttons
        btnLayout.addStretch(        2                                  )
        btnLayout.addWidget(        self.helpBtn                        )
        btnLayout.addStretch(        1                                  )
        btnLayout.addWidget(        self.cancelBtn                      )
        btnLayout.addStretch(        1                                  )
        btnLayout.addWidget(        self.okBtn                          )
        btnLayout.addStretch(        2                                  )

        #---Main buttons

        self.connect(               self.okBtn,
                                    SIGNAL("clicked()"),
                                    self.okClicked                      )

        self.connect(               self.cancelBtn,
                                    SIGNAL("clicked()"),
                                    self.cancelClicked                  )

        self.setWidgetInfo(          self.helpBtn,
                                     " Help "                           )
        self.setWidgetInfo(          self.okBtn,
                                     " Accept the changes "             )
        self.setWidgetInfo(          self.cancelBtn,
                                     " Ignore all changes "             )

        #---Dialog layout
        self.setModal(True)

        mainLayout  = QVBoxLayout(          self,       5,      5       )
        mainLayout.addWidget(               inpGBox                     )
        mainLayout.addSpacing(              10                          )
        mainLayout.addWidget(               btnGBox                     )

#----------------------------------------------------------------------
#
#----------------------------------------------------------------------

    def setWidgetInfo( self, wdg, tooltip):

        """Set tooltip and whatsthis for a widget.

        Arguments:
            wdg         : Add tooltip and whatsthis for this wigdet.
            tooltip     : The tooltip for widget.

        """

     	if type(wdg) == type(tuple):
	    for i in wdg:
                QToolTip.add(        i,	    tooltip                     )
	else:
            i =  wdg
            QToolTip.add(            i,	    tooltip			)

#----------------------------------------------------------------------
#
#----------------------------------------------------------------------

    def cancelClicked(self):

        self.xLEdit.setText("0.")
        self.yLEdit.setText("0.")
        self.zLEdit.setText("0.")
        self.reject()

#----------------------------------------------------------------------
#
#----------------------------------------------------------------------

    def okClicked(self):
        try:
            x = float(self.xLEdit.text())
            y = float(self.yLEdit.text())
            z = float(self.zLEdit.text())
            self.point = (x, y, z)
            self.accept()
        except:
            QMessageBox.critical(self, "Error", "Invaid input entered!")

#----------------------------------------------------------------------
#
#----------------------------------------------------------------------

    def closeEvent( self,   e ):
        self.cancelClicked(                                             )

#----------------------------------------------------------------------
#
#----------------------------------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = AcuRotCenterDlg(None,"Rotation Center" )

    mainWindow.show()
    app.connect(app, SIGNAL('lastWindowClosed()'), app, SLOT('quit()'))
    app.enter_loop()


# -*- coding: utf-8 -*-

from main import *

from someFits import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar

import matplotlib  


class mainWidget(QtWidgets.QWidget, Ui_Form):
    #If we have some layout in MainWindow, we can't inherit from QMainWindow.
    #You will got 'QLayout: Attempting to add QLayout "" to mainWindow "Form", which already has a layout'.
    def __init__(self, parent = None):
        super(mainWidget, self).__init__()
        self.setupUi(self)

        self.acceptButton.clicked.connect(self.acceptButtonClick)

        self.times_Adder.clicked.connect(self.times_AdderClick)
  
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        # self.canvas = FigureCanvas(self.figure)
  
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        # self.toolbar = NavigationToolbar(self.canvas, self)


    def acceptButtonClick(self):
        self.logBrowser.append("arg1: " + self.arg1_Inputer.text())
        self.arg1_Inputer.setText(self.arg1_Inputer.text())
        self.logBrowser.append("arg2: " + self.arg2_Inputer.text())
        self.arg2_Inputer.setText(self.arg2_Inputer.text())

        X = self.arg1_Inputer.text().split(",")
        X = map(float, X)
        Y = self.arg2_Inputer.text().split(",")
        Y = map(float, Y)        
        Output = linearFit_CAM(X, Y, 1)

        figureCanvasInstance = figureCanvas()
        figureCanvasInstance.figureCanvasPlot(X, Y, '.')        
        figureCanvasInstance.figureCanvasPlot(Output[0],Output[1])

        graphicScene = QtWidgets.QGraphicsScene()
        graphicScene.addWidget(figureCanvasInstance)
        self.graphic_Viewer.setScene(graphicScene)
        self.graphic_Viewer.show()
        self.logBrowser.append("-" * len(self.arg1_Inputer.text()))


######working on this part on 2016.12.03
#The Layout has .count(), and can be used.
#I can't find all child btn in self.scrollArea
    def times_AdderClick(self):
        times = self.times_selector.text()
        # print self.scrollAreaLayout.count()                
        try:
            print type(locals()['self.show%sButton' % times])
            print "we have this button"
        except:
            # locals()['self.show%sButton' % times] = QtWidgets.QPushButton()
            # locals()['self.show%sButton' % times].setObjectName('self.show%sButton' % times)
            # locals()['self.show%sButton' % times].setText("%s Times" % times)
            # locals()['self.show%sButton' % times].setMinimumHeight (20)
            # self.scrollAreaLayout.addWidget(locals()['self.show%sButton' % times], *(self.scrollAreaLayout.count() / 3, self.scrollAreaLayout.count() % 3))
            # locals()['self.show%sButton' % times].show()
            
            locals()['self.show%sButton' % times] = QtWidgets.QPushButton()
            locals()['self.show%sButton' % times].setObjectName('self.show%sButton' % times)
            locals()['self.show%sButton' % times].setText("%s Times" % times)
            locals()['self.show%sButton' % times].setMinimumHeight (20)
            self.scrollFiller.addWidget(locals()['self.show%sButton' % times], *(self.scrollFiller.count() / 3, self.scrollFiller.count() % 3))
            locals()['self.show%sButton' % times].show()


#useQt5AggToDraw
class figureCanvas(FigureCanvas):
    # Inheritting from FigureCanvas, making this class a Qwidget in PyQt5 and a FigureCanvas in matplotlib.
    # connecting pyqt5 and matplotlib.
    
    def __init__(self, parent=None):
         fig = matplotlib.figure.Figure()  
         # creat a Figure.
         # attention: this Figure isn't figure in matplotlib.pyplot, but figure in matplotlib.
 
         FigureCanvas.__init__(self, fig) 
         self.setParent(parent)
 
         self.axes = fig.add_subplot(111) 
         # There must be a axes to plot.
 
    def figureCanvasPlot(self, x, y, *arg):
        self.axes.plot(x, y, *arg)


if __name__ == '__main__':
    import sys
    
    app = QtWidgets.QApplication(sys.argv)    
    #QApplication and QWidget are in main.py. That sounds unreasonable, but just let it that way.
    mainWidget = mainWidget()
    mainWidget.show()

    sys.exit(app.exec_())
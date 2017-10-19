"""
author: Abdurrahim Burak Tekin
version: 19.10.2017
"""

import sys
import NaviController
from PySide import QtGui

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    navi = NaviController.Controller()
    navi.show()
    sys.exit(app.exec_())

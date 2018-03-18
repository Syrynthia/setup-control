import ui
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
 app = QApplication(sys.argv)
 dialog = ui.UiDialog()
 dialog.show()
 sys.exit(app.exec_())

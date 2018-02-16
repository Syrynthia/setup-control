import ui
import sys

if __name__ == '__main__':
 app = ui.QApplication(sys.argv)
 dialog = ui.UiDialog()
 dialog.show()
 sys.exit(app.exec_())

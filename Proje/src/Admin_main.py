import json
from PyQt5.QtWidgets import QApplication
import sys
from admin_Login import AdminLogin


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminLogin()
    window.show()
    sys.exit(app.exec_())

import sys

from PyQt5.QtWidgets import QApplication

from MainPage import MainPage


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def main():
    app = QApplication(sys.argv)
    application = MainPage()
    application.show()
    sys.excepthook = except_hook
    print("Started")
    sys.exit(app.exec())


if __name__ == '__main__':
    print("Starting")
    main()

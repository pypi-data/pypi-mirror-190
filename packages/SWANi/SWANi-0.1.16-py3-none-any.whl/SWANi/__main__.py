import sys, os, psutil
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QIcon, QPixmap
from SWANi.UI.mainWindow import mainWindow
from SWANi.utils.SWANiConfig import SWANiConfig
from SWANi.utils.APPLABELS import APPLABELS
import SWANi_supplement


def main():

    currentExitCode = APPLABELS.EXIT_CODE_REBOOT

    while currentExitCode == APPLABELS.EXIT_CODE_REBOOT:

        #app = QApplication([])

        if not QApplication.instance():
            app = QApplication(sys.argv)
        else:
            app = QApplication.instance()

        app.setWindowIcon(QIcon(QPixmap(SWANi_supplement.appIcon_file)))

        SWANiGlobalConfig=SWANiConfig()
        
        #escludo che ci siano altre istanze di SWANi in esecuzione        
        lastPID=SWANiGlobalConfig.getint('MAIN','lastPID')
        if lastPID!=os.getpid():
            try:
                psutil.Process(lastPID)
                msgBox = QMessageBox()
                msgBox.setText("Another instance of "+APPLABELS.APPNAME+" is already running!")
                msgBox.exec()
                break
                
            except (psutil.NoSuchProcess, ValueError):
                SWANiGlobalConfig['MAIN']['lastPID']=str(os.getpid())
                SWANiGlobalConfig.save()
        
        widget=mainWindow(SWANiGlobalConfig)
        currentExitCode=app.exec()
        

    sys.exit(currentExitCode)

if __name__ == "__main__":
    main()

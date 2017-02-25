import ts3lib, ts3defines, datetime
from ts3plugin import ts3plugin, PluginHost
from os import path


class gommeChecker(ts3plugin):
    name = "Gomme Checker"
    apiVersion = 21
    requestAutoload = False
    version = "1.0"
    author = "Bluscream"
    description = "Obwohl ich die meisten Gomme mods hasse ♥"
    offersConfigure = False
    commandKeyword = ""
    infoTitle = None
    iconPath = path.join(ts3lib.getPluginPath(), "pyTSon", "scripts", "gommeChecker", "icons")
    menuItems = [(ts3defines.PluginMenuType.PLUGIN_MENU_TYPE_GLOBAL, 0, "Check all Channels", "")]
    hotkeys = []
    debug = False

    def __init__(self):
        ts3lib.logMessage(self.name + " script for pyTSon by " + self.author + " loaded from \"" + __file__ + "\".", ts3defines.LogLevel.LogLevel_INFO, "Python Script", 0)
        if self.debug: ts3lib.printMessageToCurrentTab('[{:%Y-%m-%d %H:%M:%S}]'.format( datetime.datetime.now()) + " [color=orange]" + self.name + "[/color] Plugin for pyTSon by [url=https://github.com/" + self.author + "]" + self.author + "[/url] loaded.")

    def onMenuItemEvent(self, schid, atype, menuItemID, selectedItemID):
        if atype == ts3defines.PluginMenuType.PLUGIN_MENU_TYPE_GLOBAL and menuItemID == 0:
            self.dlg = CheckerDialog(self)
            self.dlg.show()

class CheckerDialog(QDialog):
    def buhl(self, s):
        if s.lower() == 'true' or s == 1:
            return True
        elif s.lower() == 'false' or s == 0:
            return False
        else:
            raise ValueError("Cannot convert {} to a bool".format(s))

    def __init__(self, gommeChecker, parent=None):
        self.gommeChecker=gommeChecker
        super(QDialog, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        setupUi(self, os.path.join(ts3.getPluginPath(), "pyTSon", "scripts", "gommeChecker", "check.ui"))
        self.setWindowTitle("Gomme Checker")
        self.checktable.setColumnWidth(2, 350)
        self.checkChannels()

    def checkChannels(self):
        self.checktable.clear()
        self.checktable.setRowCount(len(self.cmd.sections()))
        row = 0
        for i in self.cmd.sections():
            item = QTableWidgetItem(i)
            kitem = QTableWidgetItem(self.cmd[i]["function"])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
            item.setCheckState(Qt.Checked if self.cmd.getboolean(i, "enabled") else Qt.Unchecked)
            self.checktable.setItem(row, 1, kitem)
            self.checktable.setItem(row, 0, item)
            row += 1
        self.checktable.setRowCount(row)
        self.checktable.sortItems(0)

    def on_apply_clicked(self):
        try:
            self.serverBrowser.config.set("FILTERS", "hideEmpty", str(self.hideEmpty.isChecked()))
            self.serverBrowser.config.set("FILTERS", "hideFull", str(self.hideFull.isChecked()))
            self.serverBrowser.config.set("FILTERS", "maxUsers", str(self.maxUsers.isChecked()))
            self.serverBrowser.config.set("FILTERS", "maxUsersMin", str(self.maxUsersMin.value))
            self.serverBrowser.config.set("FILTERS", "maxUsersMax", str(self.maxUsersMax.value))
            self.serverBrowser.config.set("FILTERS", "maxSlots", str(self.maxSlots.isChecked()))
            self.serverBrowser.config.set("FILTERS", "maxSlotsMin", str(self.maxSlotsMin.value))
            self.serverBrowser.config.set("FILTERS", "maxSlotsMax", str(self.maxSlotsMax.value))
            if self.filterPasswordShowWithout.isChecked():
                self.serverBrowser.config.set("FILTERS", "filterPassword", "none")
            elif self.filterPasswordShowWith.isChecked():
                self.serverBrowser.config.set("FILTERS", "filterPassword", "only")
            elif self.filterPasswordShowAll.isChecked():
                self.serverBrowser.config.set("FILTERS", "filterPassword", "all")
            if self.filterChannelsCantCreate.isChecked():
                self.serverBrowser.config.set("FILTERS", "filterChannels", "none")
            elif self.filterChannelsCanCreate.isChecked():
                self.serverBrowser.config.set("FILTERS", "filterChannels", "only")
            elif self.filterChannelsShowAll.isChecked():
                self.serverBrowser.config.set("FILTERS", "filterChannels", "all")
            self.serverBrowser.config.set("FILTERS", "serverNameModifier", self.serverNameModifier.currentText)
            self.serverBrowser.config.set("FILTERS", "filterServerName", self.filterServerName.text)
            self.serverBrowser.config.set("FILTERS", "countryBox", self.countryBox.currentText.split(" (")[0])
            with open(self.serverBrowser.ini, 'w') as configfile:
                self.serverBrowser.config.write(configfile)
            if self.buhl(self.serverBrowser.config['GENERAL']['morerequests']):
                self.listCountries()
            self.page = 1
            self.listServers()
            if not self.cooldown:
                self.cooldown = True
                QTimer.singleShot(self.cooldown_time, self.disable_cooldown)
        except:
            ts3.logMessage(traceback.format_exc(), ts3defines.LogLevel.LogLevel_ERROR, "pyTSon", 0)

    def on_close_clicked(self):
        self.close()
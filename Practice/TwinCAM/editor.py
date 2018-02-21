#----------------------------------------------------------------------
# Name:        editor.py
# Author:      Jin Zhiqiang
# Tags:        Python3, wxPython4
#----------------------------------------------------------------------
"""TwinCAM editor."""

__author__ = "Jin Zhiqiang <jzq802@hotmail.com>"

import wx
import wx.stc as stc

import os


class EditorFrame(wx.Frame):
    """Frame containing one editor."""

    def __init__(self, *args, **kw):
        """Create EditorFrame instance."""
        super(EditorFrame, self).__init__(*args, **kw)
        self.createMenuBar()
        self.dirname = ''
        self.filename = ''
        self.leftMarginWidth = 32
        self.lineNumbersEnabled = True
        self.control = stc.StyledTextCtrl(
            self, style=wx.TE_MULTILINE | wx.TE_WORDWRAP)
        self.control.CmdKeyAssign(
            ord('+'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
        self.control.CmdKeyAssign(
            ord('-'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)
        self.control.SetViewWhiteSpace(False)
        self.control.SetMargins(5, 0)
        self.control.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.control.SetMarginWidth(1, self.leftMarginWidth)
        self.CreateStatusBar()
        self.StatusBar.SetBackgroundColour((220, 220, 220))
        self.control.Bind(wx.EVT_KEY_UP, self.UpdateLineCol)
        self.control.Bind(wx.EVT_CHAR, self.OnCharEvent)
        self.Show()
        self.UpdateLineCol(self)

    def menuData(self):
        return (("&File",
                    ("&New \tCtrl+N", "New file", self.OnNew),
                    ("&Open... \tCtrl+O", "Open file", self.OnOpen),
                    ("", "", ""),
                    ("&Save... \tCtrl+S", "Save file", self.OnSave),
                    ("Save &As \tCtrl+Shift+S", "Save file with new name", self.OnSaveAs),
                    ("", "", ""),
                    ("E&xit \tCtrl+Q", "Exit Program", self.OnClose)),
                ("&Edit",
                    ("&Undo \tCtrl+Z", "Undo the last action", self.OnUndo),
                    ("&Redo \tCtrl+Y", "Redo the last undone action", self.OnRedo),
                    ("", "", ""),
                    ("Cu&t \tCtrl+X", "Cut the selection", self.OnCut),
                    ("&Copy \tCtrl+C", "Copy the selection", self.OnCopy),
                    ("&Paste \tCtrl+V", "Paste from clipboard", self.OnPaste),
                    ("", "", ""),
                    ("Select A&ll \tCtrl+A", "Select all text", self.OnSelectAll)),
                ("&View",
                    ("Toggle &Line Numbers", "Show/Hide Line Numbers", self.OnToggleLineNumbers)),
                ("&Help",
                    ("&Help \tF1", "Help!", self.OnHowTo),
                    ("", "", ""),
                    ("&About...", "About this program", self.OnAbout)))

    def createMenuBar(self):
        menuBar = wx.MenuBar()
        for eachMenuData in self.menuData():
            menuLabel = eachMenuData[0]
            menuItems = eachMenuData[1:]
            menuBar.Append(self.createMenu(menuItems), menuLabel)
        self.SetMenuBar(menuBar)

    def createMenu(self, menuData):
        menu = wx.Menu()
        for eachLabel, eachStatus, eachHandler in menuData:
            if not eachLabel:
                menu.AppendSeparator()
                continue
            menuItem = menu.Append(-1, eachLabel, eachStatus)
            self.Bind(wx.EVT_MENU, eachHandler, menuItem)
        return menu

    def OnNew(self, e):
        self.filename = ''
        self.control.SetValue("")

    def OnOpen(self, e):
        try:
            dlg = wx.FileDialog(self, "Open a file...", self.dirname, "",
                                "*.*", wx.FD_OPEN)
            if (dlg.ShowModal() == wx.ID_OK):
                self.filename = dlg.GetFilename()
                self.dirname = dlg.GetDirectory()
                f = open(os.path.join(self.dirname, self.filename), "r")
                self.control.SetValue(f.read())
                f.close()
            dlg.Destroy()
        except:
            dlg = wx.MessageDialog(self, "Could not open file", "Error",
                                   wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()

    def OnSave(self, e):
        try:
            f = open(os.path.join(self.dirname, self.filename), 'w')
            f.write(self.control.GetValue())
            f.close()
        except:
            try:
                dlg = wx.FileDialog(self, "Save file as...", self.dirname,
                                    "Untitled", "*.*",
                                    wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
                if (dlg.ShowModal() == wx.ID_OK):
                    self.filename = dlg.GetFilename()
                    self.dirname = dlg.GetDirectory()
                    f = open(os.path.join(self.dirname, self.filename), 'w')
                    f.write(self.control.GetValue())
                    f.close()
                dlg.Destroy()
            except:
                pass

    def OnSaveAs(self, e):
        try:
            dlg = wx.FileDialog(self, "Save file as...", self.dirname,
                                "Untitled.txt", "*.*",
                                wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if (dlg.ShowModal() == wx.ID_OK):
                self.filename = dlg.GetFilename()
                self.dirname = dlg.GetDirectory()
                f = open(os.path.join(self.dirname, self.filename), 'w')
                f.write(self.control.GetValue)
                f.close()
            dlg.Destroy()
        except:
            pass

    def OnClose(self, e):
        self.Close(True)

    def OnUndo(self, e):
        self.control.Undo()

    def OnRedo(self, e):
        self.control.Redo()

    def OnSelectAll(self, e):
        self.control.SelectAll()

    def OnCopy(self, e):
        self.control.Copy()

    def OnCut(self, e):
        self.control.Cut()

    def OnPaste(self, e):
        self.control.Paste()

    def OnToggleLineNumbers(self, e):
        if (self.lineNumbersEnabled):
            self.control.SetMarginWidth(1, 0)
            self.lineNumbersEnabled = False
        else:
            self.control.SetMarginWidth(1, self.leftMarginWidth)
            self.lineNumbersEnabled = True

    def OnHowTo(self, e):
        # TODO Make 'how to' an external file
        dlg = wx.lib.dialogs.ScrolledMessageDialog(
            self, "This is How To.", "How To", size=(400, 400))
        dlg.ShowModal()
        dlg.Destroy()

    def OnAbout(self, e):
        # TODO Make 'about' an external file
        dlg = wx.MessageDialog(self, "Something goes here", "About", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def UpdateLineCol(self, e):
        line = self.control.GetCurrentLine() + 1
        col = self.control.GetColumn(self.control.GetCurrentPos())
        stat = "Line %s, Column %s" % (line, col)
        self.StatusBar.SetStatusText(stat, 0)

    def OnCharEvent(self, e):
        keycode = e.GetKeyCode()
        shiftDown = e.ShiftDown()
        if (keycode == 14):  # Ctrl + N
            self.OnNew(self)
        elif (keycode == 15):  # Ctrl + O
            self.OnOpen(self)
        elif (keycode == 19):  # Ctrl + S
            self.OnSave(self)
        elif (shiftDown and (keycode == 19)):  # Control + Shift + S
            self.OnSaveAs(self)
        elif (keycode == 23):  # Ctrl + W
            self.OnClose(self)
        elif (keycode == 340):  # F1
            self.OnHowTo()
        elif (keycode == 341):  # F2
            self.OnAbout(self)
        else:
            e.Skip()

#!/usr/bin/python


import wx
import wx.lib.dialogs
import wx.stc as stc
import os




class MainWindow(wx.Frame):
    def __init__(self,parent,title):

        self.dirname=''
        self.filename= ''

        self.leftMarginWidth = 30
        self.lineNumbersEnabled = True
        self.closeWithoutSave= True

        wx.Frame.__init__(self , parent, title=title, size=(800,600) )
        self.control=stc.StyledTextCtrl(self, style=wx.TE_MULTILINE | wx.TE_WORDWRAP)

        self.control.CmdKeyAssign(ord('+'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN) #CTRL+'+' make a zoomin
        self.control.CmdKeyAssign(ord('-'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT) #CTRL+'-' make a zoomout

        self.control.SetMargins(5, 0)
        self.control.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.control.SetMarginWidth(1, self.leftMarginWidth)

        self.CreateStatusBar()
        self.StatusBar.SetBackgroundColour((220,220,220))

        filemenu=wx.Menu()
        menuNew=filemenu.Append(wx.ID_NEW, "&New", "Crate a new document")
        menuOpen=filemenu.Append(wx.ID_OPEN,"&Open", "Open an existing document")
        menuSave =filemenu.Append(wx.ID_SAVE, "&Save", "Save current document")
        menuSaveAs =filemenu.Append(wx.ID_SAVEAS, "Save &As", "Save new document")
        filemenu.AppendSeparator()
        menuClose=filemenu.Append(wx.ID_EXIT, "&Close", "Close the application")

        editmenu=wx.Menu()
        menuUndo=editmenu.Append(wx.ID_UNDO, "&Undo", "Undo the last action")
        menuRedo=editmenu.Append(wx.ID_REDO, "&Redo", "Redo the last action")
        filemenu.AppendSeparator()
        menuSelectAll=editmenu.Append(wx.ID_SELECTALL, "&Select All", "Select the entire text")
        menuCopy=editmenu.Append(wx.ID_COPY, "&Copy", "Copy selected text")
        menuCut=editmenu.Append(wx.ID_CUT, "&CUT", "Cut selected text")
        menuPaste=editmenu.Append(wx.ID_PASTE, "&Paste", "Paste text from clipboard")

        prefmenu=wx.Menu()
        menuLineNumbers= prefmenu.Append(wx.ID_ANY, "Toggle &Line Numbers", "Show/Hide line numbers column")

        menuBar=wx.MenuBar()
        menuBar.Append(filemenu, 'File')
        menuBar.Append(editmenu, 'Edit')
        menuBar.Append(prefmenu, 'Preferences')
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU,self.OnNew,menuNew)
        self.Bind(wx.EVT_MENU,self.OnOpen,menuOpen)
        self.Bind(wx.EVT_MENU,self.OnSave,menuSave)
        self.Bind(wx.EVT_MENU,self.OnSaveAs,menuSaveAs)
        self.Bind(wx.EVT_MENU,self.OnClose,menuClose)

        self.Bind(wx.EVT_MENU,self.OnUndo,menuUndo)
        self.Bind(wx.EVT_MENU,self.OnRedo,menuRedo)
        self.Bind(wx.EVT_MENU,self.OnSelectAll,menuSelectAll)
        self.Bind(wx.EVT_MENU,self.OnCopy,menuCopy)
        self.Bind(wx.EVT_MENU,self.OnCut,menuCut)
        self.Bind(wx.EVT_MENU,self.OnPaste,menuPaste)

        self.Bind(wx.EVT_MENU,self.OnToggleLineNumbers,menuLineNumbers)

        self.control.Bind(wx.EVT_KEY_UP,self.UpdateLineCol)

        self.control.Bind(wx.EVT_KEY_UP,self.UpdateDocNS)

        self.Show()
        self.UpdateLineCol(self)

    def OnNew(self, e):
        if(self.closeWithoutSave):
            self.filename = ''
            self.control.SetValue("")
            self.closeWithoutSave= False
        else:
            dlg=wx.MessageDialog(None,"Do you want close the current document without saving your file?",'Attention',wx.YES_NO)
            answer=dlg.ShowModal()
            if (answer==5103):
                dlg.Destroy()
                self.filename = ''
                self.control.SetValue("")
                self.closeWithoutSave= False
            else:
                dlg.Destroy()
                self.OnSave(e)
                self.filename = ''
                self.control.SetValue("")
                self.closeWithoutSave= False

    def OnOpen(self, e):
            if(self.closeWithoutSave):
                dlg= wx.FileDialog(self, "Choose a file", self.dirname, "","*.*",wx.FD_OPEN)
                if(dlg.ShowModal()==wx.ID_OK):
                    self.filename=dlg.GetFilename()
                    self.dirname= dlg.GetDirectory()
                    f=open(os.path.join(self.dirname, self.filename),'r')
                    self.control.SetValue(f.read())
                    f.close()
                dlg.Destroy()
            else:
                yn=wx.MessageDialog(None,"Do you want close the current document without saving your file?",'Attention',wx.YES_NO)
                answer=yn.ShowModal()
                if (answer==5103):
                    yn.Destroy()
                    dlg= wx.FileDialog(self, "Choose a file", self.dirname, "","*.*",wx.FD_OPEN)
                    if(dlg.ShowModal()==wx.ID_OK):
                        self.filename=dlg.GetFilename()
                        self.dirname= dlg.GetDirectory()
                        f=open(os.path.join(self.dirname, self.filename),'r')
                        self.control.SetValue(f.read())
                        f.close()
                    dlg.Destroy()
                else:
                    yn.Destroy()
                    self.OnSave(e)
                    dlg= wx.FileDialog(self, "Choose a file", self.dirname, "","*.*",wx.FD_OPEN)
                    if(dlg.ShowModal()==wx.ID_OK):
                        self.filename=dlg.GetFilename()
                        self.dirname= dlg.GetDirectory()
                        f=open(os.path.join(self.dirname, self.filename),'r')
                        self.control.SetValue(f.read())
                        f.close()
                    dlg.Destroy()

    def OnSave(self, e):
        try:
            f=open(os.path.join(self.dirname,self.filename),'w')
            f.write(self.control.GetValue())
            f.close
            self.closeWithoutSave= True
        except:
            try:
                dlg=wx.FileDialog(self,"Save file as", self.dirname, "Untitled", "*.*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
                if (dlg.ShowModal()==wx.ID_OK):
                    self.filename=dlg.GetFilename()
                    self.dirname=dlg.GetDirectory()
                    file= open(os.path.join(self.dirname,self.filename),'w')
                    f.write(self.control.GetValue())
                    f.close()
                dlg.Destroy()
                self.closeWithoutSave= True
            except:
                pass
    def OnSaveAs(self, e):
        try:
            dlg=wx.FileDialog(self,"Save file as", self.dirname, "Untitled", "*.*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if (dlg.ShowModal()==wx.ID_OK):
                self.filename=dlg.GetFilename()
                self.dirname=dlg.GetDirectory()
                file= open(os.path.join(self.dirname,self.filename),'w')
                f.write(self.control.GetValue())
                f.close()
            dlg.Destroy()
            self.closeWithoutSave= True
        except:
            pass
    def OnClose(self, e):
        if (self.closeWithoutSave):
            self.Close(True)
        else:
            dlg=wx.MessageDialog(None,"Do you want close without saving your file?",'Attention',wx.YES_NO)
            answer=dlg.ShowModal()
            if (answer==5103):
                dlg.Destroy()
                self.Close(True)
            else:
                dlg.Destroy()
                self.OnSave(e)
                self.Close(True)
    def OnUndo(self,e):
        self.control.Undo()
    def OnRedo(self,e):
        self.control.Redo()
    def OnSelectAll(self, e):
        self.control.SelectAll()
    def OnCopy(self,e):
        self.control.Copy()
    def OnCut(self,e):
        self.control.Cut()
    def OnPaste(self,e):
        self.control.Paste()
    def OnToggleLineNumbers(self, e):
        if (self.lineNumbersEnabled):
            self.control.SetMarginWidth(1,0)
            self.lineNumbersEnabled=False
        else:
            self.control.SetMarginWidth(1,self.leftMarginWidth)
            self.lineNumbersEnabled=True
    def UpdateLineCol(self,e):
        line= self.control.GetCurrentLine()+1
        col=self.control.GetColumn(self.control.GetCurrentPos())
        stat= "Line %s, Column %s"%(line,col)
        self.StatusBar.SetStatusText(stat,0)
    def UpdateDocNS(self,e):
        self.closeWithoutSave=False
    def UpdateDocS(self,e):
        self.closeWithoutSave=True

app=wx.App()
frame= MainWindow(None, 'Giant - Build 0')
app.MainLoop()
class EditorFrame(frame.Frame):
    """Frame containing one editor."""

    def __init__(self, parent=None, id=-1, title='PyAlaCarte',
                 pos=wx.DefaultPosition, size=(800, 600),
                 style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE,
                 filename=None):
        """Create EditorFrame instance."""
        frame.Frame.__init__(self, parent, id, title, pos, size, style)
        self.buffers = {}
        self.buffer = None  # Current buffer.
        self.editor = None


class EditorNotebookFrame(EditorFrame):
    """Frame containing one or more editors in a notebook."""

        """Create EditorNotebookFrame instance."""
        EditorFrame.__init__(self, parent, id, title, pos,
                             size, style, filename)


class EditorNotebook(wx.Notebook):
    """A notebook containing a page for each editor."""

        """Create EditorNotebook instance."""
        wx.Notebook.__init__(self, parent, id=-1, style=wx.CLIP_CHILDREN)


class EditorShellNotebookFrame(EditorNotebookFrame):
    """Frame containing a notebook containing EditorShellNotebooks."""

        """Create EditorShellNotebookFrame instance."""
        EditorNotebookFrame.__init__(self, parent, id, title, pos,
                                     size, style, filename)


class EditorShellNotebook(wx.Notebook):
    """A notebook containing an editor page and a shell page."""

    def __init__(self, parent, filename=None):
        """Create EditorShellNotebook instance."""
        wx.Notebook.__init__(self, parent, id=-1)
        editorparent = editorpanel = wx.Panel(self, -1)
        shellparent = shellpanel = wx.Panel(self, -1)
        self.buffer = Buffer()
        self.editor = Editor(parent=editorparent)
        self.shell = Shell(parent=shellparent, locals=self.buffer.interp.locals,
                           style=wx.CLIP_CHILDREN | wx.SUNKEN_BORDER)


class Editor:
    """Editor having an EditWindow."""

    def __init__(self, parent, id=-1, pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=wx.CLIP_CHILDREN | wx.SUNKEN_BORDER):
        """Create Editor instance."""
        self.window = EditWindow(self, parent, id, pos, size, style)
        self.id = self.window.GetId()
        self.buffer = None


class EditWindow(editwindow.EditWindow):
    """EditWindow based on StyledTextCtrl."""

    def __init__(self, editor, parent, id=-1, pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=wx.CLIP_CHILDREN | wx.SUNKEN_BORDER):
        """Create EditWindow instance."""
        editwindow.EditWindow.__init__(self, parent, id, pos, size, style)
        self.editor = editor






20        self.closeWithoutSave= True                           可能不需要

    88    self.control.Bind(wx.EVT_CHAR, self.OnCharEvent)      需要
78        self.control.Bind(wx.EVT_KEY_UP,self.UpdateDocNS)     不需要

    93 def OnNew(self, e):
83    def OnNew(self, e):   处理 self.closeWithoutSave        不需要

    97 def OnOpen(self, e): 处理 try/except                   需要
103    def OnOpen(self, e): 处理 self.closeWithoutSave        不需要
    
138    def OnSave(self, e): 增加处理 self.closeWithoutSave      不需要

157    def OnSaveAs(self, e): 增加处理 self.closeWithoutSave    不需要

170    def OnClose(self, e): 增加处理 self.closeWithoutSave     不需要

    172 def OnHowTo(self, e):   不需要

    178 def OnAbout(self, e):   需要
    
207    def UpdateDocNS(self,e): 不需要

209    def UpdateDocS(self,e):  不需要

    190 def OnCharEvent(self, e):   需要
 
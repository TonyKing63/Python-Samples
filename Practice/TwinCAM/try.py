#!/usr/bin/env python
#----------------------------------------------------------------------------
# Name:         TwinCAM.py
# Purpose:      Generating G-code for CNC machines
#
# Author:       Jin Zhiqiang
#
# Copyright:    (c) 2018 by Jin Zhiqiang, All Rights Reserved
# Licence:      TwinCAM license
# Tags:         Python3, wxPython4
#----------------------------------------------------------------------------
"""TwinCAM is a CAM software to generate G-code for CNC machines."""

__author__ = "Jin Zhiqiang <jzq802@hotmail.com>"

import wx

import editor


class MyFrame(editor.EditorFrame):
    """TwinCAM main frame."""

    def __init__(self, *args, **kw):
        """Create MyFrame instance."""

        super(MyFrame, self).__init__(*args, **kw)


class MyApp(wx.App):
    """TwinCAM standalone application."""

    def OnInit(self):
        frame = MyFrame(None, title='TwinCAM', size=(800, 600))
        frame.Show()
        self.SetTopWindow(frame)
        return True


def main():
    app = MyApp()
    app.MainLoop()


if __name__ == '__main__':
    main()

"""
wbpLoglist
===============================================================================

List view for the history of wx log messages

"""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Tuple

import wx
from wx import aui

from .loglistwin import LogListWindow
from .preferences import LogListPreferences

if TYPE_CHECKING:
    from wbBase.application import App
    from wbBase.dialog.preferences import PreferencesPageBase

__version__ = "0.1.4"

name = "LogList"


logListInfo = aui.AuiPaneInfo()
logListInfo.Name(name)
logListInfo.Caption(name)
logListInfo.Dock()
logListInfo.Bottom()
logListInfo.Resizable()
logListInfo.Hide()
logListInfo.MaximizeButton(True)
logListInfo.MinimizeButton(True)
logListInfo.CloseButton(False)
logListInfo.MinSize(150, 100)
logListInfo.BestSize(250, 200)
logListInfo.Icon(wx.ArtProvider.GetBitmap("LOG", wx.ART_FRAME_ICON))

#: Panels provided by the wbpLoglist plugin.
panels: List[Tuple[type[wx.Window], aui.AuiPaneInfo]] = [(LogListWindow, logListInfo)]

#: Preference pages provided by the wbpLoglist plugin.
preferencepages:List[PreferencesPageBase] = [LogListPreferences]


def AddLogToLogChain(app:App) -> None:
    """
    Post init action which adds a new logging target to the log chain
    of the Workbench application.

    :param app: Workbench application
    """
    wx.Log.GetActiveTarget()
    app.logChain = wx.LogChain(app.TopWindow.panelManager.getWindowByCaption(name).log)

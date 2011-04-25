# -*- coding: utf-8 -*-

"""
Główne okno programu
"""

__author__ = "Karol Będkowski"
__copyright__ = "Copyright (c) Karol Będkowski, 2010"
__version__ = "2011-04-24"


import wx

from photomagick.lib.appconfig import AppConfig

from ._base_dialog import BaseDialog
from . import message_boxes as mbox


class DlgBatchOutput(BaseDialog):
	def __init__(self, parent, dest_directory=None, postfix=None):
		BaseDialog.__init__(self, parent, 'dialog_batch_output', save_pos=False)
		self._setup(dest_directory, postfix)

	def _setup(self, dest_directory, postfix):
		self.dest_directory = dest_directory or AppConfig().get('batch',
				'last_dir', '')
		self.postfix = postfix or AppConfig().get('batch', 'postfix', '')
		self['tc_dest_directory'].SetValue(self.dest_directory or '')
		self['tc_filename_postfix'].SetValue(self.postfix or '')

	def _create_bindings(self):
		BaseDialog._create_bindings(self)
		self._wnd.Bind(wx.EVT_BUTTON, self._on_select_directory,
				self['btn_select_dir'])

	def _on_ok(self, _evt):
		dest_directory = self['tc_dest_directory'].GetValue().strip()
		if not dest_directory:
			mbox.message_box_error_ex(self._wnd, _("Couldn't process files."),
					_("Please select destination directory."))
			self['tc_dest_directory'].SetFocus()
			return
		self.dest_directory = dest_directory
		self.postfix = self['tc_filename_postfix'].GetValue().strip()
		AppConfig().set('batch', 'last_dir', dest_directory)
		AppConfig().set('batch', 'postfix', self.postfix)
		self._wnd.EndModal(wx.ID_OK)

	def _on_select_directory(self, evt):
		dlg = wx.DirDialog(self._wnd, _("Please select destination directory"),
				self['tc_dest_directory'].GetValue())
		if dlg.ShowModal() == wx.ID_OK:
			self['tc_dest_directory'].SetValue(dlg.GetPath())
		dlg.Destroy()

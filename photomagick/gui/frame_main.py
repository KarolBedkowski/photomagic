#!usr/bin/python
# -*- coding: utf-8 -*-
"""
Główne okno programu
"""

__author__ = "Karol Będkowski"
__copyright__ = "Copyright (c) Karol Będkowski, 2011"
__version__ = "2011-04-24"

import os
import logging
import random
from itertools import imap

import wx
from wx import xrc

import Image

from photomagick import filters
from photomagick.lib import wxresources
from photomagick.lib import wxutils
from photomagick.lib import iconprovider
from photomagick.lib.appconfig import AppConfig
from photomagick.lib import debug
from photomagick.lib import wx_pil

from .dlg_batch_output import DlgBatchOutput
from . import dlg_about
from . import message_boxes as mbox

_LOG = logging.getLogger(__name__)


class _Img(object):
	def __init__(self, filename, image=None):
		self.filename = filename
		self._image = image
		self.thumb = None
		self.processed = None

	def __repr__(self):
		return '<_Img %r, image=%r, thumb=%r, processed=%r' % (self.filename,
				self._image, self.thumb, self.processed)

	@property
	def image(self):
		if not self._image:
			self._image = Image.open(self.filename)
			if self._image.mode != 'RGB':
				_LOG.info('Image %r mode %r; convert to RGB', self.filename,
						self._image.mode)
				self._image = self._image.convert('RGB')
		return self._image

	def create_thumb(self, size):
		self.thumb = self.image.copy()
		self.thumb.thumbnail(size)


_ACCEL_TABLE = [
		(wx.ACCEL_CTRL, ord('Q'), wx.ID_CLOSE),
		(wx.ACCEL_CTRL, ord('S'), wx.ID_SAVE),
		(wx.ACCEL_CTRL, ord('O'), wx.ID_OPEN),
		(wx.ACCEL_CTRL, ord('N'), wx.ID_NEW),
]


class FrameMain:
	''' Klasa głównego okna programu'''
	def __init__(self, filename=None):
		self.res = wxresources.load_xrc_resource('main.xrc')
		self._files = {}
		self._img = None
		self.__controls = {}
		self._load_controls()
		self._create_bindings()
		self._setup(filename)

	def __getitem__(self, key):
		if key in self.__controls:
			return self.__controls[key]
		ctrl = None
		if isinstance(key, (str, unicode)):
			ctrl = xrc.XRCCTRL(self.wnd, key)
			if not ctrl:
				ctrl = self.wnd.FindWindowByName(key)
		else:
			ctrl = self.wnd.FindWindowById(key)
		assert ctrl is not None, 'Key %r not found' % key
		self.__controls[key] = ctrl
		return ctrl

	# setup

	def _setup(self, filename):
		self.wnd.SetIcon(iconprovider.get_icon('photomagick'))
		if wx.Platform == '__WXMSW__':
			self.wnd.SetBackgroundColour(wx.SystemSettings.GetColour(
				wx.SYS_COLOUR_ACTIVEBORDER))
		self._set_size_pos()
		self._fill_filters()
		self['lc_files'].InsertColumn(0, _('Filename'))
		self['wnd_splitter'].SetSashGravity(1.0)
		self['wnd_splitter'].SetSashPosition(-200)
		self['wnd_splitter'].SetMinimumPaneSize(200)
		self.wnd.SetAcceleratorTable(wx.AcceleratorTable(_ACCEL_TABLE))
		if filename:
			wx.CallAfter(lambda: self._append_files(filename))

	def _load_controls(self):
		self.wnd = self.res.LoadFrame(None, 'frame_main')
		assert self.wnd is not None
		self._lb_filters = self['lb_filters']
		self._lb_modificators = self['lb_modificators']
		self._lb_decorators = self['lb_decorators']
		self._lb_simple = self['lb_simple']
		self._create_toolbar()
		imagelist = wx.ImageList(32, 32)
		self['lc_files'].AssignImageList(imagelist, wx.IMAGE_LIST_NORMAL)

	def _create_bindings(self):
		wnd = self.wnd
		wnd.Bind(wx.EVT_CLOSE, self._on_close)
		wnd.Bind(wx.EVT_MENU, self._on_mnu_close, id=wx.ID_CLOSE)
		wnd.Bind(wx.EVT_MENU, self._on_add_files, id=wx.ID_OPEN)
		wnd.Bind(wx.EVT_MENU, self._on_clear_files, id=wx.ID_NEW)
		wnd.Bind(wx.EVT_MENU, self._on_save_single, id=wx.ID_SAVE)
		wnd.Bind(wx.EVT_LISTBOX, self._on_filters_listbox, self._lb_filters)
		wnd.Bind(wx.EVT_LISTBOX, self._on_filters_listbox, self._lb_modificators)
		wnd.Bind(wx.EVT_LISTBOX, self._on_filters_listbox, self._lb_decorators)
		wnd.Bind(wx.EVT_LISTBOX, self._on_filters_listbox, self._lb_simple)
		wnd.Bind(wx.EVT_TOGGLEBUTTON, self._on_btn_toggle_original,
				self['btn_toggle_orig'])
		wnd.Bind(wx.EVT_BUTTON, self._on_btn_random, self['button_random'])
		wnd.Bind(wx.EVT_LIST_ITEM_SELECTED, self._on_lc_files_selected,
				self['lc_files'])
		wnd.Bind(wx.EVT_LIST_ITEM_DESELECTED, self._on_lc_files_deselected,
				self['lc_files'])
		wnd.Bind(wx.EVT_BUTTON, self._on_btn_adv_add, id=wx.ID_ADD)
		wnd.Bind(wx.EVT_BUTTON, self._on_btn_adv_del, id=wx.ID_REMOVE)
		wnd.Bind(wx.EVT_BUTTON, self._on_btn_adv_up, id=wx.ID_UP)
		wnd.Bind(wx.EVT_BUTTON, self._on_btn_adv_down, id=wx.ID_DOWN)
		wnd.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self._on_filters_listbox,
				self['notebook'])
		self['panel_preview'].Bind(wx.EVT_SIZE, self._on_panel_preview_size)

	def _create_toolbar(self):
		toolbar = self.wnd.CreateToolBar()
		tbi = toolbar.AddLabelTool(wx.ID_NEW, _('Remove all files'),
				wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR),
				shortHelp=_('Remove all files'),
				longHelp=_('Remove all files from list'))
		self.__controls['tb_clear'] = tbi.GetId()
		self.wnd.Bind(wx.EVT_TOOL, self._on_clear_files, id=tbi.GetId())
		tbi = toolbar.AddLabelTool(wx.ID_OPEN, _('Open files'),
				wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR),
				shortHelp=_('Open files for processing'),
				longHelp=_('Open one or more files for processing'))
		self.__controls['tb_open'] = tbi.GetId()
		self.wnd.Bind(wx.EVT_TOOL, self._on_add_files, id=tbi.GetId())
		tbi = toolbar.AddLabelTool(wx.ID_SAVE, _('Save file'),
				wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS, wx.ART_TOOLBAR),
				shortHelp=_('Save current file'),
				longHelp=_('Save current selected file'))
		self.__controls['tb_save'] = tbi.GetId()
		self.wnd.Bind(wx.EVT_TOOL, self._on_save_single, id=tbi.GetId())
		tbi = toolbar.AddLabelTool(wx.ID_DELETE, _('Remove selected file'),
				wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_TOOLBAR),
				shortHelp=_('Remove selected file'),
				longHelp=_('Remove selected files from list'))
		self.__controls['tb_delete'] = tbi.GetId()
		self.wnd.Bind(wx.EVT_TOOL, self._on_remove_file, id=tbi.GetId())
		toolbar.AddSeparator()
		tbi = toolbar.AddLabelTool(-1, _('Process all files'),
				wx.ArtProvider.GetBitmap(wx.ART_EXECUTABLE_FILE, wx.ART_TOOLBAR),
				shortHelp=_('Process all files'))
		self.__controls['tb_process'] = tbi.GetId()
		self.wnd.Bind(wx.EVT_TOOL, self._on_process_files, id=tbi.GetId())
		toolbar.AddSeparator()
		btn_toggle_orig = wx.ToggleButton(toolbar, -1, _(" Show original "))
		self.__controls['btn_toggle_orig'] = btn_toggle_orig
		toolbar.AddControl(btn_toggle_orig)
		toolbar.AddSeparator()
		tbi = toolbar.AddLabelTool(wx.ID_ABOUT, _('About'),
				wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_TOOLBAR),
				shortHelp=_('About application'),
				longHelp=_('About application'))
		self.wnd.Bind(wx.EVT_TOOL, self._on_btn_about, id=wx.ID_ABOUT)
		tbi = toolbar.AddLabelTool(wx.ID_CLOSE, _('Close'),
				wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_TOOLBAR),
				shortHelp=_('Close application'),
				longHelp=_('Close application'))
		toolbar.Realize()
		self.wnd.Bind(wx.EVT_UPDATE_UI, self._on_update_ui_toolbar, toolbar)
		self.wnd.Bind(wx.EVT_UPDATE_UI, self._on_update_ui_wnd)

	def _set_size_pos(self):
		appconfig = AppConfig()
		size = appconfig.get('frame_main', 'size', (800, 600))
		if size:
			self.wnd.SetSize(size)
		position = appconfig.get('frame_main', 'position')
		if position:
			self.wnd.Move(position)

	# callbacks

	def _on_close(self, _event):
		self._img = None
		appconfig = AppConfig()
		appconfig.set('frame_main', 'size', self.wnd.GetSizeTuple())
		appconfig.set('frame_main', 'position', self.wnd.GetPositionTuple())
		self.wnd.Destroy()

	def _on_panel_preview_size(self, evt):
		if self._img:
			self._update_preview(True)
		evt.Skip()

	def _on_mnu_close(self, evt):
		self.wnd.Close()

	def _on_filters_listbox(self, evt):
		self._update_preview()

	def _on_btn_about(self, evt):
		dlg_about.show_about_box(self.wnd)

	def _on_btn_toggle_original(self, evt):
		if not self._img:
			return
		self._show_preview(self._img.thumb if evt.IsChecked() \
				else self._img.processed)

	def _on_btn_random(self, evt):
		flt_idx = random.randint(0, self._lb_filters.GetCount() - 1)
		mod_idx = random.randint(0, self._lb_modificators.GetCount() - 1)
		dec_idx = random.randint(0, self._lb_decorators.GetCount() - 1)
		self._lb_filters.SetSelection(flt_idx)
		self._lb_modificators.SetSelection(mod_idx)
		self._lb_decorators.SetSelection(dec_idx)
		self._update_preview()

	def _on_btn_adv_add(self, evt):
		lb_all_filters = self['lb_all_filters']
		lb_used_filters = self['lb_used_filters']
		for sel in lb_all_filters.GetSelections():
			name = lb_all_filters.GetString(sel)
			module = lb_all_filters.GetClientData(sel)
			lb_used_filters.Append(name, module)
		self._update_preview()

	def _on_btn_adv_del(self, evt):
		lb_used_filters = self['lb_used_filters']
		for sel in reversed(lb_used_filters.GetSelections()):
			lb_used_filters.Delete(sel)
		self._update_preview()

	def _on_btn_adv_up(self, evt):
		lbox = self['lb_used_filters']
		selected = [sel for sel in lbox.GetSelections() if sel > 0]
		if not selected:
			return
		items = [(lbox.GetString(idx), lbox.GetClientData(idx))
				for idx in xrange(lbox.GetCount())]
		for idx in selected:
			items[idx - 1], items[idx] = items[idx], items[idx - 1]
		lbox.Clear()
		for name, module in items:
			lbox.Append(name, module)
		for idx in selected:
			lbox.SetSelection(idx - 1)
		self._update_preview()

	def _on_btn_adv_down(self, evt):
		lbox = self['lb_used_filters']
		count = lbox.GetCount()
		selected = [sel for sel in lbox.GetSelections() if sel < count - 1]
		if not selected:
			return
		items = [(lbox.GetString(idx), lbox.GetClientData(idx))
				for idx in xrange(lbox.GetCount())]
		for idx in reversed(selected):
			items[idx + 1], items[idx] = items[idx], items[idx + 1]
		lbox.Clear()
		for name, module in items:
			lbox.Append(name, module)
		for idx in selected:
			lbox.SetSelection(idx + 1)
		self._update_preview()

	def _on_add_files(self, _evt):
		dlg = wx.FileDialog(self.wnd, _('Please select files'),
				defaultDir=_last_dir(),
				wildcard=_("Images (*.jpg; *.png)|*.jpg;*.jpeg;*.png|All files|*.*"),
				style=wx.FD_OPEN | wx.FILE_MUST_EXIST | wx.FD_MULTIPLE | wx.FD_PREVIEW)
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPaths()
			self._append_files(path)
			_update_last_dir(os.path.dirname(path[0]))
		dlg.Destroy()

	def _on_save_single(self, evt):
		if self['lc_files'].GetSelectedItemCount() < 1:
			return
		dlg = wx.FileDialog(self.wnd, _('Select destination file'),
				os.path.dirname(self._img.filename),
				self._img.filename,
				wildcard=_("Images (*.jpg; *.png)|*.jpg;*.jpeg;*.png|All files|*.*"),
				style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
		if dlg.ShowModal() == wx.ID_OK:
			self._img.filename = filename = dlg.GetPath()
			with wxutils.with_wait_cursor():
				images = list(self._process(self._img, 'image'))
				if images:
					image = images[0].processed
					if image:
						try:
							image.save(filename, quality=95)
						except Exception, err:
							wx.SetCursor(wx.STANDARD_CURSOR)
							mbox.message_box_error_ex(self.wnd,
									_("Error saving file %s") % filename,
									_("While saving a file error occured: %s\n"
											"Cannot continue.") % str(err))

	def _on_remove_file(self, _evt):
		if not mbox.message_box_question(self.wnd,
				_("Remove selected files from list?"),
				_("This action is unrecoverable."), wx.ID_REMOVE, wx.ID_CLOSE):
			return
		to_del = []
		itemid = -1
		lc_files = self['lc_files']
		while True:
			itemid = lc_files.GetNextItem(itemid, wx.LIST_NEXT_ALL,
					wx.LIST_STATE_SELECTED)
			if itemid == -1:
				break
			to_del.append(lc_files.GetItemData(itemid))
		if to_del:
			imglist = self['lc_files'].GetImageList(wx.IMAGE_LIST_NORMAL)
			for x in reversed(to_del):
				img = self._files.pop(x)
				imglist.Remove(img['icon'])
			self._refresh_filelist()
			self._show_preview(None)

	def _on_clear_files(self, _evt):
		if not mbox.message_box_question(self.wnd, _("Remove all files from list?"),
				_("This action is unrecoverable."), wx.ID_REMOVE, wx.ID_CLOSE):
			return
		self._files.clear()
		imglist = self['lc_files'].GetImageList(wx.IMAGE_LIST_NORMAL)
		imglist.RemoveAll()
		self._refresh_filelist()
		self._show_preview(None)

	def _on_process_files(self, _evt):
		if not self._files:
			return
		dlg = DlgBatchOutput(self.wnd)
		if not dlg.run():
			return
		dest_dir = dlg.dest_directory
		postfix = dlg.postfix
		with wxutils.with_wait_cursor():
			images = (_Img(img['realpath']) for img in self._files.itervalues())
			for image in self._process(images, 'image'):
				if image.processed:
					filename = os.path.join(dest_dir,
							os.path.basename(image.filename))
					if postfix:
						filename = postfix.join(os.path.splitext(filename))
					try:
						image.processed.save(filename, quality=95)
					except Exception, err:
						wx.SetCursor(wx.STANDARD_CURSOR)
						if not mbox.message_box_question(self.wnd,
								_("Error saving file %s") % filename,
								_("While saving a file error occured: %s\n"
										"Contune processing other files?") % str(err),
								_("Continue"), _("Stop processing"),
								wx.ART_ERROR):
							break
						wx.SetCursor(wx.HOURGLASS_CURSOR)

	def _on_lc_files_selected(self, evt):
		itm_hash = evt.GetData()
		self._img = _Img(self._files[itm_hash]['realpath'])
		self._update_preview()

	def _on_lc_files_deselected(self, _evt):
		self._img = None
		self._show_preview(None)

	def _on_update_ui_toolbar(self, evt):
		toolbar = evt.GetEventObject()
		items_selected = self['lc_files'].GetSelectedItemCount() > 0
		toolbar.EnableTool(self['tb_save'], items_selected)
		toolbar.EnableTool(self['tb_delete'], items_selected)
		toolbar.EnableTool(self['tb_process'], bool(self._files))
		toolbar.EnableTool(self['tb_clear'], bool(self._files))
		toolbar.EnableTool(self['btn_toggle_orig'].GetId(), items_selected)
		evt.Skip()

	def _on_update_ui_wnd(self, evt):
		selected_lb_used_f = bool(self['lb_used_filters'].GetSelections())
		self['wxID_REMOVE'].Enable(selected_lb_used_f)
		self['wxID_UP'].Enable(selected_lb_used_f)
		self['wxID_DOWN'].Enable(selected_lb_used_f)
		selected_lb_all_f = bool(self['lb_all_filters'].GetSelections())
		self['wxID_ADD'].Enable(selected_lb_all_f)
		evt.Skip()

	###

	def _append_files(self, files):
		with wxutils.with_wait_cursor():
			imglist = self['lc_files'].GetImageList(wx.IMAGE_LIST_NORMAL)
			for idx, fname in enumerate(files):
				fname = os.path.realpath(fname)
				hname = hash(fname)
				if hname not in self._files.iterkeys():
					try:
						icon = wx.Image(fname)
						if not icon or not icon.IsOk():
							raise RuntimeError(_("Invalid file"))
					except Exception, err:
						wx.SetCursor(wx.STANDARD_CURSOR)
						if idx == len(files) - 1:
							mbox.message_box_error_ex(self.wnd,
									_("Error loading file %s") % fname,
									_("While loading a file error occured: %s\n"
											"Cannot continue.") % str(err))
							return
						else:
							if not mbox.message_box_question(self.wnd,
									_("Error loading file %s") % fname,
									_("While loading a file error occured: %s\n"
											"Contune loading files?") % str(err),
									_("Continue"), _("Stop loading"),
									wx.ART_ERROR):
								break
						wx.SetCursor(wx.HOURGLASS_CURSOR)
					else:
						scale = 32. / max(icon.GetWidth(), icon.GetHeight())
						thumb = icon.Scale(icon.GetWidth() * scale,
								icon.GetHeight() * scale)
						thumb = thumb.Resize((32, 32), (16 - thumb.GetWidth() / 2,
								16 - thumb.GetHeight() / 2))
						# win32 needs icons
						icon = wx.EmptyIcon()
						icon.CopyFromBitmap(wx.BitmapFromImage(thumb))
						imgidx = imglist.AddIcon(icon)
						self._files[hname] = {'realpath': fname,
								'name': os.path.basename(fname),
								'icon': imgidx}
			self._refresh_filelist()
			if not self['lc_files'].GetSelectedItemCount():
				self['lc_files'].SetItemState(0, wx.LIST_STATE_SELECTED,
						wx.LIST_STATE_SELECTED)

	def _fill_filters(self):
		lb_all_filters = self['lb_all_filters']
		lb_all_filters.Clear()
		self['lb_used_filters'].Clear()
		modules = sorted((filters.get_filter_name(module), module)
				for name, module in filters.MODULES.iteritems()
				if not name.startswith('test_'))
		for name, module in modules:
			category = filters.get_filter_category(module)
			if category == filters.const.CATEGORY_MODIFICATOR:
				self._lb_modificators.Append(name, module)
			elif category == filters.const.CATEGORY_DECORATOR:
				self._lb_decorators.Append(name, module)
			else:
				if category != filters.const.CATEGORY_SIMPLE:
					self._lb_filters.Append(name, module)
				self._lb_simple.Append(name, module)
			lb_all_filters.Append(name, module)
		self._lb_filters.SetSelection(0)
		self._lb_modificators.SetSelection(0)
		self._lb_decorators.SetSelection(0)
		self._lb_simple.SetSelection(0)

	def _get_modules_to_process(self):
		page_selected = self['notebook'].GetSelection()
		if page_selected == 0:  # simple
			modules = [self._lb_simple.GetClientData(
					self._lb_simple.GetSelection())]
		elif page_selected == 1:  # advanced
			modules = [listbox.GetClientData(listbox.GetSelection())
					for listbox in (self._lb_filters, self._lb_modificators,
							self._lb_decorators)]
		else:  # expert
			lb_used_filters = self['lb_used_filters']
			modules = [lb_used_filters.GetClientData(idx)
					for idx in xrange(lb_used_filters.GetCount())]
		modules = filter(None, modules)
		all_steps = sum((module.STEPS if hasattr(module, 'STEPS') else 20)
				for module in modules)
		return modules, all_steps

	@debug.log
	def _process(self, images, attr):
		images = list(images if hasattr(images, '__iter__') else (images, ))
		if not images:
			return
		modules, all_steps = self._get_modules_to_process()
		if not modules:
			for image in images:
				image.processed = getattr(image, attr).copy()
				yield image
			return
		self.wnd.SetStatusText(_("Processing..."))
		all_steps *= len(images)
		progress_dlg = wx.ProgressDialog(_("Processing images"),
				_("Starting..."), all_steps, self.wnd,
				wx.PD_AUTO_HIDE | wx.PD_APP_MODAL | wx.PD_CAN_ABORT)
		progress_dlg.SetSize((400, -1))
		progress_dlg.Show()
		try:
			for idx, msg, image in _process_files(images, modules, attr):
				if not progress_dlg.Update(min(idx, all_steps), msg):
					yield None
					break
				if image:
					yield image
		except Exception, err:
			_LOG.exception("FrameMain._process error")
			progress_dlg.Destroy()
			mbox.message_box_error_ex(self.wnd, _("Error during processing image"),
					str(err))
			self.wnd.SetStatusText('', 1)
		else:
			progress_dlg.Destroy()
			self.wnd.SetStatusText(' + '.join(imap(filters.get_filter_name,
				modules)), 1)
		self.wnd.SetStatusText(_("Ready"))

	def _refresh_filelist(self):
		lc_files = self['lc_files']
		lc_files.DeleteAllItems()
		items = sorted((img['name'], img['icon'], key)
				for key, img in self._files.iteritems())
		for idx, (name, icon, key) in enumerate(items):
			lc_files.InsertImageStringItem(idx, name, icon)
			lc_files.SetItemData(idx, key)
		lc_files.SetColumnWidth(0, -1)

	@wxutils.call_after
	def _show_preview(self, img):
		with wxutils.with_wait_cursor():
			self.wnd.SetStatusText(_("Loading..."))
			sbmp = self['bmp_preview']
			with wxutils.with_freeze(self.wnd, sbmp):
				sbmp.SetBitmap(wx.EmptyImage(1, 1).ConvertToBitmap())
				if img is None:
					return
				wximg = wx_pil.pilimage2wximage(img)
				sbmp.SetBitmap(wximg.ConvertToBitmap())
				sbmp.Refresh()
				sbmp.Update()
		self.wnd.SetStatusText("")

	@debug.log
	@wxutils.call_after
	def _update_preview(self, force_recreate_thumb=False):
		if not self._img:
			return
		with wxutils.with_wait_cursor():
			if force_recreate_thumb or not self._img.thumb:
				size = self['panel_preview'].GetSizeTuple()
				try:
					self._img.create_thumb(size)
				except Exception, err:
					wx.SetCursor(wx.STANDARD_CURSOR)
					mbox.message_box_error_ex(self.wnd, _("Error during processing image"),
						str(err))
					return
			self._img_thumb_processed = None
			self['btn_toggle_orig'].SetValue(False)
			images = list(self._process(self._img, 'thumb'))
			if images:
				image = images[0].processed
				if image:
					self._img_thumb_processed = image
					self._show_preview(image)


def _last_dir():
	return AppConfig().get("frame_main", "last_dir", "")


def _update_last_dir(path):
	return AppConfig().set("frame_main", "last_dir", path)


@debug.log
def _process_files(images, modules, attr):
	msg_templ_f = _("Processing file %(fileno)d/%(allfiles)d %(filename)s")
	msg_templ_s = _("%(module)s %(stepno)d/%(allsteps)d: %(step)s")
	idx = 0
	for fileno, image in enumerate(images):
		img = getattr(image, attr)
		msg_f = msg_templ_f % {'fileno': fileno + 1, 'allfiles': len(images),
					'filename': image.filename}
		for module in modules:
			for stepidx, (msg, img) in enumerate(module.process(img)):
				msg_s = msg_templ_s % {'module': module.NAME,
						'stepno': stepidx + 1, 'allsteps': module.STEPS, 'step': msg}
				idx += 1
				yield idx, msg_f + '\n' + msg_s, None
		image.processed = img
		yield idx, msg, image

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DisplayCls:
	"""Display commands group definition. 67 total commands, 17 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("display", core, parent)

	@property
	def window(self):
		"""window commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_window'):
			from .Window import WindowCls
			self._window = WindowCls(self._core, self._cmd_group)
		return self._window

	@property
	def minfo(self):
		"""minfo commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_minfo'):
			from .Minfo import MinfoCls
			self._minfo = MinfoCls(self._core, self._cmd_group)
		return self._minfo

	@property
	def wselect(self):
		"""wselect commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wselect'):
			from .Wselect import WselectCls
			self._wselect = WselectCls(self._core, self._cmd_group)
		return self._wselect

	@property
	def annotation(self):
		"""annotation commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_annotation'):
			from .Annotation import AnnotationCls
			self._annotation = AnnotationCls(self._core, self._cmd_group)
		return self._annotation

	@property
	def atab(self):
		"""atab commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_atab'):
			from .Atab import AtabCls
			self._atab = AtabCls(self._core, self._cmd_group)
		return self._atab

	@property
	def formatPy(self):
		"""formatPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_formatPy'):
			from .FormatPy import FormatPyCls
			self._formatPy = FormatPyCls(self._core, self._cmd_group)
		return self._formatPy

	@property
	def logo(self):
		"""logo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_logo'):
			from .Logo import LogoCls
			self._logo = LogoCls(self._core, self._cmd_group)
		return self._logo

	@property
	def theme(self):
		"""theme commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_theme'):
			from .Theme import ThemeCls
			self._theme = ThemeCls(self._core, self._cmd_group)
		return self._theme

	@property
	def cmap(self):
		"""cmap commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_cmap'):
			from .Cmap import CmapCls
			self._cmap = CmapCls(self._core, self._cmd_group)
		return self._cmap

	@property
	def faccess(self):
		"""faccess commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_faccess'):
			from .Faccess import FaccessCls
			self._faccess = FaccessCls(self._core, self._cmd_group)
		return self._faccess

	@property
	def preSelector(self):
		"""preSelector commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_preSelector'):
			from .PreSelector import PreSelectorCls
			self._preSelector = PreSelectorCls(self._core, self._cmd_group)
		return self._preSelector

	@property
	def touchscreen(self):
		"""touchscreen commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_touchscreen'):
			from .Touchscreen import TouchscreenCls
			self._touchscreen = TouchscreenCls(self._core, self._cmd_group)
		return self._touchscreen

	@property
	def tbar(self):
		"""tbar commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_tbar'):
			from .Tbar import TbarCls
			self._tbar = TbarCls(self._core, self._cmd_group)
		return self._tbar

	@property
	def sbar(self):
		"""sbar commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sbar'):
			from .Sbar import SbarCls
			self._sbar = SbarCls(self._core, self._cmd_group)
		return self._sbar

	@property
	def skeys(self):
		"""skeys commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_skeys'):
			from .Skeys import SkeysCls
			self._skeys = SkeysCls(self._core, self._cmd_group)
		return self._skeys

	@property
	def iterm(self):
		"""iterm commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_iterm'):
			from .Iterm import ItermCls
			self._iterm = ItermCls(self._core, self._cmd_group)
		return self._iterm

	@property
	def blighting(self):
		"""blighting commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_blighting'):
			from .Blighting import BlightingCls
			self._blighting = BlightingCls(self._core, self._cmd_group)
		return self._blighting

	def clone(self) -> 'DisplayCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DisplayCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

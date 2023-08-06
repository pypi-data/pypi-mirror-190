from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MsrCls:
	"""Msr commands group definition. 9 total commands, 8 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("msr", core, parent)

	@property
	def rfbWidth(self):
		"""rfbWidth commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rfbWidth'):
			from .RfbWidth import RfbWidthCls
			self._rfbWidth = RfbWidthCls(self._core, self._cmd_group)
		return self._rfbWidth

	@property
	def bcategory(self):
		"""bcategory commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bcategory'):
			from .Bcategory import BcategoryCls
			self._bcategory = BcategoryCls(self._core, self._cmd_group)
		return self._bcategory

	@property
	def mpower(self):
		"""mpower commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mpower'):
			from .Mpower import MpowerCls
			self._mpower = MpowerCls(self._core, self._cmd_group)
		return self._mpower

	@property
	def classPy(self):
		"""classPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_classPy'):
			from .ClassPy import ClassPyCls
			self._classPy = ClassPyCls(self._core, self._cmd_group)
		return self._classPy

	@property
	def band(self):
		"""band commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_band'):
			from .Band import BandCls
			self._band = BandCls(self._core, self._cmd_group)
		return self._band

	@property
	def gsm(self):
		"""gsm commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_gsm'):
			from .Gsm import GsmCls
			self._gsm = GsmCls(self._core, self._cmd_group)
		return self._gsm

	@property
	def lte(self):
		"""lte commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_lte'):
			from .Lte import LteCls
			self._lte = LteCls(self._core, self._cmd_group)
		return self._lte

	@property
	def apply(self):
		"""apply commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apply'):
			from .Apply import ApplyCls
			self._apply = ApplyCls(self._core, self._cmd_group)
		return self._apply

	def clone(self) -> 'MsrCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MsrCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

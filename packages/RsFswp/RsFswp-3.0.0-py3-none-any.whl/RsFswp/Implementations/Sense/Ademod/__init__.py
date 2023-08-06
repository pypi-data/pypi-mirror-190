from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AdemodCls:
	"""Ademod commands group definition. 42 total commands, 11 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ademod", core, parent)

	@property
	def af(self):
		"""af commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_af'):
			from .Af import AfCls
			self._af = AfCls(self._core, self._cmd_group)
		return self._af

	@property
	def mtime(self):
		"""mtime commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mtime'):
			from .Mtime import MtimeCls
			self._mtime = MtimeCls(self._core, self._cmd_group)
		return self._mtime

	@property
	def set(self):
		"""set commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_set'):
			from .Set import SetCls
			self._set = SetCls(self._core, self._cmd_group)
		return self._set

	@property
	def am(self):
		"""am commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_am'):
			from .Am import AmCls
			self._am = AmCls(self._core, self._cmd_group)
		return self._am

	@property
	def fm(self):
		"""fm commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_fm'):
			from .Fm import FmCls
			self._fm = FmCls(self._core, self._cmd_group)
		return self._fm

	@property
	def pm(self):
		"""pm commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_pm'):
			from .Pm import PmCls
			self._pm = PmCls(self._core, self._cmd_group)
		return self._pm

	@property
	def spectrum(self):
		"""spectrum commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_spectrum'):
			from .Spectrum import SpectrumCls
			self._spectrum = SpectrumCls(self._core, self._cmd_group)
		return self._spectrum

	@property
	def zoom(self):
		"""zoom commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_zoom'):
			from .Zoom import ZoomCls
			self._zoom = ZoomCls(self._core, self._cmd_group)
		return self._zoom

	@property
	def squelch(self):
		"""squelch commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_squelch'):
			from .Squelch import SquelchCls
			self._squelch = SquelchCls(self._core, self._cmd_group)
		return self._squelch

	@property
	def preset(self):
		"""preset commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_preset'):
			from .Preset import PresetCls
			self._preset = PresetCls(self._core, self._cmd_group)
		return self._preset

	@property
	def adcPrefilter(self):
		"""adcPrefilter commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_adcPrefilter'):
			from .AdcPrefilter import AdcPrefilterCls
			self._adcPrefilter = AdcPrefilterCls(self._core, self._cmd_group)
		return self._adcPrefilter

	def clone(self) -> 'AdemodCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AdemodCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

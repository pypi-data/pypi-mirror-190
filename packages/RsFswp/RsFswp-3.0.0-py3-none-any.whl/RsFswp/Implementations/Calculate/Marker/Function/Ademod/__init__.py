from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AdemodCls:
	"""Ademod commands group definition. 12 total commands, 9 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ademod", core, parent)

	@property
	def am(self):
		"""am commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_am'):
			from .Am import AmCls
			self._am = AmCls(self._core, self._cmd_group)
		return self._am

	@property
	def fm(self):
		"""fm commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fm'):
			from .Fm import FmCls
			self._fm = FmCls(self._core, self._cmd_group)
		return self._fm

	@property
	def pm(self):
		"""pm commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_pm'):
			from .Pm import PmCls
			self._pm = PmCls(self._core, self._cmd_group)
		return self._pm

	@property
	def afrequency(self):
		"""afrequency commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_afrequency'):
			from .Afrequency import AfrequencyCls
			self._afrequency = AfrequencyCls(self._core, self._cmd_group)
		return self._afrequency

	@property
	def freqError(self):
		"""freqError commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_freqError'):
			from .FreqError import FreqErrorCls
			self._freqError = FreqErrorCls(self._core, self._cmd_group)
		return self._freqError

	@property
	def sinad(self):
		"""sinad commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sinad'):
			from .Sinad import SinadCls
			self._sinad = SinadCls(self._core, self._cmd_group)
		return self._sinad

	@property
	def distortion(self):
		"""distortion commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_distortion'):
			from .Distortion import DistortionCls
			self._distortion = DistortionCls(self._core, self._cmd_group)
		return self._distortion

	@property
	def thd(self):
		"""thd commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_thd'):
			from .Thd import ThdCls
			self._thd = ThdCls(self._core, self._cmd_group)
		return self._thd

	@property
	def carrier(self):
		"""carrier commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_carrier'):
			from .Carrier import CarrierCls
			self._carrier = CarrierCls(self._core, self._cmd_group)
		return self._carrier

	def clone(self) -> 'AdemodCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AdemodCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

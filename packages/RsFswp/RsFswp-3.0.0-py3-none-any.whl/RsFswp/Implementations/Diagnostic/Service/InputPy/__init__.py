from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InputPyCls:
	"""InputPy commands group definition. 14 total commands, 7 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("inputPy", core, parent)

	@property
	def emi(self):
		"""emi commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_emi'):
			from .Emi import EmiCls
			self._emi = EmiCls(self._core, self._cmd_group)
		return self._emi

	@property
	def rf(self):
		"""rf commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_rf'):
			from .Rf import RfCls
			self._rf = RfCls(self._core, self._cmd_group)
		return self._rf

	@property
	def mc(self):
		"""mc commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_mc'):
			from .Mc import McCls
			self._mc = McCls(self._core, self._cmd_group)
		return self._mc

	@property
	def aiq(self):
		"""aiq commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_aiq'):
			from .Aiq import AiqCls
			self._aiq = AiqCls(self._core, self._cmd_group)
		return self._aiq

	@property
	def select(self):
		"""select commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_select'):
			from .Select import SelectCls
			self._select = SelectCls(self._core, self._cmd_group)
		return self._select

	@property
	def pulsed(self):
		"""pulsed commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_pulsed'):
			from .Pulsed import PulsedCls
			self._pulsed = PulsedCls(self._core, self._cmd_group)
		return self._pulsed

	@property
	def synthTwo(self):
		"""synthTwo commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_synthTwo'):
			from .SynthTwo import SynthTwoCls
			self._synthTwo = SynthTwoCls(self._core, self._cmd_group)
		return self._synthTwo

	def clone(self) -> 'InputPyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = InputPyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

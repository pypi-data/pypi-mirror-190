from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FunctionCls:
	"""Function commands group definition. 14 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("function", core, parent)

	@property
	def afPhase(self):
		"""afPhase commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_afPhase'):
			from .AfPhase import AfPhaseCls
			self._afPhase = AfPhaseCls(self._core, self._cmd_group)
		return self._afPhase

	@property
	def fixed(self):
		"""fixed commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_fixed'):
			from .Fixed import FixedCls
			self._fixed = FixedCls(self._core, self._cmd_group)
		return self._fixed

	@property
	def pnoise(self):
		"""pnoise commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_pnoise'):
			from .Pnoise import PnoiseCls
			self._pnoise = PnoiseCls(self._core, self._cmd_group)
		return self._pnoise

	@property
	def bpower(self):
		"""bpower commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_bpower'):
			from .Bpower import BpowerCls
			self._bpower = BpowerCls(self._core, self._cmd_group)
		return self._bpower

	def clone(self) -> 'FunctionCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FunctionCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

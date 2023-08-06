from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FactorCls:
	"""Factor commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("factor", core, parent)

	@property
	def numerator(self):
		"""numerator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_numerator'):
			from .Numerator import NumeratorCls
			self._numerator = NumeratorCls(self._core, self._cmd_group)
		return self._numerator

	@property
	def denominator(self):
		"""denominator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_denominator'):
			from .Denominator import DenominatorCls
			self._denominator = DenominatorCls(self._core, self._cmd_group)
		return self._denominator

	def clone(self) -> 'FactorCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FactorCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

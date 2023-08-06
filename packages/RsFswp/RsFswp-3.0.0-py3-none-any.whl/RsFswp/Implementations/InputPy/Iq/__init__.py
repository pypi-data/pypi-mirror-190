from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IqCls:
	"""Iq commands group definition. 14 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("iq", core, parent)

	@property
	def balanced(self):
		"""balanced commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_balanced'):
			from .Balanced import BalancedCls
			self._balanced = BalancedCls(self._core, self._cmd_group)
		return self._balanced

	@property
	def fullscale(self):
		"""fullscale commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_fullscale'):
			from .Fullscale import FullscaleCls
			self._fullscale = FullscaleCls(self._core, self._cmd_group)
		return self._fullscale

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePyCls
			self._typePy = TypePyCls(self._core, self._cmd_group)
		return self._typePy

	@property
	def osc(self):
		"""osc commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_osc'):
			from .Osc import OscCls
			self._osc = OscCls(self._core, self._cmd_group)
		return self._osc

	def clone(self) -> 'IqCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IqCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GsmCls:
	"""Gsm commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("gsm", core, parent)

	@property
	def cpresent(self):
		"""cpresent commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cpresent'):
			from .Cpresent import CpresentCls
			self._cpresent = CpresentCls(self._core, self._cmd_group)
		return self._cpresent

	@property
	def carrier(self):
		"""carrier commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_carrier'):
			from .Carrier import CarrierCls
			self._carrier = CarrierCls(self._core, self._cmd_group)
		return self._carrier

	def clone(self) -> 'GsmCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = GsmCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

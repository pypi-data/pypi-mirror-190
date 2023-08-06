from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PnLimitCls:
	"""PnLimit commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pnLimit", core, parent)

	@property
	def fail(self):
		"""fail commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fail'):
			from .Fail import FailCls
			self._fail = FailCls(self._core, self._cmd_group)
		return self._fail

	@property
	def auto(self):
		"""auto commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_auto'):
			from .Auto import AutoCls
			self._auto = AutoCls(self._core, self._cmd_group)
		return self._auto

	@property
	def fc(self):
		"""fc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fc'):
			from .Fc import FcCls
			self._fc = FcCls(self._core, self._cmd_group)
		return self._fc

	def clone(self) -> 'PnLimitCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PnLimitCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RecordingCls:
	"""Recording commands group definition. 1 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("recording", core, parent)

	@property
	def combine(self):
		"""combine commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_combine'):
			from .Combine import CombineCls
			self._combine = CombineCls(self._core, self._cmd_group)
		return self._combine

	def clone(self) -> 'RecordingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RecordingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

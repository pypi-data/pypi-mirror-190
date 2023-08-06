from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TriggerCls:
	"""Trigger commands group definition. 23 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("trigger", core, parent)

	@property
	def sequence(self):
		"""sequence commands group. 10 Sub-classes, 0 commands."""
		if not hasattr(self, '_sequence'):
			from .Sequence import SequenceCls
			self._sequence = SequenceCls(self._core, self._cmd_group)
		return self._sequence

	@property
	def master(self):
		"""master commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_master'):
			from .Master import MasterCls
			self._master = MasterCls(self._core, self._cmd_group)
		return self._master

	@property
	def sender(self):
		"""sender commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sender'):
			from .Sender import SenderCls
			self._sender = SenderCls(self._core, self._cmd_group)
		return self._sender

	@property
	def iq(self):
		"""iq commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_iq'):
			from .Iq import IqCls
			self._iq = IqCls(self._core, self._cmd_group)
		return self._iq

	def clone(self) -> 'TriggerCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TriggerCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

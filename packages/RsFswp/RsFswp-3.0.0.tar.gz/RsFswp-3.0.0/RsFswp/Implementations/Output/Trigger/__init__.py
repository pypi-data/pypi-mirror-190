from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TriggerCls:
	"""Trigger commands group definition. 5 total commands, 4 Subgroups, 0 group commands
	Repeated Capability: TriggerPort, default value after init: TriggerPort.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("trigger", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_triggerPort_get', 'repcap_triggerPort_set', repcap.TriggerPort.Nr1)

	def repcap_triggerPort_set(self, triggerPort: repcap.TriggerPort) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to TriggerPort.Default
		Default value after init: TriggerPort.Nr1"""
		self._cmd_group.set_repcap_enum_value(triggerPort)

	def repcap_triggerPort_get(self) -> repcap.TriggerPort:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def direction(self):
		"""direction commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_direction'):
			from .Direction import DirectionCls
			self._direction = DirectionCls(self._core, self._cmd_group)
		return self._direction

	@property
	def level(self):
		"""level commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_level'):
			from .Level import LevelCls
			self._level = LevelCls(self._core, self._cmd_group)
		return self._level

	@property
	def otype(self):
		"""otype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_otype'):
			from .Otype import OtypeCls
			self._otype = OtypeCls(self._core, self._cmd_group)
		return self._otype

	@property
	def pulse(self):
		"""pulse commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_pulse'):
			from .Pulse import PulseCls
			self._pulse = PulseCls(self._core, self._cmd_group)
		return self._pulse

	def clone(self) -> 'TriggerCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TriggerCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

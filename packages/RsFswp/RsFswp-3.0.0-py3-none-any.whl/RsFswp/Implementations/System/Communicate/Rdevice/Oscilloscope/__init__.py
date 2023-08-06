from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OscilloscopeCls:
	"""Oscilloscope commands group definition. 8 total commands, 7 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("oscilloscope", core, parent)

	@property
	def alignment(self):
		"""alignment commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_alignment'):
			from .Alignment import AlignmentCls
			self._alignment = AlignmentCls(self._core, self._cmd_group)
		return self._alignment

	@property
	def idn(self):
		"""idn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_idn'):
			from .Idn import IdnCls
			self._idn = IdnCls(self._core, self._cmd_group)
		return self._idn

	@property
	def ledState(self):
		"""ledState commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ledState'):
			from .LedState import LedStateCls
			self._ledState = LedStateCls(self._core, self._cmd_group)
		return self._ledState

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def tcpip(self):
		"""tcpip commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tcpip'):
			from .Tcpip import TcpipCls
			self._tcpip = TcpipCls(self._core, self._cmd_group)
		return self._tcpip

	@property
	def vdevice(self):
		"""vdevice commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vdevice'):
			from .Vdevice import VdeviceCls
			self._vdevice = VdeviceCls(self._core, self._cmd_group)
		return self._vdevice

	@property
	def vfirmware(self):
		"""vfirmware commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vfirmware'):
			from .Vfirmware import VfirmwareCls
			self._vfirmware = VfirmwareCls(self._core, self._cmd_group)
		return self._vfirmware

	def clone(self) -> 'OscilloscopeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = OscilloscopeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

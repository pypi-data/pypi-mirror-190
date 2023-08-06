from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MixerCls:
	"""Mixer commands group definition. 22 total commands, 10 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mixer", core, parent)

	@property
	def loPower(self):
		"""loPower commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_loPower'):
			from .LoPower import LoPowerCls
			self._loPower = LoPowerCls(self._core, self._cmd_group)
		return self._loPower

	@property
	def ports(self):
		"""ports commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ports'):
			from .Ports import PortsCls
			self._ports = PortsCls(self._core, self._cmd_group)
		return self._ports

	@property
	def signal(self):
		"""signal commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_signal'):
			from .Signal import SignalCls
			self._signal = SignalCls(self._core, self._cmd_group)
		return self._signal

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def threshold(self):
		"""threshold commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_threshold'):
			from .Threshold import ThresholdCls
			self._threshold = ThresholdCls(self._core, self._cmd_group)
		return self._threshold

	@property
	def bias(self):
		"""bias commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_bias'):
			from .Bias import BiasCls
			self._bias = BiasCls(self._core, self._cmd_group)
		return self._bias

	@property
	def harmonic(self):
		"""harmonic commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_harmonic'):
			from .Harmonic import HarmonicCls
			self._harmonic = HarmonicCls(self._core, self._cmd_group)
		return self._harmonic

	@property
	def frequency(self):
		"""frequency commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	@property
	def loss(self):
		"""loss commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_loss'):
			from .Loss import LossCls
			self._loss = LossCls(self._core, self._cmd_group)
		return self._loss

	@property
	def rfOverrange(self):
		"""rfOverrange commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_rfOverrange'):
			from .RfOverrange import RfOverrangeCls
			self._rfOverrange = RfOverrangeCls(self._core, self._cmd_group)
		return self._rfOverrange

	def clone(self) -> 'MixerCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MixerCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

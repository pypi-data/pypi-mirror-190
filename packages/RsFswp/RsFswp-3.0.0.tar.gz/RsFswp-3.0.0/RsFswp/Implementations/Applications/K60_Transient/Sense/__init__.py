from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SenseCls:
	"""Sense commands group definition. 51 total commands, 7 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sense", core, parent)

	@property
	def adjust(self):
		"""adjust commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_adjust'):
			from .Adjust import AdjustCls
			self._adjust = AdjustCls(self._core, self._cmd_group)
		return self._adjust

	@property
	def correction(self):
		"""correction commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_correction'):
			from .Correction import CorrectionCls
			self._correction = CorrectionCls(self._core, self._cmd_group)
		return self._correction

	@property
	def frequency(self):
		"""frequency commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	@property
	def mixer(self):
		"""mixer commands group. 10 Sub-classes, 0 commands."""
		if not hasattr(self, '_mixer'):
			from .Mixer import MixerCls
			self._mixer = MixerCls(self._core, self._cmd_group)
		return self._mixer

	@property
	def probe(self):
		"""probe commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_probe'):
			from .Probe import ProbeCls
			self._probe = ProbeCls(self._core, self._cmd_group)
		return self._probe

	@property
	def msra(self):
		"""msra commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_msra'):
			from .Msra import MsraCls
			self._msra = MsraCls(self._core, self._cmd_group)
		return self._msra

	@property
	def sweep(self):
		"""sweep commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sweep'):
			from .Sweep import SweepCls
			self._sweep = SweepCls(self._core, self._cmd_group)
		return self._sweep

	def clone(self) -> 'SenseCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SenseCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

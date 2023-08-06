from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SenseCls:
	"""Sense commands group definition. 131 total commands, 13 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sense", core, parent)

	@property
	def adjust(self):
		"""adjust commands group. 2 Sub-classes, 0 commands."""
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
		"""frequency commands group. 1 Sub-classes, 0 commands."""
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
	def directed(self):
		"""directed commands group. 7 Sub-classes, 2 commands."""
		if not hasattr(self, '_directed'):
			from .Directed import DirectedCls
			self._directed = DirectedCls(self._core, self._cmd_group)
		return self._directed

	@property
	def fplan(self):
		"""fplan commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_fplan'):
			from .Fplan import FplanCls
			self._fplan = FplanCls(self._core, self._cmd_group)
		return self._fplan

	@property
	def listPy(self):
		"""listPy commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_listPy'):
			from .ListPy import ListPyCls
			self._listPy = ListPyCls(self._core, self._cmd_group)
		return self._listPy

	@property
	def pmeter(self):
		"""pmeter commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_pmeter'):
			from .Pmeter import PmeterCls
			self._pmeter = PmeterCls(self._core, self._cmd_group)
		return self._pmeter

	@property
	def measure(self):
		"""measure commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_measure'):
			from .Measure import MeasureCls
			self._measure = MeasureCls(self._core, self._cmd_group)
		return self._measure

	@property
	def creference(self):
		"""creference commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_creference'):
			from .Creference import CreferenceCls
			self._creference = CreferenceCls(self._core, self._cmd_group)
		return self._creference

	@property
	def ssearch(self):
		"""ssearch commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_ssearch'):
			from .Ssearch import SsearchCls
			self._ssearch = SsearchCls(self._core, self._cmd_group)
		return self._ssearch

	@property
	def transfer(self):
		"""transfer commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_transfer'):
			from .Transfer import TransferCls
			self._transfer = TransferCls(self._core, self._cmd_group)
		return self._transfer

	def clone(self) -> 'SenseCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SenseCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

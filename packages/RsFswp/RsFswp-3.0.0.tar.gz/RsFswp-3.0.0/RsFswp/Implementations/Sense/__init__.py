from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SenseCls:
	"""Sense commands group definition. 460 total commands, 26 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sense", core, parent)

	@property
	def roscillator(self):
		"""roscillator commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_roscillator'):
			from .Roscillator import RoscillatorCls
			self._roscillator = RoscillatorCls(self._core, self._cmd_group)
		return self._roscillator

	@property
	def adjust(self):
		"""adjust commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_adjust'):
			from .Adjust import AdjustCls
			self._adjust = AdjustCls(self._core, self._cmd_group)
		return self._adjust

	@property
	def power(self):
		"""power commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def sweep(self):
		"""sweep commands group. 10 Sub-classes, 0 commands."""
		if not hasattr(self, '_sweep'):
			from .Sweep import SweepCls
			self._sweep = SweepCls(self._core, self._cmd_group)
		return self._sweep

	@property
	def mixer(self):
		"""mixer commands group. 11 Sub-classes, 0 commands."""
		if not hasattr(self, '_mixer'):
			from .Mixer import MixerCls
			self._mixer = MixerCls(self._core, self._cmd_group)
		return self._mixer

	@property
	def correction(self):
		"""correction commands group. 6 Sub-classes, 1 commands."""
		if not hasattr(self, '_correction'):
			from .Correction import CorrectionCls
			self._correction = CorrectionCls(self._core, self._cmd_group)
		return self._correction

	@property
	def rlength(self):
		"""rlength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rlength'):
			from .Rlength import RlengthCls
			self._rlength = RlengthCls(self._core, self._cmd_group)
		return self._rlength

	@property
	def rtms(self):
		"""rtms commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_rtms'):
			from .Rtms import RtmsCls
			self._rtms = RtmsCls(self._core, self._cmd_group)
		return self._rtms

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symbolRate'):
			from .SymbolRate import SymbolRateCls
			self._symbolRate = SymbolRateCls(self._core, self._cmd_group)
		return self._symbolRate

	@property
	def swapIq(self):
		"""swapIq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_swapIq'):
			from .SwapIq import SwapIqCls
			self._swapIq = SwapIqCls(self._core, self._cmd_group)
		return self._swapIq

	@property
	def ademod(self):
		"""ademod commands group. 11 Sub-classes, 0 commands."""
		if not hasattr(self, '_ademod'):
			from .Ademod import AdemodCls
			self._ademod = AdemodCls(self._core, self._cmd_group)
		return self._ademod

	@property
	def bandwidth(self):
		"""bandwidth commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_bandwidth'):
			from .Bandwidth import BandwidthCls
			self._bandwidth = BandwidthCls(self._core, self._cmd_group)
		return self._bandwidth

	@property
	def ddemod(self):
		"""ddemod commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ddemod'):
			from .Ddemod import DdemodCls
			self._ddemod = DdemodCls(self._core, self._cmd_group)
		return self._ddemod

	@property
	def filterPy(self):
		"""filterPy commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_filterPy'):
			from .FilterPy import FilterPyCls
			self._filterPy = FilterPyCls(self._core, self._cmd_group)
		return self._filterPy

	@property
	def frequency(self):
		"""frequency commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	@property
	def iq(self):
		"""iq commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_iq'):
			from .Iq import IqCls
			self._iq = IqCls(self._core, self._cmd_group)
		return self._iq

	@property
	def listPy(self):
		"""listPy commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_listPy'):
			from .ListPy import ListPyCls
			self._listPy = ListPyCls(self._core, self._cmd_group)
		return self._listPy

	@property
	def espectrum(self):
		"""espectrum commands group. 11 Sub-classes, 0 commands."""
		if not hasattr(self, '_espectrum'):
			from .Espectrum import EspectrumCls
			self._espectrum = EspectrumCls(self._core, self._cmd_group)
		return self._espectrum

	@property
	def mpower(self):
		"""mpower commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_mpower'):
			from .Mpower import MpowerCls
			self._mpower = MpowerCls(self._core, self._cmd_group)
		return self._mpower

	@property
	def pmeter(self):
		"""pmeter commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_pmeter'):
			from .Pmeter import PmeterCls
			self._pmeter = PmeterCls(self._core, self._cmd_group)
		return self._pmeter

	@property
	def probe(self):
		"""probe commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_probe'):
			from .Probe import ProbeCls
			self._probe = ProbeCls(self._core, self._cmd_group)
		return self._probe

	@property
	def sampling(self):
		"""sampling commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sampling'):
			from .Sampling import SamplingCls
			self._sampling = SamplingCls(self._core, self._cmd_group)
		return self._sampling

	@property
	def trace(self):
		"""trace commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_trace'):
			from .Trace import TraceCls
			self._trace = TraceCls(self._core, self._cmd_group)
		return self._trace

	@property
	def average(self):
		"""average commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_average'):
			from .Average import AverageCls
			self._average = AverageCls(self._core, self._cmd_group)
		return self._average

	@property
	def msra(self):
		"""msra commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_msra'):
			from .Msra import MsraCls
			self._msra = MsraCls(self._core, self._cmd_group)
		return self._msra

	@property
	def window(self):
		"""window commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_window'):
			from .Window import WindowCls
			self._window = WindowCls(self._core, self._cmd_group)
		return self._window

	def clone(self) -> 'SenseCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SenseCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

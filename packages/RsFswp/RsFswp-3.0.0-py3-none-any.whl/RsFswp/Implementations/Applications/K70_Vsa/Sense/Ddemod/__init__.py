from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DdemodCls:
	"""Ddemod commands group definition. 131 total commands, 32 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ddemod", core, parent)

	@property
	def bordering(self):
		"""bordering commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bordering'):
			from .Bordering import BorderingCls
			self._bordering = BorderingCls(self._core, self._cmd_group)
		return self._bordering

	@property
	def formatPy(self):
		"""formatPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_formatPy'):
			from .FormatPy import FormatPyCls
			self._formatPy = FormatPyCls(self._core, self._cmd_group)
		return self._formatPy

	@property
	def pattern(self):
		"""pattern commands group. 10 Sub-classes, 0 commands."""
		if not hasattr(self, '_pattern'):
			from .Pattern import PatternCls
			self._pattern = PatternCls(self._core, self._cmd_group)
		return self._pattern

	@property
	def prate(self):
		"""prate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prate'):
			from .Prate import PrateCls
			self._prate = PrateCls(self._core, self._cmd_group)
		return self._prate

	@property
	def optimization(self):
		"""optimization commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_optimization'):
			from .Optimization import OptimizationCls
			self._optimization = OptimizationCls(self._core, self._cmd_group)
		return self._optimization

	@property
	def sband(self):
		"""sband commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sband'):
			from .Sband import SbandCls
			self._sband = SbandCls(self._core, self._cmd_group)
		return self._sband

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symbolRate'):
			from .SymbolRate import SymbolRateCls
			self._symbolRate = SymbolRateCls(self._core, self._cmd_group)
		return self._symbolRate

	@property
	def time(self):
		"""time commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_time'):
			from .Time import TimeCls
			self._time = TimeCls(self._core, self._cmd_group)
		return self._time

	@property
	def ecalc(self):
		"""ecalc commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ecalc'):
			from .Ecalc import EcalcCls
			self._ecalc = EcalcCls(self._core, self._cmd_group)
		return self._ecalc

	@property
	def equalizer(self):
		"""equalizer commands group. 6 Sub-classes, 1 commands."""
		if not hasattr(self, '_equalizer'):
			from .Equalizer import EqualizerCls
			self._equalizer = EqualizerCls(self._core, self._cmd_group)
		return self._equalizer

	@property
	def epRate(self):
		"""epRate commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_epRate'):
			from .EpRate import EpRateCls
			self._epRate = EpRateCls(self._core, self._cmd_group)
		return self._epRate

	@property
	def normalize(self):
		"""normalize commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_normalize'):
			from .Normalize import NormalizeCls
			self._normalize = NormalizeCls(self._core, self._cmd_group)
		return self._normalize

	@property
	def fsk(self):
		"""fsk commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fsk'):
			from .Fsk import FskCls
			self._fsk = FskCls(self._core, self._cmd_group)
		return self._fsk

	@property
	def ask(self):
		"""ask commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ask'):
			from .Ask import AskCls
			self._ask = AskCls(self._core, self._cmd_group)
		return self._ask

	@property
	def apsk(self):
		"""apsk commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_apsk'):
			from .Apsk import ApskCls
			self._apsk = ApskCls(self._core, self._cmd_group)
		return self._apsk

	@property
	def fsync(self):
		"""fsync commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_fsync'):
			from .Fsync import FsyncCls
			self._fsync = FsyncCls(self._core, self._cmd_group)
		return self._fsync

	@property
	def kdata(self):
		"""kdata commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_kdata'):
			from .Kdata import KdataCls
			self._kdata = KdataCls(self._core, self._cmd_group)
		return self._kdata

	@property
	def msk(self):
		"""msk commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_msk'):
			from .Msk import MskCls
			self._msk = MskCls(self._core, self._cmd_group)
		return self._msk

	@property
	def psk(self):
		"""psk commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_psk'):
			from .Psk import PskCls
			self._psk = PskCls(self._core, self._cmd_group)
		return self._psk

	@property
	def signal(self):
		"""signal commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_signal'):
			from .Signal import SignalCls
			self._signal = SignalCls(self._core, self._cmd_group)
		return self._signal

	@property
	def qam(self):
		"""qam commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_qam'):
			from .Qam import QamCls
			self._qam = QamCls(self._core, self._cmd_group)
		return self._qam

	@property
	def qpsk(self):
		"""qpsk commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_qpsk'):
			from .Qpsk import QpskCls
			self._qpsk = QpskCls(self._core, self._cmd_group)
		return self._qpsk

	@property
	def rlength(self):
		"""rlength commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_rlength'):
			from .Rlength import RlengthCls
			self._rlength = RlengthCls(self._core, self._cmd_group)
		return self._rlength

	@property
	def search(self):
		"""search commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_search'):
			from .Search import SearchCls
			self._search = SearchCls(self._core, self._cmd_group)
		return self._search

	@property
	def standard(self):
		"""standard commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_standard'):
			from .Standard import StandardCls
			self._standard = StandardCls(self._core, self._cmd_group)
		return self._standard

	@property
	def factory(self):
		"""factory commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_factory'):
			from .Factory import FactoryCls
			self._factory = FactoryCls(self._core, self._cmd_group)
		return self._factory

	@property
	def filterPy(self):
		"""filterPy commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_filterPy'):
			from .FilterPy import FilterPyCls
			self._filterPy = FilterPyCls(self._core, self._cmd_group)
		return self._filterPy

	@property
	def mfilter(self):
		"""mfilter commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_mfilter'):
			from .Mfilter import MfilterCls
			self._mfilter = MfilterCls(self._core, self._cmd_group)
		return self._mfilter

	@property
	def tfilter(self):
		"""tfilter commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_tfilter'):
			from .Tfilter import TfilterCls
			self._tfilter = TfilterCls(self._core, self._cmd_group)
		return self._tfilter

	@property
	def mapping(self):
		"""mapping commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_mapping'):
			from .Mapping import MappingCls
			self._mapping = MappingCls(self._core, self._cmd_group)
		return self._mapping

	@property
	def preset(self):
		"""preset commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_preset'):
			from .Preset import PresetCls
			self._preset = PresetCls(self._core, self._cmd_group)
		return self._preset

	@property
	def user(self):
		"""user commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_user'):
			from .User import UserCls
			self._user = UserCls(self._core, self._cmd_group)
		return self._user

	def clone(self) -> 'DdemodCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DdemodCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

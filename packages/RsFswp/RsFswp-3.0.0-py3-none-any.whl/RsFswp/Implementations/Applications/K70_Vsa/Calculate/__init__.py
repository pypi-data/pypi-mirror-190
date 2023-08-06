from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CalculateCls:
	"""Calculate commands group definition. 212 total commands, 21 Subgroups, 0 group commands
	Repeated Capability: Window, default value after init: Window.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("calculate", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_window_get', 'repcap_window_set', repcap.Window.Nr1)

	def repcap_window_set(self, window: repcap.Window) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Window.Default
		Default value after init: Window.Nr1"""
		self._cmd_group.set_repcap_enum_value(window)

	def repcap_window_get(self) -> repcap.Window:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def bitErrorRate(self):
		"""bitErrorRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bitErrorRate'):
			from .BitErrorRate import BitErrorRateCls
			self._bitErrorRate = BitErrorRateCls(self._core, self._cmd_group)
		return self._bitErrorRate

	@property
	def msra(self):
		"""msra commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_msra'):
			from .Msra import MsraCls
			self._msra = MsraCls(self._core, self._cmd_group)
		return self._msra

	@property
	def feed(self):
		"""feed commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_feed'):
			from .Feed import FeedCls
			self._feed = FeedCls(self._core, self._cmd_group)
		return self._feed

	@property
	def formatPy(self):
		"""formatPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_formatPy'):
			from .FormatPy import FormatPyCls
			self._formatPy = FormatPyCls(self._core, self._cmd_group)
		return self._formatPy

	@property
	def ddem(self):
		"""ddem commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ddem'):
			from .Ddem import DdemCls
			self._ddem = DdemCls(self._core, self._cmd_group)
		return self._ddem

	@property
	def dlabs(self):
		"""dlabs commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_dlabs'):
			from .Dlabs import DlabsCls
			self._dlabs = DlabsCls(self._core, self._cmd_group)
		return self._dlabs

	@property
	def dlRel(self):
		"""dlRel commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_dlRel'):
			from .DlRel import DlRelCls
			self._dlRel = DlRelCls(self._core, self._cmd_group)
		return self._dlRel

	@property
	def dsp(self):
		"""dsp commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_dsp'):
			from .Dsp import DspCls
			self._dsp = DspCls(self._core, self._cmd_group)
		return self._dsp

	@property
	def meas(self):
		"""meas commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_meas'):
			from .Meas import MeasCls
			self._meas = MeasCls(self._core, self._cmd_group)
		return self._meas

	@property
	def elin(self):
		"""elin commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_elin'):
			from .Elin import ElinCls
			self._elin = ElinCls(self._core, self._cmd_group)
		return self._elin

	@property
	def fsk(self):
		"""fsk commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fsk'):
			from .Fsk import FskCls
			self._fsk = FskCls(self._core, self._cmd_group)
		return self._fsk

	@property
	def limit(self):
		"""limit commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_limit'):
			from .Limit import LimitCls
			self._limit = LimitCls(self._core, self._cmd_group)
		return self._limit

	@property
	def marker(self):
		"""marker commands group. 11 Sub-classes, 0 commands."""
		if not hasattr(self, '_marker'):
			from .Marker import MarkerCls
			self._marker = MarkerCls(self._core, self._cmd_group)
		return self._marker

	@property
	def deltaMarker(self):
		"""deltaMarker commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_deltaMarker'):
			from .DeltaMarker import DeltaMarkerCls
			self._deltaMarker = DeltaMarkerCls(self._core, self._cmd_group)
		return self._deltaMarker

	@property
	def statistics(self):
		"""statistics commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_statistics'):
			from .Statistics import StatisticsCls
			self._statistics = StatisticsCls(self._core, self._cmd_group)
		return self._statistics

	@property
	def tlRel(self):
		"""tlRel commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_tlRel'):
			from .TlRel import TlRelCls
			self._tlRel = TlRelCls(self._core, self._cmd_group)
		return self._tlRel

	@property
	def tlAbs(self):
		"""tlAbs commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_tlAbs'):
			from .TlAbs import TlAbsCls
			self._tlAbs = TlAbsCls(self._core, self._cmd_group)
		return self._tlAbs

	@property
	def trace(self):
		"""trace commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_trace'):
			from .Trace import TraceCls
			self._trace = TraceCls(self._core, self._cmd_group)
		return self._trace

	@property
	def unit(self):
		"""unit commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_unit'):
			from .Unit import UnitCls
			self._unit = UnitCls(self._core, self._cmd_group)
		return self._unit

	@property
	def x(self):
		"""x commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_x'):
			from .X import XCls
			self._x = XCls(self._core, self._cmd_group)
		return self._x

	@property
	def y(self):
		"""y commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_y'):
			from .Y import YCls
			self._y = YCls(self._core, self._cmd_group)
		return self._y

	def clone(self) -> 'CalculateCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CalculateCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

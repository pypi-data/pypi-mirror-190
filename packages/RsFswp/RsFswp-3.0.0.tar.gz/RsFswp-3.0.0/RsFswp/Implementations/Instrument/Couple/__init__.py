from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CoupleCls:
	"""Couple commands group definition. 21 total commands, 17 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("couple", core, parent)

	@property
	def center(self):
		"""center commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_center'):
			from .Center import CenterCls
			self._center = CenterCls(self._core, self._cmd_group)
		return self._center

	@property
	def span(self):
		"""span commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_span'):
			from .Span import SpanCls
			self._span = SpanCls(self._core, self._cmd_group)
		return self._span

	@property
	def refLevel(self):
		"""refLevel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_refLevel'):
			from .RefLevel import RefLevelCls
			self._refLevel = RefLevelCls(self._core, self._cmd_group)
		return self._refLevel

	@property
	def atten(self):
		"""atten commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_atten'):
			from .Atten import AttenCls
			self._atten = AttenCls(self._core, self._cmd_group)
		return self._atten

	@property
	def gain(self):
		"""gain commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gain'):
			from .Gain import GainCls
			self._gain = GainCls(self._core, self._cmd_group)
		return self._gain

	@property
	def presel(self):
		"""presel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_presel'):
			from .Presel import PreselCls
			self._presel = PreselCls(self._core, self._cmd_group)
		return self._presel

	@property
	def demod(self):
		"""demod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_demod'):
			from .Demod import DemodCls
			self._demod = DemodCls(self._core, self._cmd_group)
		return self._demod

	@property
	def bandwidth(self):
		"""bandwidth commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bandwidth'):
			from .Bandwidth import BandwidthCls
			self._bandwidth = BandwidthCls(self._core, self._cmd_group)
		return self._bandwidth

	@property
	def vbw(self):
		"""vbw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vbw'):
			from .Vbw import VbwCls
			self._vbw = VbwCls(self._core, self._cmd_group)
		return self._vbw

	@property
	def llines(self):
		"""llines commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_llines'):
			from .Llines import LlinesCls
			self._llines = LlinesCls(self._core, self._cmd_group)
		return self._llines

	@property
	def limit(self):
		"""limit commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_limit'):
			from .Limit import LimitCls
			self._limit = LimitCls(self._core, self._cmd_group)
		return self._limit

	@property
	def acDc(self):
		"""acDc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_acDc'):
			from .AcDc import AcDcCls
			self._acDc = AcDcCls(self._core, self._cmd_group)
		return self._acDc

	@property
	def aunit(self):
		"""aunit commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aunit'):
			from .Aunit import AunitCls
			self._aunit = AunitCls(self._core, self._cmd_group)
		return self._aunit

	@property
	def impedance(self):
		"""impedance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_impedance'):
			from .Impedance import ImpedanceCls
			self._impedance = ImpedanceCls(self._core, self._cmd_group)
		return self._impedance

	@property
	def abImpedance(self):
		"""abImpedance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_abImpedance'):
			from .AbImpedance import AbImpedanceCls
			self._abImpedance = AbImpedanceCls(self._core, self._cmd_group)
		return self._abImpedance

	@property
	def marker(self):
		"""marker commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_marker'):
			from .Marker import MarkerCls
			self._marker = MarkerCls(self._core, self._cmd_group)
		return self._marker

	@property
	def generator(self):
		"""generator commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_generator'):
			from .Generator import GeneratorCls
			self._generator = GeneratorCls(self._core, self._cmd_group)
		return self._generator

	def clone(self) -> 'CoupleCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CoupleCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

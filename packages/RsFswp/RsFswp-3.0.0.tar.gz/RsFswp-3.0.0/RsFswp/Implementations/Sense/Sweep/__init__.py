from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SweepCls:
	"""Sweep commands group definition. 31 total commands, 10 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sweep", core, parent)

	@property
	def points(self):
		"""points commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_points'):
			from .Points import PointsCls
			self._points = PointsCls(self._core, self._cmd_group)
		return self._points

	@property
	def scapture(self):
		"""scapture commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_scapture'):
			from .Scapture import ScaptureCls
			self._scapture = ScaptureCls(self._core, self._cmd_group)
		return self._scapture

	@property
	def time(self):
		"""time commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_time'):
			from .Time import TimeCls
			self._time = TimeCls(self._core, self._cmd_group)
		return self._time

	@property
	def egate(self):
		"""egate commands group. 8 Sub-classes, 1 commands."""
		if not hasattr(self, '_egate'):
			from .Egate import EgateCls
			self._egate = EgateCls(self._core, self._cmd_group)
		return self._egate

	@property
	def duration(self):
		"""duration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_duration'):
			from .Duration import DurationCls
			self._duration = DurationCls(self._core, self._cmd_group)
		return self._duration

	@property
	def window(self):
		"""window commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_window'):
			from .Window import WindowCls
			self._window = WindowCls(self._core, self._cmd_group)
		return self._window

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import ModeCls
			self._mode = ModeCls(self._core, self._cmd_group)
		return self._mode

	@property
	def typePy(self):
		"""typePy commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePyCls
			self._typePy = TypePyCls(self._core, self._cmd_group)
		return self._typePy

	@property
	def optimize(self):
		"""optimize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_optimize'):
			from .Optimize import OptimizeCls
			self._optimize = OptimizeCls(self._core, self._cmd_group)
		return self._optimize

	@property
	def count(self):
		"""count commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_count'):
			from .Count import CountCls
			self._count = CountCls(self._core, self._cmd_group)
		return self._count

	def clone(self) -> 'SweepCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SweepCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

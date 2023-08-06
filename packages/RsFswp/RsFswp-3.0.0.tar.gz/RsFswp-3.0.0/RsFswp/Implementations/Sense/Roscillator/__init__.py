from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RoscillatorCls:
	"""Roscillator commands group definition. 12 total commands, 9 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("roscillator", core, parent)

	@property
	def o100(self):
		"""o100 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_o100'):
			from .O100 import O100Cls
			self._o100 = O100Cls(self._core, self._cmd_group)
		return self._o100

	@property
	def o640(self):
		"""o640 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_o640'):
			from .O640 import O640Cls
			self._o640 = O640Cls(self._core, self._cmd_group)
		return self._o640

	@property
	def source(self):
		"""source commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_source'):
			from .Source import SourceCls
			self._source = SourceCls(self._core, self._cmd_group)
		return self._source

	@property
	def trange(self):
		"""trange commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_trange'):
			from .Trange import TrangeCls
			self._trange = TrangeCls(self._core, self._cmd_group)
		return self._trange

	@property
	def lbWidth(self):
		"""lbWidth commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lbWidth'):
			from .LbWidth import LbWidthCls
			self._lbWidth = LbWidthCls(self._core, self._cmd_group)
		return self._lbWidth

	@property
	def osync(self):
		"""osync commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_osync'):
			from .Osync import OsyncCls
			self._osync = OsyncCls(self._core, self._cmd_group)
		return self._osync

	@property
	def coupling(self):
		"""coupling commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_coupling'):
			from .Coupling import CouplingCls
			self._coupling = CouplingCls(self._core, self._cmd_group)
		return self._coupling

	@property
	def output(self):
		"""output commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_output'):
			from .Output import OutputCls
			self._output = OutputCls(self._core, self._cmd_group)
		return self._output

	@property
	def passThrough(self):
		"""passThrough commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_passThrough'):
			from .PassThrough import PassThroughCls
			self._passThrough = PassThroughCls(self._core, self._cmd_group)
		return self._passThrough

	def clone(self) -> 'RoscillatorCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RoscillatorCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

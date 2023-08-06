from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ItemCls:
	"""Item commands group definition. 10 total commands, 10 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("item", core, parent)

	@property
	def default(self):
		"""default commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_default'):
			from .Default import DefaultCls
			self._default = DefaultCls(self._core, self._cmd_group)
		return self._default

	@property
	def nonePy(self):
		"""nonePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nonePy'):
			from .NonePy import NonePyCls
			self._nonePy = NonePyCls(self._core, self._cmd_group)
		return self._nonePy

	@property
	def all(self):
		"""all commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_all'):
			from .All import AllCls
			self._all = AllCls(self._core, self._cmd_group)
		return self._all

	@property
	def hwSettings(self):
		"""hwSettings commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hwSettings'):
			from .HwSettings import HwSettingsCls
			self._hwSettings = HwSettingsCls(self._core, self._cmd_group)
		return self._hwSettings

	@property
	def lines(self):
		"""lines commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_lines'):
			from .Lines import LinesCls
			self._lines = LinesCls(self._core, self._cmd_group)
		return self._lines

	@property
	def scData(self):
		"""scData commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scData'):
			from .ScData import ScDataCls
			self._scData = ScDataCls(self._core, self._cmd_group)
		return self._scData

	@property
	def spectrogram(self):
		"""spectrogram commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spectrogram'):
			from .Spectrogram import SpectrogramCls
			self._spectrogram = SpectrogramCls(self._core, self._cmd_group)
		return self._spectrogram

	@property
	def trace(self):
		"""trace commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_trace'):
			from .Trace import TraceCls
			self._trace = TraceCls(self._core, self._cmd_group)
		return self._trace

	@property
	def transducer(self):
		"""transducer commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_transducer'):
			from .Transducer import TransducerCls
			self._transducer = TransducerCls(self._core, self._cmd_group)
		return self._transducer

	@property
	def weighting(self):
		"""weighting commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_weighting'):
			from .Weighting import WeightingCls
			self._weighting = WeightingCls(self._core, self._cmd_group)
		return self._weighting

	def clone(self) -> 'ItemCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ItemCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

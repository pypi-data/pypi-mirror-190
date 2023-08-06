from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowerCls:
	"""Lower commands group definition. 8 total commands, 8 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lower", core, parent)

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def offset(self):
		"""offset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_offset'):
			from .Offset import OffsetCls
			self._offset = OffsetCls(self._core, self._cmd_group)
		return self._offset

	@property
	def margin(self):
		"""margin commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_margin'):
			from .Margin import MarginCls
			self._margin = MarginCls(self._core, self._cmd_group)
		return self._margin

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import ModeCls
			self._mode = ModeCls(self._core, self._cmd_group)
		return self._mode

	@property
	def shift(self):
		"""shift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_shift'):
			from .Shift import ShiftCls
			self._shift = ShiftCls(self._core, self._cmd_group)
		return self._shift

	@property
	def spacing(self):
		"""spacing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spacing'):
			from .Spacing import SpacingCls
			self._spacing = SpacingCls(self._core, self._cmd_group)
		return self._spacing

	@property
	def threshold(self):
		"""threshold commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_threshold'):
			from .Threshold import ThresholdCls
			self._threshold = ThresholdCls(self._core, self._cmd_group)
		return self._threshold

	def clone(self) -> 'LowerCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = LowerCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

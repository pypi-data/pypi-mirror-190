from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SetupCls:
	"""Setup commands group definition. 10 total commands, 10 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("setup", core, parent)

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import ModeCls
			self._mode = ModeCls(self._core, self._cmd_group)
		return self._mode

	@property
	def pmode(self):
		"""pmode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pmode'):
			from .Pmode import PmodeCls
			self._pmode = PmodeCls(self._core, self._cmd_group)
		return self._pmode

	@property
	def name(self):
		"""name commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_name'):
			from .Name import NameCls
			self._name = NameCls(self._core, self._cmd_group)
		return self._name

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePyCls
			self._typePy = TypePyCls(self._core, self._cmd_group)
		return self._typePy

	@property
	def attRatio(self):
		"""attRatio commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_attRatio'):
			from .AttRatio import AttRatioCls
			self._attRatio = AttRatioCls(self._core, self._cmd_group)
		return self._attRatio

	@property
	def cmOffset(self):
		"""cmOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cmOffset'):
			from .CmOffset import CmOffsetCls
			self._cmOffset = CmOffsetCls(self._core, self._cmd_group)
		return self._cmOffset

	@property
	def dmOffset(self):
		"""dmOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dmOffset'):
			from .DmOffset import DmOffsetCls
			self._dmOffset = DmOffsetCls(self._core, self._cmd_group)
		return self._dmOffset

	@property
	def pmOffset(self):
		"""pmOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pmOffset'):
			from .PmOffset import PmOffsetCls
			self._pmOffset = PmOffsetCls(self._core, self._cmd_group)
		return self._pmOffset

	@property
	def nmOffset(self):
		"""nmOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nmOffset'):
			from .NmOffset import NmOffsetCls
			self._nmOffset = NmOffsetCls(self._core, self._cmd_group)
		return self._nmOffset

	def clone(self) -> 'SetupCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SetupCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PatternCls:
	"""Pattern commands group definition. 22 total commands, 10 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pattern", core, parent)

	@property
	def formatPy(self):
		"""formatPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_formatPy'):
			from .FormatPy import FormatPyCls
			self._formatPy = FormatPyCls(self._core, self._cmd_group)
		return self._formatPy

	@property
	def frame(self):
		"""frame commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_frame'):
			from .Frame import FrameCls
			self._frame = FrameCls(self._core, self._cmd_group)
		return self._frame

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
	def psk(self):
		"""psk commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_psk'):
			from .Psk import PskCls
			self._psk = PskCls(self._core, self._cmd_group)
		return self._psk

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
	def mapping(self):
		"""mapping commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_mapping'):
			from .Mapping import MappingCls
			self._mapping = MappingCls(self._core, self._cmd_group)
		return self._mapping

	@property
	def user(self):
		"""user commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_user'):
			from .User import UserCls
			self._user = UserCls(self._core, self._cmd_group)
		return self._user

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'PatternCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PatternCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

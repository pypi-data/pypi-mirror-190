from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HarmonicsCls:
	"""Harmonics commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("harmonics", core, parent)

	@property
	def identify(self):
		"""identify commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_identify'):
			from .Identify import IdentifyCls
			self._identify = IdentifyCls(self._core, self._cmd_group)
		return self._identify

	@property
	def mnumber(self):
		"""mnumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mnumber'):
			from .Mnumber import MnumberCls
			self._mnumber = MnumberCls(self._core, self._cmd_group)
		return self._mnumber

	@property
	def tolerance(self):
		"""tolerance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tolerance'):
			from .Tolerance import ToleranceCls
			self._tolerance = ToleranceCls(self._core, self._cmd_group)
		return self._tolerance

	def clone(self) -> 'HarmonicsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = HarmonicsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

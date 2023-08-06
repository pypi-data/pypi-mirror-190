from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScaleCls:
	"""Scale commands group definition. 6 total commands, 6 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("scale", core, parent)

	@property
	def pdivision(self):
		"""pdivision commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pdivision'):
			from .Pdivision import PdivisionCls
			self._pdivision = PdivisionCls(self._core, self._cmd_group)
		return self._pdivision

	@property
	def refPosition(self):
		"""refPosition commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_refPosition'):
			from .RefPosition import RefPositionCls
			self._refPosition = RefPositionCls(self._core, self._cmd_group)
		return self._refPosition

	@property
	def rvalue(self):
		"""rvalue commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rvalue'):
			from .Rvalue import RvalueCls
			self._rvalue = RvalueCls(self._core, self._cmd_group)
		return self._rvalue

	@property
	def start(self):
		"""start commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_start'):
			from .Start import StartCls
			self._start = StartCls(self._core, self._cmd_group)
		return self._start

	@property
	def stop(self):
		"""stop commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stop'):
			from .Stop import StopCls
			self._stop = StopCls(self._core, self._cmd_group)
		return self._stop

	@property
	def voffset(self):
		"""voffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_voffset'):
			from .Voffset import VoffsetCls
			self._voffset = VoffsetCls(self._core, self._cmd_group)
		return self._voffset

	def clone(self) -> 'ScaleCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ScaleCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

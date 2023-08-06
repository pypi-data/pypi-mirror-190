from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EspectrumCls:
	"""Espectrum commands group definition. 4 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("espectrum", core, parent)

	@property
	def peakSearch(self):
		"""peakSearch commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_peakSearch'):
			from .PeakSearch import PeakSearchCls
			self._peakSearch = PeakSearchCls(self._core, self._cmd_group)
		return self._peakSearch

	def clone(self) -> 'EspectrumCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = EspectrumCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

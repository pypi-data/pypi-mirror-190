from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AchannelCls:
	"""Achannel commands group definition. 7 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("achannel", core, parent)

	@property
	def result(self):
		"""result commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_result'):
			from .Result import ResultCls
			self._result = ResultCls(self._core, self._cmd_group)
		return self._result

	@property
	def relative(self):
		"""relative commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_relative'):
			from .Relative import RelativeCls
			self._relative = RelativeCls(self._core, self._cmd_group)
		return self._relative

	@property
	def absolute(self):
		"""absolute commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_absolute'):
			from .Absolute import AbsoluteCls
			self._absolute = AbsoluteCls(self._core, self._cmd_group)
		return self._absolute

	def clone(self) -> 'AchannelCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AchannelCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RemoveCls:
	"""Remove commands group definition. 3 total commands, 2 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("remove", core, parent)

	@property
	def all(self):
		"""all commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_all'):
			from .All import AllCls
			self._all = AllCls(self._core, self._cmd_group)
		return self._all

	@property
	def selected(self):
		"""selected commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_selected'):
			from .Selected import SelectedCls
			self._selected = SelectedCls(self._core, self._cmd_group)
		return self._selected

	def set(self, data_set: float) -> None:
		"""SCPI: HCOPy:TREPort:TEST:REMove \n
		Snippet: driver.hardCopy.treport.test.remove.set(data_set = 1.0) \n
		No command help available \n
			:param data_set: No help available
		"""
		param = Conversions.decimal_value_to_str(data_set)
		self._core.io.write(f'HCOPy:TREPort:TEST:REMove {param}')

	def clone(self) -> 'RemoveCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RemoveCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

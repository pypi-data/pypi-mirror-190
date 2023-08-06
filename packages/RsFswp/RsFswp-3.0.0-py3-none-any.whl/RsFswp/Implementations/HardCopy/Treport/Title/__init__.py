from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TitleCls:
	"""Title commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("title", core, parent)

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def set(self, title: str) -> None:
		"""SCPI: HCOPy:TREPort:TITLe \n
		Snippet: driver.hardCopy.treport.title.set(title = '1') \n
		No command help available \n
			:param title: No help available
		"""
		param = Conversions.value_to_quoted_str(title)
		self._core.io.write(f'HCOPy:TREPort:TITLe {param}')

	def get(self) -> str:
		"""SCPI: HCOPy:TREPort:TITLe \n
		Snippet: value: str = driver.hardCopy.treport.title.get() \n
		No command help available \n
			:return: title: No help available"""
		response = self._core.io.query_str(f'HCOPy:TREPort:TITLe?')
		return trim_str_response(response)

	def clone(self) -> 'TitleCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TitleCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

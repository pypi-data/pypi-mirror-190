from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CopiesCls:
	"""Copies commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("copies", core, parent)

	def set(self, copies: float) -> None:
		"""SCPI: HCOPy:COPies \n
		Snippet: driver.hardCopy.copies.set(copies = 1.0) \n
		No command help available \n
			:param copies: No help available
		"""
		param = Conversions.decimal_value_to_str(copies)
		self._core.io.write(f'HCOPy:COPies {param}')

	def get(self) -> float:
		"""SCPI: HCOPy:COPies \n
		Snippet: value: float = driver.hardCopy.copies.get() \n
		No command help available \n
			:return: copies: No help available"""
		response = self._core.io.query_str(f'HCOPy:COPies?')
		return Conversions.str_to_float(response)

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CountCls:
	"""Count commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("count", core, parent)

	def set(self, count: float) -> None:
		"""SCPI: HCOPy:PAGE:WINDow:COUNt \n
		Snippet: driver.hardCopy.page.window.count.set(count = 1.0) \n
		This command defines how many windows are displayed on a single page of the printout for method RsFswp.HardCopy.Content.
		set. \n
			:param count: integer
		"""
		param = Conversions.decimal_value_to_str(count)
		self._core.io.write(f'HCOPy:PAGE:WINDow:COUNt {param}')

	def get(self) -> float:
		"""SCPI: HCOPy:PAGE:WINDow:COUNt \n
		Snippet: value: float = driver.hardCopy.page.window.count.get() \n
		This command defines how many windows are displayed on a single page of the printout for method RsFswp.HardCopy.Content.
		set. \n
			:return: count: integer"""
		response = self._core.io.query_str(f'HCOPy:PAGE:WINDow:COUNt?')
		return Conversions.str_to_float(response)

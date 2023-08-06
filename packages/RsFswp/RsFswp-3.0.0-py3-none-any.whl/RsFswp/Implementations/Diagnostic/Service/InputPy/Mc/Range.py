from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RangeCls:
	"""Range commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("range", core, parent)

	def set(self, range_py: float) -> None:
		"""SCPI: DIAGnostic:SERVice:INPut:MC:RANGe \n
		Snippet: driver.diagnostic.service.inputPy.mc.range.set(range_py = 1.0) \n
		No command help available \n
			:param range_py: No help available
		"""
		param = Conversions.decimal_value_to_str(range_py)
		self._core.io.write(f'DIAGnostic:SERVice:INPut:MC:RANGe {param}')

	def get(self) -> float:
		"""SCPI: DIAGnostic:SERVice:INPut:MC:RANGe \n
		Snippet: value: float = driver.diagnostic.service.inputPy.mc.range.get() \n
		No command help available \n
			:return: range_py: No help available"""
		response = self._core.io.query_str(f'DIAGnostic:SERVice:INPut:MC:RANGe?')
		return Conversions.str_to_float(response)

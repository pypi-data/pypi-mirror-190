from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InputPyCls:
	"""InputPy commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("inputPy", core, parent)

	def set(self, default_input: enums.InputSelect) -> None:
		"""SCPI: SYSTem:PRESet:INPut \n
		Snippet: driver.system.preset.inputPy.set(default_input = enums.InputSelect.INPut1) \n
		No command help available \n
			:param default_input: No help available
		"""
		param = Conversions.enum_scalar_to_str(default_input, enums.InputSelect)
		self._core.io.write(f'SYSTem:PRESet:INPut {param}')

	# noinspection PyTypeChecker
	def get(self) -> enums.InputSelect:
		"""SCPI: SYSTem:PRESet:INPut \n
		Snippet: value: enums.InputSelect = driver.system.preset.inputPy.get() \n
		No command help available \n
			:return: default_input: No help available"""
		response = self._core.io.query_str(f'SYSTem:PRESet:INPut?')
		return Conversions.str_to_scalar_enum(response, enums.InputSelect)

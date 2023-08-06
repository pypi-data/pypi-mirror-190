from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, state: bool) -> None:
		"""SCPI: HCOPy:TDSTamp:STATe \n
		Snippet: driver.hardCopy.tdDtamp.state.set(state = False) \n
		This command includes or excludes the time and date in the printout. \n
			:param state: 1 | 0 | ON | OFF 1 | ON The time and date are printed. 0 | OFF The time and date are not printed.
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'HCOPy:TDSTamp:STATe {param}')

	def get(self) -> bool:
		"""SCPI: HCOPy:TDSTamp:STATe \n
		Snippet: value: bool = driver.hardCopy.tdDtamp.state.get() \n
		This command includes or excludes the time and date in the printout. \n
			:return: state: 1 | 0 | ON | OFF 1 | ON The time and date are printed. 0 | OFF The time and date are not printed."""
		response = self._core.io.query_str(f'HCOPy:TDSTamp:STATe?')
		return Conversions.str_to_bool(response)

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LogoCls:
	"""Logo commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("logo", core, parent)

	def set(self, filename: bool) -> None:
		"""SCPI: HCOPy:LOGO \n
		Snippet: driver.hardCopy.logo.set(filename = False) \n
		No command help available \n
			:param filename: No help available
		"""
		param = Conversions.bool_to_str(filename)
		self._core.io.write(f'HCOPy:LOGO {param}')

	def get(self) -> bool:
		"""SCPI: HCOPy:LOGO \n
		Snippet: value: bool = driver.hardCopy.logo.get() \n
		No command help available \n
			:return: filename: No help available"""
		response = self._core.io.query_str(f'HCOPy:LOGO?')
		return Conversions.str_to_bool(response)

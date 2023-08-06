from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ControlCls:
	"""Control commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("control", core, parent)

	def set(self, repetition: enums.HardcopyLogo) -> None:
		"""SCPI: HCOPy:TREPort:ITEM:LOGO:CONTrol \n
		Snippet: driver.hardCopy.treport.item.logo.control.set(repetition = enums.HardcopyLogo.ALWays) \n
		No command help available \n
			:param repetition: No help available
		"""
		param = Conversions.enum_scalar_to_str(repetition, enums.HardcopyLogo)
		self._core.io.write(f'HCOPy:TREPort:ITEM:LOGO:CONTrol {param}')

	# noinspection PyTypeChecker
	def get(self) -> enums.HardcopyLogo:
		"""SCPI: HCOPy:TREPort:ITEM:LOGO:CONTrol \n
		Snippet: value: enums.HardcopyLogo = driver.hardCopy.treport.item.logo.control.get() \n
		No command help available \n
			:return: repetition: No help available"""
		response = self._core.io.query_str(f'HCOPy:TREPort:ITEM:LOGO:CONTrol?')
		return Conversions.str_to_scalar_enum(response, enums.HardcopyLogo)

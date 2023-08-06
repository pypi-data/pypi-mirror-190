from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SelectCls:
	"""Select commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("select", core, parent)

	def set(self, theme: str) -> None:
		"""SCPI: HCOPy:THEMe:SELect \n
		Snippet: driver.hardCopy.theme.select.set(theme = '1') \n
		No command help available \n
			:param theme: No help available
		"""
		param = Conversions.value_to_quoted_str(theme)
		self._core.io.write(f'HCOPy:THEMe:SELect {param}')

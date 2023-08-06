from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DestinationCls:
	"""Destination commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("destination", core, parent)

	def set(self, destination: str) -> None:
		"""SCPI: HCOPy:DESTination \n
		Snippet: driver.hardCopy.destination.set(destination = '1') \n
		This command selects the destination of a print job. Note: To print a screenshot to a file, see method RsFswp.HardCopy.
		Device.Language.set. \n
			:param destination: 'MMEM' Activates 'Print to file'. Thus, if the destination of the print function is set to 'printer' (see HCOP:DEST1 'SYSTem:COMMunicate:PRINter' or HCOP:DEV:LANG GDI) , the output is redirected to a .PRN file using the selected printer driver. Select the file name with method RsFswp.MassMemory.Name.set. Note: To save a screenshot to a file, see method RsFswp.HardCopy.Device.Language.set. 'SYSTem:COMMunicate:PRINter' Sends the hardcopy to a printer and deactivates 'print to file'. Select the printer with SYSTem:COMMunicate:PRINter:SELectdi . 'SYSTem:COMMunicate:CLIPboard' Sends the hardcopy to the clipboard.
		"""
		param = Conversions.value_to_quoted_str(destination)
		self._core.io.write(f'HCOPy:DESTination {param}')

	def get(self) -> str:
		"""SCPI: HCOPy:DESTination \n
		Snippet: value: str = driver.hardCopy.destination.get() \n
		This command selects the destination of a print job. Note: To print a screenshot to a file, see method RsFswp.HardCopy.
		Device.Language.set. \n
			:return: destination: 'MMEM' Activates 'Print to file'. Thus, if the destination of the print function is set to 'printer' (see HCOP:DEST1 'SYSTem:COMMunicate:PRINter' or HCOP:DEV:LANG GDI) , the output is redirected to a .PRN file using the selected printer driver. Select the file name with method RsFswp.MassMemory.Name.set. Note: To save a screenshot to a file, see method RsFswp.HardCopy.Device.Language.set. 'SYSTem:COMMunicate:PRINter' Sends the hardcopy to a printer and deactivates 'print to file'. Select the printer with SYSTem:COMMunicate:PRINter:SELectdi . 'SYSTem:COMMunicate:CLIPboard' Sends the hardcopy to the clipboard."""
		response = self._core.io.query_str(f'HCOPy:DESTination?')
		return trim_str_response(response)

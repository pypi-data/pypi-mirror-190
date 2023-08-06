from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SaveCls:
	"""Save commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("save", core, parent)

	def set(self, filename: str = None) -> None:
		"""SCPI: DIAGnostic:SERVice:SFUNction:RESults:SAVE \n
		Snippet: driver.diagnostic.service.sfunction.results.save.set(filename = '1') \n
		This command saves the results in the output buffer for service functions you have used to a file. If no <FileName>
		parameter is provided, the results are stored to C:/R_S/INSTR/results/Servicelog.txt. Note that if the buffer is empty,
		the function returns an error. \n
			:param filename: String containing the path and file name.
		"""
		param = ''
		if filename:
			param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'DIAGnostic:SERVice:SFUNction:RESults:SAVE {param}'.strip())

	def get(self) -> str:
		"""SCPI: DIAGnostic:SERVice:SFUNction:RESults:SAVE \n
		Snippet: value: str = driver.diagnostic.service.sfunction.results.save.get() \n
		This command saves the results in the output buffer for service functions you have used to a file. If no <FileName>
		parameter is provided, the results are stored to C:/R_S/INSTR/results/Servicelog.txt. Note that if the buffer is empty,
		the function returns an error. \n
			:return: filename: String containing the path and file name."""
		response = self._core.io.query_str(f'DIAGnostic:SERVice:SFUNction:RESults:SAVE?')
		return trim_str_response(response)

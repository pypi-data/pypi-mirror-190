from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.Utilities import trim_str_response
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PathCls:
	"""Path commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("path", core, parent)

	def set(self, file_path: str, analysis_bw: float) -> None:
		"""SCPI: INPut:FILE:PATH \n
		Snippet: driver.inputPy.file.path.set(file_path = '1', analysis_bw = 1.0) \n
		This command selects the I/Q data file to be used as input for further measurements. The I/Q data must have a specific
		format as described in 'I/Q data file format (iq-tar) '. For details, see 'Basics on input from I/Q data files'. \n
			:param file_path: No help available
			:param analysis_bw: Optionally: The analysis bandwidth to be used by the measurement. The bandwidth must be smaller than or equal to the bandwidth of the data that was stored in the file. Unit: HZ
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('file_path', file_path, DataType.String), ArgSingle('analysis_bw', analysis_bw, DataType.Float))
		self._core.io.write_with_opc(f'INPut:FILE:PATH {param}'.rstrip())

	def get(self) -> str:
		"""SCPI: INPut:FILE:PATH \n
		Snippet: value: str = driver.inputPy.file.path.get() \n
		This command selects the I/Q data file to be used as input for further measurements. The I/Q data must have a specific
		format as described in 'I/Q data file format (iq-tar) '. For details, see 'Basics on input from I/Q data files'. \n
			:return: file_path: No help available"""
		response = self._core.io.query_str_with_opc(f'INPut:FILE:PATH?')
		return trim_str_response(response)

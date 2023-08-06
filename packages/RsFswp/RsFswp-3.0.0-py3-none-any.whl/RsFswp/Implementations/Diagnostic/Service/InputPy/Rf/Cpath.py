from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CpathCls:
	"""Cpath commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cpath", core, parent)

	def set(self, path_to_calibrate: enums.PathToCalibrate) -> None:
		"""SCPI: DIAGnostic:SERVice:INPut:RF:CPATh \n
		Snippet: driver.diagnostic.service.inputPy.rf.cpath.set(path_to_calibrate = enums.PathToCalibrate.FULL) \n
		No command help available \n
			:param path_to_calibrate: No help available
		"""
		param = Conversions.enum_scalar_to_str(path_to_calibrate, enums.PathToCalibrate)
		self._core.io.write(f'DIAGnostic:SERVice:INPut:RF:CPATh {param}')

	# noinspection PyTypeChecker
	def get(self) -> enums.PathToCalibrate:
		"""SCPI: DIAGnostic:SERVice:INPut:RF:CPATh \n
		Snippet: value: enums.PathToCalibrate = driver.diagnostic.service.inputPy.rf.cpath.get() \n
		No command help available \n
			:return: path_to_calibrate: No help available"""
		response = self._core.io.query_str(f'DIAGnostic:SERVice:INPut:RF:CPATh?')
		return Conversions.str_to_scalar_enum(response, enums.PathToCalibrate)

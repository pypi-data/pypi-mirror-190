from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TimeCls:
	"""Time commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("time", core, parent)

	def set(self, time: str) -> None:
		"""SCPI: CALibration:DUE:TIME \n
		Snippet: driver.calibration.due.time.set(time = '1') \n
		Defines the time at which a self-alignment is scheduled for the days specified by method RsFswp.Calibration.Due.Days.set,
		if method RsFswp.Calibration.Due.Schedule.set ON. \n
			:param time: string with format 'hh:mm' (24 hours)
		"""
		param = Conversions.value_to_quoted_str(time)
		self._core.io.write(f'CALibration:DUE:TIME {param}')

	def get(self) -> str:
		"""SCPI: CALibration:DUE:TIME \n
		Snippet: value: str = driver.calibration.due.time.get() \n
		Defines the time at which a self-alignment is scheduled for the days specified by method RsFswp.Calibration.Due.Days.set,
		if method RsFswp.Calibration.Due.Schedule.set ON. \n
			:return: time: string with format 'hh:mm' (24 hours)"""
		response = self._core.io.query_str(f'CALibration:DUE:TIME?')
		return trim_str_response(response)

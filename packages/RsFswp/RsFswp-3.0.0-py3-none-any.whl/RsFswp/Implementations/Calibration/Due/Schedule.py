from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScheduleCls:
	"""Schedule commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("schedule", core, parent)

	def set(self, state: bool) -> None:
		"""SCPI: CALibration:DUE:SCHedule \n
		Snippet: driver.calibration.due.schedule.set(state = False) \n
		If enabled, a self-alignment is performed regularly at specific days and time. Specify the date and time using the method
		RsFswp.Calibration.Due.Days.set and method RsFswp.Calibration.Due.Time.set commands. \n
			:param state: ON | OFF | 0 | 1 OFF | 0 Switches the function off ON | 1 Switches the function on
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'CALibration:DUE:SCHedule {param}')

	def get(self) -> bool:
		"""SCPI: CALibration:DUE:SCHedule \n
		Snippet: value: bool = driver.calibration.due.schedule.get() \n
		If enabled, a self-alignment is performed regularly at specific days and time. Specify the date and time using the method
		RsFswp.Calibration.Due.Days.set and method RsFswp.Calibration.Due.Time.set commands. \n
			:return: state: ON | OFF | 0 | 1 OFF | 0 Switches the function off ON | 1 Switches the function on"""
		response = self._core.io.query_str(f'CALibration:DUE:SCHedule?')
		return Conversions.str_to_bool(response)

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class WarmupCls:
	"""Warmup commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("warmup", core, parent)

	def set(self, state: bool) -> None:
		"""SCPI: CALibration:DUE:WARMup \n
		Snippet: driver.calibration.due.warmup.set(state = False) \n
		If enabled, self-alignment is started automatically after the warmup operation has completed. \n
			:param state: ON | OFF | 0 | 1 OFF | 0 Switches the function off ON | 1 Switches the function on
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'CALibration:DUE:WARMup {param}')

	def get(self) -> bool:
		"""SCPI: CALibration:DUE:WARMup \n
		Snippet: value: bool = driver.calibration.due.warmup.get() \n
		If enabled, self-alignment is started automatically after the warmup operation has completed. \n
			:return: state: ON | OFF | 0 | 1 OFF | 0 Switches the function off ON | 1 Switches the function on"""
		response = self._core.io.query_str(f'CALibration:DUE:WARMup?')
		return Conversions.str_to_bool(response)

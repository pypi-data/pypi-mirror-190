from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ShutdownCls:
	"""Shutdown commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("shutdown", core, parent)

	def set(self, state: bool) -> None:
		"""SCPI: CALibration:DUE:SHUTdown \n
		Snippet: driver.calibration.due.shutdown.set(state = False) \n
		If activated, the R&S FSWP is automatically shut down after self-alignment is completed. Note that the instrument cannot
		be restarted via remote control. \n
			:param state: ON | OFF | 0 | 1 OFF | 0 Switches the function off ON | 1 Switches the function on
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'CALibration:DUE:SHUTdown {param}')

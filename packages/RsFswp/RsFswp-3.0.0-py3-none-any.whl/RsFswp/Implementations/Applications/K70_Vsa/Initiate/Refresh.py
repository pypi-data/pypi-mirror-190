from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RefreshCls:
	"""Refresh commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("refresh", core, parent)

	def set(self) -> None:
		"""SCPI: INITiate:REFResh \n
		Snippet: driver.applications.k70Vsa.initiate.refresh.set() \n
		This command updates the current measurement results to reflect the current measurement settings. No new I/Q data is
		captured. Thus, measurement settings apply to the I/Q data currently in the capture buffer. The command applies
		exclusively to I/Q measurements. It requires I/Q data. \n
		"""
		self._core.io.write(f'INITiate:REFResh')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: INITiate:REFResh \n
		Snippet: driver.applications.k70Vsa.initiate.refresh.set_with_opc() \n
		This command updates the current measurement results to reflect the current measurement settings. No new I/Q data is
		captured. Thus, measurement settings apply to the I/Q data currently in the capture buffer. The command applies
		exclusively to I/Q measurements. It requires I/Q data. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsFswp.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'INITiate:REFResh', opc_timeout_ms)

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LevelCls:
	"""Level commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("level", core, parent)

	def set(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SENSe]:ADJust:LEVel \n
		Snippet: driver.sense.adjust.level.set() \n
		Initiates a single (internal) measurement that evaluates and sets the ideal reference level for the current input data
		and measurement settings. Thus, the settings of the RF attenuation and the reference level are optimized for the signal
		level. The R&S FSWP is not overloaded and the dynamic range is not limited by an S/N ratio that is too small. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SENSe:ADJust:LEVel', opc_timeout_ms)

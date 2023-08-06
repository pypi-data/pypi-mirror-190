from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class O640Cls:
	"""O640 commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("o640", core, parent)

	def set(self, state: bool) -> None:
		"""SCPI: [SENSe]:ROSCillator:O640 \n
		Snippet: driver.sense.roscillator.o640.set(state = False) \n
		This command turns the output of a reference signal on the corresponding connector ('Ref Output') on and off.
		[SENSe:]ROSCillator:O100: Provides a 100 MHz reference signal on corresponding connector. [SENSe:]ROSCillator:O640:
		Provides a 640 MHz reference signal on corresponding connector. \n
			:param state: ON | OFF | 1 | 0 OFF | 0 Switches the reference off. ON | 1 Switches the reference on
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write_with_opc(f'SENSe:ROSCillator:O640 {param}')

	def get(self) -> bool:
		"""SCPI: [SENSe]:ROSCillator:O640 \n
		Snippet: value: bool = driver.sense.roscillator.o640.get() \n
		This command turns the output of a reference signal on the corresponding connector ('Ref Output') on and off.
		[SENSe:]ROSCillator:O100: Provides a 100 MHz reference signal on corresponding connector. [SENSe:]ROSCillator:O640:
		Provides a 640 MHz reference signal on corresponding connector. \n
			:return: state: ON | OFF | 1 | 0 OFF | 0 Switches the reference off. ON | 1 Switches the reference on"""
		response = self._core.io.query_str_with_opc(f'SENSe:ROSCillator:O640?')
		return Conversions.str_to_bool(response)

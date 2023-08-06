from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ModeCls:
	"""Mode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mode", core, parent)

	def set(self, arg_0: enums.RoscillatorFreqMode, externalRosc=repcap.ExternalRosc.Nr1) -> None:
		"""SCPI: SOURce:EXTernal<ext>:ROSCillator:EXTernal:FREQuency:MODE \n
		Snippet: driver.source.external.roscillator.external.frequency.mode.set(arg_0 = enums.RoscillatorFreqMode.E10, externalRosc = repcap.ExternalRosc.Nr1) \n
		No command help available \n
			:param arg_0: No help available
			:param externalRosc: optional repeated capability selector. Default value: Nr1
		"""
		param = Conversions.enum_scalar_to_str(arg_0, enums.RoscillatorFreqMode)
		externalRosc_cmd_val = self._cmd_group.get_repcap_cmd_value(externalRosc, repcap.ExternalRosc)
		self._core.io.write(f'SOURce:EXTernal{externalRosc_cmd_val}:ROSCillator:EXTernal:FREQuency:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, externalRosc=repcap.ExternalRosc.Nr1) -> enums.RoscillatorFreqMode:
		"""SCPI: SOURce:EXTernal<ext>:ROSCillator:EXTernal:FREQuency:MODE \n
		Snippet: value: enums.RoscillatorFreqMode = driver.source.external.roscillator.external.frequency.mode.get(externalRosc = repcap.ExternalRosc.Nr1) \n
		No command help available \n
			:param externalRosc: optional repeated capability selector. Default value: Nr1
			:return: arg_0: No help available"""
		externalRosc_cmd_val = self._cmd_group.get_repcap_cmd_value(externalRosc, repcap.ExternalRosc)
		response = self._core.io.query_str(f'SOURce:EXTernal{externalRosc_cmd_val}:ROSCillator:EXTernal:FREQuency:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.RoscillatorFreqMode)

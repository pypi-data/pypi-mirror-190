from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrequencyCls:
	"""Frequency commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import ModeCls
			self._mode = ModeCls(self._core, self._cmd_group)
		return self._mode

	def set(self, frequency: float, externalRosc=repcap.ExternalRosc.Nr1) -> None:
		"""SCPI: SOURce:EXTernal<ext>:ROSCillator:EXTernal:FREQuency \n
		Snippet: driver.source.external.roscillator.external.frequency.set(frequency = 1.0, externalRosc = repcap.ExternalRosc.Nr1) \n
		This command defines the frequency of the external reference oscillator. If the external reference oscillator is selected,
		the reference signal must be connected to the rear panel of the instrument. \n
			:param frequency: Range: 1 MHz to 50 MHz, Unit: HZ
			:param externalRosc: optional repeated capability selector. Default value: Nr1
		"""
		param = Conversions.decimal_value_to_str(frequency)
		externalRosc_cmd_val = self._cmd_group.get_repcap_cmd_value(externalRosc, repcap.ExternalRosc)
		self._core.io.write(f'SOURce:EXTernal{externalRosc_cmd_val}:ROSCillator:EXTernal:FREQuency {param}')

	def get(self, externalRosc=repcap.ExternalRosc.Nr1) -> float:
		"""SCPI: SOURce:EXTernal<ext>:ROSCillator:EXTernal:FREQuency \n
		Snippet: value: float = driver.source.external.roscillator.external.frequency.get(externalRosc = repcap.ExternalRosc.Nr1) \n
		This command defines the frequency of the external reference oscillator. If the external reference oscillator is selected,
		the reference signal must be connected to the rear panel of the instrument. \n
			:param externalRosc: optional repeated capability selector. Default value: Nr1
			:return: frequency: Range: 1 MHz to 50 MHz, Unit: HZ"""
		externalRosc_cmd_val = self._cmd_group.get_repcap_cmd_value(externalRosc, repcap.ExternalRosc)
		response = self._core.io.query_str(f'SOURce:EXTernal{externalRosc_cmd_val}:ROSCillator:EXTernal:FREQuency?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'FrequencyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FrequencyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

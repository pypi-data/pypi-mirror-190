from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OutputCls:
	"""Output commands group definition. 1 total commands, 0 Subgroups, 1 group commands
	Repeated Capability: OutputConnector, default value after init: OutputConnector.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("output", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_outputConnector_get', 'repcap_outputConnector_set', repcap.OutputConnector.Nr1)

	def repcap_outputConnector_set(self, outputConnector: repcap.OutputConnector) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to OutputConnector.Default
		Default value after init: OutputConnector.Nr1"""
		self._cmd_group.set_repcap_enum_value(outputConnector)

	def repcap_outputConnector_get(self) -> repcap.OutputConnector:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	def set(self, ref_out: enums.RoscillatorRefOut, outputConnector=repcap.OutputConnector.Default) -> None:
		"""SCPI: [SENSe]:ROSCillator:OUTPut<o> \n
		Snippet: driver.sense.roscillator.output.set(ref_out = enums.RoscillatorRefOut.EXTernal1, outputConnector = repcap.OutputConnector.Default) \n
		No command help available \n
			:param ref_out: No help available
			:param outputConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
		"""
		param = Conversions.enum_scalar_to_str(ref_out, enums.RoscillatorRefOut)
		outputConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(outputConnector, repcap.OutputConnector)
		self._core.io.write(f'SENSe:ROSCillator:OUTPut{outputConnector_cmd_val} {param}')

	# noinspection PyTypeChecker
	def get(self, outputConnector=repcap.OutputConnector.Default) -> enums.RoscillatorRefOut:
		"""SCPI: [SENSe]:ROSCillator:OUTPut<o> \n
		Snippet: value: enums.RoscillatorRefOut = driver.sense.roscillator.output.get(outputConnector = repcap.OutputConnector.Default) \n
		No command help available \n
			:param outputConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: ref_out: No help available"""
		outputConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(outputConnector, repcap.OutputConnector)
		response = self._core.io.query_str(f'SENSe:ROSCillator:OUTPut{outputConnector_cmd_val}?')
		return Conversions.str_to_scalar_enum(response, enums.RoscillatorRefOut)

	def clone(self) -> 'OutputCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = OutputCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

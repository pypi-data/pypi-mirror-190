from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TextCls:
	"""Text commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("text", core, parent)

	def set(self, description: str, line=repcap.Line.Default) -> None:
		"""SCPI: HCOPy:TREPort:ITEM:HEADer:LINE<li>:TEXT \n
		Snippet: driver.hardCopy.treport.item.header.line.text.set(description = '1', line = repcap.Line.Default) \n
		No command help available \n
			:param description: No help available
			:param line: optional repeated capability selector. Default value: Ix1 (settable in the interface 'Line')
		"""
		param = Conversions.value_to_quoted_str(description)
		line_cmd_val = self._cmd_group.get_repcap_cmd_value(line, repcap.Line)
		self._core.io.write(f'HCOPy:TREPort:ITEM:HEADer:LINE{line_cmd_val}:TEXT {param}')

	def get(self, line=repcap.Line.Default) -> str:
		"""SCPI: HCOPy:TREPort:ITEM:HEADer:LINE<li>:TEXT \n
		Snippet: value: str = driver.hardCopy.treport.item.header.line.text.get(line = repcap.Line.Default) \n
		No command help available \n
			:param line: optional repeated capability selector. Default value: Ix1 (settable in the interface 'Line')
			:return: description: No help available"""
		line_cmd_val = self._cmd_group.get_repcap_cmd_value(line, repcap.Line)
		response = self._core.io.query_str(f'HCOPy:TREPort:ITEM:HEADer:LINE{line_cmd_val}:TEXT?')
		return trim_str_response(response)

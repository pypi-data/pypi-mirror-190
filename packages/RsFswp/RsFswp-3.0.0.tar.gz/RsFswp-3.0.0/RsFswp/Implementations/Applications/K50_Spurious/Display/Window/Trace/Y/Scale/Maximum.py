from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MaximumCls:
	"""Maximum commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("maximum", core, parent)

	def set(self, max_py: float, window=repcap.Window.Default) -> None:
		"""SCPI: DISPlay[:WINDow<n>]:TRACe:Y[:SCALe]:MAXimum \n
		Snippet: driver.applications.k50Spurious.display.window.trace.y.scale.maximum.set(max_py = 1.0, window = repcap.Window.Default) \n
		Defines the maximum value on the y-axis in the specified window. \n
			:param max_py: numeric value
			:param window: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Window')
		"""
		param = Conversions.decimal_value_to_str(max_py)
		window_cmd_val = self._cmd_group.get_repcap_cmd_value(window, repcap.Window)
		self._core.io.write(f'DISPlay:WINDow{window_cmd_val}:TRACe:Y:SCALe:MAXimum {param}')

	def get(self, window=repcap.Window.Default) -> float:
		"""SCPI: DISPlay[:WINDow<n>]:TRACe:Y[:SCALe]:MAXimum \n
		Snippet: value: float = driver.applications.k50Spurious.display.window.trace.y.scale.maximum.get(window = repcap.Window.Default) \n
		Defines the maximum value on the y-axis in the specified window. \n
			:param window: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Window')
			:return: max_py: numeric value"""
		window_cmd_val = self._cmd_group.get_repcap_cmd_value(window, repcap.Window)
		response = self._core.io.query_str(f'DISPlay:WINDow{window_cmd_val}:TRACe:Y:SCALe:MAXimum?')
		return Conversions.str_to_float(response)

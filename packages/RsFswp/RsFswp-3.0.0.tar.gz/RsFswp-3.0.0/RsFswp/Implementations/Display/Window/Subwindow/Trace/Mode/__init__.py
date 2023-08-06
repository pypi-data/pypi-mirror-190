from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ModeCls:
	"""Mode commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mode", core, parent)

	@property
	def hcontinuous(self):
		"""hcontinuous commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hcontinuous'):
			from .Hcontinuous import HcontinuousCls
			self._hcontinuous = HcontinuousCls(self._core, self._cmd_group)
		return self._hcontinuous

	def set(self, trace_mode: enums.TraceModeF, window=repcap.Window.Default, subWindow=repcap.SubWindow.Default, trace=repcap.Trace.Default) -> None:
		"""SCPI: DISPlay[:WINDow<n>][:SUBWindow<w>]:TRACe<t>:MODE \n
		Snippet: driver.display.window.subwindow.trace.mode.set(trace_mode = enums.TraceModeF.AVERage, window = repcap.Window.Default, subWindow = repcap.SubWindow.Default, trace = repcap.Trace.Default) \n
		This command selects the trace mode. If necessary, the selected trace is also activated. For max hold, min hold or
		average trace mode, you can set the number of single measurements with [SENSe:]SWEep:COUNt. Note that synchronization to
		the end of the measurement is possible only in single sweep mode. For more information, see 'Analyzing several traces -
		trace mode'. \n
			:param trace_mode: WRITe (default:) Overwrite mode: the trace is overwritten by each sweep. AVERage The average is formed over several sweeps. The 'Sweep/Average Count' determines the number of averaging procedures. MAXHold The maximum value is determined over several sweeps and displayed. The R&S FSWP saves the sweep result in the trace memory only if the new value is greater than the previous one. MINHold The minimum value is determined from several measurements and displayed. The R&S FSWP saves the sweep result in the trace memory only if the new value is lower than the previous one. VIEW The current contents of the trace memory are frozen and displayed. BLANk Hides the selected trace. WRHold The trace is overwritten when new data is available, but only after all cross-correlation operations defined for a half decade are done.
			:param window: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Window')
			:param subWindow: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subwindow')
			:param trace: optional repeated capability selector. Default value: Tr1 (settable in the interface 'Trace')
		"""
		param = Conversions.enum_scalar_to_str(trace_mode, enums.TraceModeF)
		window_cmd_val = self._cmd_group.get_repcap_cmd_value(window, repcap.Window)
		subWindow_cmd_val = self._cmd_group.get_repcap_cmd_value(subWindow, repcap.SubWindow)
		trace_cmd_val = self._cmd_group.get_repcap_cmd_value(trace, repcap.Trace)
		self._core.io.write(f'DISPlay:WINDow{window_cmd_val}:SUBWindow{subWindow_cmd_val}:TRACe{trace_cmd_val}:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, window=repcap.Window.Default, subWindow=repcap.SubWindow.Default, trace=repcap.Trace.Default) -> enums.TraceModeF:
		"""SCPI: DISPlay[:WINDow<n>][:SUBWindow<w>]:TRACe<t>:MODE \n
		Snippet: value: enums.TraceModeF = driver.display.window.subwindow.trace.mode.get(window = repcap.Window.Default, subWindow = repcap.SubWindow.Default, trace = repcap.Trace.Default) \n
		This command selects the trace mode. If necessary, the selected trace is also activated. For max hold, min hold or
		average trace mode, you can set the number of single measurements with [SENSe:]SWEep:COUNt. Note that synchronization to
		the end of the measurement is possible only in single sweep mode. For more information, see 'Analyzing several traces -
		trace mode'. \n
			:param window: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Window')
			:param subWindow: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subwindow')
			:param trace: optional repeated capability selector. Default value: Tr1 (settable in the interface 'Trace')
			:return: trace_mode: WRITe (default:) Overwrite mode: the trace is overwritten by each sweep. AVERage The average is formed over several sweeps. The 'Sweep/Average Count' determines the number of averaging procedures. MAXHold The maximum value is determined over several sweeps and displayed. The R&S FSWP saves the sweep result in the trace memory only if the new value is greater than the previous one. MINHold The minimum value is determined from several measurements and displayed. The R&S FSWP saves the sweep result in the trace memory only if the new value is lower than the previous one. VIEW The current contents of the trace memory are frozen and displayed. BLANk Hides the selected trace. WRHold The trace is overwritten when new data is available, but only after all cross-correlation operations defined for a half decade are done."""
		window_cmd_val = self._cmd_group.get_repcap_cmd_value(window, repcap.Window)
		subWindow_cmd_val = self._cmd_group.get_repcap_cmd_value(subWindow, repcap.SubWindow)
		trace_cmd_val = self._cmd_group.get_repcap_cmd_value(trace, repcap.Trace)
		response = self._core.io.query_str(f'DISPlay:WINDow{window_cmd_val}:SUBWindow{subWindow_cmd_val}:TRACe{trace_cmd_val}:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.TraceModeF)

	def clone(self) -> 'ModeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ModeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

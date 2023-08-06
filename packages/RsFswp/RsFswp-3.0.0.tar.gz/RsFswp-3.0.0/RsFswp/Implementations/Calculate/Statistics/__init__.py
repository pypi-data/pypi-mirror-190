from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StatisticsCls:
	"""Statistics commands group definition. 11 total commands, 5 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("statistics", core, parent)

	@property
	def amplitudeProbDensity(self):
		"""amplitudeProbDensity commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_amplitudeProbDensity'):
			from .AmplitudeProbDensity import AmplitudeProbDensityCls
			self._amplitudeProbDensity = AmplitudeProbDensityCls(self._core, self._cmd_group)
		return self._amplitudeProbDensity

	@property
	def cumulativeDistribFnc(self):
		"""cumulativeDistribFnc commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_cumulativeDistribFnc'):
			from .CumulativeDistribFnc import CumulativeDistribFncCls
			self._cumulativeDistribFnc = CumulativeDistribFncCls(self._core, self._cmd_group)
		return self._cumulativeDistribFnc

	@property
	def nsamples(self):
		"""nsamples commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsamples'):
			from .Nsamples import NsamplesCls
			self._nsamples = NsamplesCls(self._core, self._cmd_group)
		return self._nsamples

	@property
	def scale(self):
		"""scale commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_scale'):
			from .Scale import ScaleCls
			self._scale = ScaleCls(self._core, self._cmd_group)
		return self._scale

	@property
	def result(self):
		"""result commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_result'):
			from .Result import ResultCls
			self._result = ResultCls(self._core, self._cmd_group)
		return self._result

	def preset(self, window=repcap.Window.Default) -> None:
		"""SCPI: CALCulate<n>:STATistics:PRESet \n
		Snippet: driver.calculate.statistics.preset(window = repcap.Window.Default) \n
		No command help available \n
			:param window: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Calculate')
		"""
		window_cmd_val = self._cmd_group.get_repcap_cmd_value(window, repcap.Window)
		self._core.io.write(f'CALCulate{window_cmd_val}:STATistics:PRESet')

	def preset_with_opc(self, window=repcap.Window.Default, opc_timeout_ms: int = -1) -> None:
		window_cmd_val = self._cmd_group.get_repcap_cmd_value(window, repcap.Window)
		"""SCPI: CALCulate<n>:STATistics:PRESet \n
		Snippet: driver.calculate.statistics.preset_with_opc(window = repcap.Window.Default) \n
		No command help available \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsFswp.utilities.opc_timeout_set() to set the timeout value. \n
			:param window: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Calculate')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'CALCulate{window_cmd_val}:STATistics:PRESet', opc_timeout_ms)

	def clone(self) -> 'StatisticsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = StatisticsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

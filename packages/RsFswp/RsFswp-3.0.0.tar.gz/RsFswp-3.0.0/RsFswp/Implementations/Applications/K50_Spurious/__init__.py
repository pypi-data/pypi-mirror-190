from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class K50_SpuriousCls:
	"""K50_Spurious commands group definition. 235 total commands, 16 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("k50_Spurious", core, parent)

	@property
	def layout(self):
		"""layout commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_layout'):
			from .Layout import LayoutCls
			self._layout = LayoutCls(self._core, self._cmd_group)
		return self._layout

	@property
	def trace(self):
		"""trace commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_trace'):
			from .Trace import TraceCls
			self._trace = TraceCls(self._core, self._cmd_group)
		return self._trace

	@property
	def triggerInvoke(self):
		"""triggerInvoke commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_triggerInvoke'):
			from .TriggerInvoke import TriggerInvokeCls
			self._triggerInvoke = TriggerInvokeCls(self._core, self._cmd_group)
		return self._triggerInvoke

	@property
	def calculate(self):
		"""calculate commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_calculate'):
			from .Calculate import CalculateCls
			self._calculate = CalculateCls(self._core, self._cmd_group)
		return self._calculate

	@property
	def display(self):
		"""display commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_display'):
			from .Display import DisplayCls
			self._display = DisplayCls(self._core, self._cmd_group)
		return self._display

	@property
	def formatPy(self):
		"""formatPy commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_formatPy'):
			from .FormatPy import FormatPyCls
			self._formatPy = FormatPyCls(self._core, self._cmd_group)
		return self._formatPy

	@property
	def inputPy(self):
		"""inputPy commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_inputPy'):
			from .InputPy import InputPyCls
			self._inputPy = InputPyCls(self._core, self._cmd_group)
		return self._inputPy

	@property
	def initiate(self):
		"""initiate commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_initiate'):
			from .Initiate import InitiateCls
			self._initiate = InitiateCls(self._core, self._cmd_group)
		return self._initiate

	@property
	def massMemory(self):
		"""massMemory commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_massMemory'):
			from .MassMemory import MassMemoryCls
			self._massMemory = MassMemoryCls(self._core, self._cmd_group)
		return self._massMemory

	@property
	def output(self):
		"""output commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_output'):
			from .Output import OutputCls
			self._output = OutputCls(self._core, self._cmd_group)
		return self._output

	@property
	def sense(self):
		"""sense commands group. 13 Sub-classes, 0 commands."""
		if not hasattr(self, '_sense'):
			from .Sense import SenseCls
			self._sense = SenseCls(self._core, self._cmd_group)
		return self._sense

	@property
	def trigger(self):
		"""trigger commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_trigger'):
			from .Trigger import TriggerCls
			self._trigger = TriggerCls(self._core, self._cmd_group)
		return self._trigger

	@property
	def calibration(self):
		"""calibration commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_calibration'):
			from .Calibration import CalibrationCls
			self._calibration = CalibrationCls(self._core, self._cmd_group)
		return self._calibration

	@property
	def fetch(self):
		"""fetch commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fetch'):
			from .Fetch import FetchCls
			self._fetch = FetchCls(self._core, self._cmd_group)
		return self._fetch

	@property
	def read(self):
		"""read commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_read'):
			from .Read import ReadCls
			self._read = ReadCls(self._core, self._cmd_group)
		return self._read

	@property
	def unit(self):
		"""unit commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_unit'):
			from .Unit import UnitCls
			self._unit = UnitCls(self._core, self._cmd_group)
		return self._unit

	def clone(self) -> 'K50_SpuriousCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = K50_SpuriousCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

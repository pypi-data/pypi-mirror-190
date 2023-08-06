from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class K70_VsaCls:
	"""K70_Vsa commands group definition. 466 total commands, 12 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("k70_Vsa", core, parent)

	@property
	def status(self):
		"""status commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_status'):
			from .Status import StatusCls
			self._status = StatusCls(self._core, self._cmd_group)
		return self._status

	@property
	def layout(self):
		"""layout commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_layout'):
			from .Layout import LayoutCls
			self._layout = LayoutCls(self._core, self._cmd_group)
		return self._layout

	@property
	def trace(self):
		"""trace commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_trace'):
			from .Trace import TraceCls
			self._trace = TraceCls(self._core, self._cmd_group)
		return self._trace

	@property
	def massMemory(self):
		"""massMemory commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_massMemory'):
			from .MassMemory import MassMemoryCls
			self._massMemory = MassMemoryCls(self._core, self._cmd_group)
		return self._massMemory

	@property
	def calculate(self):
		"""calculate commands group. 21 Sub-classes, 0 commands."""
		if not hasattr(self, '_calculate'):
			from .Calculate import CalculateCls
			self._calculate = CalculateCls(self._core, self._cmd_group)
		return self._calculate

	@property
	def display(self):
		"""display commands group. 1 Sub-classes, 0 commands."""
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
	def initiate(self):
		"""initiate commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_initiate'):
			from .Initiate import InitiateCls
			self._initiate = InitiateCls(self._core, self._cmd_group)
		return self._initiate

	@property
	def inputPy(self):
		"""inputPy commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_inputPy'):
			from .InputPy import InputPyCls
			self._inputPy = InputPyCls(self._core, self._cmd_group)
		return self._inputPy

	@property
	def output(self):
		"""output commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_output'):
			from .Output import OutputCls
			self._output = OutputCls(self._core, self._cmd_group)
		return self._output

	@property
	def sense(self):
		"""sense commands group. 7 Sub-classes, 0 commands."""
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

	def clone(self) -> 'K70_VsaCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = K70_VsaCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

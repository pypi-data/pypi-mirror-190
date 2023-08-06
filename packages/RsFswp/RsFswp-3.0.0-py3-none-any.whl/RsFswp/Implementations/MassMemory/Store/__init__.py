from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StoreCls:
	"""Store commands group definition. 15 total commands, 10 Subgroups, 0 group commands
	Repeated Capability: Store, default value after init: Store.Pos1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("store", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_store_get', 'repcap_store_set', repcap.Store.Pos1)

	def repcap_store_set(self, store: repcap.Store) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Store.Default
		Default value after init: Store.Pos1"""
		self._cmd_group.set_repcap_enum_value(store)

	def repcap_store_get(self) -> repcap.Store:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def state(self):
		"""state commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def iq(self):
		"""iq commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_iq'):
			from .Iq import IqCls
			self._iq = IqCls(self._core, self._cmd_group)
		return self._iq

	@property
	def trace(self):
		"""trace commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_trace'):
			from .Trace import TraceCls
			self._trace = TraceCls(self._core, self._cmd_group)
		return self._trace

	@property
	def table(self):
		"""table commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_table'):
			from .Table import TableCls
			self._table = TableCls(self._core, self._cmd_group)
		return self._table

	@property
	def peak(self):
		"""peak commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_peak'):
			from .Peak import PeakCls
			self._peak = PeakCls(self._core, self._cmd_group)
		return self._peak

	@property
	def spurious(self):
		"""spurious commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spurious'):
			from .Spurious import SpuriousCls
			self._spurious = SpuriousCls(self._core, self._cmd_group)
		return self._spurious

	@property
	def listPy(self):
		"""listPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_listPy'):
			from .ListPy import ListPyCls
			self._listPy = ListPyCls(self._core, self._cmd_group)
		return self._listPy

	@property
	def spectrogram(self):
		"""spectrogram commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spectrogram'):
			from .Spectrogram import SpectrogramCls
			self._spectrogram = SpectrogramCls(self._core, self._cmd_group)
		return self._spectrogram

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePyCls
			self._typePy = TypePyCls(self._core, self._cmd_group)
		return self._typePy

	@property
	def tfactor(self):
		"""tfactor commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tfactor'):
			from .Tfactor import TfactorCls
			self._tfactor = TfactorCls(self._core, self._cmd_group)
		return self._tfactor

	def clone(self) -> 'StoreCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = StoreCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

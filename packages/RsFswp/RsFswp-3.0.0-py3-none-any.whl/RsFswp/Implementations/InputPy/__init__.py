from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.RepeatedCapability import RepeatedCapability
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InputPyCls:
	"""InputPy commands group definition. 46 total commands, 17 Subgroups, 0 group commands
	Repeated Capability: InputIx, default value after init: InputIx.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("inputPy", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_inputIx_get', 'repcap_inputIx_set', repcap.InputIx.Nr1)

	def repcap_inputIx_set(self, inputIx: repcap.InputIx) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to InputIx.Default
		Default value after init: InputIx.Nr1"""
		self._cmd_group.set_repcap_enum_value(inputIx)

	def repcap_inputIx_get(self) -> repcap.InputIx:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def file(self):
		"""file commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_file'):
			from .File import FileCls
			self._file = FileCls(self._core, self._cmd_group)
		return self._file

	@property
	def connector(self):
		"""connector commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_connector'):
			from .Connector import ConnectorCls
			self._connector = ConnectorCls(self._core, self._cmd_group)
		return self._connector

	@property
	def diq(self):
		"""diq commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_diq'):
			from .Diq import DiqCls
			self._diq = DiqCls(self._core, self._cmd_group)
		return self._diq

	@property
	def eatt(self):
		"""eatt commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_eatt'):
			from .Eatt import EattCls
			self._eatt = EattCls(self._core, self._cmd_group)
		return self._eatt

	@property
	def iq(self):
		"""iq commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_iq'):
			from .Iq import IqCls
			self._iq = IqCls(self._core, self._cmd_group)
		return self._iq

	@property
	def sanalyzer(self):
		"""sanalyzer commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sanalyzer'):
			from .Sanalyzer import SanalyzerCls
			self._sanalyzer = SanalyzerCls(self._core, self._cmd_group)
		return self._sanalyzer

	@property
	def uport(self):
		"""uport commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_uport'):
			from .Uport import UportCls
			self._uport = UportCls(self._core, self._cmd_group)
		return self._uport

	@property
	def loscillator(self):
		"""loscillator commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_loscillator'):
			from .Loscillator import LoscillatorCls
			self._loscillator = LoscillatorCls(self._core, self._cmd_group)
		return self._loscillator

	@property
	def egain(self):
		"""egain commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_egain'):
			from .Egain import EgainCls
			self._egain = EgainCls(self._core, self._cmd_group)
		return self._egain

	@property
	def attenuation(self):
		"""attenuation commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_attenuation'):
			from .Attenuation import AttenuationCls
			self._attenuation = AttenuationCls(self._core, self._cmd_group)
		return self._attenuation

	@property
	def terminator(self):
		"""terminator commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_terminator'):
			from .Terminator import TerminatorCls
			self._terminator = TerminatorCls(self._core, self._cmd_group)
		return self._terminator

	@property
	def coupling(self):
		"""coupling commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_coupling'):
			from .Coupling import CouplingCls
			self._coupling = CouplingCls(self._core, self._cmd_group)
		return self._coupling

	@property
	def dpath(self):
		"""dpath commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dpath'):
			from .Dpath import DpathCls
			self._dpath = DpathCls(self._core, self._cmd_group)
		return self._dpath

	@property
	def filterPy(self):
		"""filterPy commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_filterPy'):
			from .FilterPy import FilterPyCls
			self._filterPy = FilterPyCls(self._core, self._cmd_group)
		return self._filterPy

	@property
	def gain(self):
		"""gain commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_gain'):
			from .Gain import GainCls
			self._gain = GainCls(self._core, self._cmd_group)
		return self._gain

	@property
	def impedance(self):
		"""impedance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_impedance'):
			from .Impedance import ImpedanceCls
			self._impedance = ImpedanceCls(self._core, self._cmd_group)
		return self._impedance

	@property
	def select(self):
		"""select commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_select'):
			from .Select import SelectCls
			self._select = SelectCls(self._core, self._cmd_group)
		return self._select

	def clone(self) -> 'InputPyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = InputPyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

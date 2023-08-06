from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UserCls:
	"""User commands group definition. 40 total commands, 12 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("user", core, parent)

	@property
	def iq(self):
		"""iq commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_iq'):
			from .Iq import IqCls
			self._iq = IqCls(self._core, self._cmd_group)
		return self._iq

	@property
	def spectrum(self):
		"""spectrum commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_spectrum'):
			from .Spectrum import SpectrumCls
			self._spectrum = SpectrumCls(self._core, self._cmd_group)
		return self._spectrum

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def fstate(self):
		"""fstate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fstate'):
			from .Fstate import FstateCls
			self._fstate = FstateCls(self._core, self._cmd_group)
		return self._fstate

	@property
	def scope(self):
		"""scope commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scope'):
			from .Scope import ScopeCls
			self._scope = ScopeCls(self._core, self._cmd_group)
		return self._scope

	@property
	def adjust(self):
		"""adjust commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_adjust'):
			from .Adjust import AdjustCls
			self._adjust = AdjustCls(self._core, self._cmd_group)
		return self._adjust

	@property
	def valid(self):
		"""valid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_valid'):
			from .Valid import ValidCls
			self._valid = ValidCls(self._core, self._cmd_group)
		return self._valid

	@property
	def scovered(self):
		"""scovered commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scovered'):
			from .Scovered import ScoveredCls
			self._scovered = ScoveredCls(self._core, self._cmd_group)
		return self._scovered

	@property
	def store(self):
		"""store commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_store'):
			from .Store import StoreCls
			self._store = StoreCls(self._core, self._cmd_group)
		return self._store

	@property
	def flist(self):
		"""flist commands group. 8 Sub-classes, 1 commands."""
		if not hasattr(self, '_flist'):
			from .Flist import FlistCls
			self._flist = FlistCls(self._core, self._cmd_group)
		return self._flist

	@property
	def slist(self):
		"""slist commands group. 8 Sub-classes, 2 commands."""
		if not hasattr(self, '_slist'):
			from .Slist import SlistCls
			self._slist = SlistCls(self._core, self._cmd_group)
		return self._slist

	@property
	def pstate(self):
		"""pstate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pstate'):
			from .Pstate import PstateCls
			self._pstate = PstateCls(self._core, self._cmd_group)
		return self._pstate

	def preset(self) -> None:
		"""SCPI: [SENSe]:CORRection:FRESponse:USER:PRESet \n
		Snippet: driver.sense.correction.fresponse.user.preset() \n
		No command help available \n
		"""
		self._core.io.write(f'SENSe:CORRection:FRESponse:USER:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SENSe]:CORRection:FRESponse:USER:PRESet \n
		Snippet: driver.sense.correction.fresponse.user.preset_with_opc() \n
		No command help available \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsFswp.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SENSe:CORRection:FRESponse:USER:PRESet', opc_timeout_ms)

	def load(self, file_path: str) -> None:
		"""SCPI: [SENSe]:CORRection:FRESponse:USER:LOAD \n
		Snippet: driver.sense.correction.fresponse.user.load(file_path = '1') \n
		No command help available \n
			:param file_path: No help available
		"""
		param = Conversions.value_to_quoted_str(file_path)
		self._core.io.write(f'SENSe:CORRection:FRESponse:USER:LOAD {param}')

	def clone(self) -> 'UserCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UserCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

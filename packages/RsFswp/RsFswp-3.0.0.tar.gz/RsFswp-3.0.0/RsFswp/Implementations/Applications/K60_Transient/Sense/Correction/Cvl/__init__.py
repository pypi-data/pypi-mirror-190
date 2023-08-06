from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CvlCls:
	"""Cvl commands group definition. 11 total commands, 10 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cvl", core, parent)

	@property
	def band(self):
		"""band commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_band'):
			from .Band import BandCls
			self._band = BandCls(self._core, self._cmd_group)
		return self._band

	@property
	def bias(self):
		"""bias commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bias'):
			from .Bias import BiasCls
			self._bias = BiasCls(self._core, self._cmd_group)
		return self._bias

	@property
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_catalog'):
			from .Catalog import CatalogCls
			self._catalog = CatalogCls(self._core, self._cmd_group)
		return self._catalog

	@property
	def comment(self):
		"""comment commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_comment'):
			from .Comment import CommentCls
			self._comment = CommentCls(self._core, self._cmd_group)
		return self._comment

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	@property
	def harmonic(self):
		"""harmonic commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_harmonic'):
			from .Harmonic import HarmonicCls
			self._harmonic = HarmonicCls(self._core, self._cmd_group)
		return self._harmonic

	@property
	def mixer(self):
		"""mixer commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mixer'):
			from .Mixer import MixerCls
			self._mixer = MixerCls(self._core, self._cmd_group)
		return self._mixer

	@property
	def ports(self):
		"""ports commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ports'):
			from .Ports import PortsCls
			self._ports = PortsCls(self._core, self._cmd_group)
		return self._ports

	@property
	def select(self):
		"""select commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_select'):
			from .Select import SelectCls
			self._select = SelectCls(self._core, self._cmd_group)
		return self._select

	@property
	def snumber(self):
		"""snumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_snumber'):
			from .Snumber import SnumberCls
			self._snumber = SnumberCls(self._core, self._cmd_group)
		return self._snumber

	def clear(self) -> None:
		"""SCPI: [SENSe]:CORRection:CVL:CLEar \n
		Snippet: driver.applications.k60Transient.sense.correction.cvl.clear() \n
		No command help available \n
		"""
		self._core.io.write(f'SENSe:CORRection:CVL:CLEar')

	def clear_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SENSe]:CORRection:CVL:CLEar \n
		Snippet: driver.applications.k60Transient.sense.correction.cvl.clear_with_opc() \n
		No command help available \n
		Same as clear, but waits for the operation to complete before continuing further. Use the RsFswp.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SENSe:CORRection:CVL:CLEar', opc_timeout_ms)

	def clone(self) -> 'CvlCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CvlCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

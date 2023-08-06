from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StatisticCls:
	"""Statistic commands group definition. 19 total commands, 16 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("statistic", core, parent)

	@property
	def all(self):
		"""all commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_all'):
			from .All import AllCls
			self._all = AllCls(self._core, self._cmd_group)
		return self._all

	@property
	def adroop(self):
		"""adroop commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_adroop'):
			from .Adroop import AdroopCls
			self._adroop = AdroopCls(self._core, self._cmd_group)
		return self._adroop

	@property
	def cfError(self):
		"""cfError commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cfError'):
			from .CfError import CfErrorCls
			self._cfError = CfErrorCls(self._core, self._cmd_group)
		return self._cfError

	@property
	def evm(self):
		"""evm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_evm'):
			from .Evm import EvmCls
			self._evm = EvmCls(self._core, self._cmd_group)
		return self._evm

	@property
	def gimbalance(self):
		"""gimbalance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gimbalance'):
			from .Gimbalance import GimbalanceCls
			self._gimbalance = GimbalanceCls(self._core, self._cmd_group)
		return self._gimbalance

	@property
	def fdError(self):
		"""fdError commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fdError'):
			from .FdError import FdErrorCls
			self._fdError = FdErrorCls(self._core, self._cmd_group)
		return self._fdError

	@property
	def iqImbalance(self):
		"""iqImbalance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iqImbalance'):
			from .IqImbalance import IqImbalanceCls
			self._iqImbalance = IqImbalanceCls(self._core, self._cmd_group)
		return self._iqImbalance

	@property
	def merror(self):
		"""merror commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_merror'):
			from .Merror import MerrorCls
			self._merror = MerrorCls(self._core, self._cmd_group)
		return self._merror

	@property
	def mpower(self):
		"""mpower commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mpower'):
			from .Mpower import MpowerCls
			self._mpower = MpowerCls(self._core, self._cmd_group)
		return self._mpower

	@property
	def ooffset(self):
		"""ooffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ooffset'):
			from .Ooffset import OoffsetCls
			self._ooffset = OoffsetCls(self._core, self._cmd_group)
		return self._ooffset

	@property
	def perror(self):
		"""perror commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_perror'):
			from .Perror import PerrorCls
			self._perror = PerrorCls(self._core, self._cmd_group)
		return self._perror

	@property
	def qerror(self):
		"""qerror commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_qerror'):
			from .Qerror import QerrorCls
			self._qerror = QerrorCls(self._core, self._cmd_group)
		return self._qerror

	@property
	def rho(self):
		"""rho commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rho'):
			from .Rho import RhoCls
			self._rho = RhoCls(self._core, self._cmd_group)
		return self._rho

	@property
	def srError(self):
		"""srError commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_srError'):
			from .SrError import SrErrorCls
			self._srError = SrErrorCls(self._core, self._cmd_group)
		return self._srError

	@property
	def snr(self):
		"""snr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_snr'):
			from .Snr import SnrCls
			self._snr = SnrCls(self._core, self._cmd_group)
		return self._snr

	@property
	def fsk(self):
		"""fsk commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_fsk'):
			from .Fsk import FskCls
			self._fsk = FskCls(self._core, self._cmd_group)
		return self._fsk

	def clone(self) -> 'StatisticCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = StatisticCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

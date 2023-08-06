from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ServiceCls:
	"""Service commands group definition. 32 total commands, 12 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("service", core, parent)

	@property
	def date(self):
		"""date commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_date'):
			from .Date import DateCls
			self._date = DateCls(self._core, self._cmd_group)
		return self._date

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def calibration(self):
		"""calibration commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_calibration'):
			from .Calibration import CalibrationCls
			self._calibration = CalibrationCls(self._core, self._cmd_group)
		return self._calibration

	@property
	def inputPy(self):
		"""inputPy commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_inputPy'):
			from .InputPy import InputPyCls
			self._inputPy = InputPyCls(self._core, self._cmd_group)
		return self._inputPy

	@property
	def sfunction(self):
		"""sfunction commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfunction'):
			from .Sfunction import SfunctionCls
			self._sfunction = SfunctionCls(self._core, self._cmd_group)
		return self._sfunction

	@property
	def stest(self):
		"""stest commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_stest'):
			from .Stest import StestCls
			self._stest = StestCls(self._core, self._cmd_group)
		return self._stest

	@property
	def spCheck(self):
		"""spCheck commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_spCheck'):
			from .SpCheck import SpCheckCls
			self._spCheck = SpCheckCls(self._core, self._cmd_group)
		return self._spCheck

	@property
	def biosInfo(self):
		"""biosInfo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_biosInfo'):
			from .BiosInfo import BiosInfoCls
			self._biosInfo = BiosInfoCls(self._core, self._cmd_group)
		return self._biosInfo

	@property
	def hwInfo(self):
		"""hwInfo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hwInfo'):
			from .HwInfo import HwInfoCls
			self._hwInfo = HwInfoCls(self._core, self._cmd_group)
		return self._hwInfo

	@property
	def versionInfo(self):
		"""versionInfo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_versionInfo'):
			from .VersionInfo import VersionInfoCls
			self._versionInfo = VersionInfoCls(self._core, self._cmd_group)
		return self._versionInfo

	@property
	def sinfo(self):
		"""sinfo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sinfo'):
			from .Sinfo import SinfoCls
			self._sinfo = SinfoCls(self._core, self._cmd_group)
		return self._sinfo

	@property
	def nsource(self):
		"""nsource commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsource'):
			from .Nsource import NsourceCls
			self._nsource = NsourceCls(self._core, self._cmd_group)
		return self._nsource

	def clone(self) -> 'ServiceCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ServiceCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

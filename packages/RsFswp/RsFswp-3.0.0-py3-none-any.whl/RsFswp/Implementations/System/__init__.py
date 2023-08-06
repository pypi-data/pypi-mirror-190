from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SystemCls:
	"""System commands group definition. 86 total commands, 29 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("system", core, parent)

	@property
	def preset(self):
		"""preset commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_preset'):
			from .Preset import PresetCls
			self._preset = PresetCls(self._core, self._cmd_group)
		return self._preset

	@property
	def communicate(self):
		"""communicate commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_communicate'):
			from .Communicate import CommunicateCls
			self._communicate = CommunicateCls(self._core, self._cmd_group)
		return self._communicate

	@property
	def error(self):
		"""error commands group. 4 Sub-classes, 1 commands."""
		if not hasattr(self, '_error'):
			from .Error import ErrorCls
			self._error = ErrorCls(self._core, self._cmd_group)
		return self._error

	@property
	def help(self):
		"""help commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_help'):
			from .Help import HelpCls
			self._help = HelpCls(self._core, self._cmd_group)
		return self._help

	@property
	def set(self):
		"""set commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_set'):
			from .Set import SetCls
			self._set = SetCls(self._core, self._cmd_group)
		return self._set

	@property
	def test(self):
		"""test commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_test'):
			from .Test import TestCls
			self._test = TestCls(self._core, self._cmd_group)
		return self._test

	@property
	def identify(self):
		"""identify commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_identify'):
			from .Identify import IdentifyCls
			self._identify = IdentifyCls(self._core, self._cmd_group)
		return self._identify

	@property
	def revision(self):
		"""revision commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_revision'):
			from .Revision import RevisionCls
			self._revision = RevisionCls(self._core, self._cmd_group)
		return self._revision

	@property
	def display(self):
		"""display commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_display'):
			from .Display import DisplayCls
			self._display = DisplayCls(self._core, self._cmd_group)
		return self._display

	@property
	def firmware(self):
		"""firmware commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_firmware'):
			from .Firmware import FirmwareCls
			self._firmware = FirmwareCls(self._core, self._cmd_group)
		return self._firmware

	@property
	def ifGain(self):
		"""ifGain commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ifGain'):
			from .IfGain import IfGainCls
			self._ifGain = IfGainCls(self._core, self._cmd_group)
		return self._ifGain

	@property
	def language(self):
		"""language commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_language'):
			from .Language import LanguageCls
			self._language = LanguageCls(self._core, self._cmd_group)
		return self._language

	@property
	def plugin(self):
		"""plugin commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_plugin'):
			from .Plugin import PluginCls
			self._plugin = PluginCls(self._core, self._cmd_group)
		return self._plugin

	@property
	def psa(self):
		"""psa commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_psa'):
			from .Psa import PsaCls
			self._psa = PsaCls(self._core, self._cmd_group)
		return self._psa

	@property
	def preamp(self):
		"""preamp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_preamp'):
			from .Preamp import PreampCls
			self._preamp = PreampCls(self._core, self._cmd_group)
		return self._preamp

	@property
	def rsweep(self):
		"""rsweep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rsweep'):
			from .Rsweep import RsweepCls
			self._rsweep = RsweepCls(self._core, self._cmd_group)
		return self._rsweep

	@property
	def formatPy(self):
		"""formatPy commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_formatPy'):
			from .FormatPy import FormatPyCls
			self._formatPy = FormatPyCls(self._core, self._cmd_group)
		return self._formatPy

	@property
	def compatible(self):
		"""compatible commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_compatible'):
			from .Compatible import CompatibleCls
			self._compatible = CompatibleCls(self._core, self._cmd_group)
		return self._compatible

	@property
	def clogging(self):
		"""clogging commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_clogging'):
			from .Clogging import CloggingCls
			self._clogging = CloggingCls(self._core, self._cmd_group)
		return self._clogging

	@property
	def shutdown(self):
		"""shutdown commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_shutdown'):
			from .Shutdown import ShutdownCls
			self._shutdown = ShutdownCls(self._core, self._cmd_group)
		return self._shutdown

	@property
	def reboot(self):
		"""reboot commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reboot'):
			from .Reboot import RebootCls
			self._reboot = RebootCls(self._core, self._cmd_group)
		return self._reboot

	@property
	def osystem(self):
		"""osystem commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_osystem'):
			from .Osystem import OsystemCls
			self._osystem = OsystemCls(self._core, self._cmd_group)
		return self._osystem

	@property
	def deviceFootprint(self):
		"""deviceFootprint commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_deviceFootprint'):
			from .DeviceFootprint import DeviceFootprintCls
			self._deviceFootprint = DeviceFootprintCls(self._core, self._cmd_group)
		return self._deviceFootprint

	@property
	def lxi(self):
		"""lxi commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_lxi'):
			from .Lxi import LxiCls
			self._lxi = LxiCls(self._core, self._cmd_group)
		return self._lxi

	@property
	def sequencer(self):
		"""sequencer commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sequencer'):
			from .Sequencer import SequencerCls
			self._sequencer = SequencerCls(self._core, self._cmd_group)
		return self._sequencer

	@property
	def security(self):
		"""security commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_security'):
			from .Security import SecurityCls
			self._security = SecurityCls(self._core, self._cmd_group)
		return self._security

	@property
	def srecorder(self):
		"""srecorder commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_srecorder'):
			from .Srecorder import SrecorderCls
			self._srecorder = SrecorderCls(self._core, self._cmd_group)
		return self._srecorder

	@property
	def shImmediate(self):
		"""shImmediate commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_shImmediate'):
			from .ShImmediate import ShImmediateCls
			self._shImmediate = ShImmediateCls(self._core, self._cmd_group)
		return self._shImmediate

	@property
	def option(self):
		"""option commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_option'):
			from .Option import OptionCls
			self._option = OptionCls(self._core, self._cmd_group)
		return self._option

	def clone(self) -> 'SystemCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SystemCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

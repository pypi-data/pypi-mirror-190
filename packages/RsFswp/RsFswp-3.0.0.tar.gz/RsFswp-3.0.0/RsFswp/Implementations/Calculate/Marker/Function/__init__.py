from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FunctionCls:
	"""Function commands group definition. 90 total commands, 17 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("function", core, parent)

	@property
	def afPhase(self):
		"""afPhase commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_afPhase'):
			from .AfPhase import AfPhaseCls
			self._afPhase = AfPhaseCls(self._core, self._cmd_group)
		return self._afPhase

	@property
	def fpeaks(self):
		"""fpeaks commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_fpeaks'):
			from .Fpeaks import FpeaksCls
			self._fpeaks = FpeaksCls(self._core, self._cmd_group)
		return self._fpeaks

	@property
	def ndbDown(self):
		"""ndbDown commands group. 5 Sub-classes, 1 commands."""
		if not hasattr(self, '_ndbDown'):
			from .NdbDown import NdbDownCls
			self._ndbDown = NdbDownCls(self._core, self._cmd_group)
		return self._ndbDown

	@property
	def noise(self):
		"""noise commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_noise'):
			from .Noise import NoiseCls
			self._noise = NoiseCls(self._core, self._cmd_group)
		return self._noise

	@property
	def pnoise(self):
		"""pnoise commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_pnoise'):
			from .Pnoise import PnoiseCls
			self._pnoise = PnoiseCls(self._core, self._cmd_group)
		return self._pnoise

	@property
	def mdepth(self):
		"""mdepth commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_mdepth'):
			from .Mdepth import MdepthCls
			self._mdepth = MdepthCls(self._core, self._cmd_group)
		return self._mdepth

	@property
	def toi(self):
		"""toi commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_toi'):
			from .Toi import ToiCls
			self._toi = ToiCls(self._core, self._cmd_group)
		return self._toi

	@property
	def bpower(self):
		"""bpower commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_bpower'):
			from .Bpower import BpowerCls
			self._bpower = BpowerCls(self._core, self._cmd_group)
		return self._bpower

	@property
	def center(self):
		"""center commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_center'):
			from .Center import CenterCls
			self._center = CenterCls(self._core, self._cmd_group)
		return self._center

	@property
	def cstep(self):
		"""cstep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cstep'):
			from .Cstep import CstepCls
			self._cstep = CstepCls(self._core, self._cmd_group)
		return self._cstep

	@property
	def reference(self):
		"""reference commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reference'):
			from .Reference import ReferenceCls
			self._reference = ReferenceCls(self._core, self._cmd_group)
		return self._reference

	@property
	def ademod(self):
		"""ademod commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_ademod'):
			from .Ademod import AdemodCls
			self._ademod = AdemodCls(self._core, self._cmd_group)
		return self._ademod

	@property
	def power(self):
		"""power commands group. 6 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def strack(self):
		"""strack commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_strack'):
			from .Strack import StrackCls
			self._strack = StrackCls(self._core, self._cmd_group)
		return self._strack

	@property
	def summary(self):
		"""summary commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_summary'):
			from .Summary import SummaryCls
			self._summary = SummaryCls(self._core, self._cmd_group)
		return self._summary

	@property
	def msummary(self):
		"""msummary commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_msummary'):
			from .Msummary import MsummaryCls
			self._msummary = MsummaryCls(self._core, self._cmd_group)
		return self._msummary

	@property
	def harmonics(self):
		"""harmonics commands group. 5 Sub-classes, 1 commands."""
		if not hasattr(self, '_harmonics'):
			from .Harmonics import HarmonicsCls
			self._harmonics = HarmonicsCls(self._core, self._cmd_group)
		return self._harmonics

	def clone(self) -> 'FunctionCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FunctionCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

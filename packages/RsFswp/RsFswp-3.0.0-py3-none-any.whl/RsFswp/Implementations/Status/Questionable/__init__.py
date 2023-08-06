from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class QuestionableCls:
	"""Questionable commands group definition. 100 total commands, 20 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("questionable", core, parent)

	@property
	def event(self):
		"""event commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_event'):
			from .Event import EventCls
			self._event = EventCls(self._core, self._cmd_group)
		return self._event

	@property
	def condition(self):
		"""condition commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_condition'):
			from .Condition import ConditionCls
			self._condition = ConditionCls(self._core, self._cmd_group)
		return self._condition

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .Enable import EnableCls
			self._enable = EnableCls(self._core, self._cmd_group)
		return self._enable

	@property
	def ptransition(self):
		"""ptransition commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ptransition'):
			from .Ptransition import PtransitionCls
			self._ptransition = PtransitionCls(self._core, self._cmd_group)
		return self._ptransition

	@property
	def ntransition(self):
		"""ntransition commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ntransition'):
			from .Ntransition import NtransitionCls
			self._ntransition = NtransitionCls(self._core, self._cmd_group)
		return self._ntransition

	@property
	def power(self):
		"""power commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_power'):
			from .Power import PowerCls
			self._power = PowerCls(self._core, self._cmd_group)
		return self._power

	@property
	def limit(self):
		"""limit commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_limit'):
			from .Limit import LimitCls
			self._limit = LimitCls(self._core, self._cmd_group)
		return self._limit

	@property
	def lmargin(self):
		"""lmargin commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_lmargin'):
			from .Lmargin import LmarginCls
			self._lmargin = LmarginCls(self._core, self._cmd_group)
		return self._lmargin

	@property
	def acpLimit(self):
		"""acpLimit commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_acpLimit'):
			from .AcpLimit import AcpLimitCls
			self._acpLimit = AcpLimitCls(self._core, self._cmd_group)
		return self._acpLimit

	@property
	def frequency(self):
		"""frequency commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	@property
	def sync(self):
		"""sync commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_sync'):
			from .Sync import SyncCls
			self._sync = SyncCls(self._core, self._cmd_group)
		return self._sync

	@property
	def diq(self):
		"""diq commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_diq'):
			from .Diq import DiqCls
			self._diq = DiqCls(self._core, self._cmd_group)
		return self._diq

	@property
	def time(self):
		"""time commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_time'):
			from .Time import TimeCls
			self._time = TimeCls(self._core, self._cmd_group)
		return self._time

	@property
	def transducer(self):
		"""transducer commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_transducer'):
			from .Transducer import TransducerCls
			self._transducer = TransducerCls(self._core, self._cmd_group)
		return self._transducer

	@property
	def temperature(self):
		"""temperature commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_temperature'):
			from .Temperature import TemperatureCls
			self._temperature = TemperatureCls(self._core, self._cmd_group)
		return self._temperature

	@property
	def pnoise(self):
		"""pnoise commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_pnoise'):
			from .Pnoise import PnoiseCls
			self._pnoise = PnoiseCls(self._core, self._cmd_group)
		return self._pnoise

	@property
	def correction(self):
		"""correction commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_correction'):
			from .Correction import CorrectionCls
			self._correction = CorrectionCls(self._core, self._cmd_group)
		return self._correction

	@property
	def extended(self):
		"""extended commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_extended'):
			from .Extended import ExtendedCls
			self._extended = ExtendedCls(self._core, self._cmd_group)
		return self._extended

	@property
	def calibration(self):
		"""calibration commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_calibration'):
			from .Calibration import CalibrationCls
			self._calibration = CalibrationCls(self._core, self._cmd_group)
		return self._calibration

	@property
	def integrity(self):
		"""integrity commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_integrity'):
			from .Integrity import IntegrityCls
			self._integrity = IntegrityCls(self._core, self._cmd_group)
		return self._integrity

	def clone(self) -> 'QuestionableCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = QuestionableCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

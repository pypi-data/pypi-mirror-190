from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TreportCls:
	"""Treport commands group definition. 29 total commands, 10 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("treport", core, parent)

	@property
	def append(self):
		"""append commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_append'):
			from .Append import AppendCls
			self._append = AppendCls(self._core, self._cmd_group)
		return self._append

	@property
	def description(self):
		"""description commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_description'):
			from .Description import DescriptionCls
			self._description = DescriptionCls(self._core, self._cmd_group)
		return self._description

	@property
	def item(self):
		"""item commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_item'):
			from .Item import ItemCls
			self._item = ItemCls(self._core, self._cmd_group)
		return self._item

	@property
	def new(self):
		"""new commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_new'):
			from .New import NewCls
			self._new = NewCls(self._core, self._cmd_group)
		return self._new

	@property
	def pageSize(self):
		"""pageSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pageSize'):
			from .PageSize import PageSizeCls
			self._pageSize = PageSizeCls(self._core, self._cmd_group)
		return self._pageSize

	@property
	def pcolors(self):
		"""pcolors commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_pcolors'):
			from .Pcolors import PcolorsCls
			self._pcolors = PcolorsCls(self._core, self._cmd_group)
		return self._pcolors

	@property
	def pagecount(self):
		"""pagecount commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_pagecount'):
			from .Pagecount import PagecountCls
			self._pagecount = PagecountCls(self._core, self._cmd_group)
		return self._pagecount

	@property
	def tdDtamp(self):
		"""tdDtamp commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_tdDtamp'):
			from .TdDtamp import TdDtampCls
			self._tdDtamp = TdDtampCls(self._core, self._cmd_group)
		return self._tdDtamp

	@property
	def test(self):
		"""test commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_test'):
			from .Test import TestCls
			self._test = TestCls(self._core, self._cmd_group)
		return self._test

	@property
	def title(self):
		"""title commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_title'):
			from .Title import TitleCls
			self._title = TitleCls(self._core, self._cmd_group)
		return self._title

	def clone(self) -> 'TreportCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TreportCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

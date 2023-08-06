from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ItemCls:
	"""Item commands group definition. 13 total commands, 6 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("item", core, parent)

	@property
	def default(self):
		"""default commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_default'):
			from .Default import DefaultCls
			self._default = DefaultCls(self._core, self._cmd_group)
		return self._default

	@property
	def header(self):
		"""header commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_header'):
			from .Header import HeaderCls
			self._header = HeaderCls(self._core, self._cmd_group)
		return self._header

	@property
	def logo(self):
		"""logo commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_logo'):
			from .Logo import LogoCls
			self._logo = LogoCls(self._core, self._cmd_group)
		return self._logo

	@property
	def select(self):
		"""select commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_select'):
			from .Select import SelectCls
			self._select = SelectCls(self._core, self._cmd_group)
		return self._select

	@property
	def listPy(self):
		"""listPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_listPy'):
			from .ListPy import ListPyCls
			self._listPy = ListPyCls(self._core, self._cmd_group)
		return self._listPy

	@property
	def template(self):
		"""template commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_template'):
			from .Template import TemplateCls
			self._template = TemplateCls(self._core, self._cmd_group)
		return self._template

	def clone(self) -> 'ItemCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ItemCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

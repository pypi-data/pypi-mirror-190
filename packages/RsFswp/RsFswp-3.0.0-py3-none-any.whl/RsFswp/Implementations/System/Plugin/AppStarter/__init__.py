from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AppStarterCls:
	"""AppStarter commands group definition. 7 total commands, 6 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("appStarter", core, parent)

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .Execute import ExecuteCls
			self._execute = ExecuteCls(self._core, self._cmd_group)
		return self._execute

	@property
	def select(self):
		"""select commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_select'):
			from .Select import SelectCls
			self._select = SelectCls(self._core, self._cmd_group)
		return self._select

	@property
	def params(self):
		"""params commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_params'):
			from .Params import ParamsCls
			self._params = ParamsCls(self._core, self._cmd_group)
		return self._params

	@property
	def directory(self):
		"""directory commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_directory'):
			from .Directory import DirectoryCls
			self._directory = DirectoryCls(self._core, self._cmd_group)
		return self._directory

	@property
	def name(self):
		"""name commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_name'):
			from .Name import NameCls
			self._name = NameCls(self._core, self._cmd_group)
		return self._name

	@property
	def icon(self):
		"""icon commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_icon'):
			from .Icon import IconCls
			self._icon = IconCls(self._core, self._cmd_group)
		return self._icon

	def delete(self, application_group: str, display_name: str) -> None:
		"""SCPI: SYSTem:PLUGin:APPStarter:DELete \n
		Snippet: driver.system.plugin.appStarter.delete(application_group = '1', display_name = '1') \n
		No command help available \n
			:param application_group: No help available
			:param display_name: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('application_group', application_group, DataType.String), ArgSingle('display_name', display_name, DataType.String))
		self._core.io.write(f'SYSTem:PLUGin:APPStarter:DELete {param}'.rstrip())

	def clone(self) -> 'AppStarterCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AppStarterCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

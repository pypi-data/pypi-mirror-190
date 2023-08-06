from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SelectCls:
	"""Select commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("select", core, parent)

	def set(self, item: str, arg_1: str = None) -> None:
		"""SCPI: HCOPy:TREPort:ITEM:SELect \n
		Snippet: driver.hardCopy.treport.item.select.set(item = r1, arg_1 = '1') \n
		No command help available \n
			:param item: No help available
			:param arg_1: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('item', item, DataType.RawString), ArgSingle('arg_1', arg_1, DataType.String, None, is_optional=True))
		self._core.io.write(f'HCOPy:TREPort:ITEM:SELect {param}'.rstrip())

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, channel: str, window: str, state: bool) -> None:
		"""SCPI: HCOPy:PAGE:WINDow:STATe \n
		Snippet: driver.hardCopy.page.window.state.set(channel = '1', window = '1', state = False) \n
		This command selects the windows to be included in the printout for method RsFswp.HardCopy.Content.set. \n
			:param channel: String containing the name of the channel. For a list of available channel types use method RsFswp.Instrument.ListPy.get_.
			:param window: String containing the name of the existing window. By default, the name of a window is the same as its index. To determine the name and index of all active windows in the active channel, use the method RsFswp.Layout.Catalog.Window.get_ query.
			:param state: 1 | 0 | ON | OFF 1 | ON The window is included in the printout. 0 | OFF The window is not included in the printout.
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('channel', channel, DataType.String), ArgSingle('window', window, DataType.String), ArgSingle('state', state, DataType.Boolean))
		self._core.io.write(f'HCOPy:PAGE:WINDow:STATe {param}'.rstrip())

	# noinspection PyTypeChecker
	class StateStruct(StructBase):
		"""Response structure. Fields: \n
			- Channel: str: String containing the name of the channel. For a list of available channel types use [CMDLINK: INSTrument:LIST? CMDLINK].
			- Window: str: String containing the name of the existing window. By default, the name of a window is the same as its index. To determine the name and index of all active windows in the active channel, use the [CMDLINK: LAYout:CATalog[:WINDow]? CMDLINK] query.
			- State: bool: 1 | 0 | ON | OFF 1 | ON The window is included in the printout. 0 | OFF The window is not included in the printout."""
		__meta_args_list = [
			ArgStruct.scalar_str('Channel'),
			ArgStruct.scalar_str('Window'),
			ArgStruct.scalar_bool('State')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Channel: str = None
			self.Window: str = None
			self.State: bool = None

	def get(self) -> StateStruct:
		"""SCPI: HCOPy:PAGE:WINDow:STATe \n
		Snippet: value: StateStruct = driver.hardCopy.page.window.state.get() \n
		This command selects the windows to be included in the printout for method RsFswp.HardCopy.Content.set. \n
			:return: structure: for return value, see the help for StateStruct structure arguments."""
		return self._core.io.query_struct(f'HCOPy:PAGE:WINDow:STATe?', self.__class__.StateStruct())

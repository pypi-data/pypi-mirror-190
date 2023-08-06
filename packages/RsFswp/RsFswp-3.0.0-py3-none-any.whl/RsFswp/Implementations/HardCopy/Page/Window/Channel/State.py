from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, channel: str, state: bool) -> None:
		"""SCPI: HCOPy:PAGE:WINDow:CHANnel:STATe \n
		Snippet: driver.hardCopy.page.window.channel.state.set(channel = '1', state = False) \n
		This command selects all windows of the specified channel to be included in the printout for method RsFswp.HardCopy.
		Content.set. \n
			:param channel: String containing the name of the channel. For a list of available channel types use method RsFswp.Instrument.ListPy.get_.
			:param state: 1 | 0 | ON | OFF 1 | ON The channel windows are included in the printout. 0 | OFF The channel windows are not included in the printout.
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('channel', channel, DataType.String), ArgSingle('state', state, DataType.Boolean))
		self._core.io.write(f'HCOPy:PAGE:WINDow:CHANnel:STATe {param}'.rstrip())

	# noinspection PyTypeChecker
	class StateStruct(StructBase):
		"""Response structure. Fields: \n
			- Channel: str: String containing the name of the channel. For a list of available channel types use [CMDLINK: INSTrument:LIST? CMDLINK].
			- State: bool: 1 | 0 | ON | OFF 1 | ON The channel windows are included in the printout. 0 | OFF The channel windows are not included in the printout."""
		__meta_args_list = [
			ArgStruct.scalar_str('Channel'),
			ArgStruct.scalar_bool('State')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Channel: str = None
			self.State: bool = None

	def get(self) -> StateStruct:
		"""SCPI: HCOPy:PAGE:WINDow:CHANnel:STATe \n
		Snippet: value: StateStruct = driver.hardCopy.page.window.channel.state.get() \n
		This command selects all windows of the specified channel to be included in the printout for method RsFswp.HardCopy.
		Content.set. \n
			:return: structure: for return value, see the help for StateStruct structure arguments."""
		return self._core.io.query_struct(f'HCOPy:PAGE:WINDow:CHANnel:STATe?', self.__class__.StateStruct())

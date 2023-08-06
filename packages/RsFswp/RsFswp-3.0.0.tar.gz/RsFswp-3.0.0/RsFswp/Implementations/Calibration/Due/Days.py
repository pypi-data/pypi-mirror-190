from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DaysCls:
	"""Days commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("days", core, parent)

	# noinspection PyTypeChecker
	class DaysStruct(StructBase):
		"""Structure for setting input parameters. Contains optional setting parameters. Fields: \n
			- Day_1: enums.DaysOfWeek: ALL | MONDay | TUESday | WEDNesday | THURsday | FRIDay | SATurday | SUNDay
			- Day_2: enums.DaysOfWeek: Optional setting parameter. ALL | MONDay | TUESday | WEDNesday | THURsday | FRIDay | SATurday | SUNDay
			- Day_3: enums.DaysOfWeek: Optional setting parameter. ALL | MONDay | TUESday | WEDNesday | THURsday | FRIDay | SATurday | SUNDay
			- Day_4: enums.DaysOfWeek: Optional setting parameter. ALL | MONDay | TUESday | WEDNesday | THURsday | FRIDay | SATurday | SUNDay
			- Day_5: enums.DaysOfWeek: Optional setting parameter. ALL | MONDay | TUESday | WEDNesday | THURsday | FRIDay | SATurday | SUNDay
			- Day_6: enums.DaysOfWeek: Optional setting parameter. ALL | MONDay | TUESday | WEDNesday | THURsday | FRIDay | SATurday | SUNDay
			- Day_7: enums.DaysOfWeek: Optional setting parameter. ALL | MONDay | TUESday | WEDNesday | THURsday | FRIDay | SATurday | SUNDay"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Day_1', enums.DaysOfWeek),
			ArgStruct.scalar_enum_optional('Day_2', enums.DaysOfWeek),
			ArgStruct.scalar_enum_optional('Day_3', enums.DaysOfWeek),
			ArgStruct.scalar_enum_optional('Day_4', enums.DaysOfWeek),
			ArgStruct.scalar_enum_optional('Day_5', enums.DaysOfWeek),
			ArgStruct.scalar_enum_optional('Day_6', enums.DaysOfWeek),
			ArgStruct.scalar_enum_optional('Day_7', enums.DaysOfWeek)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Day_1: enums.DaysOfWeek = None
			self.Day_2: enums.DaysOfWeek = None
			self.Day_3: enums.DaysOfWeek = None
			self.Day_4: enums.DaysOfWeek = None
			self.Day_5: enums.DaysOfWeek = None
			self.Day_6: enums.DaysOfWeek = None
			self.Day_7: enums.DaysOfWeek = None

	def set(self, structure: DaysStruct) -> None:
		"""SCPI: CALibration:DUE:DAYS \n
		Snippet with structure: \n
		structure = driver.calibration.due.days.DaysStruct() \n
		structure.Day_1: enums.DaysOfWeek = enums.DaysOfWeek.ALL \n
		structure.Day_2: enums.DaysOfWeek = enums.DaysOfWeek.ALL \n
		structure.Day_3: enums.DaysOfWeek = enums.DaysOfWeek.ALL \n
		structure.Day_4: enums.DaysOfWeek = enums.DaysOfWeek.ALL \n
		structure.Day_5: enums.DaysOfWeek = enums.DaysOfWeek.ALL \n
		structure.Day_6: enums.DaysOfWeek = enums.DaysOfWeek.ALL \n
		structure.Day_7: enums.DaysOfWeek = enums.DaysOfWeek.ALL \n
		driver.calibration.due.days.set(structure) \n
		Defines the days on which a self-alignment is scheduled for method RsFswp.Calibration.Due.Schedule.set ON.
		Up to 7 different days can be scheduled. \n
			:param structure: for set value, see the help for DaysStruct structure arguments.
		"""
		self._core.io.write_struct(f'CALibration:DUE:DAYS', structure)

	def get(self) -> DaysStruct:
		"""SCPI: CALibration:DUE:DAYS \n
		Snippet: value: DaysStruct = driver.calibration.due.days.get() \n
		Defines the days on which a self-alignment is scheduled for method RsFswp.Calibration.Due.Schedule.set ON.
		Up to 7 different days can be scheduled. \n
			:return: structure: for return value, see the help for DaysStruct structure arguments."""
		return self._core.io.query_struct(f'CALibration:DUE:DAYS?', self.__class__.DaysStruct())

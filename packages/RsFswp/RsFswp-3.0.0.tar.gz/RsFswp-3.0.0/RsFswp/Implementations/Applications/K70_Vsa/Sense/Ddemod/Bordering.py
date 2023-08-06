from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BorderingCls:
	"""Bordering commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bordering", core, parent)

	def set(self, bit_ordering: enums.BitOrdering) -> None:
		"""SCPI: [SENSe]:DDEMod:BORDering \n
		Snippet: driver.applications.k70Vsa.sense.ddemod.bordering.set(bit_ordering = enums.BitOrdering.LSB) \n
		Determines how the bits in the symbols are ordered in all symbol displays. \n
			:param bit_ordering: MSB | LSB LSB Least-significant bit first (used in Bluetooth specification, for example) MSB Most significant bit first (default)
		"""
		param = Conversions.enum_scalar_to_str(bit_ordering, enums.BitOrdering)
		self._core.io.write(f'SENSe:DDEMod:BORDering {param}')

	# noinspection PyTypeChecker
	def get(self) -> enums.BitOrdering:
		"""SCPI: [SENSe]:DDEMod:BORDering \n
		Snippet: value: enums.BitOrdering = driver.applications.k70Vsa.sense.ddemod.bordering.get() \n
		Determines how the bits in the symbols are ordered in all symbol displays. \n
			:return: bit_ordering: MSB | LSB LSB Least-significant bit first (used in Bluetooth specification, for example) MSB Most significant bit first (default)"""
		response = self._core.io.query_str(f'SENSe:DDEMod:BORDering?')
		return Conversions.str_to_scalar_enum(response, enums.BitOrdering)

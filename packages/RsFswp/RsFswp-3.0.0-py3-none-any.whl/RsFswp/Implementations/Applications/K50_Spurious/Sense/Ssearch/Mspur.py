from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MspurCls:
	"""Mspur commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mspur", core, parent)

	def set(self, type_py: enums.MspurSearchType) -> None:
		"""SCPI: [SENSe]:SSEarch:MSPur \n
		Snippet: driver.applications.k50Spurious.sense.ssearch.mspur.set(type_py = enums.MspurSearchType.DMINimum) \n
		Defines the condition for matching the measured to the predicted spurs. \n
			:param type_py: DMINimum | PMAXimum DMINimum If multiple measured spurs are inside the tolerance range around a predicted spur, the measured spur closest to the predicted spur is identified as the predicted. PMAXimum If multiple measured spurs are inside the tolerance range around a predicted spur, the measured spur with the highest power will be identified as the predicted.
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.MspurSearchType)
		self._core.io.write(f'SENSe:SSEarch:MSPur {param}')

	# noinspection PyTypeChecker
	def get(self) -> enums.MspurSearchType:
		"""SCPI: [SENSe]:SSEarch:MSPur \n
		Snippet: value: enums.MspurSearchType = driver.applications.k50Spurious.sense.ssearch.mspur.get() \n
		Defines the condition for matching the measured to the predicted spurs. \n
			:return: type_py: DMINimum | PMAXimum DMINimum If multiple measured spurs are inside the tolerance range around a predicted spur, the measured spur closest to the predicted spur is identified as the predicted. PMAXimum If multiple measured spurs are inside the tolerance range around a predicted spur, the measured spur with the highest power will be identified as the predicted."""
		response = self._core.io.query_str(f'SENSe:SSEarch:MSPur?')
		return Conversions.str_to_scalar_enum(response, enums.MspurSearchType)

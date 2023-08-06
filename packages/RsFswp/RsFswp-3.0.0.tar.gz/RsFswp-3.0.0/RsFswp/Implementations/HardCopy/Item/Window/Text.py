from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TextCls:
	"""Text commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("text", core, parent)

	def set(self, comment: str) -> None:
		"""SCPI: HCOPy:ITEM:WINDow:TEXT \n
		Snippet: driver.hardCopy.item.window.text.set(comment = '1') \n
		This command defines a comment to be added to the printout. \n
			:param comment: String containing the comment.
		"""
		param = Conversions.value_to_quoted_str(comment)
		self._core.io.write(f'HCOPy:ITEM:WINDow:TEXT {param}')

	def get(self) -> str:
		"""SCPI: HCOPy:ITEM:WINDow:TEXT \n
		Snippet: value: str = driver.hardCopy.item.window.text.get() \n
		This command defines a comment to be added to the printout. \n
			:return: comment: String containing the comment."""
		response = self._core.io.query_str(f'HCOPy:ITEM:WINDow:TEXT?')
		return trim_str_response(response)

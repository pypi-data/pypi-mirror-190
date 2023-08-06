from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CommentCls:
	"""Comment commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("comment", core, parent)

	def set(self, comment: str) -> None:
		"""SCPI: HCOPy:COMMent \n
		Snippet: driver.hardCopy.comment.set(comment = '1') \n
		No command help available \n
			:param comment: No help available
		"""
		param = Conversions.value_to_quoted_str(comment)
		self._core.io.write(f'HCOPy:COMMent {param}')

	def get(self) -> str:
		"""SCPI: HCOPy:COMMent \n
		Snippet: value: str = driver.hardCopy.comment.get() \n
		No command help available \n
			:return: comment: No help available"""
		response = self._core.io.query_str(f'HCOPy:COMMent?')
		return trim_str_response(response)

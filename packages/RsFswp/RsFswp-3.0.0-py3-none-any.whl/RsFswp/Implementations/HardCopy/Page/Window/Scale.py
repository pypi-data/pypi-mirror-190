from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScaleCls:
	"""Scale commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("scale", core, parent)

	def set(self, scale: bool) -> None:
		"""SCPI: HCOPy:PAGE:WINDow:SCALe \n
		Snippet: driver.hardCopy.page.window.scale.set(scale = False) \n
		This command determines the scaling of the windows in the printout for method RsFswp.HardCopy.Content.set. \n
			:param scale: 1 | 0 | ON | OFF 1 | ON Each window is scaled to fit the page size optimally, not regarding the aspect ratio of the original display. If more than one window is printed on one page (see method RsFswp.HardCopy.Page.Window.Count.set) , each window is printed in equal size. ('Size to fit') 0 | OFF Each window is printed as large as possible while maintaining the aspect ratio of the original display. ('Maintain aspect ratio')
		"""
		param = Conversions.bool_to_str(scale)
		self._core.io.write(f'HCOPy:PAGE:WINDow:SCALe {param}')

	def get(self) -> bool:
		"""SCPI: HCOPy:PAGE:WINDow:SCALe \n
		Snippet: value: bool = driver.hardCopy.page.window.scale.get() \n
		This command determines the scaling of the windows in the printout for method RsFswp.HardCopy.Content.set. \n
			:return: scale: 1 | 0 | ON | OFF 1 | ON Each window is scaled to fit the page size optimally, not regarding the aspect ratio of the original display. If more than one window is printed on one page (see method RsFswp.HardCopy.Page.Window.Count.set) , each window is printed in equal size. ('Size to fit') 0 | OFF Each window is printed as large as possible while maintaining the aspect ratio of the original display. ('Maintain aspect ratio')"""
		response = self._core.io.query_str(f'HCOPy:PAGE:WINDow:SCALe?')
		return Conversions.str_to_bool(response)

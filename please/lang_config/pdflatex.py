import os
import os.path
from ..template.template_utils import get_template_full_path
from .base import BaseConfig
from ..utils.exceptions import PleaseException
import subprocess

LANGUAGE = "latex"

def is_compilation_garbage(source):
    if os.path.splitext(source)[1] == '':
        return False
    extension = os.path.splitext(source)[1]
    return extension.lower() in {'aux'}

class BaseLaTeXConfig(BaseConfig):
    template_path = get_template_full_path('')
    _command_prefix = ['pdflatex', '-output-format', 'pdf', '-interaction', 'nonstopmode']

    def _get_compile_commands(self, source):
        prefix = self._command_prefix
        return (prefix + ['-draftmode', source],
                prefix + [source])

    def is_compile_garbage (self, source):
        #return is_compilation_garbage(source)
        return False

    def _get_binaries(self, source):
        return [os.path.splitext(source)[0] + ".pdf"]

class TeXLiveConfig(BaseLaTeXConfig):
    def _get_environment(self, source):
        return {'TEXINPUTS': '.:{}:'.format(self.template_path)}

class MiKTeXConfig(BaseLaTeXConfig):
    def _setup(self):
        self._command_prefix = (BaseLaTeXConfig._command_prefix +
                                ['-include-directory', self.template_path])

class UnknownVersionTeXConfig(BaseLaTeXConfig):
    def __init__(self, source):
        raise PleaseException('Your TeX version is unknown. Please contact us'
                              ' at code.google.com/p/please')

def get_config():
    try:
        version_info = subprocess.check_output(['tex', '--version'])
    except OSError:
        raise PleaseException('Cannot run TeX, check if it is installed')
    if b'MiKTeX' in version_info:
        return MiKTeXConfig
    elif b'TeX Live' in version_info:
        return TeXLiveConfig
    else:
        return UnknownVersionTeXConfig

from .python import get_python_configurator, get_python3_configurator
from ..language import language
from .cpp import get_cpp_configurator
from .dpr import get_dpr_configurator
from .java import get_java_configurator
from .pdflatex import get_pdflatex_configurator
from .command import get_command_configurator

def get_language_configurator(file_name):
    ''' Returns configurator object by file path '''
    lang = language.get(file_name)
    if lang in ["c", "c++"]:
        return get_cpp_configurator()
    elif lang in ["pascal", "delphi"]:
        return get_dpr_configurator()
    elif lang == "java":
        return get_java_configurator()
    elif lang == "python2":
        return get_python_configurator()
    elif lang == "python3":
        return get_python3_configurator()
    elif lang in ["latex_pdf", "latex", "tex", "pdflatex"]:
        return get_pdflatex_configurator()
    elif lang in ["command"]:
        return get_command_configurator()
    else:
        return None
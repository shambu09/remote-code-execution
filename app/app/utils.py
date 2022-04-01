import sys
import io
import importlib
from types import ModuleType
from typing import List, Optional, Any
from dataclasses import dataclass, field


def __save_module_to_file(code: str, module_name: str) -> None:
    """
    Save the code to a file.
    :param str code: Code to be saved.
    :param str module_name: Name of the module.
    :return: None
    :rtype: NoneType
    """

    with open(module_name + ".py", "w") as f:
        f.write(code)


def import_file(mod_name: str) -> ModuleType:
    """
    Import a file.
    :param str mod_name: Name of the module.
    :return: Module.
    :rtype: ModuleType
    """

    module = importlib.import_module(mod_name)
    return module


def import_dmod(name: str, code: str) -> ModuleType:
    """
    Import dynamically generated code as module.
    :param str name: Name of the module.
    :param str code: Code to be imported as module.
    :return: Module.
    :rtype: ModuleType
    """

    spec = importlib.util.spec_from_loader(name, loader=None)
    module = importlib.util.module_from_spec(spec)
    exec(code, module.__dict__)

    return module


class PropertyMissingException(Exception):
    """
    Exception for missing properities.
    """
    pass


class CodeMissingException(Exception):
    """
    Exception for missing properities.
    """
    pass


class ProxyStream:
    """
    Proxy stream object for temporary storage. 
    """
    value: str = ""

    @classmethod
    def write(cls, string: str) -> None:
        cls.value += string

    @classmethod
    def flush(cls) -> None:
        pass


class PatchStd:
    """
    Context manager for monkey-patching stdout and stderr.
    """
    def __init__(self) -> None:
        self._out = sys.stdout
        self._err = sys.stderr
        self.out = io.StringIO()
        self.err = io.StringIO()
        self.value = ""

    def _print(self, *args) -> None:
        print(*args, file=self._out)

    def __enter__(self) -> "PatchStd":
        sys.stdout = self.out
        sys.stderr = self.err
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        sys.stdout = self._out
        sys.stderr = self._err
        del self.out
        del self.err


def validate_properties(module: ModuleType, properties: List[str]) -> None:
    """
    Validate properties.
    :param ModuleType module: Module or code class.
    :return: None
    """
    for property in properties:
        if not hasattr(module, property):
            raise PropertyMissingException(f"Property {property} is missing.")


@dataclass(frozen=True)
class Code:
    """
    //:param str uid: Unique identifier.
    :param str name: Name of the module.
    :param str code: Code to be imported as module.
    :param ModuleType module: Module oobject of the code.

    @param code should have following properties:
        - r_lambda : function to run.
        - r_args : arguments to pass to the function.
        - r_kwargs : keyword arguments to pass to the function.
        - r_schedule : schedule to run the function.
    """

    #//uid: str = field(default="")
    name: str = field(default="")
    code: str = field(default="", repr=False)
    run: Optional[ModuleType] = field(default=None, repr=False)

    def __post_init__(self) -> None:
        """
        Post init.
        :return: None
        :rtype: NoneType
        """
        if self.code != "":
            object.__setattr__(self, "run", import_dmod(self.name, self.code))
        else:
            raise CodeMissingException(f"Source code is missing.")

        validate_properties(self.run,
                            ["r_lambda", "r_args", "r_kwargs", "r_schedule"])


if __name__ == "__main__":
    code = """
def r_lambda(*args, **kwargs):
    print("Hello")
"""
    module_name = "test_module"

    module = Code(module_name, code)
    module.run.r_lambda()
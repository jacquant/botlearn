from RestrictedPython import compile_restricted
from RestrictedPython.PrintCollector import PrintCollector


_print_ = PrintCollector
_getattr_ = getattr
src = """{{ code_input }}
result = printed
"""
byte_code = compile_restricted(
    source=src, filename="{{ filename }}", mode="exec"
)
exec(byte_code)
print(result[:-1])

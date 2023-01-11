from callchain_checker.callchain_checker import callchain_exists
from diopter.compiler import Language, SourceProgram


def test_basic_callchain() -> None:
    program = SourceProgram(
        code="""void bar(); void foo(){bar();}""", language=Language.C
    )
    assert callchain_exists(program, "foo", "bar")
    assert not callchain_exists(program, "bar", "foo")

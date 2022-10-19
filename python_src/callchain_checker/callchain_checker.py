from __future__ import annotations

from typing import Optional
from pathlib import Path

from diopter.compiler import SourceProgram, CompilerExe, ClangTool, ClangToolMode


def get_callchain_checker(
    callchain_checker: Optional[ClangTool] = None, clang: Optional[CompilerExe] = None
) -> ClangTool:
    if not callchain_checker:
        if not clang:
            clang = CompilerExe.get_system_clang()
        callchain_checker = ClangTool.init_with_paths_from_llvm(
            Path(__file__).parent / "ccc", clang
        )
    return callchain_checker


def callchain_exists(
    program: SourceProgram,
    source_function: str,
    target_function: str,
    callchain_checker: Optional[ClangTool] = None,
    clang: Optional[CompilerExe] = None,
) -> bool:
    """Statically check if a callchain exists between the source and target
    functions in this program.

    Args:
        program (Source): The program to check
        source_function (str): the function where the search starts
        target_function (str): the function where the search ends
        callchain_checker (ClangTool): The callchain_checker
        clang (CompilerExe): Which clang to use for searching the standard include paths
    Returns:
        bool: whether a callchain exists
    """
    callchain_checker = get_callchain_checker(callchain_checker, clang)
    return (
        f"call chain exists between {source_function} -> {target_function}".strip()
        in callchain_checker.run_on_program(
            program,
            [f"--from={source_function}", f"--to={target_function}"],
            ClangToolMode.CAPTURE_OUT_ERR,
        )
    )

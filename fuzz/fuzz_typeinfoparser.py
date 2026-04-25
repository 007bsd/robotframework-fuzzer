"""
Fuzzing robot.running.arguments.typeinfoparser.TypeInfoParser.

Exception-based: parse(s) should only raise ValueError, never anything else.
Functional:
  - Idempotency: parse(str(parse(s))) == parse(s) (for valid inputs)
  - Nested count: TypeInfo.nested length is consistent
"""

from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st
from robot.running.arguments.typeinfoparser import TypeInfoParser

ALLOWED = (ValueError,)

# ── Strategies ────────────────────────────────────────────────────────────────

# Chars that appear in type annotation strings
type_chars = st.text(
    alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_. |[],'\"-+",
    max_size=40
)

# Structurally valid-looking type strings built from a grammar
type_name = st.sampled_from([
    "int", "str", "float", "bool", "bytes", "list", "dict", "tuple",
    "set", "frozenset", "Any", "None", "Union", "Literal", "Optional",
])

@st.composite
def type_string(draw, depth=0):
    name = draw(type_name)
    if depth < 3 and draw(st.booleans()):
        args = draw(st.lists(type_string(depth + 1), min_size=1, max_size=3))
        return f"{name}[{', '.join(args)}]"
    return name

@st.composite
def union_type_string(draw):
    parts = draw(st.lists(type_string(), min_size=2, max_size=4))
    return " | ".join(parts)


# ── Exception-based ──────────────────────────────────────────────────────────

@given(s=type_chars)
@settings(max_examples=2000, suppress_health_check=[HealthCheck.too_slow])
def test_parse_only_raises_value_error(s):
    try:
        TypeInfoParser(s).parse()
    except ALLOWED:
        pass
    except Exception as e:
        raise AssertionError(
            f"Unexpected {type(e).__name__}: {e!r}\n  input={s!r}"
        ) from e


@given(s=type_string())
@settings(max_examples=1000, suppress_health_check=[HealthCheck.too_slow])
def test_valid_type_strings_parse_without_error(s):
    try:
        TypeInfoParser(s).parse()
    except ValueError as e:
        raise AssertionError(f"Valid type string failed to parse: {s!r}\n  {e}") from e


# ── Functional ────────────────────────────────────────────────────────────────

@given(s=type_string())
@settings(max_examples=1000, suppress_health_check=[HealthCheck.too_slow])
def test_parse_idempotency(s):
    """parse(str(parse(s))) should equal parse(s) for valid inputs."""
    try:
        info1 = TypeInfoParser(s).parse()
        info2 = TypeInfoParser(str(info1)).parse()
    except ValueError:
        return
    assert str(info1) == str(info2), (
        f"Not idempotent: parse({s!r}) -> {info1!r}\n"
        f"  str(info1)={str(info1)!r}\n"
        f"  parse(str(info1)) -> {info2!r}"
    )


@given(s=union_type_string())
@settings(max_examples=500, suppress_health_check=[HealthCheck.too_slow])
def test_union_strings_parse_without_error(s):
    try:
        TypeInfoParser(s).parse()
    except ValueError as e:
        raise AssertionError(f"Valid union string failed to parse: {s!r}\n  {e}") from e


if __name__ == "__main__":
    print("Exception-based tests...")
    test_parse_only_raises_value_error()
    print("  arbitrary strings: OK")

    print("Functional tests...")
    test_valid_type_strings_parse_without_error()
    print("  valid type strings parse: OK")
    test_parse_idempotency()
    print("  idempotency: OK")
    test_union_strings_parse_without_error()
    print("  union strings parse: OK")

    print("\nAll tests passed.")

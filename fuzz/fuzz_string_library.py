# explore_rf_bugs.py
from hypothesis import given, settings, strategies as st
from hypothesis import HealthCheck
from robot.libraries.String import String
from robot.libraries.Collections import Collections
from robot.libraries.XML import XML

s = String()

@given(
    string=st.one_of(st.text(), st.binary()),
    exclude=st.one_of(
        st.none(),
        st.text(),
        st.binary()
    )
)
@settings(
    max_examples=1000,
    deadline=None,
    suppress_health_check=[HealthCheck.too_slow]
)
def fuzz_title_case(string, exclude):
    try:
        s.convert_to_title_case(string, exclude=exclude)
    except Exception as e:
        allowed = ['DataError', 'ValueError', 
                   'TypeError', 'AttributeError']
        if type(e).__name__ not in allowed:
            print(f"INTERESTING: {type(e).__name__}: {e}")
            print(f"Input: string={repr(string)}, exclude={repr(exclude)}")
            raise

@given(
    template=st.one_of(st.text(), st.binary()),
    positional=st.lists(
        st.one_of(st.text(), st.integers(), st.binary()),
        max_size=5
    )
)
@settings(max_examples=1000, deadline=None)
def fuzz_format_string(template, positional):
    try:
        s.format_string(template, *positional)
    except Exception as e:
        allowed = ['DataError', 'ValueError', 'KeyError',
                   'IndexError', 'TypeError', 'AttributeError']
        if type(e).__name__ not in allowed:
            print(f"INTERESTING: {type(e).__name__}: {e}")
            print(f"Input: template={repr(template)}")
            raise

@given(
    string=st.one_of(st.text(), st.binary()),
    pattern=st.text(),
    replace_with=st.one_of(st.text(), st.binary()),
    flags=st.one_of(st.none(), st.text())
)
@settings(max_examples=1000, deadline=None)
def fuzz_replace_regexp(string, pattern, replace_with, flags):
    try:
        s.replace_string_using_regexp(
            string, pattern, replace_with, flags=flags)
    except Exception as e:
        allowed = ['DataError', 'error', 'ValueError', 'TypeError']
        if type(e).__name__ not in allowed:
            print(f"INTERESTING: {type(e).__name__}: {e}")
            print(f"Input: string={repr(string)}, pattern={repr(pattern)}")
            raise

if __name__ == '__main__':
    bugs_found = []

    for name, fn in [
        ("String.convert_to_title_case", fuzz_title_case),
        ("String.format_string", fuzz_format_string),
        ("String.replace_string_using_regexp", fuzz_replace_regexp),
    ]:
        print("="*50)
        print(f"Fuzzing {name}...")
        print("="*50)
        try:
            fn()
            print(f"DONE - no unexpected exceptions\n")
        except Exception as e:
            bugs_found.append((name, e))
            print(f"BUGS FOUND in {name}: {e}\n")

    print("="*50)
    print(f"SUMMARY: {len(bugs_found)} function(s) had unexpected exceptions")
    for name, e in bugs_found:
        print(f"  - {name}: {type(e).__name__}")
    print("="*50)
"""
Functional fuzzing of RF Collections library using Hypothesis.
Tests invariants and oracle comparisons against Python stdlib.
"""
from hypothesis import given, settings, assume, strategies as st
from hypothesis import HealthCheck
from robot.libraries.Collections import Collections

c = Collections()

items = st.one_of(st.integers(), st.text(max_size=5))
list_strategy = st.lists(items, min_size=1, max_size=10)


# --- 1. remove_duplicates: first-occurrence order preserved ---
# Every item in result must appear in the same relative order as in original.

@given(list_=st.lists(items, max_size=15))
@settings(max_examples=2000, deadline=None, suppress_health_check=[HealthCheck.too_slow])
def fuzz_remove_duplicates_order(list_):
    result = c.remove_duplicates(list_)

    # No duplicates in result
    assert len(result) == len(set(map(str, result))), (
        f"DUPLICATES REMAIN: {result}"
    )

    # Each item in result is the FIRST occurrence from original
    seen = []
    expected = []
    for item in list_:
        if item not in seen:
            seen.append(item)
            expected.append(item)

    assert result == expected, (
        f"ORDER WRONG:\n"
        f"original : {list_}\n"
        f"expected : {expected}\n"
        f"got      : {result}"
    )


# --- 2. get_index_from_list: negative start can collide with -1 sentinel ---
# When value IS found, return value must never be -1.

@given(
    list_=list_strategy,
    start=st.integers(min_value=-10, max_value=0),
)
@settings(max_examples=2000, deadline=None, suppress_health_check=[HealthCheck.too_slow])
def fuzz_get_index_negative_start(list_, start):
    assume(abs(start) <= len(list_))
    # pick a value that is actually in the slice so it must be found
    slice_ = list_[start:]
    assume(len(slice_) > 0)
    value = slice_[-1]  # last element of slice → index in slice = len(slice)-1
                        # return = start + (len(slice)-1) which can equal -1

    result = c.get_index_from_list(list_, value, start=start)

    # If value is in the list, result must NOT be -1
    if value in list_[start:]:
        assert result != -1, (
            f"BUG: get_index_from_list returned -1 (not found) but value IS present\n"
            f"list_  : {list_}\n"
            f"value  : {repr(value)}\n"
            f"start  : {start}\n"
            f"slice  : {list_[start:]}\n"
            f"result : {result}"
        )


# --- 3. count_values_in_list matches Python list.count ---

@given(
    list_=list_strategy,
    value=items,
)
@settings(max_examples=2000, deadline=None, suppress_health_check=[HealthCheck.too_slow])
def fuzz_count_values_matches_python(list_, value):
    rf_result = c.count_values_in_list(list_, value)
    py_result = list_.count(value)
    assert rf_result == py_result, (
        f"MISMATCH: RF={rf_result} vs Python={py_result}\n"
        f"list_={list_}, value={repr(value)}"
    )


# --- 4. sort_list: result is actually sorted and same elements ---

@given(list_=st.lists(st.integers(), min_size=0, max_size=15))
@settings(max_examples=2000, deadline=None, suppress_health_check=[HealthCheck.too_slow])
def fuzz_sort_list_correctness(list_):
    original = list(list_)
    result = c.sort_list(list_)

    assert result == sorted(original), (
        f"SORT WRONG:\n"
        f"original : {original}\n"
        f"expected : {sorted(original)}\n"
        f"got      : {result}"
    )


# --- 5. reverse_list twice == original ---

@given(list_=list_strategy)
@settings(max_examples=2000, deadline=None, suppress_health_check=[HealthCheck.too_slow])
def fuzz_reverse_twice_is_identity(list_):
    original = list(list_)
    c.reverse_list(list_)
    c.reverse_list(list_)
    assert list_ == original, (
        f"DOUBLE REVERSE != ORIGINAL:\n"
        f"original : {original}\n"
        f"got      : {list_}"
    )


if __name__ == '__main__':
    bugs_found = []

    tests = [
        ("remove_duplicates: first-occurrence order preserved", fuzz_remove_duplicates_order),
        ("get_index_from_list: negative start sentinel collision", fuzz_get_index_negative_start),
        ("count_values_in_list matches Python list.count", fuzz_count_values_matches_python),
        ("sort_list: result is correctly sorted", fuzz_sort_list_correctness),
        ("reverse_list twice == original", fuzz_reverse_twice_is_identity),
    ]

    for name, fn in tests:
        print("=" * 60)
        print(f"Testing: {name}")
        print("=" * 60)
        try:
            fn()
            print(f"PASS - no functional bugs found\n")
        except Exception as e:
            bugs_found.append((name, e))
            print(f"BUG FOUND: {e}\n")

    print("=" * 60)
    print(f"SUMMARY: {len(bugs_found)} functional bug(s) found")
    for name, e in bugs_found:
        print(f"  - {name}")
    print("=" * 60)

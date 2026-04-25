from robot.libraries.Collections import Collections

c = Collections()

print("=" * 50)
print("Bug 3: get_index_from_list returns -1 when value IS present (Not yet reported)")
print("=" * 50)

cases = [
    ([0],       0, -1),
    ([1, 2, 3], 3, -1),
    ([1, 2, 3], 3, -2),
    ([0, 1, 2, 3, 4], 4, -1),
]

for list_, value, start in cases:
    result = c.get_index_from_list(list_, value, start=start)
    in_list = value in list_[start:]
    flag = "BUG - should not be -1" if result == -1 and in_list else "ok"
    print(f"list={list_}, value={value}, start={start} → result={result}  [{flag}]")

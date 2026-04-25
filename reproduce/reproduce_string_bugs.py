from robot.libraries.String import String

s = String()

print("=" * 50)
print("Bug 1: UnicodeEncodeError with bytes + non-latin-1 (Fixed in RF master)")
print("=" * 50)
print("convert_to_title_case(b'hello', exclude='Ā')")
try:
    s.convert_to_title_case(b"hello", exclude="Ā")
except Exception as e:
    print(f"{type(e).__name__}: {e}")

print()
print("replace_string_using_regexp(b'hello', 'Ā', 'replacement')")
try:
    s.replace_string_using_regexp(b"hello", "Ā", "replacement")
except Exception as e:
    print(f"{type(e).__name__}: {e}")

print()
print("=" * 50)
print("Bug 2: re.error for invalid regex in exclude (Not yet reported)")
print("=" * 50)
print("convert_to_title_case('hello', exclude='[')")
try:
    s.convert_to_title_case("hello", exclude="[")
except Exception as e:
    print(f"{type(e).__name__}: {e}")

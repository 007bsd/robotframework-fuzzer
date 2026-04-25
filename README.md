# Robot Framework Fuzzer

Property-based fuzzing of [Robot Framework](https://github.com/robotframework/robotframework) using [Hypothesis](https://hypothesis.readthedocs.io/).

Tested against **RF 7.4.2** on **Python 3.12** with **Hypothesis 6.152.2**.

## Bugs Found

| Issue | Library | Description |
|-------|---------|-------------|
| [#5636](https://github.com/robotframework/robotframework/issues/5636) | `String` | Bytes input leaks `UnicodeEncodeError` |
| [#5648](https://github.com/robotframework/robotframework/issues/5648) | `String` | Invalid regex in `exclude` leaks raw `re.error` |
| [#5649](https://github.com/robotframework/robotframework/issues/5649) | `Collections` | Negative `start` collides with `-1` sentinel |
| [#5650](https://github.com/robotframework/robotframework/issues/5650) | `TypeInfoParser` | `\|` inside `[...]` causes crash or infinite loop |

## Setup

```bash
pip install -r requirements.txt
```

## Running the Fuzzers

```bash
python fuzz/fuzz_string_library.py
python fuzz/fuzz_collections_library.py
python fuzz/fuzz_typeinfoparser.py
```

## Reproducing Bugs

```bash
python reproduce/reproduce_string_bugs.py
python reproduce/reproduce_collections_bugs.py
python reproduce/reproduce_typeinfoparser_bug.py

python -m robot reproduce/reproduce_string_bugs.robot
python -m robot reproduce/reproduce_collections_bugs.robot
cd reproduce && python -m robot reproduce_typeinfoparser_bug.robot
```

## CI

`.github/workflows/reproduce-bugs.yml` runs the fuzz harnesses and all reproduce scripts on **Windows** and **Linux**.

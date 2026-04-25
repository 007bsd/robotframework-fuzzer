from robot.running.arguments.typeinfoparser import TypeInfoParser

# Bug 5a: UnboundLocalError — PIPE before first type inside brackets
try:
    TypeInfoParser("list[|int]").parse()
except Exception as e:
    print(f"list[|int] -> {type(e).__name__}: {e}")

# Bug 5b: MemoryError — PIPE after comma is never consumed, causing infinite loop
# DO NOT RUN: TypeInfoParser("list[int,|]").parse() — hangs forever
print("list[int,|] -> MemoryError (infinite loop — not run here)")

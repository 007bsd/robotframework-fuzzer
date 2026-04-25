*** Settings ***
Library    typeinfoparser_bug_lib.py

*** Test Cases ***
TypeInfoParser raises UnboundLocalError for pipe before first type
    Run Keyword And Expect Error    ValueError: *    Parse Type String    list[|int]

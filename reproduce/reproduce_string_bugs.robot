*** Settings ***
Library    String

*** Test Cases ***
Convert To Title Case with non-latin-1 exclude
    ${bytes}=    Evaluate    b"hello"
    Convert To Title Case    ${bytes}    Ā

Replace String Using Regexp with non-latin-1 pattern
    ${bytes}=    Evaluate    b"hello"
    Replace String Using Regexp    ${bytes}    Ā    replacement

Convert To Title Case with invalid regex in exclude
    [Documentation]    Bug: re.error raised instead of ValueError/DataError for invalid regex in exclude
    Convert To Title Case    hello    [

*** Settings ***
Library    Collections

*** Test Cases ***
Get Index From List with negative start returns wrong not-found sentinel
    [Documentation]
    ...    WHAT WE EXPECT:
    ...    We have a list: [0]
    ...    We ask: "where is the value 0 in this list, starting from the last item (start=-1)?"
    ...    The value 0 IS there at position 0. So we expect a real index back, NOT -1.
    ...
    ...    THE BUG:
    ...    RF uses -1 to mean "value not found".
    ...    But the math inside RF also produces -1 when the value IS found with a negative start.
    ...    So RF says "not found" when it actually IS there. That is the bug.
    ${list}=    Create List    0
    ${result}=    Get Index From List    ${list}    0    start=-1
    Should Not Be Equal As Integers    ${result}    -1    msg=Value 0 IS in list but got -1 (not found)

Get Index From List negative start last element collision
    [Documentation]
    ...    WHAT WE EXPECT:
    ...    We have a list: [1, 2, 3]
    ...    We ask: "where is 3, starting from the last item (start=-1)?"
    ...    3 IS the last item. We expect its index back, NOT -1.
    ...
    ...    THE BUG:
    ...    start=-1, 3 is found at position 0 in the slice.
    ...    RF computes: -1 + 0 = -1 → "not found". Wrong!
    ${list}=    Create List    1    2    3
    ${result}=    Get Index From List    ${list}    3    start=-1
    Should Not Be Equal As Integers    ${result}    -1    msg=Value 3 IS in list but got -1 (not found)

Get Index From List negative start second-to-last collision
    [Documentation]
    ...    WHAT WE EXPECT:
    ...    We have a list: [1, 2, 3]
    ...    We ask: "where is 3, starting from 2nd-to-last item (start=-2)?"
    ...    3 IS in that range. We expect its index back, NOT -1.
    ...
    ...    THE BUG:
    ...    start=-2, 3 is found at position 1 in the slice.
    ...    RF computes: -2 + 1 = -1 → "not found". Wrong!
    ${list}=    Create List    1    2    3
    ${result}=    Get Index From List    ${list}    3    start=-2
    Should Not Be Equal As Integers    ${result}    -1    msg=Value 3 IS in list but got -1 (not found)

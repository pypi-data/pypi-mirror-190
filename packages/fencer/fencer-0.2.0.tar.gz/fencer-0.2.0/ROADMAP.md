-------------------------
Testing injection attacks
-------------------------
> Testing SQL injection through URL query parameters
    GET /orders .
    GET /orders/{orderId} .
    ...
> Testing SQL injection through URL path parameters
> Testing SQL injection through request payloads
> Testing noSQL injection, command injection... Possible injection for kakfa and so on?
----------------------------
Testing unauthorized access
----------------------------
> Testing access without token
> Tampering token's payload
> Attempting to break token's signature
> Attempting to bypass token's signature validation
> Attempting access with random tokens
----------------------------
> Attempting access to another user's resources (we don't know if this is allowed or not so user needs to specify)
----------------------
Surface attack testing
----------------------
> Looking for undocumented endpoints (by leveraging IDs in payloads and looking for common words, subdomains, etc.)
----------------------
Testing mass assignment
-----------------------
Testing unbound arrays
----------------------

Summary
> Number of tests
|=====================================|
| Test category     | Number of tests |
|-------------------------------------|
| Injection attacks |      350        |
|=====================================|
> Vulnerabilities found by severity
|=========================================|
| Test category     | Low | Medium | High |
|-----------------------------------------|
| Injection attacks |  20 |   50   |  0   |
|=========================================|

The results of the last test run are stored under .fencer/
test_case = {
    "id": "asdf",
    "timestamp": "2023-02-01:09:00:00TZ:GMT",
    "category": "injection_attack",
    "target_test": "injection_attack__sql_injection__optional_query_parameters",
    "result": "fail",
    "severity": "medium",
    "description": {
        "http_method": "GET",
        "url": "http://localhost:5000/orders?limit=1' 1 OR 1",
        "base_url": "http://localhost:5000",
        "path": "/orders",
        "payload": None,
    }
}
by default, we only store failing tests; can save all by doing
$ fencer run --save all
fencer replay --last --category injection_attack --target optional-query-parameters
every test case is a JSON
=> .fencer/injection_attacks/, .fencer/unauthorized_tests/, etc.
fencer

maybe possible to configure fencer to save the results of each test run; then it creates a hash
for each or something like that

fencer clean-test-cache

SQL injection tests

1. Move API parsing to its own module (and create an openapi parser package)
2. Keep track of all the tests and the results. Output summary stats at the end like schemathesis
3. Add debug flag by default False. Only give detailed output of payloads and such of on debug.
4. Test with secured endpoints. User provides the token, and we test the endpoints with token and without
5. Then test the security of the token with the strategies already devised
6. Add type annotations everywhere and mypy tests
7. Add tests
8. Add Docker builds so people can run from docker directly - and update docs
9. Start creating docs, both tutorials and API docs; also for pypi
10. Add github actions and automation
11. If user provides two valid tokens, we can test creating resources with one user and accessing with another
12. Add more sql injection cases. Add also command and noSQL injection
- mass assignment
- repeated retries of same resource changing tokens
- multiple login attempts
- DDoS
- arrays without minimum or max
- look for undocumented endpoints
- exploit too many IDs
12. Continue with the weak API implementation example
13. Save tests in casette so we can replay them
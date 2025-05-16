# pytest

## Terminologies

### Fixture

A reusable piece of setup/teardown logic, injected into tests or other fixtures.

```python
@pytest.fixture
def client():
    ...
```
then can be used as:
```python
def test_something(client):
    response = client.get('/some-url')
    assert response.status_code == 200
```

### Fixture Scope

Determines how long a fixture is active.

- `function`: (default) recreated for each test function. the fixture is destroyed at the end of the test function.
- `class`: recreated for each test class. the fixture is destroyed at the end of the test class.
- `module`: recreated for each test module (file). the fixture is destroyed at the end of the test module.
- `session`: recreated once per test session (whole test suite). the fixture is destroyed at the end of the test session.


### Fixture Autouse

Automatically used in every test, no need to explicitly pass it.

```python
@pytest.fixture(autouse=True)
def setup_database():
    # Setup code
    yield
    # Teardown code
```
### Monkeypatching

Temporarily change/replace attributes, methods, or environment variables during a test.

```python
def test_some_function(monkeypatch):
    def mock_function():
        return "mocked value"

    monkeypatch.setattr('module_name.function_name', mock_function)

    assert module_name.function_name() == "mocked value"
```

### Async Fixtures

A fixture defined with async def, often used for DB or HTTP work.

```python
@pytest.fixture
async def async_client():
    async with AsyncClient() as client:
        yield client
```
Then can be used in an async test function:
```python
@pytest.mark.asyncio
async def test_async_function(async_client):
    response = await async_client.get('/some-url')
    assert response.status_code == 200
```

### Yield Fixtures

Yield fixtures allow for setup and teardown in a single fixture.

```python
@pytest.fixture
def resource():
    # Setup code
    yield resource_instance
    # Teardown code
```
Then can be used in a test function:
```python
def test_resource(resource):
    assert resource.is_valid()
```

### Dependency Override (FastAPI Specific)

In FastAPI, you can override dependencies in tests to provide mock implementations.

```python
app.dependency_overrides[get_session] = override_get_session
```


### conftest.py

A special file where you can define fixtures and hooks that are shared across multiple test files.

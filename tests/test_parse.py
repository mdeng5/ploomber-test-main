import pytest

from ploomber_test import parse


no_code_chunks = """
# heading
"""

one_code_chunk = """
# heading

```python
1 + 1
```

"""

many_code_chunks = """

# heading

```python
1 + 1
```

```sql
select * from penguins.csv
```

"""


@pytest.mark.parametrize(
    "text, expected",
    [
        (
            no_code_chunks,
            [],
        ),
        (
            one_code_chunk,
            [
                {"code": "1 + 1", "language": "python"},
            ],
        ),
        (
            many_code_chunks,
            [
                {"code": "1 + 1", "language": "python"},
                {"code": "select * from penguins.csv", "language": "sql"},
            ],
        ),
    ],
)
def test_iterate_code_chunks(text, expected):
    parsed = list(parse.iterate_code_chunks(text))
    assert parsed == expected

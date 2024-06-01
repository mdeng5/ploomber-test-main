from pathlib import Path

import sqlite3
import duckdb
import pytest

from ploomber_test.runner import CodeRunner

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
select * from penguins.csv limit 3
```

"""

create_table_then_query = """

```sql
CREATE TABLE numbers (
    number INT
);
```

```sql
INSERT INTO numbers (number) VALUES (1);
INSERT INTO numbers (number) VALUES (2);
INSERT INTO numbers (number) VALUES (3);
INSERT INTO numbers (number) VALUES (4);
INSERT INTO numbers (number) VALUES (5);
```

```sql
SELECT * FROM numbers;
```

"""


@pytest.mark.parametrize(
    "text",
    [
        no_code_chunks,
        one_code_chunk,
        many_code_chunks,
        create_table_then_query,
    ],
)
@pytest.mark.parametrize(
    "conn",
    [
        None,
        duckdb.connect(),
    ],
)
def test_runner(tmp_penguins, text, conn):
    CodeRunner(text, conn=conn).run()


@pytest.fixture(scope="session")
def tmp_sqlite():
    if Path("my-database.db").exists():
        Path("my-database.db").unlink()

    conn = sqlite3.connect("my-database.db")

    conn.execute(
        """
CREATE TABLE numbers (
    number INT
);
"""
    )

    conn.execute(
        """
INSERT INTO numbers (number) VALUES (1), (2), (3), (4), (5);
"""
    )

    conn.commit()

    yield conn

    conn.execute("DROP TABLE numbers;")

    conn.close()

    Path("my-database.db").unlink()


@pytest.mark.xfail(reason="We're getting a database is locked error")
def test_runner_sqlite(tmp_sqlite):
    text = """
```python
import math

math.sqrt(42)
```

```sql
CREATE TEMP TABLE my_table AS SELECT 42;
```
    
```python
import sqlite3

conn = sqlite3.connect("my-database.db")
results = conn.execute("SELECT * FROM numbers")
print(results)
```


```sql
SELECT * FROM my_table;
```
"""

    CodeRunner(text).run()

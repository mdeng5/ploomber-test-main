# sql query


```python
from urllib.request import urlretrieve

urlretrieve(
    "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/master/inst/extdata/penguins.csv",
    "penguins.csv",
)
```


```sql
SELECT * FROM penguins.csv LIMIT 3
```


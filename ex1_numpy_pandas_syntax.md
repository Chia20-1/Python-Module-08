# Ex1 NumPy And Pandas Syntax Guide

This guide is for writing `ex1/loading.py` from scratch.

The big picture of ex1 is:

```text
NumPy creates the data
Pandas stores and analyzes the data
Matplotlib visualizes the data
```

This file focuses only on NumPy and pandas syntax, because that is the part where a blank file can feel hardest.

Small naming note:

- The library is called `pandas`, with an `s`.
- The common alias is `pd`.
- The library is called `numpy`.
- The common alias is `np`.

Because your current `loading.py` loads dependencies with `importlib`, you may not literally write `import numpy as np` at the top. But once you have the module stored in a variable named `np`, the syntax is the same.

## 1. The Mental Model

### NumPy

NumPy is good at creating and working with many numbers at once.

Think of a NumPy array like a column of values:

```python
[70.5, 68.2, 91.0, 55.4, ...]
```

For this exercise, NumPy should generate the fake Matrix data.

### Pandas

Pandas is good at working with tables.

Think of a pandas DataFrame like this:

```text
signal_strength | latency_ms | anomaly_score | energy_usage
------------------------------------------------------------
70.5            | 125        | 0.12          | 48.9
68.2            | 80         | 0.72          | 51.3
91.0            | 190        | 0.98          | 60.1
```

For this exercise, pandas should analyze the data that NumPy created.

## 2. Standard Imports

In a normal file, you often see:

```python
import numpy as np
import pandas as pd
```

This means:

- `np` is the short name for `numpy`.
- `pd` is the short name for `pandas`.

So instead of writing:

```python
numpy.random.default_rng()
pandas.DataFrame()
```

You can write:

```python
np.random.default_rng()
pd.DataFrame()
```

In your ex1 solution, you are using `importlib` first to check whether packages exist. After that, you still use the same style:

```python
np = modules["numpy"]
pd = modules["pandas"]
```

Then:

```python
rng = np.random.default_rng(seed=42)
df = pd.DataFrame(data)
```

## 3. NumPy Syntax You Need For Ex1

### Create a random generator

Use this:

```python
rng = np.random.default_rng(seed=42)
```

Meaning:

- `np.random` is NumPy's random tools.
- `default_rng()` creates a random number generator.
- `seed=42` makes the random results repeatable.

Repeatable means every time you run the program, you get the same fake data. That is useful for debugging.

### Create normal distributed numbers

Your current ex1 uses:

```python
signal_strength = rng.normal(loc=70, scale=10, size=1000)
```

Meaning:

- `normal()` creates values around an average.
- `loc=70` means the average is around 70.
- `scale=10` means values spread around 70 by about 10.
- `size=1000` means create 1000 values.

Example mental picture:

```text
Most signal values are near 70.
Some are lower, like 55.
Some are higher, like 88.
```

Good for:

- signal strength
- energy usage
- temperature
- score-like values

### Create random integers

Your current ex1 uses:

```python
latency_ms = rng.integers(low=10, high=200, size=1000)
```

Meaning:

- `integers()` creates whole numbers.
- `low=10` is the smallest possible value.
- `high=200` is the upper limit.
- `size=1000` means create 1000 values.

Important: `high=200` means values go up to 199, not 200.

Good for:

- latency in milliseconds
- count values
- IDs
- number of attempts

### Create random decimal values from 0 to 1

Your current ex1 uses:

```python
anomaly_score = rng.random(1000)
```

Meaning:

- `random()` creates decimal values.
- Values are between `0.0` and `1.0`.
- `1000` means create 1000 values.

Good for:

- probability
- anomaly score
- risk score
- percentage-like values

Example:

```text
0.12 means low anomaly
0.98 means high anomaly
```

### Create several NumPy arrays

For ex1, you can generate each column separately:

```python
rng = np.random.default_rng(seed=42)

signal_strength = rng.normal(loc=70, scale=10, size=1000)
latency_ms = rng.integers(low=10, high=200, size=1000)
anomaly_score = rng.random(1000)
energy_usage = rng.normal(loc=50, scale=8, size=1000)
```

Each variable now holds 1000 values.

The important rule:

```text
Every column should have the same number of rows.
```

If `signal_strength` has 1000 values, then `latency_ms`, `anomaly_score`, and `energy_usage` should also have 1000 values.

### Put NumPy arrays into a dictionary

Pandas can create a table from a dictionary:

```python
data = {
    "signal_strength": signal_strength,
    "latency_ms": latency_ms,
    "anomaly_score": anomaly_score,
    "energy_usage": energy_usage,
}
```

Meaning:

- The dictionary keys become column names.
- The NumPy arrays become column values.

You can also write it directly:

```python
data = {
    "signal_strength": rng.normal(loc=70, scale=10, size=1000),
    "latency_ms": rng.integers(low=10, high=200, size=1000),
    "anomaly_score": rng.random(1000),
    "energy_usage": rng.normal(loc=50, scale=8, size=1000),
}
```

That is what your current `simulate_matrix_data()` function does.

## 4. Pandas Syntax You Need For Ex1

### Create a DataFrame

Use:

```python
df = pd.DataFrame(data)
```

Meaning:

- `pd.DataFrame()` creates a table.
- `data` is the dictionary of column names and values.
- `df` is the common variable name for a DataFrame.

After this, `df` is your Matrix data table.

### See the first few rows

Useful while learning:

```python
print(df.head())
```

Meaning:

- `head()` shows the first 5 rows.

To show more:

```python
print(df.head(10))
```

This shows the first 10 rows.

### Count rows

Your current ex1 uses:

```python
len(df)
```

Meaning:

- `len(df)` returns the number of rows.

Example:

```python
print(f"Processing {len(df)} data points...")
```

If your NumPy arrays used `size=1000`, then `len(df)` should be `1000`.

### Check table shape

Use:

```python
print(df.shape)
```

Meaning:

```text
(rows, columns)
```

Example:

```text
(1000, 4)
```

That means 1000 rows and 4 columns.

### See column names

Use:

```python
print(df.columns)
```

This helps you check spelling.

Column spelling matters. This works:

```python
df["latency_ms"]
```

This fails if the column is not spelled exactly:

```python
df["latency"]
```

### Select one column

Use square brackets:

```python
df["latency_ms"]
```

This returns one column.

That one column is called a Series.

Mental model:

```text
DataFrame = full table
Series = one column from the table
```

### Select multiple columns

Use double square brackets:

```python
df[["signal_strength", "latency_ms"]]
```

Why double brackets?

- Inner list: `["signal_strength", "latency_ms"]`
- Outer brackets: `df[...]`

This returns a smaller DataFrame with only those columns.

### Calculate the average of one column

Your current ex1 uses:

```python
average_latency = df["latency_ms"].mean()
```

Meaning:

- `df["latency_ms"]` selects the column.
- `.mean()` calculates the average.

Other useful methods:

```python
df["latency_ms"].min()
df["latency_ms"].max()
df["latency_ms"].median()
df["latency_ms"].std()
```

Meaning:

- `min()` gets the smallest value.
- `max()` gets the largest value.
- `median()` gets the middle value.
- `std()` gets the standard deviation.

### Convert a pandas result to a normal float

Your current ex1 uses:

```python
average_latency = float(df["latency_ms"].mean())
```

Why?

Pandas and NumPy often return their own number types, such as NumPy floats. Converting to `float` gives a plain Python number.

This is useful when storing values in a simple data structure like your `MatrixStats` tuple.

### Summarize all numeric columns

Use:

```python
summary = df.describe()
print(summary)
```

This gives common statistics:

- count
- mean
- standard deviation
- minimum
- quartiles
- maximum

This is a quick way to understand your generated data.

### Filter rows with a condition

Your current ex1 uses:

```python
high_anomalies = df[df["anomaly_score"] > 0.95]
```

Read it in two pieces.

First:

```python
df["anomaly_score"] > 0.95
```

This creates a True or False result for every row:

```text
False
True
False
False
True
```

Then:

```python
df[condition]
```

This keeps only rows where the condition is True.

Full version:

```python
condition = df["anomaly_score"] > 0.95
high_anomalies = df[condition]
```

Short version:

```python
high_anomalies = df[df["anomaly_score"] > 0.95]
```

### Count filtered rows

Use:

```python
len(high_anomalies)
```

Example:

```python
high_anomaly_count = len(high_anomalies)
```

This gives the number of rows with anomaly score above `0.95`.

### Filter with two conditions

Use `&` for "and":

```python
unstable_rows = df[
    (df["anomaly_score"] > 0.95)
    & (df["latency_ms"] > 150)
]
```

Important pandas rule:

Use parentheses around each condition.

This is correct:

```python
(df["anomaly_score"] > 0.95) & (df["latency_ms"] > 150)
```

This is not correct:

```python
df["anomaly_score"] > 0.95 & df["latency_ms"] > 150
```

Use `|` for "or":

```python
risky_rows = df[
    (df["anomaly_score"] > 0.95)
    | (df["signal_strength"] < 50)
]
```

### Add a new column

You can create a new column from existing columns:

```python
df["signal_per_energy"] = df["signal_strength"] / df["energy_usage"]
```

Meaning:

- For each row, divide signal strength by energy usage.
- Store the result in a new column.

### Add a category column with NumPy

Use `np.where()`:

```python
df["status"] = np.where(
    df["anomaly_score"] > 0.95,
    "unstable",
    "stable",
)
```

Meaning:

```text
if anomaly_score > 0.95:
    status = "unstable"
else:
    status = "stable"
```

But it works across the whole column at once.

### Sort rows

Highest anomaly scores first:

```python
sorted_df = df.sort_values("anomaly_score", ascending=False)
```

Lowest latency first:

```python
sorted_df = df.sort_values("latency_ms", ascending=True)
```

### Get the top rows

Top 5 anomaly rows:

```python
top_anomalies = df.nlargest(5, "anomaly_score")
```

Lowest 5 latency rows:

```python
fastest_rows = df.nsmallest(5, "latency_ms")
```

### Looping is usually not needed

Beginner instinct:

```python
total = 0
for value in df["latency_ms"]:
    total += value
average = total / len(df)
```

Pandas way:

```python
average = df["latency_ms"].mean()
```

For ex1, prefer pandas methods over manual loops.

## 5. How Your Current Ex1 Functions Use NumPy And Pandas

### `simulate_matrix_data(np, pd)`

Purpose:

```text
Create fake Matrix data.
```

Core syntax:

```python
rng = np.random.default_rng(seed=42)
```

This creates the random generator.

Then:

```python
data = {
    "signal_strength": rng.normal(loc=70, scale=10, size=1000),
    "latency_ms": rng.integers(low=10, high=200, size=1000),
    "anomaly_score": rng.random(1000),
    "energy_usage": rng.normal(loc=50, scale=8, size=1000),
}
```

This creates four columns of data.

Then:

```python
return pd.DataFrame(data)
```

This converts the NumPy-generated data into a pandas table.

### `analyze_matrix_data(df)`

Purpose:

```text
Calculate useful summary values from the table.
```

Core syntax:

```python
average_latency = float(df["latency_ms"].mean())
```

This calculates the average of one column.

Then:

```python
average_signal = float(df["signal_strength"].mean())
```

This calculates the average signal strength.

Then:

```python
high_anomalies = df[df["anomaly_score"] > 0.95]
```

This filters rows where anomaly score is higher than `0.95`.

Then:

```python
high_anomaly_count = len(high_anomalies)
```

This counts those rows.

## 6. Build It From Scratch In Small Pieces

If you feel stuck, do not start by writing the final program.

Start with this tiny version:

```python
import numpy as np
import pandas as pd

rng = np.random.default_rng(seed=42)

data = {
    "signal_strength": rng.normal(loc=70, scale=10, size=1000),
    "latency_ms": rng.integers(low=10, high=200, size=1000),
    "anomaly_score": rng.random(1000),
}

df = pd.DataFrame(data)

print(df.head())
print(len(df))
print(df["latency_ms"].mean())
```

Once that works, add:

```python
high_anomalies = df[df["anomaly_score"] > 0.95]
print(len(high_anomalies))
```

Then turn each part into a function.

### First function

```python
def simulate_matrix_data(np, pd):
    rng = np.random.default_rng(seed=42)
    data = {
        "signal_strength": rng.normal(loc=70, scale=10, size=1000),
        "latency_ms": rng.integers(low=10, high=200, size=1000),
        "anomaly_score": rng.random(1000),
        "energy_usage": rng.normal(loc=50, scale=8, size=1000),
    }
    return pd.DataFrame(data)
```

### Second function

```python
def analyze_matrix_data(df):
    average_latency = float(df["latency_ms"].mean())
    average_signal = float(df["signal_strength"].mean())
    high_anomalies = df[df["anomaly_score"] > 0.95]

    print(f"Average latency: {average_latency:.2f} ms")
    print(f"Average signal: {average_signal:.2f}")
    print(f"High anomalies: {len(high_anomalies)}")
```

After that, connect the functions:

```python
df = simulate_matrix_data(np, pd)
analyze_matrix_data(df)
```

## 7. Common Mistakes And Fixes

### Mistake: using a normal list as the dataset

Avoid:

```python
data = [1, 2, 3, 4]
```

For this subject, NumPy must create the dataset.

Prefer:

```python
data = rng.normal(loc=70, scale=10, size=1000)
```

### Mistake: using `range()` as the data source

Avoid:

```python
latency_ms = range(1000)
```

Prefer:

```python
latency_ms = rng.integers(low=10, high=200, size=1000)
```

### Mistake: forgetting that column names are strings

Wrong:

```python
df[latency_ms]
```

Correct:

```python
df["latency_ms"]
```

### Mistake: using `and` with pandas conditions

Wrong:

```python
df[(df["anomaly_score"] > 0.95) and (df["latency_ms"] > 150)]
```

Correct:

```python
df[(df["anomaly_score"] > 0.95) & (df["latency_ms"] > 150)]
```

### Mistake: forgetting parentheses around conditions

Wrong:

```python
df[df["anomaly_score"] > 0.95 & df["latency_ms"] > 150]
```

Correct:

```python
df[(df["anomaly_score"] > 0.95) & (df["latency_ms"] > 150)]
```

### Mistake: counting a condition incorrectly

This gives filtered rows:

```python
high_anomalies = df[df["anomaly_score"] > 0.95]
```

This counts them:

```python
len(high_anomalies)
```

### Mistake: making columns with different lengths

Wrong:

```python
data = {
    "signal_strength": rng.normal(loc=70, scale=10, size=1000),
    "latency_ms": rng.integers(low=10, high=200, size=500),
}
```

Pandas will complain because one column has 1000 values and another has 500.

Correct:

```python
data = {
    "signal_strength": rng.normal(loc=70, scale=10, size=1000),
    "latency_ms": rng.integers(low=10, high=200, size=1000),
}
```

## 8. Mini Cheat Sheet

### NumPy

```python
rng = np.random.default_rng(seed=42)
```

Create repeatable random generator.

```python
rng.normal(loc=70, scale=10, size=1000)
```

Create 1000 values around average 70.

```python
rng.integers(low=10, high=200, size=1000)
```

Create 1000 whole numbers from 10 to 199.

```python
rng.random(1000)
```

Create 1000 decimal numbers from 0.0 to 1.0.

```python
np.where(condition, value_if_true, value_if_false)
```

Create values based on a condition.

### Pandas

```python
df = pd.DataFrame(data)
```

Create table from dictionary.

```python
df.head()
```

Show first 5 rows.

```python
len(df)
```

Count rows.

```python
df.shape
```

Get row and column count.

```python
df["latency_ms"]
```

Select one column.

```python
df[["signal_strength", "latency_ms"]]
```

Select multiple columns.

```python
df["latency_ms"].mean()
```

Average one column.

```python
df.describe()
```

Summarize numeric columns.

```python
df[df["anomaly_score"] > 0.95]
```

Filter rows.

```python
df.sort_values("anomaly_score", ascending=False)
```

Sort rows.

```python
df.nlargest(5, "anomaly_score")
```

Get top 5 rows by a column.

## 9. Practice Path

To become able to write this from scratch, practice in this order:

1. Create one NumPy array with `rng.normal()`.
2. Print the array.
3. Create three NumPy arrays with the same size.
4. Put them into a dictionary.
5. Convert the dictionary into `pd.DataFrame`.
6. Print `df.head()`.
7. Print `len(df)`.
8. Calculate one average with `.mean()`.
9. Filter rows with one condition.
10. Count the filtered rows with `len()`.
11. Move the data generation into a function.
12. Move the analysis into another function.

Once those steps feel natural, the full ex1 program becomes much easier to write.

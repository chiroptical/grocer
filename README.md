grocer
---

## Motivation

I like using [https://dataset.readthedocs.io/en/latest/](dataset) with
[https://www.sqlite.org/index.html](SQLite) because I am lazy and the interface
is convenient. I really like the simplicity, but I also want _some_ concurrency.

When I need to write concurrently, I have reached for MongoDB because it scales
well. However, I need to install and run the MongoDB server which can be a
burden for some people.

## What If?

What if we just stored JSON documents on the filesystem using a simple file
locking mechanism to allow for concurrent access? Interested? Then it is time to
become a grocer and open your own store.

## Opening your own store

Import grocer:

```python
import grocer
```

Initialize a `Store`:

```python
store = grocer.Store("./store")
```

The `Store` is initialized with the path `./store` on your filesystem which may
or may not exist. You access your `Store`, similarly to a dictionary, via an
`Aisle`. An `Aisle` is analogous to a collection or table in other databases.
Example:

```python
aisle = store["produce"]
```

This will access the `Aisle` `./store/produce` which will contain JSON objects
called `SKU`s. SKU stands for stockkeeping unit and must be unique. An example:

```python
aisle.stock_one({"sku": "eggplant", "price": 3.50})
```

The above command will create the file `./store/produce/eggplant.json` with
the following JSON inside:

```json
{"price": 3.5}
```

## Dependencies

- Platform independent file locking mechanism
    - https://github.com/benediktschmitt/py-filelock
- Creating usable file names from store, aisle, and SKUs
    - https://github.com/un33k/python-slugify

## Goals

Be as simple as possible. Lock SKUs for concurrent writes.

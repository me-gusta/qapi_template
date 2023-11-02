# Query API Template

## What
This is a tool for exploring behavior of web services and prototyping.
It allows us to simplify the design of web services, in situations when we don't know in advance which data structures will be used.

It allows you to quickly add, delete and edit existing functionality without rewriting the code.

## Why

1. Since we do not have models like they introduced `sqlalchemy`, we don't need to think about data stored in the database, we create required models on the fly.
2. When we use `pymongo` + (`pydatic` or `dataclasses`) in constantly shifting environment, 90% of our code consist of `Optional` parameters. It's not always clear what we are working with. 
3. And if we use dictionaries, there is a high probability of making a typo.

## Current State

So far it has been used only to *create static websites and work with jinja templates*.
This template shows how QueryAPI can be implemented for static site generation.

Requirements
- `Flask`
- `mongodb`
- `markdown`

Generate dummy data
```commandline
pip install -r requirements.txt
python /website/help_scripts/1_generate_dummy_entities.py
```

For storing articles content we use `markdown` and `.md` files are located in `/content`

Admin page is built with `Svelte`. It allows us to work with data in a spreadsheet. It's available on `DOMAIN/qapi/admin`

## How it works

For example, if there is an entity "Article", then it will have the following components:
```
tag: str
title: str
description: str
```

Since this article is rendered into a template, we can make html blocks that will change for different articles.
```
block_nav # 'big' or 'small'
block_banner # 'image' or 'none'
```

So we can examine this entity in two different perspectives, while maintaining its integrity as a one thing.
```
article = query_one(title, description, tag='initial')

blocks = query_one(block_nav, block_banner)
```

Some articles may have their unique template or path, if so we can add such components.
```
template: str
path: str
```

In this case `block_nav` and `block_banner` above will not be used, but we do not need to rewrite anything and deal with child-parent relationships, etc.
```
all_with_template = query(template)
```

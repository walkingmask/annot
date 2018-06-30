# Simple Annotation Tool
Written by Django.


## Setup
1. Place image files under static/
1. `sqlite3 sqlite3.db < schema.sql`

```
for p in `find ./static -name "*.jpg"`; do sqlite3 sqlite3.db "INSERT INTO dataset(filepath) VALUES ('$p');"; done
```


## Run
```
python main.py
```

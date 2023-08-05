- install and update build tool.

```bat
python -m pip install --upgrade build
```
- build

```bat
python -m build
```

- install and update twine

```bat
python -m pip install --upgrade twine
```

- upload 

```bat
python -m twine upload --verbose dist/* 
```
# Tips and references

## 1. Specifying Versions of a Package
[Pipenv documentation](https://pipenv-fork.readthedocs.io/en/latest/basics.html#specifying-versions-of-a-package)

The use of ~= is preferred over the == identifier as the latter prevents pipenv from updating the packages.
It locks the major version of the package and install version 1.2 and any **minor** updates, but **not 2.0**.
```shell
$ pipenv install "requests~=1.2"
```

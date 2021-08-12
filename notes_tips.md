# Tips and references

## Specifying Versions of a Package
[Pipenv documentation](https://pipenv-fork.readthedocs.io/en/latest/basics.html#specifying-versions-of-a-package)

The use of ~= is preferred over the == identifier as the latter prevents pipenv from updating the packages.
It locks the major version of the package and install version 1.2 and any **minor** updates, but **not 2.0**.
```shell
$ pipenv install "requests~=1.2"
```

## Testing Best Practices

1. If it can break, it should be tested. This includes models, views, forms, templates, validators, and so forth.
2. Each test should generally only test one function.
3. Keep it simple. You do not want to have to write tests on top of other tests.
4. Run tests whenever code is PULLed or PUSHed from the repo and in the staging environment before PUSHing to production.
5. When upgrading to a newer version of Django:
   - upgrade locally,
   - run your test suite,
   - fix bugs,
   - PUSH to the repo and staging, and then
   - test again in staging before shipping the code.


## How to debug in running container with breakpoint()? (Py3.7+)
The built-in breakpoint(), when called with defaults, can be used instead of _import pdb; pdb.set_trace()._
1. In docker-compose.yml add these lines for **web** service [ref.](https://docs.docker.com/compose/compose-file/compose-file-v3/#domainname-hostname-ipc-mac_address-privileged-read_only-shm_size-stdin_open-tty-user-working_dir "Docker docs")
```yaml
stdin_open: true
tty: true
```
2. Re-run containers/services
3. docker attach <container_id_of_django_posts_to_telegram_web>
4. You can interact with container's stdin/stdout/stderr, i.e. with (Pdb).

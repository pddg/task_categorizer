## Environment

- Python >= 3.7

The `pg_config` command is needed. Please install it.

```bash
$ pipenv install
# For macOS
$ env LDFLAGS="-L$(brew --prefix openssl)/lib" pipenv install
```

## How to use

```bash
$ pipenv run manage.py migrate
$ pipenv run manage.py load_tasks \
    --csv path/to/task.csv \
    --root path/to/GHQ_ROOT
$ pipenv run manage.py createsuperuser
$ pipenv run manage.py runserver
```

If you want to deploy them, you can use Heroku.

## Author

pddg

## License

MIT

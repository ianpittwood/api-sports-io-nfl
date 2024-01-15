API_KEY := ""

build:
    poetry build

update:
    poetry update

check:
    poetry check

test:
    TEST_API_KEY="{{API_KEY}}" poetry run python -m unittest discover -s tests

fmt:
    poetry run python -m black --line-length=120 --target-version=py310 .
    poetry run python -m isort --line-length=120 --python-version=310 --profile=black --atomic .

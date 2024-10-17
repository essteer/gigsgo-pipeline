<h1 align="center" id="title">Gigsgo Pipeline</h1>

<p align="center">
  <a href="https://github.com/essteer/gigsgo-pipeline/actions/workflows/test.yaml"><img src="https://github.com/essteer/gigsgo-pipeline/actions/workflows/test.yaml/badge.svg"></a>
  <a href="https://pypi.org/project/gigsgo-pipeline/"><img src="https://img.shields.io/badge/Python-3.10_~_3.13-3776AB.svg?style=flat&logo=Python&logoColor=white"></a>
  <a href="https://snyk.io/test/github/essteer/gigsgo-pipeline"><img src="https://snyk.io/test/github/essteer/gigsgo-pipeline/badge.svg?name=Snyk&style=flat&logo=Snyk"></a>
</p>

<p align="center">
An ETL pipeline for live music listings.
</p>

## Operation

```console
$ uv run python3 -m src.main -v 'https://www.example.com'
```

## Tests

```console
$ uv run python3 -m unittest discover -s tests
```

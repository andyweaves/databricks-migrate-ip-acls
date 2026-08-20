# Databricks Migrate IP ACLs - NOTICE File

Copyright (2026) Databricks, Inc.

This Software includes software developed at Databricks (https://www.databricks.com/) and its use is subject to the included LICENSE.md file.

---

## Third-party dependencies are grouped below by license.

Each table row lists a package used by this project, along with its version, ecosystem, role (runtime or dev), copyright holder/author, and upstream source.

This inventory was generated from real package metadata: `pip-licenses` (run via `uv run --with pip-licenses`) against the project virtual environment for Python packages (direct and transitive), and `uv tree --no-dev` to distinguish runtime from dev dependencies.

A few packages resolved in `uv.lock` are platform- or Python-version-conditional and are not installed in this environment, so they are not inventoried below:

- `colorama` — installed only on Windows.
- `tzdata` and `pytz` — pandas timezone data, pulled in only where the system lacks its own zoneinfo.
- `typing_extensions` — back-ports for older Python versions.
- `exceptiongroup` and `tomli` — dev/test back-ports for Python < 3.11.

**Dual-licensed and multi-licensed packages** — the following packages declare more than one license:

- `cffi` — MIT-0 (MIT No Attribution; listed under MIT No Attribution License).
- `cryptography` — Apache-2.0 **OR** BSD-3-Clause (listed under Apache License 2.0).
- `numpy` — BSD-3-Clause **AND** 0BSD **AND** MIT **AND** Zlib **AND** CC0-1.0 (combined work; listed under BSD 3-Clause License).
- `packaging` — Apache-2.0 **OR** BSD-2-Clause (listed under Apache License 2.0).
- `python-dateutil` — Apache-2.0 **OR** BSD-3-Clause (listed under Apache License 2.0).

---

## Apache License 2.0

Full license text: [https://www.apache.org/licenses/LICENSE-2.0](https://www.apache.org/licenses/LICENSE-2.0).

| Package | Version | Ecosystem | Role | Copyright holder / author | Source |
| --- | --- | --- | --- | --- | --- |
| coverage | 7.15.4 | Python | dev | Ned Batchelder and 263 others | [https://github.com/coveragepy/coveragepy](https://github.com/coveragepy/coveragepy) |
| cryptography | 50.0.0 | Python | runtime | The Python Cryptographic Authority and individual contributors | [https://github.com/pyca/cryptography](https://github.com/pyca/cryptography) |
| databricks-sdk | 0.130.0 | Python | runtime | Databricks | [https://github.com/databricks/databricks-sdk-py](https://github.com/databricks/databricks-sdk-py) |
| google-auth | 2.56.3 | Python | runtime | Google Cloud Platform | [https://github.com/googleapis/google-auth-library-python](https://github.com/googleapis/google-auth-library-python) |
| packaging | 26.3 | Python | dev | Donald Stufft | [https://github.com/pypa/packaging](https://github.com/pypa/packaging) |
| python-dateutil | 2.9.0.post0 | Python | runtime | Gustavo Niemeyer | [https://github.com/dateutil/dateutil](https://github.com/dateutil/dateutil) |
| requests | 2.34.2 | Python | runtime | Kenneth Reitz | [https://github.com/psf/requests](https://github.com/psf/requests) |

---

## BSD 2-Clause License

Full license text: [https://opensource.org/licenses/BSD-2-Clause](https://opensource.org/licenses/BSD-2-Clause).

| Package | Version | Ecosystem | Role | Copyright holder / author | Source |
| --- | --- | --- | --- | --- | --- |
| pyasn1 | 0.6.4 | Python | runtime | Ilya Etingof | [https://github.com/pyasn1/pyasn1](https://github.com/pyasn1/pyasn1) |
| pyasn1_modules | 0.4.2 | Python | runtime | Ilya Etingof | [https://github.com/pyasn1/pyasn1-modules](https://github.com/pyasn1/pyasn1-modules) |
| Pygments | 2.20.0 | Python | runtime | Georg Brandl | [https://pygments.org](https://pygments.org) |

---

## BSD 3-Clause License

Full license text: [https://opensource.org/licenses/BSD-3-Clause](https://opensource.org/licenses/BSD-3-Clause).

| Package | Version | Ecosystem | Role | Copyright holder / author | Source |
| --- | --- | --- | --- | --- | --- |
| click | 8.4.2 | Python | dev | Pallets | [https://github.com/pallets/click/](https://github.com/pallets/click/) |
| idna | 3.18 | Python | runtime | Kim Davies | [https://github.com/kjd/idna](https://github.com/kjd/idna) |
| numpy | 2.4.6 | Python | runtime | Travis E. Oliphant et al. | [https://numpy.org](https://numpy.org) |
| pandas | 3.0.5 | Python | runtime | The Pandas Development Team | [https://pandas.pydata.org](https://pandas.pydata.org) |
| prompt_toolkit | 3.0.53 | Python | runtime | Jonathan Slenders | [https://github.com/prompt-toolkit/python-prompt-toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) |
| protobuf | 6.33.6 | Python | runtime | Google | [https://github.com/protocolbuffers/protobuf](https://github.com/protocolbuffers/protobuf) |
| pycparser | 3.0 | Python | runtime | Eli Bendersky | [https://github.com/eliben/pycparser](https://github.com/eliben/pycparser) |

---

## ISC License

Full license text: [https://opensource.org/licenses/ISC](https://opensource.org/licenses/ISC).

| Package | Version | Ecosystem | Role | Copyright holder / author | Source |
| --- | --- | --- | --- | --- | --- |
| shellingham | 1.5.4 | Python | runtime | Tzu-ping Chung | [https://github.com/sarugaku/shellingham](https://github.com/sarugaku/shellingham) |

---

## MIT License

Full license text: [https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT).

| Package | Version | Ecosystem | Role | Copyright holder / author | Source |
| --- | --- | --- | --- | --- | --- |
| annotated-doc | 0.0.5 | Python | runtime | Sebastián Ramírez | [https://github.com/fastapi/annotated-doc](https://github.com/fastapi/annotated-doc) |
| black | 26.5.1 | Python | dev | Łukasz Langa | [https://github.com/psf/black](https://github.com/psf/black) |
| charset-normalizer | 3.5.1 | Python | runtime | Ahmed R. TAHRI | [https://github.com/jawah/charset_normalizer](https://github.com/jawah/charset_normalizer) |
| iniconfig | 2.3.0 | Python | dev | Ronny Pfannschmidt, Holger Krekel | [https://github.com/pytest-dev/iniconfig](https://github.com/pytest-dev/iniconfig) |
| markdown-it-py | 4.2.0 | Python | runtime | Chris Sewell | [https://github.com/executablebooks/markdown-it-py](https://github.com/executablebooks/markdown-it-py) |
| mdurl | 0.1.2 | Python | runtime | Taneli Hukkinen | [https://github.com/executablebooks/mdurl](https://github.com/executablebooks/mdurl) |
| mypy_extensions | 1.1.0 | Python | dev | The mypy developers | [https://github.com/python/mypy_extensions](https://github.com/python/mypy_extensions) |
| platformdirs | 4.11.3 | Python | dev | The platformdirs developers | [https://github.com/tox-dev/platformdirs](https://github.com/tox-dev/platformdirs) |
| pluggy | 1.6.0 | Python | dev | Holger Krekel | [https://github.com/pytest-dev/pluggy](https://github.com/pytest-dev/pluggy) |
| pytest | 9.1.1 | Python | dev | Holger Krekel, Bruno Oliveira, Ronny Pfannschmidt, Floris Bruynooghe, Brianna Laugher, Freya Bruhin, Others (See AUTHORS) | [https://github.com/pytest-dev/pytest](https://github.com/pytest-dev/pytest) |
| pytest-cov | 7.1.0 | Python | dev | Marc Schlaich | [https://github.com/pytest-dev/pytest-cov](https://github.com/pytest-dev/pytest-cov) |
| pytokens | 0.4.1 | Python | dev | Tushar Sadhwani | [https://github.com/tusharsadhwani/pytokens](https://github.com/tusharsadhwani/pytokens) |
| questionary | 2.1.1 | Python | runtime | Tom Bocklisch | [https://github.com/tmbo/questionary](https://github.com/tmbo/questionary) |
| rich | 15.0.0 | Python | runtime | Will McGugan | [https://github.com/Textualize/rich](https://github.com/Textualize/rich) |
| ruff | 0.16.3 | Python | dev | Astral Software Inc. | [https://github.com/astral-sh/ruff](https://github.com/astral-sh/ruff) |
| six | 1.17.0 | Python | runtime | Benjamin Peterson | [https://github.com/benjaminp/six](https://github.com/benjaminp/six) |
| truststore | 0.10.4 | Python | runtime | Seth Michael Larson, David Glick | [https://github.com/sethmlarson/truststore](https://github.com/sethmlarson/truststore) |
| typer | 0.27.1 | Python | runtime | Sebastián Ramírez | [https://github.com/fastapi/typer](https://github.com/fastapi/typer) |
| urllib3 | 2.7.0 | Python | runtime | Andrey Petrov | [https://github.com/urllib3/urllib3](https://github.com/urllib3/urllib3) |
| wcwidth | 0.8.2 | Python | runtime | Jeff Quast | [https://github.com/jquast/wcwidth](https://github.com/jquast/wcwidth) |

---

## MIT No Attribution License (MIT-0)

Full license text: [https://spdx.org/licenses/MIT-0.html](https://spdx.org/licenses/MIT-0.html).

| Package | Version | Ecosystem | Role | Copyright holder / author | Source |
| --- | --- | --- | --- | --- | --- |
| cffi | 2.1.1 | Python | runtime | Armin Rigo, Maciej Fijalkowski | [https://github.com/python-cffi/cffi](https://github.com/python-cffi/cffi) |

---

## Mozilla Public License 2.0

Full license text: [https://opensource.org/licenses/MPL-2.0](https://opensource.org/licenses/MPL-2.0).

| Package | Version | Ecosystem | Role | Copyright holder / author | Source |
| --- | --- | --- | --- | --- | --- |
| certifi | 2026.7.22 | Python | runtime | Kenneth Reitz | [https://github.com/certifi/python-certifi](https://github.com/certifi/python-certifi) |
| pathspec | 1.1.1 | Python | dev | Caleb P. Burns | [https://github.com/cpburnz/python-pathspec](https://github.com/cpburnz/python-pathspec) |

---

## Support

Databricks does not offer official support for Databricks Solutions and its repository. For any issue with this asset or the demos installed, please open an issue using GitHub and the team will have a look on a best-effort basis.

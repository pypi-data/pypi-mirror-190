# sysnet-ident

Tento balíček obsahuje procedury generování a kontrolu identifikačních kódů

## Požadavky

Python 3.9+

## Instalace a použití
### pip install --update sysnet-ident

(pokud potřebujete ke spuštění  `pip` with oprávnění rool: `sudo pip install sysnet-ident`)

Pak importujte balíček:

```python
import sysnet_ident
```

### Setuptools

Instalace via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user sysnet-sysnet_ident
```
(nebo `sudo python setup.py install sysnet-ident` pro instalaci balíčku pro všechny uživatele)

A import balíčku:

```python
import sysnet_ident
```

## Použití v programu

Balíček poskytuje řadu procedur.
- **check_pid** - Kontroluje spravnost PID
- **correct_pid** - Zkontroluje a opravi PID
- **next_api_key** - Vytvoří nový URL-safe API Key
- **next_pid** - vytvoří nový PID
- **next_token** - Vytvoří náhodný URL-safe textový řetězec v kódování Base64
- **next_uuid** - vytvoří nový UUID identifikátor
- **is_identifier_pid** - test identifikátoru: je ve formátu PID?
- **is_identifier_unid** - test identifikátoru: je ve formátu  UNID?
- **is_identifier_uuid** - test identifikátoru: je ve formátu  UUID?
- **is_valid_uuid** - je identifikátor validním UUID?
- **hash_<enc>** - kontrolní součet textu
- **hash_files_<enc>** - fontrolní součet souborů


## Systémové proměnné

Nastavení factory je řízeno systémovými proměnnými

- **PID_PREFIX** - implicitní tříznakový prefix pro PID
- **PASSWORD_USE_LOWER** - použití malých písmen při generování hesla (True)
- **PASSWORD_USE_UPPER** - použití velkých písmen při generování hesla (True)
- **PASSWORD_USE_DIGITS** - použití číslic při generování hesla (True)
- **PASSWORD_USE_PUNCTUATION** - použití interpunkce při generování hesla (False)


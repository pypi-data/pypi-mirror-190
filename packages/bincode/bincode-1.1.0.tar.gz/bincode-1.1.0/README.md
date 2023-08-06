## BIN Code Search

### Installation

```console
$ pip install bincode
```

### Usage

```python
>>> import bincode
>>> bincode.search(38520000023237)
{'id': 'diners', 'valid': True}
```

### Credit Card Type

| ID | Network | Length
| --- | --- | ---
| `amex` | American Express | 15
| `diners` | Diners Club | 14–19
| `discover` | Discover | 16–19
| `jcb` | JCB | 16–19
| `maestro` | Maestro | 12–19
| `mastercard` | Mastercard | 16
| `uatp` | UATP | 15
| `unionpay` | UnionPay | 16–19
| `visa` | Visa | 13, 16

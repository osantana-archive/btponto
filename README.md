# btponto

This software register your presence based on a discoverable Bluetooth device
that you normaly brings together with you (eg. your cell phone).

## Requirements

- Python 2
- Python BlueZ

## Installation

1. Download the latest release and extract btponto source code.
2. Run:

```
$ sudo python2.5 setup.py install
```

3. Add the content of ``btponto.crontab`` example in your crontab.

```
crontab -e
```


## Changelog

- **2015-01-30** - 0.1 - Moved from Google Code into Github and update README
- **2007-06-01** - 0.1 - First release.

## To-Do List

- Check the state sanity
- Discard invalid registers in log file


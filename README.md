# antechamber-abmpresp.py

## 概要
* Program to replace atom charge with ABINIT-MP RESP charge
* Wrapper program for antechamber


## 使用方法
```sh
$ antechamber-abmpresp.py -il ABINIT-MP.log ANTECHAMBER_OPTIONS ...
```

* `-il ABINIT-MP.log`
	: log file for ABINIT-MP with resp option


## 動作要件
* antechamber ([AmberTools](https://ambermd.org/AmberTools.php))
* Python3
	* parmed

## License
* GPL
* Copyright (c) 2023 Tatsuya Ohyama


## Authors
* Tatsuya Ohyama


## ChangeLog
### Ver. 1.0.1 (2023-09-11)
* Change license.

### Ver. 1.0 (2023-09-06)
* Release.

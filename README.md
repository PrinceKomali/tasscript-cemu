# TAS Script support for Cemu (and other pc games I guess...)
Extremely crude but it seems to work fairly well
Uses a very basic format of the [Electron TAS UI Format](https://github.com/TigerGold59/electron-tas-ui/blob/master/script-format.md)
```scala
+ ON{KEY_ZL} LSTICK{0,32767}
2 ON{KEY_X}
3 OFF{ALL}
10 ON{KEY_L}
2 OFF{KEY_L}
6 ON{KEY_ZR}
1 OFF{ALL} LSTICK{0,0}
4 ON{KEY_DUP}
4 RSTICK{90,32767}
4 OFF{ALL} RSTICK{0,0}
6 ON{KEY_L}
4 OFF{KEY_L}
4 ON{KEY_DUP}
4 RSTICK{270,32767}
4 OFF{ALL} RSTICK{0,0}
4 ON{KEY_L}
4 OFF{KEY_L}
```

Run with `python3 tas.py` while the tas.txt file is in the same directory

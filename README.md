# x86_64-Reverse Shell [![version](https://img.shields.io/badge/Version-Alpha-yellow.svg?style=style=flat-square)](https://twitter.com/133_cesium) [![license](https://img.shields.io/badge/License-GPL_3-orange.svg?style=style=flat-square)](https://github.com/C3s1um133/x86_64/blob/master/LICENSE)

Reverse shell + setreuid in ASM Intel 64 bits.
By default the target is 127.0.0.1.

Download the repository then use Makefile to build the project fastly :

```
git clone git@github.com:C3s1um133/x86_64.git
cd x86_64/
Make
```

## To test locally

Listen a socket on localhost :

```
nc -lvp 9876
```

Then we trigger it :

```
./prssr64
```

Foobar.

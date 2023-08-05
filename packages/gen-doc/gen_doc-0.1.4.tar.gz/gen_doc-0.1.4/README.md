## ``gen_doc`` - Library to generate documentation

### Installation

```commandline
pip install gen_doc
```

### What it does?
+ aggregates all `.py` files into one or multiple `.md` files, keeping the same hierarchy
+ collects all classes and methods with their information
+ parses `google` & `sphinx` py docstrings.

### How to use:

+ install the library
+ in your project directory open the terminal
+ run the command `gen_doc init`
+ adjust config file accordingly
+ run the command `gen_doc build -c`

### Details

#### General
```text
Usage: gen_doc [OPTIONS] COMMAND [ARGS]...

  Utility for generating project documentation from docstrings

Options:
  -v, --version  Get library version
  -i, --init     Init gen_doc config with default parameters
  -b, --build    Build documentation by config
  --help         Show this message and exit.

Commands:
  build  Build documentation
  init   To init config file in order to generate documentation.
```
#### Init
```text
Usage: gen_doc init [OPTIONS]
  To init config file in order to generate documentation.
Options:
  -f, --file-config TEXT  Config file name  [default: gen_doc.yaml]
  -o, --overwrite         To overwrite, in case file already exists
  --help                  Show this message and exit.
```
#### Build
```text
Usage: gen_doc build [OPTIONS] [[py]]
  Build documentation
Options:
  -sm, --save-mode [md]      Save mode
  -hi, --hierarchically      Extract with the same hierarchy
  -o, --overwrite            To overwrite, in case file already exists
  -p2r, --path-to-root TEXT  Path to the directory for which documentation
                             should be compiled
  -p2s, --path-to-save TEXT  Path to the directory where the documentation
                             should be saved
  -f2s, --file-to-save TEXT  Path to the directory where the documentation
                             should be saved
  -c, --config               Use config to build documentation.
  -f, --file-config TEXT     Config file name  [default: gen_doc.yaml]
  --help                     Show this message and exit.
```
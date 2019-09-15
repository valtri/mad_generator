# MAD Generator

A standalone program that simulates cloud life and generates accounting records based on received arguments . The program is used to generate consistent data for functional and scaling tests.

## Arguments

Run `python mad.py --help` to see arguments  
To see debug logs use `-d` or `--debug`
To run flood mode use `-f` or `--flood`

## Example

```
python3 mad.py --output-type=opennebulaxml --count=5 --max-objects=10 --mode=vm -f

```

#!/usr/bin/python

from glob import glob
import re
from os.path import basename
from pprint import pformat


#=============================================================================
def main():
    all_files = glob("/data/schuetto/git/cp2k/cp2k/src/*.F")
    all_mods = {}
    for fn in all_files:
        this_mod = basename(fn)[:-2]
        content = open(fn).read()
        use_mods = re.findall(r"\n\s*USE\s+(\w+)", content)
        all_mods[this_mod] = use_mods

    f = open("cp2k_moddeps.txt", "w")
    f.write(pformat(all_mods))
    f.close()
        
#=============================================================================
main()
#EOF

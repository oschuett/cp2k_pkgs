#!/usr/bin/python

from glob import glob
import re
from os.path import basename
from pprint import pprint
import os

#=============================================================================
def read_mod2pkg():
    content = open("cp2k_packages.txt").read()
    cur_pkg = None
    mod2pkg = dict()
    for line in content.strip().split("\n"):
        if(len(line.strip())==0): continue
        if(line[0] == "#"): continue
        m = re.match(r"=== (.*) ===", line)
        if(m):
            cur_pkg = m.group(1)
            #print("Found package: "+cur_pkg)
        else:
            assert(line[-2:] == ".F")
            mod = line[:-2]
            mod2pkg[mod] = cur_pkg

    print("Found %d packages."%len(set(mod2pkg.values())))
    return(mod2pkg)


#=============================================================================
def main():
    moddeps = eval(open("cp2k_moddeps.txt").read())
    mod2pkg = read_mod2pkg()
    mod2pkg = dict([(k, v.split("/",1)[0]) for k,v in mod2pkg.items()])

    bad_links = [('common', 'subsys'),
                 ('common', 'force_eval'),
                 ('common', 'else'),
                 ('common', 'program'),
                 ('common', 'motion'),
                 ('common', 'cp_base'),
                 ('force_eval', 'motion'),
                 ('force_eval', 'program'),
                 ('subsys','force_eval'),
                 ('subsys','motion'),
                 ('subsys','program'), ]

    #all_mods = set()
    all_links = set()
    for this_mod, mods_used in moddeps.items():
        this_pkg = mod2pkg[this_mod]
        for m in mods_used:
            if(m not in mod2pkg.keys()):
                #print("Module not found in mod2pkg: "+m)
                continue
            p = mod2pkg[m]
            #print p
            if(p == this_pkg): continue

            for a, b in bad_links:
                if(this_pkg==a and p==b):
                    print this_pkg+" depends on "+p+" becaus "+this_mod+" uses "+m

            all_links.add( (this_pkg, p) )

    all_links_by_pkg = dict()
    print("Found %d links between packages"%len(all_links))


    #-------------------------------------------------------------------------
    hide_pkgs = ("cp_base", "else",)
    #hide_pkgs = ()

    f = open("cp2k_overview.dot","w")
    f.write("digraph cp2k {\n")
    for a, b in all_links:
        if(a in hide_pkgs or b in hide_pkgs): continue
        color = 'black'
        for a2, b2 in bad_links:
            if(a==a2 and b==b2):
                color = 'red'
        f.write("%s -> %s [color=%s];\n"%(a,b,color))

    f.write("}\n")
    f.close()
    print("Wrote cp2k_overview.dot")

    os.system("dot -Tpng cp2k_overview.dot > cp2k_overview.png")
    print("Wrote cp2k_overview.png")


#=============================================================================
main()
#EOF

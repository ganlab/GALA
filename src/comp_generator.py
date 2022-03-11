#!/usr/bin/env python3
################################################################
#  This file part of GALA Gap-free Long-reads Assembler        #
#  Auther: Mohamed awad                                        #
#  Company: Xiangchao Gan lab (MPIPZ)                          #
#  Released under the (MIT) license (see LICENSE file)         #
################################################################

import os
def comp_generator(genomes,output=os.getcwd()):
    z=list(open(genomes))
    z=filter(lambda i:'=' in i, z)
    a=[]
    for base in z:
        a.append(base.split('=')[0])
    #c=[]
    if output[-1]!='/':
        output=output+'/'
    b=open(output+'draft_comp.sh','w')
    b.writelines('mkdir -p comparison\ncd comparison\n')
    b.writelines(''.join(z))
    for base in a:
        for ba in a:
            if base!=ba:
                b.writelines('minimap2 -x asm5 $'+base+' $'+ba+' > '+base+'vs'+ba+'.paf\n')
            #else:
            #    c.append('minimap2 -x asm5 $'+base+' $'+ba+' > '+base+'vs'+ba+'\n')
    #for base in c:
    #    b.writelines(base)
    #b.close()

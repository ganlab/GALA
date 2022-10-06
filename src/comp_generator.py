#!/usr/bin/env python3
################################################################
#  This file part of GALA Gap-free Long-reads Assembler        #
#  Auther: Mohamed awad                                        #
#  Company: Xiangchao Gan lab (MPIPZ)                          #
#  Released under the (MIT) license (see LICENSE file)         #
################################################################

import os

def DEPRECATED_comp_generator(genomes,output=os.getcwd()):
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








def comp_generator(genomes, output=os.getcwd(), mm2params=""):
    ''' This version was introduced in JohnUrban Fork. '''
    z=list(open(genomes))
    z=filter(lambda i:'=' in i, z)
    a={}                                                     	## DICTIONARY INSTEAD OF LIST
    for base in z:
        k,v = base.strip().split('=')					## GET KEY VALUE PAIRS
        a[k] = v						## ADD TO DICT
    #c=[]
    if output[-1]!='/':
        output=output+'/'
    b=open(output+'draft_comp.sh','w')
    b.writelines('mkdir -p comparison\ncd comparison\n')
    b.writelines(''.join(z))
    DRAFTS = list(a.keys())					## MAKE LIST OF KEYS IN DICT (THESE ARE THE DRAFT NICKNAMES)
    for base in DRAFTS:						## ITERATE OVER DRAFTS LIST
        for ba in DRAFTS:					## ITERATE OVER DRAFTS LIST
            if base!=ba:
                ### USE a[base] and a[ba] TO GET ASSEMBLY PATHS FOR MM2, INSTEAD OF "$" SIGNS AND NICKNAMES; USE NICKNAMES FOR PAF FILE.
                ### Added echo of the command used for easier diagnosis of issues.
                ### mm2params allows threading options (and perhaps others in the future).
                OUT=''.join([base, 'vs', ba, '.paf'])
                CMD=' '.join(['minimap2 -x asm5', mm2params, a[base], a[ba], '>', OUT])	## TO AVOID REPEATED CMD EDITNG IN ECHO AND ACTIVE VERSIONS.
                b.writelines('echo "' + CMD + '"\n' + CMD + '\necho\n\n')

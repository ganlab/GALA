#!/usr/bin/env python2
################################################################
#  This file part of GALA Gap-free chromosome-scALe Assembler  #
#  Auther: Mohamed awad                                        #
#  Company: Xiangchao Gan lab (MPIPZ)                          #
#  Released under the (MIT) license (see LICENSE file)         #
################################################################

import os
def new_genome(cut_file,old_genome,out_path=os.getcwd(),name='new_genome'):
    a=list(open(cut_file))
    n=0
    while n<len(a):
        if a[n]=='\n':
            del a[n]
        else:
            n=n+1
    b={}
    for base in a:
        b[base.split()[0]]=[]
    for base in a:
        b[base.split()[0]]+=[base.split()[1]]
    for base in b.keys():
        b[base].insert(0,0)
    for base in b.keys():
        b[base].append('end')
    c=list(open(old_genome))
    c=''.join(c)
    c=c.split('>')
    del c[0]
    d={}
    for base in c:
        e=base.split('\n')
        d[e[0].split()[0]]=''.join(e[1:])
    e,f={},{}
    for base in d.keys():
        if base in b.keys():
            e[base]=d[base]
        else:
            f[base]=d[base]
    i={}
    for base in b.keys():
        g=b[base]
        h=1
        j=0
        while j <len(g)-1:
            if g[j+1]!='end':
                i[base+'_'+str(h)+'_'+'awad']=e[base][int(g[j]):int(g[j+1])]
            else:
                i[base+'_'+str(h)+'_'+'awad']=e[base][int(g[j]):]
            j=j+1
            h=h+1
    g=open(out_path+'/'+name+'.fa','w')
    for base in i.keys():
        g.writelines('>'+base+'\t'+str(len(i[base]))+'\n')
        h=0
        while h<len(i[base]):
            g.writelines(i[base][h:h+80]+'\n')
            j=h
            h=h+80

    for base in f.keys():
        g.writelines('>'+base+'_awad'+'\t'+str(len(f[base]))+'\n')
        h=0
        while h<len(f[base]):
            g.writelines(f[base][h:h+80]+'\n')
            j=h
            h=h+80
    g.close()
    return(i,f)

def genomes(genomes,gathering,gathering_name='gathering_',outpath=os.getcwd()):
    z=list(open(genomes))
    if outpath[-1]!='/':
        outpath=outpath+'/'
    if gathering[-1]!='/':
        gathering=gathering+'/'
    c=open(outpath+'new_draft_names_paths.txt','w')
    for base in z:
        a=base.split('=')[0]
        aa=base.split('=')[1].replace('\n','')
        b=new_genome(cut_file=gathering+gathering_name+'_'+a+'_cuts.txt',old_genome=aa,out_path=outpath,name='new_'+a)
        c.writelines('new_'+a+'='+outpath+'new_'+a+'.fa\n')
    c.close()
    return()

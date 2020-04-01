#!/usr/bin/env python2
################################################################
#  This file part of GALA Gap-free chromosome-scALe Assembler  #
#  Auther: Mohamed awad                                        #
#  Company: Xiangchao Gan lab (MPIPZ)                          #
#  Released under the (MIT) license (see LICENSE file)         #
################################################################
import os
def file_filter(path,number_of_drafts,output=os.getcwd(),block=10000,percentage=70,shortage_contig=50000,quality=20,file_output=False):

    files=os.listdir(path)
    c={}
    for base in files:
        '''
        change it in 11th of Feb 2020
        a=base.split('_')
        b=a[1].split('vs')
        key=a[0][0]+b[0][0]+'v'+b[1][0]+a[-1][0]
        c[key]=list(open(path+'/'+base))
        '''
        key=base.replace('.paf','')
        c[key]=list(open(path+'/'+base))
    a=list(c.keys())
    #a=sorted(a, key=lambda i:i.replace(i[:3],''))change it in 11th of Feb 2020
    a=sorted(a, key=lambda i:i.replace(i[:i.index('vs')+2],''))
    d={}
    n=0
    while n<len(a):
        '''
        change it in 11th of Feb 2020
        no=1
        d[a[n][3:]]=[[a[n],c[a[n]]]]
        while no<(number_of_drafts-1):
            d[a[n][3:]].append([a[n+no],c[a[n+no]]])
            no=no+1
        no=1
        n=n+(number_of_drafts-1)
        '''
        no=1
        ind=a[n].index('vs')
        d[a[n][ind+2:]]=[[a[n],c[a[n]]]]
        while no<(number_of_drafts-1):
            d[a[n][ind+2:]].append([a[n+no],c[a[n+no]]])
            no=no+1
        no=1
        n=n+(number_of_drafts-1)
    e={}
    ee={}
    for bo in list(d.keys()):
        b=d[bo]
        for base in b:
            for ba in base[1]:
                if ba.split('\t')[0] in e.keys():
                    e[ba.split('\t')[0]]+=['\t'.join(ba.split('\t')[:12])+'\t'+str(int(float(ba.split('\t')[9])/float(ba.split('\t')[10])*100))+'\t'+base[0]+'\n']
                else:
                    e[ba.split('\t')[0]]=['\t'.join(ba.split('\t')[:12])+'\t'+str(int(float(ba.split('\t')[9])/float(ba.split('\t')[10])*100))+'\t'+base[0]+'\n']
        for base in e.keys():
            e[base]=sorted(e[base],key=lambda i:(int(i.split('\t')[2]),i[-1]))
        ee[bo]=e
        e={}
    ff=ee.copy()
    for bo in ff.keys():
        f=ff[bo]
        for base in f.keys():
            n=0
            while n<len(f[base]):
                if int(f[base][n].split('\t')[10])<block:
                    del f[base][n]
                elif int(f[base][n].split('\t')[11])<quality:
                    del f[base][n]
                elif int(f[base][n].split('\t')[12])<percentage:
                    del f[base][n]
                elif int(f[base][n].split('\t')[1])<shortage_contig or int(f[base][n].split('\t')[6])<shortage_contig:
                    del f[base][n]
                else:
                    n=n+1
        ff[bo]=f
    r={}
    rr={}
    for bo in ff.keys():
        f=ff[bo]
        for base in f.keys():
            g=f[base][:]
            m=0
            gg=[]
            while m<len(g):
                gg+=[g[m]]
                del g[m]
                n=0
                while n<len(g):
                    if gg[-1].split('\t')[5]==g[n].split('\t')[5]:
                        gg.append(g[n])
                        del g[n]
                    else:
                        n=n+1
                m=0
            r[base]=gg
        rr[bo]=r
        r={}
    if file_output==True:
        for bo in rr.keys():
            z=open(output+bo+'_new.txt','w')
            r=rr[bo]
            for base in r.keys():
                for ba in r[base]:
                    z.writelines(ba)
            z.close()
    return(rr)

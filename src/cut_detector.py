#!/usr/bin/env python3
################################################################
#  This file part of GALA Gap-free Long-reads Assembler        #
#  Auther: Mohamed awad                                        #
#  Company: Xiangchao Gan lab (MPIPZ)                          #
#  Released under the (MIT) license (see LICENSE file)         #
################################################################

import os
from joining import reformated

def stat(sq,eq,st,et,diff_sq,diff_eq,diff_st,diff_et,lq):
    if (sq<=diff_sq and eq>=diff_eq) or (st<=diff_st and et>=diff_et) or (sq<=diff_sq and et>=diff_et) or (eq>=diff_eq and st<=diff_st):
        if (sq<=diff_sq and eq>=diff_eq):
            return('bass','complete')
        else:
            if (sq>diff_sq and eq<diff_eq):
                return('bass','from '+str(sq)+' to '+str(eq))
            elif sq<=diff_sq:
                return('bass','from '+str(0)+' to '+str(eq))
            else:
                return('bass','from '+str(sq)+' to '+str(lq))
    else:
        if (sq<=diff_sq or st<=diff_st):
            return ('cut', str(eq)+' or '+str(et),str(eq))
        elif (eq>=diff_eq or et>=diff_et):
            return ('cut', str(sq)+' or '+str(st),str(sq))
        else:
            return ('cut', str(sq)+' or '+str(st) +' and '+str(eq)+' or '+str(et),str(sq),str(eq))

def stat2(sq,eq,st,et,diff_sq,diff_eq,diff_st,diff_et,lq):
    if (sq<=diff_sq and eq>=diff_eq) or (st<=diff_st and et>=diff_et) or (sq<=diff_sq and st<=diff_st) or (eq>=diff_eq and et>=diff_et):
        if (sq<=diff_sq and eq>=diff_eq):
            return('bass','complete')
        else:
            if (sq>diff_sq and eq<diff_eq):
                return('bass','from '+str(sq)+' to '+str(eq))
            elif sq<=diff_sq:
                return('bass','from '+str(0)+' to '+str(eq))
            else:
                return('bass','from '+str(sq)+' to '+str(lq))
    else:
        if (sq<=diff_sq or et>=diff_et):
            return ('cut', str(eq)+' or '+str(st),str(eq))
        elif (eq>=diff_eq or st<=diff_st):
            return ('cut', str(sq)+' or '+str(et),str(sq))
        else:
            return ('cut', str(sq)+' or '+str(st) +' and '+str(eq)+' or '+str(et),str(sq),str(eq))

#path='/netscratch/dep_tsiantis/grp_gan/awad/todo/cor.reads/drafts_comp'
def cut_detector(path,number_of_drafts,block=10000,percentage=70,shortage_contig=50000,quality=20,out_file=False,only_cut=False,output=os.getcwd(),diff_1=50000,diff_2=25000,diff_3=15000):
    a=reformated(path,number_of_drafts,block=block,percentage=percentage,shortage_contig=shortage_contig,quality=quality)
    l={}
    o={}
    for draft in list(a.keys()):
        b=a[draft]
        g={}
        w={}
        for key in list(b.keys()):
            c=b[key]
            e=[]
            h=[]
            u=[]
            for base in c:
                d=base.split('\t')
                sq=int(float(d[2]))
                eq=int(float(d[3]))
                s=d[4]
                st=int(float(d[7]))
                et=int(float(d[8]))
                lq=int(float(d[1]))
                lt=int(float(d[6]))
                if lq>1000000:
                    diff_sq=diff_1#12000
                    diff_eq=lq-diff_1#12000
                elif lq>100000:
                    diff_sq=diff_2#10000
                    diff_eq=lq-diff_2#10000
                else:
                    diff_sq=diff_3#5000
                    diff_eq=lq-diff_3#5000
                if lt>1000000:
                    diff_st=diff_1
                    diff_et=lt-diff_1
                elif lt>100000:
                    diff_st=diff_2
                    diff_et=lt-diff_2
                else:
                    diff_st=diff_3
                    diff_et=lt-diff_3
                if s=='+':
                    f=stat(sq,eq,st,et,diff_sq,diff_eq,diff_st,diff_et,lq)
                else:
                    f=stat2(sq,eq,st,et,diff_sq,diff_eq,diff_st,diff_et,lq)
                e.append('\t'.join(d).replace('\n','')+'\t'+'\t'.join(f)+'\n')
            b[key]=e
            for line in e:
                if 'cut' in line:
                    h.append(line)
            g[key]=h
            for line in e:
                if 'bass' in line:
                    u.append(line)
            w[key]=u
        a[draft]=b
        l[draft]=g
        o[draft]=w
        if out_file==True:
            f=open(output+'/cut_detector_'+draft+'.txt','w')
            for key in list(b.keys()):
                c=b[key]
                for base in c:
                    f.writelines(base)
            f.close()
        if only_cut==True:
            f=open(output+'/cut_detector_only_'+draft+'.txt','w')
            for key in list(b.keys()):
                c=b[key]
                for base in c:
                    if 'cut' in base:
                        f.writelines(base)
            f.close()

    return(a,l,o)#a=all,l=only cut,o=only pass

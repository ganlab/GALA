#!/usr/bin/env python2
################################################################
#  This file part of GALA Gap-free Long-reads Assembler        #
#  Auther: Mohamed awad                                        #
#  Company: Xiangchao Gan lab (MPIPZ)                          #
#  Released under the (MIT) license (see LICENSE file)         #
################################################################

from cut_detector import cut_detector
from file_filter import file_filter

def scaff(scaffolds):
    h={}
    i=1
    k=0
    l={}
    for base in scaffolds.keys():
        sca=sorted(scaffolds[base], key=lambda i:len(i), reverse=True)
        for ba in sca:
            k=0
            if len(h)==0:
                if len(ba)>1:
                    h['scaff_'+str(i)]=ba
                elif len(ba)==1 and type(ba)==list:
                    h['scaff_'+str(i)]=ba
                else:
                    h['scaff_'+str(i)]=[ba]
            else:
                for bas in ba:
                    for basee in h.keys():
                        if bas in h[basee]:
                            h[basee]=h[basee]+ba
                            h[basee].sort()
                            h[basee]=list(set(h[basee]))
                            k=1
                            break
                if k==0:
                    i=i+1
                    if len(ba)>1:
                        h['scaff_'+str(i)]=ba
                    elif len(ba)==1 and type(ba)==list:
                        h['scaff_'+str(i)]=ba
                    else:
                        h['scaff_'+str(i)]=[ba]

        l[base]=h
        h={}
        i=1
    return(l)
import os
def scaffolding(path,number_of_drafts,block=10000,percentage=70,shortage_contig=50000,quality=20,out_file=False,output_name='scaffolds',output=os.getcwd()):
    aa=cut_detector(path,number_of_drafts,block,percentage,shortage_contig,quality)
    a=aa[2]
    #ori_block=block
    #ori_per=percentage
    #ori_con=shortage_contig
    #ori_qual=quality
    h={}
    for base in a.keys():
        m={}
        for ba in a[base].keys():
            if len(a[base][ba])==0:
                m[ba]=[]
        h[base]=m
    o=file_filter(path,number_of_drafts,block=1,percentage=0,shortage_contig=0,quality=-1)
    for base in h.keys():
        for ba in h[base].keys():
            try:
               h[base][ba]=sorted(o[base][ba],key=lambda i:(int(i.split('\t')[9]),int(i.split('\t')[6]),int(i.split('\t')[11]),int(i.split('\t')[12])),reverse=True)
            except:
                continue
    '''
    for base in h.keys():
        for ba in h[base].keys():
            n=0
            num=True
            while num==True:
                if int(h[base][ba][0].split('\t')[6])<ori_block:
                    del h[base][ba][0]
                else:
                    num=False
    '''
    for base in h.keys():
        for ba in h[base].keys():
            try:
                a[base][ba]=[h[base][ba][0]]
                op=h[base][ba][0].split('\t')
                op0=op[0]
                op1=op[1]
                op2=op[2]
                op3=op[3]
                op4=op[4]
                op5=op[5]
                op6=op[6]
                op7=op[7]
                op8=op[8]
                op9=op[9]
                op10=op[10]
                op11=op[11]
                op12=op[12]
                op13=op[13].split('vs')
                newop=[op5,op6,op7,op8,op4,op0,op1,op2,op3,op9,op10,op11,op12,op13[1].replace('\n','')+'vs'+op13[0],'bass','from '+op7+' to '+op8]
                newop='\t'.join(newop)
                a[op13[0]][op5]+=[newop]

            except:
                continue
    '''
    for base in a.keys():
        for bas in a[base].keys():
            bom=a[base][bas]
            for ba in bom:
                op=ba.split('\t')
                op0=op[0]
                op1=op[1]
                op2=op[2]
                op3=op[3]
                op4=op[4]
                op5=op[5]
                op6=op[6]
                op7=op[7]
                op8=op[8]
                op9=op[9]
                op10=op[10]
                op11=op[11]
                op12=op[12]
                op13=op[13].split('vs')
                op14=op[14]
                op15=op[15]
                newop=[op5,op6,op7,op8,op4,op0,op1,op2,op3,op9,op10,op11,op12,op13[1].replace('\n','')+'vs'+op13[0],op14,op15]
                newop='\t'.join(newop)
                a[op13[0]][op5]+=[newop]
    '''
    z={}
    for key in a.keys():
        b=a[key]
        for base in b.keys():
            n=0
            while n<len(b[base]):
                if len(b[base][n].split('\t'))==14:
                    b[base][n]=b[base][n].replace('\n','\t')+'bass\tcomplete\n'
                    n=n+1
                else:
                    n=n+1
        c={}
        for base in b.keys():
            for ba in b[base]:
                if ba.split('\t')[-3] not in c.keys():
                    c[ba.split('\t')[-3].replace('\n','')]={}
        for base in b.keys():
            for ba in b[base]:
                d=ba.split('\t')[-3].replace('\n','')
                e=ba.split('\t')[5]
                if e in c[d].keys():
                    c[d][e]+=[ba]
                else:
                    c[d][e]=[ba]
        for base in c.keys():
            d=base.split('vs')
            e=d[0]
            f=d[1]
            for ba in c[base].keys():
                for bas in a[e][ba]:
                    if f in bas:
                        op=bas.split('\t')
                        op0=op[0]
                        op1=op[1]
                        op2=op[2]
                        op3=op[3]
                        op4=op[4]
                        op5=op[5]
                        op6=op[6]
                        op7=op[7]
                        op8=op[8]
                        op9=op[9]
                        op10=op[10]
                        op11=op[11]
                        op12=op[12]
                        op13=op[13].split('vs')
                        newop=[op5,op6,op7,op8,op4,op0,op1,op2,op3,op9,op10,op11,op12,op13[1].replace('\n','')+'vs'+op13[0],'bass','from '+op7+' to '+op8]
                        newop='\t'.join(newop)
                        c[base][ba]+=[newop]

        d={}
        for base in b.keys():
            d[base]=[]

        for base in b.keys():
            for ba in b[base]:
                e=ba.split('\t')[-3].replace('\n','')
                f=ba.split('\t')[5]
                d[base]+=c[e][f]
        e={}
        f={}
        for base in d.keys():
            e[base]=[]
            f[base]=[]
        for base in d.keys():
            n=0
            while n<len(d[base]):
                if d[base][n].split('\t')[0] in f[base]:
                    n=n+1
                else:
                    f[base]+=[d[base][n].split('\t')[0]]
                    e[base]+=[d[base][n]]
                    if (d[base][n].split('\t')[-3].replace('\n','')==d[base][n-1].split('\t')[-3].replace('\n','')) and (d[base][n].split('\t')[5]==d[base][n-1].split('\t')[5]):
                        f[base]+=[d[base][n-1].split('\t')[0]]
                        e[base]+=[d[base][n-1]]
                    elif (d[base][n].split('\t')[-3].replace('\n','')==d[base][n+1].split('\t')[-3].replace('\n','')) and (d[base][n].split('\t')[5]==d[base][n+1].split('\t')[5]):
                        f[base]+=[d[base][n+1].split('\t')[0]]
                        e[base]+=[d[base][n+1]]
                    n=n+1
        print(key+str(len(f)))
        z[key]=f
        single={}
        scaffolds={}
        for key in z.keys():
            g=z[key]
            s=[]
            sc=[]
            for base in g:
                if len(g[base])<=1:
                    s.append(base)
                else:
                    sc.append(list(set(g[base])))
            sc=sorted(sc)
            sa=[]
            for base in sc:
                if base not in sa:
                    sa.append(base)
            single[key]=s
            scaffolds[key]=sa
    scaffolds_list=scaff(scaffolds)
    for ay in scaffolds_list.keys():
        for ya in scaffolds_list[ay].keys():
            if len(scaffolds_list[ay][ya])==1:
                single[ay]+=[scaffolds_list[ay][ya][0]]
                del scaffolds_list[ay][ya]

    zom=0
    for ien in scaffolds_list.keys():
        for bot in scaffolds_list[ien].keys():
            for bac in scaffolds_list[ien][bot]:
                zom=zom+int(a[ien][bac][0].split('\t')[1])
            scaffolds_list[ien][bot].append(str(zom))
            zom=0
    for ien in single.keys():
        qq=0
        for bot in single[ien]:
            zom=int(a[ien][bot][0].split('\t')[1])
            single[ien][qq]=single[ien][qq]+'\t'+str(zom)
            qq=qq+1
    if out_file==True:
        os.system('mkdir -p '+output+'/'+output_name)
        output=output+'/'+output_name
        for bo in scaffolds_list.keys():
            z=open(output+'/'+output_name+'_'+bo+'.scaff','w')
            r=scaffolds_list[bo]
            rr=single[bo]
            z.writelines('Scaffolds List:\n\n')
            for bn in sorted(r.keys(),key=lambda i:int(i.replace('scaff_',''))):
                z.writelines(bn+'\t')
                for i in r[bn]:
                    z.writelines(i+'\t')
                z.writelines('\n')
            z.writelines('\nSingle Contigs:\n\n')
            for bn in rr:
                z.writelines(bn+'\n')
            z.close()
    return(scaffolds_list,single)

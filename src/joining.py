#!/usr/bin/env python2
################################################################
#  This file part of GALA Gap-free chromosome-scALe Assembler  #
#  Auther: Mohamed awad                                        #
#  Company: Xiangchao Gan lab (MPIPZ)                          #
#  Released under the (MIT) license (see LICENSE file)         #
################################################################

from file_filter import file_filter
import os
def reformated(path,number_of_drafts,block=5000,percentage=70,shortage_contig=5000,quality=20,files=False,output='reformated_',out_path=os.getcwd()):
    a=file_filter(path,number_of_drafts,block=block,percentage=percentage,shortage_contig=shortage_contig,quality=quality,file_output=False)
    c={}
    for base in a.keys():
        c[base]=[]
    for key in a.keys():
        k={}
        for ke in a[key].keys():
            k[ke]=[]
        for ky in a[key].keys():
            b=a[key][ky]
            z=b[:]
            d=[]
            for base in b:
                e=base.split('\t')
                f=e[5]
                n=0
                m=0
                while m<len(b):
                    if f in b[m]:
                        n=n+1
                        m=m+1
                    else:
                        m=m+1
                if n==1:
                    d.append(base)
            for element in d:
                if element in b:
                    b.remove(element)

            g={}
            for base in b:
                g[base.split('\t')[5]]=[]
            for base in b:
                g[base.split('\t')[5]]+=[base]

            for base in g.keys():
                m=g[base]
                n=0
                while n<len(m):
                    try:
                        e=m[n].split('\t')
                        f=m[n+1].split('\t')
                        h=m[n-1].split('\t')
                        str1=int(e[2])
                        end1=int(e[3])
                        str2=int(e[7])
                        end2=int(e[8])
                        strand1=e[4]
                        str3=int(f[2])
                        end3=int(f[3])
                        str4=int(f[7])
                        end4=int(f[8])
                        dif1=int((end1-str1)*0.85)
                        dif2=int((end2-str2)*0.85)
                        dif3=int((end3-str3)*0.85)
                        dif4=int((end4-str4)*0.85)
                        if int(e[1])>=100000:
                            dif5=20000
                        else:
                            dif5=5000
                        strand2=f[4]
                        if (str3>=str1-1500 and str3<=end1+1500 and (end3<=end1+dif5)) or (str4>=str2-1500 and str4<=end2+1500 and (end4<=end2+dif5)):
                            del g[base][n+1]
                        elif (str1>=str3-1500 and (end1<=end3+dif5)) or (str2>=str4-1500 and (end2<=end4+dif5)):
                            del g[base][n]
                        else:
                            n=n+1
                    except:
                        break


            for base in g.keys():
                m=g[base]
                n=0
                while n<len(m):
                    try:
                        e=m[n].split('\t')
                        f=m[n+1].split('\t')
                        h=m[n-1].split('\t')
                        str1=int(e[2])
                        end1=int(e[3])
                        str2=int(e[7])
                        end2=int(e[8])
                        strand1=e[4]
                        str3=int(f[2])
                        end3=int(f[3])
                        str4=int(f[7])
                        end4=int(f[8])
                        strand2=f[4]
                        dif1=int((end1-str1)*0.85)
                        dif2=int((end2-str2)*0.85)
                        dif3=int((end3-str3)*0.85)
                        dif4=int((end4-str4)*0.85)
                        if int(e[1])>=1000000:
                            dif5=100000
                        elif int(e[1])>=100000:
                            dif5=20000
                        else:
                            dif5=5000
                        if strand1==strand2 and strand1=='+':
                            if ((str3>(str1+dif1)) and (str3<end1+dif5)) and ((str4>(str2+dif2)) and (str4<end2+dif5)):
                                qstart=str1
                                qend=end3
                                tstart=str2
                                tend=end4
                                new_hit=e[:2]+[str(qstart)]+[str(qend)]+e[4:7]+[str(tstart)]+[str(tend)]+[str(int(e[9])+int(f[9]))]+[str(int(e[10])+int(f[10]))]+[str((int(e[11])+int(f[11]))/2)]+[e[12]]+[e[13]]
                                new_hit='\t'.join(new_hit)
                                del m[n]
                                del m[n]
                                m.insert(n,new_hit)
                            else:
                                n=n+1
                        elif strand1==strand2 and strand1=='-':
                            if ((str3>(str1+dif1)) and (str3<end1+dif5)) and ((str2>(str4+dif4)) and (str2<end4+dif5)):
                                qstart=str1
                                qend=end3
                                tstart=str4
                                tend=end2
                                new_hit=e[:2]+[str(qstart)]+[str(qend)]+e[4:7]+[str(tstart)]+[str(tend)]+[str(int(e[9])+int(f[9]))]+[str(int(e[10])+int(f[10]))]+[str((int(e[11])+int(f[11]))/2)]+[e[12]]+[e[13]]
                                new_hit='\t'.join(new_hit)
                                del m[n]
                                del m[n]
                                m.insert(n,new_hit)
                            else:
                                n=n+1
                        else:
                            n=n+1
                    except:
                        n=0
                        while n<len(m):
                            try:
                                e=m[n].split('\t')
                                f=m[n+1].split('\t')
                                h=m[n-1].split('\t')
                                str1=int(e[2])
                                end1=int(e[3])
                                str2=int(e[7])
                                end2=int(e[8])
                                strand1=e[4]
                                str3=int(f[2])
                                end3=int(f[3])
                                str4=int(f[7])
                                end4=int(f[8])
                                dif1=int((end1-str1)*0.85)
                                dif2=int((end2-str2)*0.85)
                                dif3=int((end3-str3)*0.85)
                                dif4=int((end4-str4)*0.85)
                                if int(e[1])>=100000:
                                    dif5=20000
                                else:
                                    dif5=5000
                                strand2=f[4]
                                if (str3>=str1-1500 and str3<=end1+1500 and (end3<=end1+dif5)) or (str4>=str2-1500 and str4<=end2+1500 and (end4<=end2+dif5)):
                                    del m[n+1]
                                elif (str1==str3-1500 and (end1<=end3+dif5)) or (str2>=str4-1500 and (end2<=end4+dif5)):
                                    del m[n]
                                else:
                                    n=n+1
                            except:
                                break
                        g[base]=m
                        break

            for base in g.keys():
                for ba in g[base]:
                    d.append(ba)
            k[ky]=d

        c[key]=k
    if files==True:
        os.system('mkdir -p '+out_path+'/'+output)
        out_path=out_path+'/'+output
        for bo in c.keys():
            z=open(out_path+'/'+output+bo+'.txt','w')
            r=c[bo]
            for bn in r.keys():
                for ba in r[bn]:
                    z.writelines(ba)
            z.close()
    return c

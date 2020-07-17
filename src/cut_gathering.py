#!/usr/bin/env python2
################################################################
#  This file part of GALA Gap-free Long-reads Assembler        #
#  Auther: Mohamed awad                                        #
#  Company: Xiangchao Gan lab (MPIPZ)                          #
#  Released under the (MIT) license (see LICENSE file)         #
################################################################

from cut_detector import cut_detector
import os
def cut_gathering(path,number_of_drafts,block=5000,percentage=70,shortage_contig=5000,quality=20,cut_block=175,out_file=False,out_name='gathering',out_path=os.getcwd(),lowest_cut=1,threshold=False,threshold_value=3):
    a=cut_detector(path,number_of_drafts,block=block,percentage=percentage,shortage_contig=shortage_contig,quality=quality)
    b=a[1]
    k=a[0]
    bk=a[2]
    w={}
    ww={}
    for draft in b.keys():
        c=b[draft]
        l=k[draft]
        cl=bk[draft]
        v={}
        vv={}
        for key in c.keys():
            d=c[key]
            m=l[key]
            dm=cl[key]
            h=[]
            for base in d:
                if 'and' in base:
                    h.append(int(base.split('\t')[-2]))
                    h.append(int(base.split('\t')[-1].replace('\n','')))
                else:
                    h.append(int(base.split('\t')[-1].replace('\n','')))
            h.sort()
            i=[]
            n=0

            while n<len(h)-1:
                if h[n+1]-h[n]<175:#play in this
                    n=n+1
                else:
                    i.append(h[:n+1])
                    del h[:n+1]
                    n=0
            if len(d)==1:
                i.append(h[-1:])
                del h[-1]
            elif len(d)>1 and len(i)==0:
                i.append(h)
            elif len(d)==0:
                ana_awad=0#1_10_2019
            elif h[-1]-i[-1][-1]<175:
                i[-1].append(h[-1])
                del h[-1]
            else:
                i.append(h[-1:])
                del h[-1]
            j={}
            for base in i:
                j[sum(base)/len(base)]=[len(base),base[0],base[-1]]
            jj={}
            for base in j.keys():
                #o=j[base][0]
                p=j[base][1]
                q=j[base][2]
                u=[]
                j[base].append(0)
                for ba in m:
                    r=int(ba.split('\t')[2])
                    s=int(ba.split('\t')[3])
                    if (r<=p-50 and s>=q+50) or (r>=q-50 and s<=p+50):
                        j[base][-1]+=1
                        u.append(ba.split('\t')[13])
                j[base][-1]=j[base][-1]
                j[base].append(0)
                for ba in dm:
                    if 'from' in ba:
                        r=int(ba.split('\t')[-1].replace('from','').replace('to','').replace('\n','').split()[0])
                        s=int(ba.split('\t')[-1].replace('from','').replace('to','').replace('\n','').split()[1])
                        if (r>=p-20 and r<=p+20) or (r>=q-20 and r<=p+20) or (s>=p-20 and s<=p+20) or (s>=q-20 and s<=p+20):
                             j[base][-1]+=1
                j[base][-1]=j[base][-1]
                j[base].append(len(set(u))-j[base][0])
                if j[base][0]>=float(number_of_drafts)/2 and j[base][3]<=j[base][0]:#1_10_2019
                    jj[base]=j[base]
                elif j[base][0]>float(number_of_drafts)/2:
                    jj[base]=j[base]
                elif j[base][3]==0 and j[base][0]>= lowest_cut:
                    jj[base]=j[base]
                elif j[base][0]> j[base][3] and j[base][0]>= lowest_cut and (float(j[base][3])/float(j[base][0]))<=0.50:
                    jj[base]=j[base]
                elif j[base][0]> (j[base][3]-j[base][4]) and j[base][0]>= lowest_cut and j[base][0]>=j[base][3] and j[base][4]>0  and (float(j[base][3]-j[base][4])/float(j[base][0]))<=0.60:
                    jj[base]=j[base]
                #elif j[base][0]> (j[base][3]-j[base][4]) and j[base][0]>= lowest_cut and j[base][0]>=j[base][3] and j[base][4]>0  and (float(j[base][3]-j[base][4])/float(j[base][0]))<=0.60:
                #    jj[base]=j[base]
            v[key]=j
            if len(jj)>0:
                vv[key]=jj
        w[draft]=v
        ww[draft]=vv
    if out_file==True:
        os.system('mkdir -p '+out_path+'/'+out_name)
        out_path=out_path+'/'+out_name
        for draft in w.keys():
            t=open(out_path+'/'+out_name+'_'+draft+'.txt','w')
            tt=open(out_path+'/'+out_name+'_'+draft+'_cuts.txt','w')
            z=w[draft]
            zt=ww[draft]
            for key in z.keys():
                zz=z[key]
                for base in sorted(list(zz.keys())):
                    t.writelines(key+'\t'+str(base)+'\t'+str(zz[base][0])+'\t'+str(zz[base][1])+'\t'+str(zz[base][2])+'\t'+str(zz[base][3])+'\t'+str(zz[base][4])+'\n')
            for key in zt.keys():
                zz=zt[key]
                for base in sorted(list(zz.keys())):
                    tt.writelines(key+'\t'+str(base)+'\t'+str(zz[base][0])+'\t'+str(zz[base][3])+'\t'+str(zz[base][4])+'\n')
            t.close()
            tt.close()
    return(a[0],a[1],w,a[2],ww)

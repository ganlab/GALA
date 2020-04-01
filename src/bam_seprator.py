#!/usr/bin/env python2
################################################################
#  This file part of GALA Gap-free chromosome-scALe Assembler  #
#  Auther: Mohamed awad                                        #
#  Company: Xiangchao Gan lab (MPIPZ)                          #
#  Released under the (MIT) license (see LICENSE file)         #
################################################################

#use the below command for contig_name file
#samtools view -H bam_file |grep "SQ"|cut -f 2|cut -d : -f 2 > contig_names
import os
def bam_seprator(contig_name,bam_file,out_put_path=os.getcwd(),out_put_name='bam_seprator.sh',folder_name='bams'):
    a=list(open(contig_name))
    c=open(out_put_path+'/'+out_put_name,'w')
    c.writelines('#!bin/sh login\n')
    c.writelines('bam='+bam_file+'\n')
    c.writelines('mkdir '+folder_name+'\ncd '+folder_name+'\n')
    for base in a:
        c.writelines('samtools view -b $bam "'+base.replace('\n','')+'" > '+base.replace('\n','')+'.bam\n')
    #c.writelines('for var in '+folder_name+'/*bam; do samtools view $var | cut -f 1 > $var.read_names; done')
    c.close()

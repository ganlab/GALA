		########################################################################
		#                                                                      #
		# 		Gala Human genome reference guide assembly             #
		#       		Mohamed Awad & Xiangchao Gan	               #
		#       		(10.1101/2020.05.15.097428)  		       #	
		#								       #
		########################################################################

#Create working directory
mkdir -p human
#Move helping files to working directory
mv sep_chr_ref.sh human/.
mv drafts.txt human/.
mv chr.sh human/.

cd human
workdir=$(pwd)

#Create important folders
mkdir -p $workdir/20k
mkdir -p $workdir/20k/scaffold_reads
mkdir -p $workdir/10k
mkdir -p $workdir/10k/scaffold_reads
mkdir -p $workdir/ref
mkdir -p $workdir/canu_draft
mkdir -p $workdir/assembly
mkdir -p $workdir/reads_mix
for i in {1..23}; do mkdir -p $workdir/assembly/chrom$i;done;

#Download
#--------------------------------------------------------------------------------------
#Download GALA
git clone https://github.com/ganlab/GALA.git
#fastq-dump from Sratools
software=fastq-dump

#Download Human genome GRCh38.p13
cd $workdir/ref
wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.39_GRCh38.p13/GCF_000001405.39_GRCh38.p13_genomic.fna.gz
gunzip GCF_000001405.39_GRCh38.p13_genomic.fna.gz && mv GCF_000001405.39_GRCh38.p13_genomic.fna GRCh38.p13.genome.fa
ref=$workdir/ref/GRCh38.p13.genome.fa

#Separte contigs according to chromosomes
sh $workdir/sep_chr_ref.sh # It is better to filter the output of this step to include primary scaffolds only
for i in ch*; do cut -d ' ' -f 1 $i|sed 's/>//g' > $i.scaff;done;
for i in *scaff; do echo -n "cat "| cat - $i >> temp  && sed ':a;N;$!ba;s/\n/.bam.read_names /g' temp  > temp2 && echo -e "> $i.read_names" >> temp2 && sed ':a;N;$!ba;s/\n/.bam.read_names /g' temp2  > temp3 && mv temp3 $i.sh && rm temp*;done;

#Download draft genomes from Sergey Nurk etal 2020 (10.1101/gr.263566.120)
cd $workdir/canu_draft
wget https://obj.umiacs.umd.edu/marbl_publications/hicanu/chm13_20k_hicanu_hifi.fasta.gz
wget https://obj.umiacs.umd.edu/marbl_publications/hicanu/chm13_10k_hicanu_hifi.fasta.gz
draft=$workdir/canu_draft/chm13_20k_hicanu_hifi.fasta.gz
draft2=$workdir/canu_draft/chm13_10k_hicanu_hifi.fasta.gz

cd $workdir/10k
#Download first dataset 
wget https://sra-download.ncbi.nlm.nih.gov/traces/sra38/SRR/008874/SRR9087597
wget https://sra-download.ncbi.nlm.nih.gov/traces/sra34/SRR/008874/SRR9087598
wget https://sra-download.ncbi.nlm.nih.gov/traces/sra73/SRR/008874/SRR9087599
wget https://sra-download.ncbi.nlm.nih.gov/traces/sra39/SRR/008874/SRR9087600
for i in ./SRR*;do $software --table SEQUENCE $i -O $(pwd);done
cat *fastq > seq.fq

cd $workdir/20k
#Download second dataset
wget https://sra-download.ncbi.nlm.nih.gov/traces/sra58/SRR/011027/SRR11292120
wget https://sra-download.ncbi.nlm.nih.gov/traces/sra58/SRR/011027/SRR11292121
wget https://sra-download.ncbi.nlm.nih.gov/traces/sra55/SRR/011027/SRR11292122
wget https://sra-download.ncbi.nlm.nih.gov/traces/sra58/SRR/011027/SRR11292123
for i in ./SRR*;do $software --table SEQUENCE $i -O $(pwd);done
cat *fastq > seq.fq
#--------------------------------------------------------------------------------------



#Use Gala for reformating mapping files and scaffolding 
#--------------------------------------------------------------------------------------
cd $workdir
$workdir/GALA/comp drafts.txt
sh draft_comp.sh
$workdir/GALA/reformat comparison 3
$workdir/GALA/ccm comparison 3 # You can use the scaffolding information from CCM output but this will need manual curation to ignore samll contigs, mis-assembly and alignment errors. 
cp chr.sh reformat*/.
cd reformat*
sh chr.sh
##Here I use reformat output to create the scaffolds bins instead of CCM. Also, it is better to try manual curation. Which is easer in this case by comparing the contigs in reformat_ref.txt file with those in the output 
for i in chrom*; do echo -n "cat "| cat - $i >> temp  && sed ':a;N;$!ba;s/\n/.bam.read_names /g' temp  > temp2 && echo -e "> $i.read_names" >> temp2 && sed ':a;N;$!ba;s/\n/.bam.read_names /g' temp2  > temp3 && mv temp3 $i.sh && rm temp*;done;
#--------------------------------------------------------------------------------------


#Mapping
#--------------------------------------------------------------------------------------
cd $workdir/10k
#Mapping vs the reference 
reads=$workdir/10k/seq.fq
minimap2 -ax asm20 $ref $reads | samtools view -Sb | samtools sort > ref.bam
samtools index ref.bam

#Mapping vs the draft assembly from Sergey Nurk etal 2020
minimap2 -ax asm20 $draft $reads | samtools view -Sb | samtools sort > draft.bam
samtools index draft.bam

cd $workdir/20k
#Mapping vs the reference 
reads=$workdir/20k/seq.fq
minimap2 -ax asm20 $ref $reads | samtools view -Sb | samtools sort > ref.bam
samtools index ref.bam

#Mapping vs the draft assembly from Sergey Nurk etal 2020
minimap2 -ax asm20 $draft $reads | samtools view -Sb | samtools sort > draft.bam
samtools index draft.bam
#--------------------------------------------------------------------------------------


#Linkage Group Assembly Module (LGAM)
#--------------------------------------------------------------------------------------
cd $workdir/10k
#Use Gala to seperate bams
samtools view -H ref.bam|grep '@SQ'|cut -f 2|cut -d ':' -f 2 > ref.contigs
$workdir/GALA/seprator ref.contigs $workdir/10k/ref.bam -f ref_sep.sh -b ref_bams
sh ref_sep.sh 

samtools view -H draft.bam|grep '@SQ'|cut -f 2|cut -d ':' -f 2 > draft.contigs
$workdir/GALA/seprator draft.contigs $workdir/10k/draft.bam -f draft_sep.sh -b draft_bams
sh draft_sep.sh

#Use Gala to extract each scaffold reads
cp $workdir/ref/*sh ref_bams/.
cd ref_bams
for i in *bam; do samtools view $i | cut -f 1 > $i.read_names;done;
for i in *sh; do sh $i;done
for i in *scaff.read.names; do $workdir/GALA/readsep $reads $i -f fq;done;
mv *fq $workdir/10k/scaffold_reads

cd $workdir/10k
cp $workdir/reformat*/chrom*sh draft_bams/.
cd draft_bams
for i in *bam; do samtools view $i | cut -f 1 > $i.read_names;done;
for i in *sh; do sh $i;done
for i in chrom*.read.names; do $workdir/GALA/readsep $reads $i -f fq;done;
mv *fq $workdir/10k/scaffold_reads

#Merge the reads 
cd $workdir/10k/scaffold_reads
for i in {1..22}; do cat $workdir/10k/draft_bams/chrom$i.scaff.read_names $workdir/10k/ref_bams/chr$i.scaff.read_names > $i.read_names;done;
cat $workdir/10k/draft_bams/chromx.scaff.read_names $workdir/10k/ref_bams/chr23.scaff.read_names > 23.read_names
for i in *.read.names; do $workdir/GALA/readsep $reads $i -f fq;done;
rm *.read_names

cd $workdir/20k

#Use Gala to seperate bams
samtools view -H ref.bam|grep '@SQ'|cut -f 2|cut -d ':' -f 2 > ref.contigs
$workdir/GALA/seprator ref.contigs $workdir/20k/ref.bam -f ref_sep.sh -b ref_bams
sh ref_sep.sh

samtools view -H draft.bam|grep '@SQ'|cut -f 2|cut -d ':' -f 2 > draft.contigs
$workdir/GALA/seprator draft.contigs $workdir/20k/draft.bam -f draft_sep.sh -b draft_bams
sh draft_sep.sh

#Use Gala to extract each scaffold reads 
cp $workdir/ref/*sh ref_bams/.
cd ref_bams
for i in *bam; do samtools view $i | cut -f 1 > $i.read_names;done;
for i in *sh; do sh $i;done
for i in *scaff.read.names; do $workdir/GALA/readsep $reads $i -f fq;done;
mv *fq $workdir/20k/scaffold_reads

cd $workdir/20k
cp $workdir/reformat*/chrom*sh draft_bams/.
cd draft_bams
for i in *bam; do samtools view $i | cut -f 1 > $i.read_names;done;
for i in *sh; do sh $i;done
for i in chrom*.read.names; do $workdir/GALA/readsep $reads $i -f fq;done;
mv *fq $workdir/20k/scaffold_reads

#Merge the reads 
cd $workdir/20k/scaffold_reads
for i in {1..20}; do cat $workdir/20k/draft_bams/chrom$i.scaff.read_names $workdir/20k/ref_bams/chr$i.scaff.read_names > $i.read_names;done;
cat $workdir/20k/draft_bams/chromx.scaff.read_names $workdir/20k/ref_bams/chr23.scaff.read_names > 23.read_names
for i in *.read.names; do $workdir/GALA/readsep $reads $i -f fq;done;
rm *.read_names

#Merge the reads from both_datasets
cd $workdir/reads_mix
for i in {1..22}; do cat $workdir/20k/scaffold_reads/chrom$i.scaff.read.fq $workdir/10k/scaffold_reads/chrom$i.scaff.read.fq > chrom$i.mix.fq;done;
$workdir/20k/scaffold_reads/chromx.scaff.read.fq $workdir/10k/scaffold_reads/chromx.scaff.read.fq > chromx.mix.fq
for i in {1..23}; do cat $workdir/20k/scaffold_reads/chr$i.scaff.read.fq $workdir/10k/scaffold_reads/chr$i.scaff.read.fq > chr$i.mix.fq;done;
for i in {1..23}; do cat $workdir/20k/scaffold_reads/$i.read.fq $workdir/10k/scaffold_reads/$i.read.fq > $i.mix.fq;done;
mv $workdir/20k/scaffold_reads/*fq .


##Now in reads_mix folder there are 6 datasets for each Chromsome. by assembling ($i.mix.fq) file we can reach most of chromosomes for some chromosmes we need to assemble another dataset from the 5 remaining sets. Also we used the Hifiasm as a primary assembler, but for some chromosmes canu was required.  

#--------------------------------------------------------------------------------------

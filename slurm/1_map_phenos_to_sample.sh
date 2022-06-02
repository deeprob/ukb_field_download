#!/bin/bash
#SBATCH --account=girirajan
#SBATCH --partition=girirajan
#SBATCH --job-name=pheno_down
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=24
#SBATCH --time=400:0:0
#SBATCH --mem-per-cpu=12G
#SBATCH --chdir /data5/deepro/ukbiobank/download/download_phenotypes/src
#SBATCH -o /data5/deepro/ukbiobank/download/download_phenotypes/slurm/logs/out_map_samples.log
#SBATCH -e /data5/deepro/ukbiobank/download/download_phenotypes/slurm/logs/err_map_samples.log
#SBATCH --nodelist qingyu

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/data5/deepro/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/data5/deepro/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/data5/deepro/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/data5/deepro/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<


conda activate ukbiobank

echo `date` starting job on $HOSTNAME

#### GLOBALS ####
root_dir="/data5/deepro/ukbiobank/download/download_phenotypes/data"
phenos_of_interest_file="/data5/deepro/ukbiobank/preprocess/rarecomb_pheno_prepare/data/lifestyle.xlsx"
sample_to_phenoval_file="/data5/deepro/ukbiobank/preprocess/rarecomb_pheno_prepare/data/ukb30075.csv"
cpus=24

python /data5/deepro/ukbiobank/download/download_phenotypes/src/1_map_phenos_to_samples.py $root_dir $phenos_of_interest_file $sample_to_phenoval_file $cpus

echo `date` ending job on $HOSTNAME

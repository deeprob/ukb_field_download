#!/bin/bash
#SBATCH --account=girirajan
#SBATCH --partition=girirajan
#SBATCH --job-name=pheno_down
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --time=400:0:0
#SBATCH --mem-per-cpu=4G
#SBATCH --chdir /data5/deepro/ukbiobank/download/download_phenotypes/src
#SBATCH -o /data5/deepro/ukbiobank/download/download_phenotypes/slurm/logs/out_download_%a.log
#SBATCH -e /data5/deepro/ukbiobank/download/download_phenotypes/slurm/logs/err_download_%a.log
#SBATCH --array 1-2

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
LINE=$(sed -n "$SLURM_ARRAY_TASK_ID"p /data5/deepro/ukbiobank/download/download_phenotypes/slurm/slurm_files/download_fields_info.txt)

echo $LINE
python /data5/deepro/ukbiobank/download/download_phenotypes/src/0_download_fields_info.py $LINE 

echo `date` ending job

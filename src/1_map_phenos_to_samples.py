#!/usr/bin/env python

FILE_OBJECTIVE = """
Given, 
1) a phenotype of interest file, 
2) a UKBiobank csv file that maps samples to all phenotype values,
3) a csv file that maps samples to their exome files, 
this file will map all samples that have exomes to their phenotypic values for the
phenotype of interest.
"""

import argparse
import pandas as pd
import utils as ut
import multiprocessing as mp


def read_phenos_of_interest_data(file, min_samples=2000):
    """
    This function reads interesting phenotype file of type xlsx prepared manually, 
    selects the shortlisted phenotypes with at least 2000 exome samples and
    returns a filtered dataframe 
    """
    df = pd.read_excel(file)
    df = df.loc[df.shortlist=="X"]
    df = df.loc[df.Num_exome_samples_with_phenotype>=min_samples]
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=FILE_OBJECTIVE)
    parser.add_argument("root_dir", type=str, help="The path to the root dir where phenotype files will be stored")
    parser.add_argument("phenos_of_interest", type=str, help="The file path that points to the phenotype of interest file")
    parser.add_argument("sample_to_phenovals", type=str, help="The file path that maps samples to their phenotype values")
    parser.add_argument("n_threads", type=int, help="Number of cpus to use for this task", default=24)

    args = parser.parse_args()

    phenos_of_interest_df = read_phenos_of_interest_data(args.phenos_of_interest)

    pool_iter = [(args.sample_to_phenovals, args.root_dir, t, c, i) for t,c,i in zip(phenos_of_interest_df.Type, phenos_of_interest_df.Phenotype_group, phenos_of_interest_df.Phenotype_ID)]
    pool = mp.Pool(args.n_threads)
    pool.starmap(ut.create_pheno2sample_files_map, pool_iter)
    pool.close()
    pool.join()

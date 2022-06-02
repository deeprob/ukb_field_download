#!/usr/bin/env python

FILE_OBJECTIVE = """
Download all phenotypic field infos (their names, ids, encodings) 
from UKBiobank and store them in their appropriate directories under field 
type and field category
"""

import argparse
import utils as ut

##### GLOBALS #####

# the basket id of the phenotypes
id_of_interest = "2001392"

# Parse the main project page to get all the phenotype categories and their fields which are part of the 
# project
def parse_project_pheno(project_html):
    project_soup = ut.make_soup(project_html)
    pheno_dict = ut.filtration_steps(project_soup, id_of_interest)
    return pheno_dict

# Parse phenotype type html  get all the phenotypic fields which are annotated under them
def parse_type_pheno(type_html):
    type_soup = ut.make_soup(type_html)
    type_dict = ut.get_field_dict(type_soup)
    return type_dict

# Filter phenodict
# 1. Only phenotypes which are not bulk or retired.
# 2. Only phenotypes which are present under the specified type

def filter_project_pheno(pheno_dict, type_dict):
    pheno_dict_no_bulk_or_retired = ut.filter_bulk_retired(pheno_dict)
    pheno_dict_cat = ut.filter_by_field(pheno_dict_no_bulk_or_retired, type_dict)
    return pheno_dict_cat


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=FILE_OBJECTIVE)
    parser.add_argument("project_html", type=str, help="The html file path of the main project")
    parser.add_argument("type_html", type=str, help="The html file path of type of the phenotype fields")
    parser.add_argument("type_outdir", type=str, help="The folder where fields under this type will be stored")

    args = parser.parse_args()

    # project pheno dict creation
    pheno_dict = parse_project_pheno(args.project_html)
    # type pheno dict creation
    type_dict = parse_type_pheno(args.type_html)
    # filter type pheno by fields of interest present in our project phenos
    pheno_dict_field = filter_project_pheno(pheno_dict, type_dict)
    # Add pheno field info as a json file under their respective type and category dirs 
    ut.add_field_info_to_outdir(args.type_outdir, pheno_dict_field)
    # Add pheno field encodings as a json file under their respective type and category dirs
    ut.get_field_data_encodings(args.type_outdir)

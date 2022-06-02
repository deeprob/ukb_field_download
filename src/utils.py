import os
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup
from itertools import islice
from bs4.element import NavigableString


#################################
# project page parser functions #
#################################

def make_soup(html_doc):
    """
    Create a bs compatible file
    """
    with open(html_doc) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
    return soup

def get_child_phenos_from_parent_pheno(tclass, href):
    """
    Get all the sub phenotypic fields that fall under the main category
    """
    tids =  [t for t in tclass if "id" in t.attrs]
    href_id = href.replace("#", "")
    tcollapsed_row = [t for t in tids if t["id"]==href_id]
    return tcollapsed_row

def get_tag_text(tag):
    return tag.text.strip()

def get_fields_from_tags(tag):
    all_fields = tag.find_all("div")
    assert len(all_fields) == 2
    fields = [t.text.strip() for t in all_fields]
    return tuple(fields)


def filtration_steps(html_soup, id_of_interest):
    """
    Creates a dictionary with the phenotypic category as keys
    and their field info as values
    """
    # filter tags which have a class attribute
    tags_with_class = [t for t in html_soup.body.find_all("div") if "class" in t.attrs]
    # filter tags which have a showcase head, these have the phenotype main categories
    tags_with_showcase = [t for t in tags_with_class if t["class"] == ["showcaseHead"]]
    # filter showcase tags which are phenotypes
    tags_with_main_pheno = [t for t in tags_with_showcase if id_of_interest in t["href"]]

    # get all the phenotype fields from the phenotype category
    tcrows = [get_child_phenos_from_parent_pheno(tags_with_class, tmp["href"]) for tmp in tags_with_main_pheno]

    # create a dictionary that stores the phenotypes category we want as keys and their fields
    # as values

    mp_dict = dict()

    for main_pheno, pheno_rows in  zip(tags_with_main_pheno, tcrows):
        mp_text = get_tag_text(main_pheno)
        mp_fields = [get_fields_from_tags(prc) for pheno_row in pheno_rows for prc in islice(pheno_row.children, 3, None, 2)]
        mp_dict[mp_text] = mp_fields

    return mp_dict


#########################################
# phenotypic type html parser functions #
#########################################

def get_field_info(tr_tag):
    all_field_tags = tr_tag.find_all("td")
    all_fields = [t.text.strip() for t in all_field_tags]
    return tuple(all_fields)

def get_field_dict(field_soup):
    """
    Returns a dictionary with the keys as the fields which have been annotated 
    under a specific type in UKBiobank and the values as the repective fields info
    """
    all_table_rows = field_soup.find("table").find_all("tr")
    table_fields = list(map(get_field_info, all_table_rows[1:]))
    field_id = [f[0] for f in table_fields]
    field_info = [(f[1], f[2]) for f in table_fields]
    return dict(zip(field_id, field_info))


###################################
# phenotype dict filter functions #
###################################

def filter_bulk_retired(pheno_dict):
    """
    Given a project phenotypic dict,
    this function will filter all phenotypes 
    which are annotated as bulk or retired and return a filtered dict
    """
    pheno_dict_no_bulk_or_retired = {}
    for k,v in pheno_dict.items():
        tmpv = [vi for vi in v if "Bulk" not in vi[1]]
        newv = [vi for vi in tmpv if "Retired" not in vi[1]]
        if newv:
            pheno_dict_no_bulk_or_retired[k] = newv
    return pheno_dict_no_bulk_or_retired


def filter_by_field(pheno_dict, annot_dict):
    """
    Given a project phenotypic dict, and a type annotated pheno dict, 
    this function will filter all phenotypes 
    which are not in the annotated dict
    """    
    pheno_dict_cat = {}

    for k,v in pheno_dict.items():
        newv = [vi for vi in v if vi[0] in annot_dict]
        if newv:
            pheno_dict_cat[k] = newv
    return pheno_dict_cat


######################################################
# add fields names as a json under type/category dir #
######################################################

def add_field_info_to_outdir(main_cat_outdir, pheno_cat_dict):
    """
    This function creates a type outdir, a category outdir and stores the field id and 
    field name of all the fields present under the specific type and category of phenotypes
    """
    for k, v in pheno_cat_dict.items():
        outdir_pheno = os.path.join(main_cat_outdir, k.replace("/", "").replace(" ", "_"))
        os.makedirs(os.path.join(outdir_pheno), exist_ok=True)
        fs = [i for i,j in v]
        fis = [j for i,j in v]
        field_map = dict(zip(fs, fis))
        outjson = os.path.join(outdir_pheno, "fields.json")
        with open(outjson, "w") as f:
            json.dump(field_map, f, indent=4)
    return 


#########################################################
# add field encodings as a json under type/category dir #
#########################################################

def read_json(json_file):
    with open(json_file, "r") as f:
        data_dict = json.load(f)
    return data_dict

def check_data_header(first_tag):
    if first_tag.text == "Data":
        return True
    return False

def get_field_response(field_id):
    r = requests.get(f"https://biobank.ndph.ox.ac.uk/showcase/field.cgi?id={field_id}")
    return r

def get_data_code_response(data_code):
    r = requests.get(f"https://biobank.ndph.ox.ac.uk/showcase/coding.cgi?id={data_code}")
    return r

def get_field_id_data_info(response_out):
    """
    Returns the data coding id from the response of a field id if present
    """
    page = BeautifulSoup(response_out.text, "html.parser")
    # the div tag with class attribute tabbertab should have the data field info
    tt = [tags for tags in page.find_all("div") if tags["class"]==["tabbertab"]]
    # check that the header tag is Data
    assert check_data_header(list(tt[0].children)[0])
    # iterate through the children text to see if Data Coding is present
    for idx, child in enumerate(tt[0].children):
        if isinstance(child, NavigableString):
            if "data-coding" in child.strip().lower():
                data_coding_id = list(tt[0].children)[idx+1].text
                return data_coding_id
    return

def check_categories_header(first_tag):
    if first_tag.text.split()[1] == "Categories":
        return True
    return False

def get_data_coding_table_header(tr_tag):
    return tuple([th.text for th in tr_tag.find_all("th")])

def get_data_coding_table_rows(tr_tag):
    return tuple([td.text for td in tr_tag.find_all("td")])

def get_data_coding_info(response_out):
    """
    Returns the data coding mappings from the response of a data code
    """
    page = BeautifulSoup(response_out.text, "html.parser")
    # the div tag with class attribute tabbertab should have the data field info
    tt = [tags for tags in page.find_all("div") if tags["class"]==["tabbertab"]]
    # check that the header tag is Categories
    try:
        assert check_categories_header(list(tt[0].children)[0])
        # get the categories table
        categories_tag = tt[0]
        trs = categories_tag.find_all("tr")
        th = get_data_coding_table_header(trs[0])
        tds = list(map(get_data_coding_table_rows, trs[1:]))
        assert list(map(len, tds)) == [len(th) for _ in range(len(tds))]
        tds_dict = {td[0]: td[1] for td in tds}
        return tds_dict
    except:
        print("Tree like structure might be present")
    return "Tree-like"

def get_field_data_encodings(pheno_type_folder):
    """
    This function scans an user defined folder denoting a main quantitative phenotype 
    for example integer and collects the field ids of the phenotypes from each subfolder/
    sub categories of the main phenotype, then for the fields in each subfolder, it looks 
    at the data encodings given in UKBiobank and stores those encodings as a json file named
    field_data_encoded.json
    
    Returns: .
    """
    # scanning through the main type of quantitative phenotypes
    for folder in os.scandir(pheno_type_folder):
        # for each sub category, look at the fields.json file to find all fields per subcategory
        json_file_with_fields = os.path.join(folder.path, "fields.json")
        field_dict = read_json(json_file_with_fields)
        # for each field, find the data encodings given in UKBiobank, if any
        meta_data_coding_dict = {}
        for field_id in field_dict.keys():
            fr = get_field_response(field_id)
            data_coding_id = get_field_id_data_info(fr)
            if data_coding_id:
                dr = get_data_code_response(data_coding_id)
                dc_dict = get_data_coding_info(dr)
                meta_data_coding_dict[field_id] = dc_dict
            else:
                meta_data_coding_dict[field_id] = None
        json_with_field_data_coding = os.path.join(folder.path, "fields_data_coding.json")
        with open(json_with_field_data_coding, "w") as f:
            json.dump(meta_data_coding_dict, f, indent=4)

    return


##########################################
# adding sample info to phenotype fields #
##########################################

def get_sample_to_pheno_columns(sample_to_pheno):
    """
    Get all the phenotypic values that are mapped to ukb samples
    """
    sample_to_pheno_columns = list(pd.read_csv(sample_to_pheno, nrows=1).columns) 
    return sample_to_pheno_columns

def create_pheno2sample_files(sample_to_phenoval_file, pheno_main_dir, pheno_field):
    """
    takes in,
    1) samples to phenotype values mapped file
    2) the dir where pheno field info will be stored 
    3) the pheno field of interest
    """
    sample_to_pheno_columns = get_sample_to_pheno_columns(sample_to_phenoval_file)

    # find the columns which may have this value
    # edited this to ensure other fields that start with this field id don't come out: eg. field 34 might also involve fields 3406,3416,3426 etc
    sample_to_pheno_subset_columns = [bfc for bfc in sample_to_pheno_columns if bfc.startswith(pheno_field+"-")] 
    if sample_to_pheno_subset_columns:
        # load only these columns of the dataframe and keep on adding samples
        sample_to_pheno_subset_columns = ["eid"] + sample_to_pheno_subset_columns
        mode = "w"
        header=True
        csv_out = os.path.join(pheno_main_dir, f"{pheno_field}.csv")
        for chunk in pd.read_csv(sample_to_phenoval_file, encoding= 'unicode_escape', usecols=sample_to_pheno_subset_columns, low_memory=False, chunksize=10**4):
            chunk = chunk.set_index("eid").dropna(how="all")
            chunk.to_csv(csv_out, index=True, header=header, mode=mode)
            header = False
            mode = "a"
    return  

def create_pheno2sample_files_map(sample_to_phenoval_file, root_dir, pheno_type, pheno_cat, pheno_field):
    """
    Takes in
    1) samples to phenotype values mapped file
    2) phenotype type dir e.g. integer
    3) phenotype category dir e.g. Alcohol Use
    4) phenotype field id e.g. 20403,
    Creates a table that maps the samples to their values for this particular phenotype
    """
    pheno_main_dir = os.path.join(root_dir, pheno_type, pheno_cat.replace("/", "").replace(" ", "_"), "tables")
    pheno_field = str(pheno_field)
    os.makedirs(pheno_main_dir, exist_ok=True)
    create_pheno2sample_files(sample_to_phenoval_file, pheno_main_dir, pheno_field)
    return

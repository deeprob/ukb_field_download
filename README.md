# Downloading quantitative phenotypes from UKBiobank and mapping them to their samples

UKBiobank denotes a field as any specific information about an individual, such as *cooked vegetable intake*. A field is divided into a category, for example cooked vegetable intake falls under the category of *diet*. Each field also has a type, for instance the cooked vegetable intake field values are of type *integer*. Some of the field values also have special data encodings.


This repository downloads fields along with their encodings provided by UKBiobank and categorises them by storing under the fields type and category. The field type -> field category -> field id hierarchy is represented as a directory structure. 


Subsequently, it maps each of the field values to their sample ids by eliminating any sample ids which do not have information about that field. The final result will be a table for each field where the table is a csv file under following format:

```
eid, field_n_info0, field_n_info1, ...
```

where eid denotes the sample id of an individual and field_n_info{x} denotes the xth information provided for field_n.

## Downloading field information and field encodings from UKBiobank

1. Download the main project page and the specific field ids, categories and type provided in UKBiobank webpage as an html document. Details provided in *data/README.md* file.

2. Run *src/0_download_fields_info.py* script which has 3 required arguments:
    - project_html: previously downloaded main project webpage html path
    - type_html: previously downloaded field type webpage html path
    - type_outdir: the directory where information about the fields that fall under the specific field type will be stored according to field type -> field category -> field id hierarchical directory structure.

## Mapping field values to their samples

1. Run *src/1_map_phenos_to_samples.py* script which has 3 required arguments:
    - root_dir: The directory where the mapped sample to field val files will be stored.
    - phenos_of_interest: An excel file which contains the fields of interest (denoted by *Phenotype_ID* column) along with the field category (denoted by *Phenotype_group* column) and field type (denoted by *Phenotype_Type* column).These three columns **must** be present in the excel file and their naming conventions **must** match for the script to work.
    - sample_to_phenovals: A csv file generated from UKBiobank that contains all the sample ids as rows and their field values as columns.

# Downloading specific files from UKBiobank required for extracting field information

## Required file descriptions
1. project_page.html: The main project page of UKBiobank Application ID: 45023.

2. phenotypic_fields/categorical_multiple.html : All fields that fall under the category *Categorical (multiple)* as annotated by UKBiobank.

3. phenotypic_fields/categorical_single.html : All fields that fall under the category *Categorical (single)* as annotated by UKBiobank. 

4. phenotypic_fields/compound.html : All fields that fall under the category *Compound* as annotated by UKBiobank.

5. phenotypic_fields/continuous_fields.html : All fields that fall under the category *Continuous* as annotated by UKBiobank. 

6. phenotypic_fields/date.html : All fields that fall under the category *Date* as annotated by UKBiobank. 

7. phenotypic_fields/integer.html : All fields that fall under the category *Integer* as annotated by UKBiobank. 

8. phenotypic_fields/text.html : All fields that fall under the category *Text* as annotated by UKBiobank.

9. phenotypic_fields/time.html : All fields that fall under the category *Time* as annotated by UKBiobank.


## Downloading main project page html 
The main project page in UKBiobank contains information about all the data fields (standard and bulk) that we requested as part of the project. We will extract all the phenotypes provided to us by UKBiobank from the main page. To download the project page html:

1. Follow the link: *UKBiobank -> Researcher log in -> AMS -> Projects -> {application_id} -> View/Update -> Project details -> Show All Baskets and Overall Summary*

2. Download the web page as an html file.


## Downloading standard field information from UKBiobank
Each standard field is divided by their type, e.g. integer or continuous, and category, e.g. addictions or anxiety. We will extract all these standard field information along with thier respective type, category and data encodings from UKBiobank. To download these standard fields:

1. Follow the link: *UKBiobank -> Data Showcase -> Catalogues -> Fields -> {type of the field}*

2. Download the type of field web page as an html file.

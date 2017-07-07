import json
import sys
import os
from ..parsers.ase_parser import parse_ase
from ..utils.file_utils import find_files
from tqdm import tqdm
from ..validator.schema_validator import Validator

# VERSION 0.2.0

# This is the converter for the bfcc-13 dataset: Cluster expansion made easy with Bayesian compressive sensing
# Arguments:
#   input_path (string): The file or directory where the data resides.
#       NOTE: Do not hard-code the path to the data in the converter (the filename can be hard-coded, though). The converter should be portable.
#   metadata (string or dict): The path to the JSON dataset metadata file, a dict or json.dumps string containing the dataset metadata, or None to specify the metadata here. Default None.
#   verbose (bool): Should the script print status messages to standard output? Default False.
#       NOTE: The converter should have NO output if verbose is False, unless there is an error.
def convert(input_path, metadata=None, verbose=False):
    if verbose:
        print("Begin converting")

    # Collect the metadata
    if not metadata:
        dataset_metadata = {
            "mdf-title": "Cluster expansion made easy with Bayesian compressive sensing",
            "mdf-acl": ['public'],
            "mdf-source_name": "bfcc13",
            "mdf-citation": ["Lance J. Nelson, Vidvuds Ozoliņš, C. Shane Reese, Fei Zhou, Gus L.W. Hart: Cluster expansion made easy with Bayesian compressive sensing, Physical Review B 88(15): 155105, 2013."],
            "mdf-data_contact": {

                "given_name": "Gus",
                "family_name": "Hart",

                "email": "gus.hart@gmail.com",
                "institution": "Brigham Young University",
                },

            "mdf-author": [{
                
                "given_name": "Gus",
                "family_name": "Hart",
                
                "email": "gus.hart@gmail.com",
                "instituition": "Brigham Young University"
                
                },
                {
                    
                "given_name": "Lance",
                "family_name": "Nelson",
                
                "institution": "Brigham Young University"
                
                },
                {
                
                "given_name": "Vidvuds",
                "family_name": "Ozoliņš",
                
                "instituition": "University of California Los Angeles",
                
                },
                {
                
                "given_name": "Shane",
                "family_name": "Reese",
                
                "instituition": "Brigham Young University",
                
                },
                {
                
                "given_name": "Fei",
                "family_name": "Zhou",
                
                "instituition": "Lawrence Livermore National Laboratory",
                
                }],

#            "mdf-license": ,

            "mdf-collection": "bfcc13",
            "mdf-data_format": ["vasp"],
            "mdf-data_type": ["DFT"],
#            "mdf-tags": ,

            "mdf-description": "4k DFT calculations for solid AgPd, CuPt and AgPt FCC superstructures. DFT/PBE energy, forces and stresses for cell sizes 1-16 across all compositions including primitive cells.",
            "mdf-year": 2013,

            "mdf-links": {

                "mdf-landing_page": "http://qmml.org/datasets.html#bfcc-13",

                "mdf-publication": ["https://journals.aps.org/prb/abstract/10.1103/PhysRevB.88.155105"],
               # "mdf-dataset_doi": ,

#                "mdf-related_id": ,

                "tar_bz2": {
                
                    #"globus_endpoint": ,
                    "http_host": "http://qmml.org",

                    "path": "/Datasets/bfcc-13.tar.bz2",
                    }
                },

#            "mdf-mrr": ,

            "mdf-data_contributor": [{
                "given_name": "Evan",
                "family_name": "Pike",
                "email": "dep78@uchicago.edu",
                "institution": "The University of Chicago",
                "github": "dep78"
                }]
            }
        
    elif type(metadata) is str:
        try:
            dataset_metadata = json.loads(metadata)
        except Exception:
            try:
                with open(metadata, 'r') as metadata_file:
                    dataset_metadata = json.load(metadata_file)
            except Exception as e:
                sys.exit("Error: Unable to read metadata: " + repr(e))
    elif type(metadata) is dict:
        dataset_metadata = metadata
    else:
        sys.exit("Error: Invalid metadata parameter")



    # Make a Validator to help write the feedstock
    # You must pass the metadata to the constructor
    # Each Validator instance can only be used for a single dataset
    # If the metadata is incorrect, the constructor will throw an exception and the program will exit
    dataset_validator = Validator(dataset_metadata)


    # Get the data
    #    Each record should be exactly one dictionary
    #    You must write your records using the Validator one at a time
    #    It is recommended that you use a parser to help with this process if one is available for your datatype
    #    Each record also needs its own metadata
    errors = 0
    for data_file in tqdm(find_files(input_path, "OUTCAR"), desc="Processing files", disable=not verbose):
        try:
            data = parse_ase(os.path.join(data_file["path"], data_file["filename"]), "vasp-out")
        except Exception as e:
            print("error on: " + str(e))
            errors +=1
        if data:
            uri = "https://data.materialsdatafacility.org/collections/" + "bfcc-13/bfcc-13/" + data_file["no_root_path"] + "/" + data_file["filename"]
        record_metadata = {
            "mdf-title": "bfcc13 - " + data["chemical_formula"],
            "mdf-acl": ['public'],

#            "mdf-tags": ,
#            "mdf-description": ,
            
            "mdf-composition": data["chemical_formula"],
#            "mdf-raw": ,

            "mdf-links": {
                "mdf-landing_page": uri,

#                "mdf-publication": ,
#                "mdf-dataset_doi": ,

#                "mdf-related_id": ,

                "data_links": {
                    "globus_endpoint": "82f1b5c6-6e9b-11e5-ba47-22000b92c6ec",
                    #"http_host": ,

                    "path": "/collections/bfcc-13/bfcc-13/" + data_file["no_root_path"] + '/' + data_file["filename"],
                    },
                },

#            "mdf-citation": ,
#            "mdf-data_contact": {

#                "given_name": ,
#                "family_name": ,

#                "email": ,
#                "institution":,

#                },

#            "mdf-author": ,

#            "mdf-license": ,
#            "mdf-collection": ,
#            "mdf-data_format": ,
#            "mdf-data_type": ,
#            "mdf-year": ,

#            "mdf-mrr":

#            "mdf-processing": ,
#            "mdf-structure":,
            }
        # Pass each individual record to the Validator
        result = dataset_validator.write_record(record_metadata)

        # Check if the Validator accepted the record, and print a message if it didn't
        # If the Validator returns "success" == True, the record was written successfully
        if result["success"] is not True:
            print("Error:", result["message"])

    # You're done!
    if verbose:
        print("Total errors: " + str(errors))
        print("Finished converting")

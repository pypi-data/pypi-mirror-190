from typing import Union
import json
from zipfile import ZipFile
from pathlib import Path
import pandas as pd
import os
from glob import glob

package_dir = Path(__file__).parent.parent

def bundles_query(path: str) -> pd.DataFrame:
    """
        Takes in a path pointing to .zip, .feather, or directory of FHIR bundles
        adds concept of bundle_index (i.e. where was it in the list) for PMI
        ensures / overwrites 'total'
        Returns Bundles in a DataFrame. 
    """
    filetype = path.split(".")[-1]
    if "synthea_100" in path:
        # dont live this 
        bundles = pd.read_feather("https://storage.googleapis.com/cdn.dqfit.org/cohort_synthea_100_bundles.feather")[0:100]
    elif filetype == "feather":
        bundles = pd.read_feather(path)
    elif filetype == "zip":
        zf = ZipFile(path)
        bundles = [json.load(zf.open(f)) for f in zf.namelist()[1::]]
        bundles = pd.DataFrame(bundles)
    elif os.path.isdir(path):
        
        def _open(bundle_path):
            with open(bundle_path, 'r') as f:
                data = json.loads(f.read())
            if pd.isna(data):
                # handle a null bundle better
                return {}
            else:
                return data
        bundle_paths =  glob(f"{path}/*.json")
        bundles = pd.DataFrame([_open(p) for p in bundle_paths])
        bundles = bundles.dropna(subset=['resourceType'])
        # todo # handle a null bundle better

        
    bundles = bundles.reset_index().rename(columns={'index':'bundle_index'})
    bundles['total'] = bundles['entry'].apply(lambda x: len(x))
    assert("bundle_index" in bundles.columns)
    return bundles



def valueset_query(oid: str) -> pd.DataFrame:
    """
        Query OID from package data
    """
    def _get_vs(oid: str) -> dict:
        vs_path = f"{package_dir}/data/valuesets/{oid}.json"
        with open(vs_path, "r") as f:
            vs = json.load(f)
        return vs

    return pd.DataFrame([_get_vs(oid)])

def ig_struct_query(
    structs_dir=f"{package_dir}/data/structs", resource_types=[], must_support = False
) -> pd.DataFrame:
    """
    Point at a directory of fhir struct defitition directory
    And the relavent resource_types
    Returns the path, datatypes 
    """

    def _struct_element_snapshot_query(struct_path: str) -> pd.DataFrame:
        with open(struct_path, "r") as f:
            data = json.load(f)
        df = pd.DataFrame(data["snapshot"]["element"])
        df["_file"] = struct_path
        return df
    
    struct_paths = glob(f"{structs_dir}/*")[1::]
    df = pd.concat(
        _struct_element_snapshot_query(p) for p in struct_paths
    ).reset_index()
    cols = ["path", "min", "max", "type", "mustSupport"]
    if must_support == True:
        df = df[df['mustSupport'] == True]
    df = df[cols]
    df["_resource_type"] = df["path"].apply(lambda x: x.split(".")[0])
    if len(resource_types) > 0:
        df = df.query(f"_resource_type in {resource_types}")
    return df.reset_index(drop=True)




# -*- coding: utf-8 -*-
from rpy2.robjects import r
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages
import json


def load_model(model_path):
    readRDS = robjects.r["readRDS"]
    return readRDS(model_path)


def dump_model(model, path):
    r.saveRDS(model, path)


def load_r_packages(package_list):
    if package_list:
        package_list = f"('{package_list[0]}')" if len(package_list) == 1 else tuple(package_list)
        load_func = f"""function(){{
                        packages <- c{package_list}
                        for (package in packages){{
                            library(package, character.only = TRUE)
                        }}}}"""
        try:
            robjects.r(load_func)()
            print('Successfully loaded packages')
        except Exception as ex:
            print('Error while loading packages: ', ex)


def get_r_packages():
    fetch_package_name = """
        function(){
            packages <- installed.packages()
            df <- data.frame(packages)
            package_name <- sapply(df$Package, as.character)
            return(package_name)
        }
    """
    fetch_version_name = """
        function(){
            packages <- installed.packages()
            df <- data.frame(packages)
            package_version <- sapply(df$Version, as.character)
            return(package_version)
        }
    """
    package_name_r = robjects.r(fetch_package_name)
    version_name_r = robjects.r(fetch_version_name)

    packages = package_name_r()
    versions = version_name_r()
    package_list = list(packages)
    version_list = list(versions)
    return package_list, version_list


def load_r_json(val):
    rjson = rpackages.importr("rjson")
    r_json_val = rjson.fromJSON(json.dumps(val))
    return r_json_val


def check_pre_installed_packages(packages_list, version_list, cran_package_list):
    packages = []
    for i, package in enumerate(packages_list):
        if package not in cran_package_list:
            packages.append({"name": package, "version": version_list[i]})

    if len(packages) == 0:
        packages.append({"name": "devtools", "version": "2.3.2"})
        packages.append({"name": "versions", "version": "0.3"})

    return packages

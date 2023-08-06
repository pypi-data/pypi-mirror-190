# -*- coding: utf-8 -*-
class Notebook:
    url = "http://notebooks-api:5000/notebooks/api"
    git_access_api = "/v1/git-repo/Enabled"
    get_repo_by_id_api = "/v1/git-repo-by-id/"

    
class MosaicVersionControl:
    url = "http://mosaic-version-control:9000/vcs/api"
    git_tag = "/v1/repo/{repo}/{version_id}/gittag?repo_id={repo_id}&branch={branch}"


class Headers:
    x_project_id = "X-Project-Id"
    x_username = "X-Auth-Username"
    x_userid = "X-Auth-Userid"
    x_email_id = "X-Auth-Email"

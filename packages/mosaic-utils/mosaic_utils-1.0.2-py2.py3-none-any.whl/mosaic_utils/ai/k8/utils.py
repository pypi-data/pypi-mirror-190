import os
from uuid import uuid4


def fetching_cpu_value(current_cpu_usage):
    if "n" in current_cpu_usage:
        cpu = int(current_cpu_usage.replace("n", "")) / 1000000000
    elif "m" in current_cpu_usage:
        cpu = int(current_cpu_usage.replace("m", "")) / 1000
    else:
        cpu = int(current_cpu_usage)
    return cpu


def create_job_name(file_path: str, instance_id: int = None) -> str:
    """
    Returns k8s compliant job name from filepath string
    :param file_path:
    :return: jobname str
    :param instance_id: in case instance_id is present add that in name instead of uuid
    :type instance_id: int
    """
    # get file name from file_path
    file_name = os.path.basename(file_path)
    # remove extensions from file name
    revised_notebook_name = os.path.splitext(file_name)[0]

    job_name = "{}-{}-job".format(revised_notebook_name.lower(), instance_id if instance_id else str(uuid4()))
    job_name = "".join(e for e in job_name if e == "-" or e.isalnum())
    if len(job_name) > 55:
        job_name = job_name[-55:]

    # first character of job name should always be alphanumeric
    if not job_name[0].isalnum():
        job_name = "0" + job_name[1:]
    return job_name

# -*- coding: utf-8 -*-
from kubernetes.client import CustomObjectsApi, CoreV1Api
from kubernetes import config
import os
import shutil
import math
from .utils import fetching_cpu_value
import requests
from .constants import GenericConstants
from typing import Dict


if shutil.which("minikube"):
    config.load_kube_config()
elif os.getenv("KUBERNETES_SERVICE_HOST"):
    config.load_incluster_config()
else:
    pass

custom_object = CustomObjectsApi()
core_v1 = CoreV1Api()


def fetch_resource_limitscaling_guarantee(cpu, memory, resource_extra, limitpercentage):

    """limit vertical scaling"""
    if resource_extra == "nvidia":
        return {"nvidia.com/gpu": cpu}
    if resource_extra == "amd":
        return {"amd.com/gpu": cpu}
    limit_cpu_specified = cpu
    if limit_cpu_specified[-1:] == "m":
        limit_cpu = int(limit_cpu_specified[:-1])
    else:
        limit_cpu = int(limit_cpu_specified)
        limit_cpu = limit_cpu * 1000
    limitpercentage = int(limitpercentage)
    limitcpu_scale = (limit_cpu * (100 + limitpercentage)) / 100
    limitcpu_scale = str(math.trunc(limitcpu_scale))
    limitcpu_scale = limitcpu_scale + "m"
    limit_memory_specified = memory
    limit_memory = limit_memory_specified[:-2]
    if limit_memory_specified[-2:] == "Gi":
        limit_memory = int(limit_memory)
        limit_memory = limit_memory * 1000
    elif limit_memory_specified[-2:] == "Mi":
        limit_memory = int(limit_memory)
    limit_unit = "Mi"
    limitmemory_scale = str(math.trunc((limit_memory * (100 + limitpercentage)) / 100))
    limitmemory_scale = limitmemory_scale + limit_unit
    return {"cpu": limitcpu_scale, "memory": limitmemory_scale}


def fetch_pod_metrics(pod_name, namespace, user_name):
    pod_metrics = {}

    resp = custom_object.get_namespaced_custom_object(
        "metrics.k8s.io", "v1beta1", namespace, "pods", pod_name
    )
    status = core_v1.read_namespaced_pod_status(namespace=namespace, name=pod_name)
    pod_status = status.status.phase
    pod_start_time = status.status.start_time

    for container in resp["containers"]:
        current_cpu_usage = container["usage"]["cpu"]
        current_memory_usage = container["usage"]["memory"]

        for container_resource in status.spec.containers:
            if container_resource.name == container["name"]:
                pod_container_limits = container_resource.resources.limits
                pod_container_requests = container_resource.resources.requests

                # Calculating CPU percentages

                # fetching cpu value
                cpu = fetching_cpu_value(current_cpu_usage)

                if "m" in pod_container_limits["cpu"]:
                    revised_pod_limits = int(
                        pod_container_limits["cpu"].replace("m", "")
                    )
                    core_limit = revised_pod_limits / 1000
                else:
                    core_limit = int(pod_container_limits["cpu"])

                core_usage_percentage = (cpu * 100) / core_limit

                # Converting memory usage from KB's to MB's
                memory_usage = current_memory_usage.replace("Ki", "")
                memory_usage_mb = int(memory_usage) / 1024

                data = {
                    container_resource.name: {
                        "cpu_cores_used": str(cpu),
                        "memory": str(memory_usage_mb),
                        "pod_status": pod_status,
                        "limits": pod_container_limits,
                        "requests": pod_container_requests,
                        "cpu_percent_used": str(core_usage_percentage),
                        "created_by": user_name,
                        "pod_start_time": pod_start_time,
                    }
                }
                pod_metrics.update(data)

    return pod_metrics


def volume_count(project_id, username):
    url = f"http://mosaic-console-backend/mosaic-console-backend/secured/api/pvc/project/{project_id}"
    url2 = f"http://mosaic-console-backend/mosaic-console-backend/secured/api/pvc/project/all"
    volume = []
    headers = {"X-Auth-Username": username}
    for item in [url, url2]:
        response = requests.get(item, headers=headers)
        response = response.json()
        if response:
            for x in range(len(response)):
                desc = {
                    "name": response[x]["pvcName"],
                    "persistentVolumeClaim": {"claimName": response[x]["pvcName"]},
                }
                volume.append(desc)
    return volume

def volume_custom(project_id, pvc_name):
    volume = []
    desc = {
        "name": project_id,
        "persistentVolumeClaim": {"claimName": pvc_name},
    }
    volume.append(desc)
    return volume

def volume_custom_mount(project_id=None, minio_bucket=None, resource_quota_full=None):
    volume = []
    desc = {
        "name": project_id,
        "mountPath": "/data",
        "subPath": f"{minio_bucket}/{project_id}/{project_id}-Data"
    }
    if resource_quota_full:
        desc["readOnly"]=True
    volume.append(desc)
    return volume

def volume_mount_count(project_id, username):
    url = f"http://mosaic-console-backend/mosaic-console-backend/secured/api/pvc/project/{project_id}"
    url2 = f"http://mosaic-console-backend/mosaic-console-backend/secured/api/pvc/project/all"
    volume = []
    headers = {"X-Auth-Username": username}
    for item in [url, url2]:
        response = requests.get(item, headers=headers)
        response = response.json()
        if response:
            for x in range(len(response)):
                desc = {
                    "name": response[x]["pvcName"],
                    "mountPath": response[x]["mountpath"],
                }
                volume.append(desc)
    return volume


def attach_default_volume(project_id=None, shared_volumes=None, storage_class=None):
    """
    This method is used to attach default volume mount to the spawned containers
    :return:
    """
    return {
        "type": storage_class,
        "path": shared_volumes
        + GenericConstants.project_data_dir.format(project_id, project_id),
        "name": project_id,
    }


def attach_snapshot_volume(
    project_id=None, shared_volumes=None, storage_class=None, text=None, snap=None
):
    """
    This method is used to attach default volume mount to the spawned containers
    :return:
    """
    if snap == GenericConstants.default:
        return {
            "type": storage_class,
            "path": shared_volumes
            + GenericConstants.all_snapshot_data.format(project_id, project_id),
            "name": text,
        }
    return {
        "type": storage_class,
        "path": shared_volumes
        + GenericConstants.snapshot_data_fir.format(project_id, project_id, snap),
        "name": text,
    }


def attach_default_volume_mount(project_id=None, resource_quota_full=None):
    """
    This method is used to attach default volume mount to the spawned containers
    :return:
    """
    if resource_quota_full:
        return {"name": project_id, "mountPath": "/data", "readOnly": True}
    return {"name": project_id, "mountPath": "/data"}


def attach_snapshot_volume_mount(project_id=None, snapshot_type=None, snapshot_id=None, minio_bucket=None, resource_quota_full=None):
    """
    This method is used to attach default volume mount to the spawned containers
    :return:
    """
    if snapshot_type == GenericConstants.default:
        return {"name": project_id, "mountPath": "/input", "subPath": f"{minio_bucket}/{project_id}/{project_id}-Snapshot/{snapshot_id}", "readOnly": True}
    if resource_quota_full:
        return {"name": project_id, "mountPath": "/output", "subPath": f"{minio_bucket}/{project_id}/{project_id}-Snapshot/{snapshot_id}","readOnly": True}
    return {"name": project_id, "mountPath": "/output", "subPath": f"{minio_bucket}/{project_id}/{project_id}-Snapshot/{snapshot_id}"}


def fetch_resource_request_limit(
    requested_cpu: str,
    requested_memory: str,
    resource_percent: int,
    resource_extra: str = None,
) -> Dict:
    """
    Limits resource request to resource_percent of the requested resource
    :param requested_cpu: Value of requested cpu by user. ex: cpu: "100m", "1"
    :param requested_memory:  Value of requested memory by user. ex: cpu: "256Mi", "2Gi"
    :param resource_percent: percent value from config-map
    :param resource_extra: GPU if present, else None
    :return: dict of request cpu and memory
    """

    resources_mapping = {
        "nvidia": {"nvidia.com/gpu": requested_cpu},
        "amd": {"amd.com/gpu": requested_cpu},
    }
    units = {"m": "m", "Gi": "Gi", "Mi": "Mi"}
    resource_percentage = int(resource_percent)
    request_memory = int(requested_memory[:-2])

    if resource_extra in resources_mapping.keys():
        return resources_mapping[resource_extra]

    if requested_cpu[-1:] == units["m"]:
        requested_cpu = int(requested_cpu[:-1])
    else:
        requested_cpu = int(requested_cpu) * 1000
    requested_cpu = str(math.trunc((requested_cpu * resource_percentage) / 100))
    requested_cpu += units["m"]

    if requested_memory[-2:] == units["Gi"]:
        request_memory = request_memory * 1000
    requested_memory = str(math.trunc((request_memory * resource_percentage) / 100))
    requested_memory += units["Mi"]

    return {"cpu": requested_cpu, "memory": requested_memory}

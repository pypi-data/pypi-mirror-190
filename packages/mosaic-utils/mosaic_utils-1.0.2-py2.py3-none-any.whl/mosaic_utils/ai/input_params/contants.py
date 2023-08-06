# -*- coding: utf-8 -*-


class InputParamPath:
    """
    Define url path for different parameters
    """

    notebook = "/inputParameter/getInputParameterListForReferenceIdAndReferenceType/referenceId={notebook_id}/inputReferenceType=NOTEBOOK"

    project = "/inputParameter/getInputParameterListForProjectId/projectId={project_id}"

    user = "/inputParameter/getInputParameterListForUserName/"

    model = "/inputParameter/getInputParameterListForReferenceIdAndReferenceType/referenceId={version_id}/inputReferenceType=MODEL"

    input_params_path = "/inputParameter/getInputParameterValuesForReferenceIdAndInputReferenceType/referenceId={reference_id}/inputReferenceType={inputReferenceType}"


class InputParamReferenceType:

    ref_type_model = "MODEL"
    ref_type_notebook = "NOTEBOOK"
    ref_type_project = "PROJECT"
    ref_type_user = "USER"

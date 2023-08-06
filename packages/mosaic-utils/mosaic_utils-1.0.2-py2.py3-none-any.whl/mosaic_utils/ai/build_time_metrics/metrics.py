# -*- coding: utf-8 -*-
import json
import numpy as np
import pandas as pd
import requests
import yaml
from sklearn import metrics
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    fbeta_score,
    log_loss,
    matthews_corrcoef,
    precision_score,
    recall_score,
    roc_curve,
    zero_one_loss,
    explained_variance_score,
    mean_absolute_error,
    mean_squared_error,
    mean_squared_log_error,
    r2_score,
    roc_auc_score,
)

from .utils import (
    get_headers,
    get_model_type_handler,
    try_or,
    get_array_type_handler,
    get_pred_and_true_values,
    update_progress,
)
from .constants import MosaicAI, MLModelMetricsV1


def update_metrics(pipeline_id, metrics, tag):
    payload = {"metric_value": json.dumps(metrics)}
    url = MosaicAI.server + MLModelMetricsV1.u.format(pipeline_id=pipeline_id, tag=tag)
    response = requests.put(url, json=payload, headers=get_headers())
    response.raise_for_status()


def get_estimator_obj(model_obj):
    if hasattr(model_obj, "estimators_"):
        try:
            model_estimator = model_obj.estimators_[0][0]
        except:
            model_estimator = model_obj.estimators_[0]
        return model_estimator


def metrics_stats(
    pipeline_id,
    ml_model_id,
    version_id,
    y_true,
    y_pred,
    prob,
    model_type,
    model_summary,
    model_obj,
    labels,
    features,
    original_features,
    encoded_columns,
):
    type_handler = get_model_type_handler(model_type)
    array_handler = get_array_type_handler(y_true, y_pred)
    if array_handler == "df":
        y_true, y_pred = get_pred_and_true_values(y_true, y_pred)
    all_matrix = type_handler(
        pipeline_id,
        ml_model_id,
        version_id,
        y_true,
        y_pred,
        prob,
        model_summary,
        model_type,
        model_obj,
        labels,
        features,
        original_features,
        encoded_columns,
    )
    return all_matrix


node_sum = 0


def tree_generator(
    clf, features, labels, original_features, node_index=0, side=0, prev_index=0
):
    global node_sum
    class_names = labels
    if node_sum <= 5000000:
        node = {}
        if clf.tree_.children_left[node_index] == -1:  # indicates leaf
            count_labels = zip(clf.tree_.value[node_index, 0], labels)
            node["pred"] = ", ".join(
                ("{} of {}".format(int(count), label) for count, label in count_labels)
            )

            node["side"] = "left" if side == "l" else "right"
            feature = features[clf.tree_.feature[prev_index]]
            threshold = clf.tree_.threshold[prev_index]

            if node_index == 0:
                node["name"] = "Root >"
            elif ("_-_" in feature) and (feature not in original_features):

                node["name"] = (
                    "{} = {}".format(feature.split("_-_")[0], feature.split("_-_")[1])
                    if side == "r"
                    else "{} != {}".format(
                        feature.split("_-_")[0], feature.split("_-_")[1]
                    )
                )
                node["type"] = "categorical"
            else:
                node["name"] = (
                    "{} > {}".format(feature, round(threshold, 2))
                    if side == "r"
                    else "{} <= {}".format(feature, round(threshold, 2))
                )
                node["type"] = "numerical"

            left_index = clf.tree_.children_left[node_index]
            right_index = clf.tree_.children_right[node_index]

            if clf.tree_.n_classes[0] != 1 and clf.tree_.n_outputs == 1:
                node["value"] = str(
                    class_names[np.argmax(clf.tree_.value[node_index, 0])]
                )
            else:
                node["value"] = sum(clf.tree_.value[node_index, 0])
        else:

            count_labels = zip(clf.tree_.value[node_index, 0], labels)
            node["pred"] = ", ".join(
                ("{} of {}".format(int(count), label) for count, label in count_labels)
            )

            node["side"] = "left" if side == "l" else "right"
            feature = features[clf.tree_.feature[prev_index]]
            threshold = clf.tree_.threshold[prev_index]

            if node_index == 0:
                node["name"] = "Root >"
            elif ("_-_" in feature) and (feature not in original_features):

                node["name"] = (
                    "{} = {}".format(feature.split("_-_")[0], feature.split("_-_")[1])
                    if side == "r"
                    else "{} != {}".format(
                        feature.split("_-_")[0], feature.split("_-_")[1]
                    )
                )
                node["type"] = "categorical"
            else:
                node["name"] = (
                    "{} > {}".format(feature, round(threshold, 2))
                    if side == "r"
                    else "{} <= {}".format(feature, round(threshold, 2))
                )
                node["type"] = "numerical"

            left_index = clf.tree_.children_left[node_index]
            right_index = clf.tree_.children_right[node_index]

            if clf.tree_.n_classes[0] != 1 and clf.tree_.n_outputs == 1:
                node["value"] = str(
                    class_names[np.argmax(clf.tree_.value[node_index, 0])]
                )
            else:
                node["value"] = sum(clf.tree_.value[node_index, 0])
            node_length = len(str(node))
            node_sum += node_length
            node["children"] = [
                tree_generator(
                    clf,
                    features,
                    labels,
                    original_features,
                    right_index,
                    "r",
                    node_index,
                ),
                tree_generator(
                    clf,
                    features,
                    labels,
                    original_features,
                    left_index,
                    "l",
                    node_index,
                ),
            ]
        return node


class MetricsBase:
    def __init__(
        self,
        pipeline_id,
        ml_model_id,
        version_id,
        y_true,
        y_pred,
        prob,
        model_info,
        model_type,
        model_obj,
        labels,
        features,
        original_features,
        encoded_columns,
    ):
        self.pipeline_id = pipeline_id
        self.ml_model_id = ml_model_id
        self.version_id = version_id
        self.y_true = y_true
        self.y_pred = y_pred
        self.prob = prob
        self.model_info = model_info
        self.model_type = model_type
        self.model_obj = model_obj
        self.labels = labels
        self.features = features
        self.original_features = original_features
        self.encoded_columns = encoded_columns
        self.progress_counter = 1
        self.progress_base_value = 12 if model_type == "classification" else 10

    def db_call(self, summary, tag):
        """
        Method for database operation

        Returns:
            json
        """
        if self.pipeline_id:
            payload = {
                "pipeline_id": self.pipeline_id,
                "metric_value": summary,
                "tag": tag,
            }
        else:
            payload = {
                "ml_model_id": self.ml_model_id,
                "version_id": self.version_id,
                "metric_value": summary,
                "tag": tag,
            }
        url = MosaicAI.server + MLModelMetricsV1.lc.format(version_id=self.version_id)
        response = requests.post(url, json=payload, headers=get_headers())
        response.raise_for_status()
        update_progress(self.progress_counter / self.progress_base_value)
        self.progress_counter += 1
        return response.json()

    def model_summary(self):
        summary_dict = {
            k: self.model_info[k] for k in list(self.model_info.keys())[:11]
        }
        model_dict = {"tag": "model_summary", "model_metric_value": summary_dict}
        update_progress(self.progress_counter / self.progress_base_value)
        self.progress_counter += 1
        return str(json.dumps(model_dict))

    def decision_tree(self):
        try:
            d_tree = tree_generator(
                self.model_obj,
                self.features,
                [self.labels, np.unique(self.y_pred)][self.labels is None],
                self.original_features,
            )
        except:
            try:
                d_tree = tree_generator(
                    get_estimator_obj(self.model_obj),
                    self.features,
                    [self.labels, np.unique(self.y_pred)][self.labels is None],
                    self.original_features,
                )
            except:
                d_tree = None
        decision_tree = json.dumps(d_tree).replace(", null", "").replace("null", "")
        model_metric_value = json.loads(decision_tree) if decision_tree else None
        decision_tree_dict = {
            "tag": "decision_tree",
            "model_metric_value": model_metric_value,
        }
        update_progress(self.progress_counter / self.progress_base_value)
        self.progress_counter += 1
        return str(json.dumps(decision_tree_dict))

    def cal_feature_importance(self):
        """
        Method to calculate variable importance

        Returns:
            String
        """
        try:
            index = self.encoded_columns if self.encoded_columns else self.features

            feature_imp = pd.Series(self.model_obj.feature_importances_, index=index)
            imp_list = []
            for index, value in feature_imp.items():
                d = {"column_name": index, "importance": value}
                imp_list.append(d.copy())
        except Exception:
            imp_list = None
        feature_importance_dict = {
            "tag": "feature_importance",
            "model_metric_value": imp_list,
        }
        update_progress(self.progress_counter / self.progress_base_value)
        self.progress_counter += 1
        return str(json.dumps(feature_importance_dict))


class Classification(MetricsBase):
    def __init__(
        self,
        pipeline_id,
        ml_model_id,
        version_id,
        y_true,
        y_pred,
        prob,
        model_info,
        model_type,
        model_obj,
        labels,
        features,
        original_features,
        encoded_columns,
    ):
        super().__init__(
            pipeline_id,
            ml_model_id,
            version_id,
            y_true,
            y_pred,
            prob,
            model_info,
            model_type,
            model_obj,
            labels,
            features,
            original_features,
            encoded_columns,
        )
        self.all_metrics()

    def all_metrics(self):
        """
        Calculate all metrics value to plot graph

        Returns:
            List
        """
        all_summary = {
            self.model_summary(),
            self.confusion_metrics(),
            self.decision_tree(),
            self.cal_roc_auc(),
            self.detailed_matrix(),
            self.cal_feature_importance(),
        }
        for summary in all_summary:
            tag = json.loads(summary)
            self.db_call(json.dumps(tag["model_metric_value"]), tag["tag"])
            update_progress(self.progress_counter / self.progress_base_value)
            self.progress_counter += 1
        return all_summary

    def confusion_metrics(self):
        """
        Method to return confusion matrix string

        Returns:
            String
        """
        try:
            dlist = []
            conf_matrix = confusion_matrix(self.y_true, self.y_pred)
            conf_list = conf_matrix.tolist()
            for idx, item in enumerate(conf_list):
                for index, val in enumerate(item):
                    d = {
                        "column_1_counter": idx,
                        "column_2_counter": index,
                        "prediction": val,
                        "column_1": idx,
                        "column_2": index,
                    }
                    dlist.append(d.copy())
        except Exception as ex:
            dlist = None
        conf_dict = {"tag": "confusion_matrix", "model_metric_value": dlist}
        update_progress(self.progress_counter / self.progress_base_value)
        self.progress_counter += 1
        return str(json.dumps(conf_dict))

    def detailed_matrix(self):
        """
        Method to calculate detailed matrix parameters

        Returns:
            String
        """
        accuracy_score_value = try_or(lambda: accuracy_score(self.y_true, self.y_pred))
        balanced_accuracy_score_value = try_or(
            lambda: metrics.balanced_accuracy_score(self.y_true, self.y_pred)
        )
        matthews_corrcoef_value = try_or(
            lambda: matthews_corrcoef(self.y_true, self.y_pred)
        )
        f1_score_value = try_or(
            lambda: f1_score(
                self.y_true,
                self.y_pred,
                average="weighted",
                labels=np.unique(self.y_pred),
            )
        )
        fbeta_score_value = try_or(
            lambda: fbeta_score(
                self.y_true,
                self.y_pred,
                average="weighted",
                beta=0.5,
                labels=np.unique(self.y_pred),
            )
        )
        precision_score_value = try_or(
            lambda: precision_score(
                self.y_true,
                self.y_pred,
                average="weighted",
                labels=np.unique(self.y_pred),
            )
        )
        recall_score_value = try_or(
            lambda: recall_score(self.y_true, self.y_pred, average="weighted")
        )
        zero_one_loss_value = try_or(lambda: zero_one_loss(self.y_true, self.y_pred))
        average_precision_score_value = try_or(
            lambda: average_precision_score(self.y_true, self.y_pred, pos_label=0)
        )
        log_loss_value = try_or(lambda: log_loss(self.y_true, self.prob))
        beier_score_loss_value = try_or(
            lambda: brier_score_loss(self.y_true, self.y_pred)
        )

        value_dict = {
            "Accuracy Score": accuracy_score_value,
            "Average Precision Score": average_precision_score_value,
            "Balanced Accuracy Score": balanced_accuracy_score_value,
            "Brier Score Loss": beier_score_loss_value,
            "Matthews Correlation Coefficient": matthews_corrcoef_value,
            "F1 Score": f1_score_value,
            "F-beta Score": fbeta_score_value,
            "Log Loss": log_loss_value,
            "Precision Score": precision_score_value,
            "Recall Score": recall_score_value,
            "Zero One Loss": zero_one_loss_value,
        }
        detailed_dict = {"tag": "detailed_matrix", "model_metric_value": value_dict}
        update_progress(self.progress_counter / self.progress_base_value)
        self.progress_counter += 1
        return str(json.dumps(detailed_dict))

    def cal_roc_auc(self):
        """
        Method to calculate roc auc curve parameters

        Returns:
            String
        """
        try:
            roc_auc = roc_auc_score(self.y_true, self.prob, average="macro")
            fpr, tpr, thresholds = roc_curve(self.y_true, self.prob)
            fpr = fpr.tolist()
            tpr = tpr.tolist()
            roc_auc_value = {"fpr": fpr, "tpr": tpr, "data": roc_auc}
        except Exception as ex:
            roc_auc_value = None
        roc_auc_dict = {"tag": "roc_auc", "model_metric_value": roc_auc_value}
        update_progress(self.progress_counter / self.progress_base_value)
        self.progress_counter += 1
        return str(json.dumps(roc_auc_dict))


class Regression(MetricsBase):
    def __init__(
        self,
        pipeline_id,
        ml_model_id,
        version_id,
        y_true,
        y_pred,
        prob,
        model_info,
        model_type,
        model_obj,
        labels,
        features,
        original_features,
        encoded_columns,
    ):
        super().__init__(
            pipeline_id,
            ml_model_id,
            version_id,
            y_true,
            y_pred,
            prob,
            model_info,
            model_type,
            model_obj,
            labels,
            features,
            original_features,
            encoded_columns,
        )
        self.all_matrix()

    def all_matrix(self):
        """
        Calculate all metrics value to plot graph

        Returns:
            List
        """
        all_summary = (
            self.model_summary(),
            self.cal_scatter_plot(get_array_type_handler(self.y_true, self.y_pred)),
            self.detailed_matrix(),
            self.decision_tree(),
            self.cal_feature_importance(),
        )
        for summary in all_summary:
            tag = yaml.safe_load(summary)
            self.db_call(json.dumps(tag["model_metric_value"]), tag["tag"])
            update_progress(self.progress_counter / self.progress_base_value)
            self.progress_counter += 1
        return all_summary

    def cal_scatter_plot(self, array_type):
        """
        Method to calculate parameters required for scatter plot
        Args:

        Returns:
            String
        """
        if not array_type == "list":
            y_true = self.y_true.ravel().tolist()
            y_pred = self.y_pred.ravel().tolist()
            list1 = [[f, b] for f, b in zip(y_true, y_pred)]
        else:
            list1 = [[f, b] for f, b in zip(self.y_true, self.y_pred)]
        scatt_dict = {"tag": "scatter_plot", "model_metric_value": list1}
        update_progress(self.progress_counter / self.progress_base_value)
        self.progress_counter += 1
        return str(json.dumps(scatt_dict))

    def mean_absolute_percentage_error(self):
        """
        Method to calculate mean absolute percentage error
        Args:

        Returns:
            String
        """
        y_true, y_pred = np.array(self.y_true), np.array(self.y_pred)
        # handling inifinity value for MAPE
        a = np.abs((y_true - y_pred) / y_true)
        return np.mean(a[np.isinf(a) == False]) * 100

    def detailed_matrix(self):
        """
        Method to calculate detailed matrix parameters
        Args:

        Returns:
            String
        """
        explained_variance_score_value = try_or(
            lambda: explained_variance_score(self.y_true, self.y_pred)
        )
        mean_absolute_error_value = try_or(
            lambda: mean_absolute_error(self.y_true, self.y_pred)
        )
        mean_absolute_percentage_error_value = try_or(
            lambda: self.mean_absolute_percentage_error()
        )
        mean_squared_error_value = try_or(
            lambda: mean_squared_error(self.y_true, self.y_pred)
        )
        rmse_value = try_or(
            lambda: np.sqrt(mean_squared_error(self.y_true, self.y_pred))
        )
        r2_score_value = try_or(lambda: r2_score(self.y_true, self.y_pred))
        root_mean_squared_log_error = try_or(
            lambda: np.sqrt(mean_squared_log_error(self.y_true, self.y_pred))
        )
        value_dict = {
            "Explained Variance Score": explained_variance_score_value,
            "Mean Absolute Error": mean_absolute_error_value,
            "Mean Absolute Percentage Error": mean_absolute_percentage_error_value,
            "Mean Squared Error": mean_squared_error_value,
            "Root Mean Square Error": rmse_value,
            "Root Mean Squared Logarithmic Error": root_mean_squared_log_error,
            "R2 score": r2_score_value,
        }
        dict = {"tag": "detailed_matrix", "model_metric_value": value_dict}
        update_progress(self.progress_counter / self.progress_base_value)
        self.progress_counter += 1
        return str(json.dumps(dict))

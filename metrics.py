# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import copy
import cv2
import joblib
import numpy as np
import skimage.measure as measure
import sklearn.metrics as metrics
import torch


def compute_classification_metrics(
    anomaly_scores,
    ground_truth_labels
):
    """
    Computes classification metrics (AUROC, FPR, TPR).

    Args:
        anomaly_scores: [np.array or list] [N] Anomaly scores.
         Higher indicates higher probability of being an anomaly.
        ground_truth_labels: [np.array or list] [N] Binary labels:
        1 if image is an anomaly, 0 if normal.
    """
    fpr, tpr, thresholds = metrics.roc_curve(ground_truth_labels,
                                             anomaly_scores)
    auroc = metrics.roc_auc_score(ground_truth_labels,
                                  anomaly_scores)

    precision, recall, thresholds = metrics.precision_recall_curve(np.array(ground_truth_labels), np.array(anomaly_scores))
    au_pr = metrics.auc(recall, precision)
    return {'auroc': auroc, 'fpr': fpr, 'tpr': tpr, 'threshold': thresholds, 'au_pr': au_pr}


def compute_localization_metrics(
    predicted_masks,
    ground_truth_masks,
    include_optimal_threshold_rates=False,
):
    """
    Computes pixel-wise statistics (AUROC, FPR, TPR) for anomaly segmentations
    and ground truth segmentation masks.

    Args:
        predicted_masks: [list of np.arrays or np.array] [NxHxW] Contains
                               generated segmentation masks.
        ground_truth_masks: [list of np.arrays or np.array] [NxHxW] Contains
                            predefined ground truth segmentation masks
    """
    pred_mask = copy.deepcopy(predicted_masks)
    gt_mask = copy.deepcopy(ground_truth_masks)
    num = 200
    out = {}

    if pred_mask is None or gt_mask is None:
        for key in out:
            out[key].append(float('nan'))
    else:
        fprs, tprs = [], []
        precisions, f1s = [], []
        gt_mask = np.array(gt_mask, np.uint8)

        t = (gt_mask == 1)
        f = ~t
        n_true = t.sum()
        n_false = f.sum()
        th_min = pred_mask.min() - 1e-8
        th_max = pred_mask.max() + 1e-8
        pred_gt = pred_mask[t]
        th_gt_min = pred_gt.min()
        th_gt_max = pred_gt.max()

        '''
        Using scikit learn to compute pixel au_roc results in a memory error since it tries to store the NxHxW float score values.
        To avoid this, we compute the tp, fp, tn, fn at equally spaced thresholds in the range between min of predicted 
        scores and maximum of predicted scores
        '''
        percents = np.linspace(100, 0, num=num // 2)
        th_gt_per = np.percentile(pred_gt, percents)
        th_unif = np.linspace(th_gt_max, th_gt_min, num=num // 2)
        thresholds = np.concatenate([th_gt_per, th_unif, [th_min, th_max]])
        thresholds = np.flip(np.sort(thresholds))

        if n_true == 0 or n_false == 0:
            raise ValueError("gt_submasks must contains at least one normal and anomaly samples")

        for th in thresholds:
            p = (pred_mask > th).astype(np.uint8)
            p = (p == 1)
            fp = (p & f).sum()
            tp = (p & t).sum()

            fpr = fp / n_false
            tpr = tp / n_true
            if tp + fp > 0:
                prec = tp / (tp + fp)
            else:
                prec = 1.0
            if prec > 0. and tpr > 0.:
                f1 = (2 * prec * tpr) / (prec + tpr)
            else:
                f1 = 0.0
            fprs.append(fpr)
            tprs.append(tpr)
            precisions.append(prec)
            f1s.append(f1)

        roc_auc = metrics.auc(fprs, tprs)
        roc_auc = round(roc_auc, 4)
        pr_auc = metrics.auc(tprs, precisions)
        pr_auc = round(pr_auc, 4)
        out['roc_auc'] = (roc_auc)
        out['pr_auc'] = (pr_auc)
        out['fpr'] = (fprs)
        out['tpr'] = (tprs)
        out['precision'] = (precisions)
        out['f1'] = (f1s)
        out['thresholds'] = (thresholds)

    return out

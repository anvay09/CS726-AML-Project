
import numpy as np

from .utils import is_dag


def threshold_till_dag(B):
    """
    Remove the edges with smallest absolute weight until a DAG is obtained.

    Parameters
    ----------
    B: numpy.ndarray
        [d, d] weighted matrix.

    Return
    ------
    B: numpy.ndarray
        [d, d] weighted matrix of DAG.
    dag_thres: float
        Minimum threshold to obtain DAG.
    """
    if is_dag(B):
        return B, 0

    B = np.copy(B)
    # Get the indices with non-zero weight
    nonzero_indices = np.where(B != 0)
    # Each element in the list is a tuple (weight, j, i)
    weight_indices_ls = list(zip(B[nonzero_indices],
                                 nonzero_indices[0],
                                 nonzero_indices[1]))
    # Sort based on absolute weight
    sorted_weight_indices_ls = sorted(weight_indices_ls, key=lambda tup: abs(tup[0]))

    for weight, j, i in sorted_weight_indices_ls:
        if is_dag(B):
            # A DAG is found
            break

        # Remove edge with smallest absolute weight
        B[j, i] = 0
        dag_thres = abs(weight)

    return B, dag_thres


def postprocess(B, graph_thres=0.3):
    """
    Post-process estimated solution:
        (1) Thresholding.
        (2) Remove the edges with smallest absolute weight until a DAG
            is obtained.

    Parameters
    ----------
    B: numpy.ndarray
        [d, d] weighted matrix.
    graph_thres: float
        Threshold for weighted matrix. Default: 0.3.

    Return
    ------
    B: numpy.ndarray
        [d, d] weighted matrix of DAG.
    """
    B = np.copy(B)
    B[np.abs(B) <= graph_thres] = 0    # Thresholding
    B, _ = threshold_till_dag(B)

    return B


import torch.nn.functional as f
import torch
import numpy as np
from sklearn.linear_model import LinearRegression


def calculate_tau(y_censored):
    """
    Calculate the censoring rate of the observed competing events
    :param y_censored: time to competing events
    :return: tau
    """
    if len(y_censored.index) == 0:
        tau = 10 ** 20  # inf
        return tau
    num, bin_edges = np.histogram(y_censored["time"], bins=30)
    # calculate slope
    y_censored["num"] = num[
        np.clip(np.digitize(y_censored["time"], bin_edges, right=True), a_min=1, a_max=len(num)) - 1]
    # find the slope by regression
    reg = LinearRegression(fit_intercept=False).fit(y_censored["time"].to_frame(), y_censored["num"].to_frame())
    slope = reg.coef_
    tau = 1 / slope
    return float(tau)


def RATIO(y, y_hat):
    """
    RATIO loss implementation, this loss is implemented with the MSE loss, but it can be changed to any other loss function
    :param y: real TTE
    :param y_hat: predicted TTE
    :return: RATIO loss
    """
    # censored = 0
    # uncensored = 1
    loss = 0.
    uncensored_idx = y[:, 0] == 1
    censored_idx = y[:, 0] == 0
    y_cen, y_hat_cen = y[censored_idx], y_hat[censored_idx]
    # calculate tau
    tau = calculate_tau(y_cen)

    y_hat = y_hat.flatten()
    if any(uncensored_idx):
        loss += (f.mse_loss(y[uncensored_idx, 1], y_hat[uncensored_idx]) + f.l1_loss(y[uncensored_idx, 1],
                                                                                     y_hat[uncensored_idx]) + y[
                     uncensored_idx, 1] / tau) * 0.001
    if len(y_cen) == 0:
        if type(loss) == float:
            loss = torch.tensor(0., torch.float32, requires_grad=True)
        return loss

    to_change = y_hat_cen.flatten() < y_cen[:, 1].flatten()
    if any(to_change):
        loss += f.mse_loss(y_cen[to_change, 1], y_hat_cen[to_change]) * 0.5

    not_changed = len(y_cen) - sum(to_change)

    if (len(y_hat) - not_changed) != 0:
        loss = (loss * len(y_hat)) / (len(y_hat) - not_changed)
    else:
        loss = torch.tensor(loss, dtype=torch.float32, requires_grad=True)
    return loss

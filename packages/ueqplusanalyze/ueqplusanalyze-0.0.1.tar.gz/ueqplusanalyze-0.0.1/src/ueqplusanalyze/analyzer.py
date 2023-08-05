"""
The copied algorithms to analyze UEQ+ Data
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# ------- DATA_IMPORT -------

def read_in_ueq_observed_data(file_name):
    """
    Reads in data from a file_path

    :param file_name: file path to csv file
    :return: data frame with ueq data
    """

    dataframe = pd.read_csv(file_name, delimiter=',', quotechar='"', encoding='utf-8')
    return dataframe


# ------- DATA_ITEMS -------

def get_observed_item_ratings(filtered_df, ueq):
    """
    Returns the observed item ratings for each item.
    """
    multilevel_column = []
    results = []
    for scale in ueq.keys():
        if scale != 'importance_of_scales':
            scale_df = filtered_df[ueq[scale]]
            for column in scale_df.columns:
                multilevel_column.append((scale, column))
            results.append(pd.DataFrame(scale_df))

    df_merged = pd.concat(results, join='outer', axis=1)
    col_list = pd.MultiIndex.from_tuples(multilevel_column)
    df_merged.columns = col_list
    return df_merged


def scale_means_per_participant(filtered_df, ueq):
    """
    Calculates the mean values for each scale.
    """
    scales = []
    results = []
    for scale in ueq.keys():
        if scale != 'importance_of_scales':
            scales.append(scale)
            scale_df = filtered_df[ueq[scale]]
            scale_means = scale_df.mean(axis=1)
            results.append(scale_means)

    df = pd.DataFrame(results, scales).transpose()
    return df


# ------- DATA_IMPORTANCE -------


def get_observed_importance_ratings(filtered_df, ueq):
    """
    Returns the observed importance ratings for each scale.
    """
    importance_of_scales = filtered_df[ueq['importance_of_scales']]
    scales = []
    for scale in ueq.keys():
        if scale != 'importance_of_scales':
            scales.append(scale)

    importance_of_scales.columns = scales
    return importance_of_scales


def relative_importance_ratings(filtered_df, ueq):
    """
    Calculates the relative importance ratings for each scale.
    """
    importance_of_scales = get_observed_importance_ratings(filtered_df, ueq)
    relative_importance_ratings = importance_of_scales.apply(lambda x: x / x.sum(), axis=1)
    return relative_importance_ratings.round(2)


# ------- MEANS -------


def mean_and_confidence_intervall_per_scale(filtered_df, ueq):
    """
    Here means for the scales (mean over all items in a scale), standard deviations and confidence intervalls are calculated.
    """
    scales = []
    results = []
    for scale in ueq.keys():
        if scale != 'importance_of_scales':
            scale_df = filtered_df[ueq[scale]]
            all_items_in_a_scale = scale_df.to_numpy().flatten()

            (
                mean,
                var,
                std,
                n,
                confidence,
                confidence_intervall,
            ) = helper_mean_and_confidence_interval(all_items_in_a_scale, scale_df)

            scales.append(scale)
            results.append(
                {
                    'mean': mean,
                    'variance': var,
                    'std_dev': std,
                    'n': n,
                    'confidence': confidence,
                    'confidence_interval': confidence_intervall,
                }
            )

    df = pd.DataFrame(results, scales)
    return df.round(2)


def mean_importance_ratings(filtered_df, ueq):
    """
    Calculates the mean importance ratings for each scale.
    """
    importance_of_scales = filtered_df[ueq['importance_of_scales']]

    mean, var, std, n, confidence, confidence_intervall = helper_mean_and_confidence_interval(
        importance_of_scales.to_numpy(), importance_of_scales
    )

    scales = []
    for scale in ueq.keys():
        if scale != 'importance_of_scales':
            scales.append(scale)

    n = [n] * (len(scales))

    results = []
    for i in range(len(scales)):
        results.append(
            [
                mean[i],
                var[i],
                std[i],
                n[i],
                confidence[i],
                [confidence_intervall[0][i], confidence_intervall[1][i]],
            ]
        )

    df = pd.DataFrame(
        results,
        columns=['mean', 'variance', 'std_dev', 'n', 'confidence', 'confidence_interval'],
        index=scales,
    )

    return df.round(2)


def mean_and_confidence_interval_per_item(filtered_df, ueq):
    """
    Here means, standard deviations and confidence intervalls for the individual items are calculated.
    """
    scales = []
    results = []
    for scale in ueq.keys():
        if scale != 'importance_of_scales':
            scale_df = filtered_df[ueq[scale]]
            for item in scale_df.columns:
                item_df = scale_df[item]

                (
                    mean,
                    var,
                    std,
                    n,
                    confidence,
                    confidence_intervall,
                ) = helper_mean_and_confidence_interval(item_df, scale_df, axis=0)

                scales.append((scale, item))
                results.append(
                    {
                        'mean': mean,
                        'variance': var,
                        'std_dev': std,
                        'n': n,
                        'confidence': confidence,
                        'confidence_interval': confidence_intervall,
                    }
                )

    col_list = pd.MultiIndex.from_tuples(scales)
    df = pd.DataFrame(results, col_list)
    return df.round(2)


def helper_mean_and_confidence_interval(data, scale, axis=0):
    """
    Here means for the scales (mean over all items in a scale), standard deviations and confidence intervalls are calculated.
    The mean values are transformed from a 1 to 7 range to a -3 to +3 range to be compatible with the reporting format of the original UEQ.
    """
    mean = data.mean(axis=axis) - 4
    var = data.var(axis=axis, ddof=1)
    std = data.std(axis=axis, ddof=0)
    n = len(scale)
    confidence = 1.96 * (std / np.sqrt(n))
    confidence_intervall = [(mean - confidence).round(2), (mean + confidence).round(2)]
    return mean, var, std, n, confidence, confidence_intervall


# ------- CONSISTENCY -------


def scale_consistency(filtered_df, ueq):
    """
    Indicator for the consistency of the scales by calculating the alpha coefficient between a scales columns.
    """
    scales = []
    results = []
    for scale in ueq.keys():
        if scale != 'importance_of_scales':
            scales.append(scale)
            scale_df = filtered_df[ueq[scale]]

            corr_l1_l2 = np.corrcoef(scale_df[scale_df.columns[0]], scale_df[scale_df.columns[1]])[
                0, 1
            ]
            corr_l1_l3 = np.corrcoef(scale_df[scale_df.columns[0]], scale_df[scale_df.columns[2]])[
                0, 1
            ]
            corr_l1_l4 = np.corrcoef(scale_df[scale_df.columns[0]], scale_df[scale_df.columns[3]])[
                0, 1
            ]
            corr_l2_l3 = np.corrcoef(scale_df[scale_df.columns[1]], scale_df[scale_df.columns[2]])[
                0, 1
            ]
            corr_l2_l4 = np.corrcoef(scale_df[scale_df.columns[1]], scale_df[scale_df.columns[3]])[
                0, 1
            ]
            corr_l3_l4 = np.corrcoef(scale_df[scale_df.columns[2]], scale_df[scale_df.columns[3]])[
                0, 1
            ]

            average_corr = (
                                   corr_l1_l2 + corr_l1_l3 + corr_l1_l4 + corr_l2_l3 + corr_l2_l4 + corr_l3_l4
                           ) / 6

            cronbach_alpha = (4 * average_corr) / (1 + 3 * average_corr)

            results.append(
                [
                    corr_l1_l2,
                    corr_l1_l3,
                    corr_l1_l4,
                    corr_l2_l3,
                    corr_l2_l4,
                    corr_l3_l4,
                    average_corr,
                    cronbach_alpha,
                ]
            )

    df = pd.DataFrame(
        results,
        columns=[
            'corr(l1,l2)',
            'corr(l1,l3)',
            'corr(l1,l4)',
            'corr(l2,l3)',
            'corr(l2,l4)',
            'corr(l3,l4)',
            'average_corr',
            'cronbach_alpha',
        ],
        index=scales,
    )
    return df.round(2)


# ------- KPI -------


def calculation_of_a_kpi(filtered_df, ueq):
    """
    Calculation of a KPI.
    """
    importance_of_scales = get_observed_importance_ratings(filtered_df, ueq)
    relative_importance_ratings = importance_of_scales.apply(lambda x: x / x.sum(), axis=1)

    scales = []
    results = []
    for scale in ueq.keys():
        if scale != 'importance_of_scales':
            scales.append(scale)
            scale_df = filtered_df[ueq[scale]]
            kpi_per_scale_per_participant = (
                    scale_df.mean(axis=1) * relative_importance_ratings[scale]
            )
            results.append(kpi_per_scale_per_participant)

    df = pd.DataFrame(results, scales).transpose()
    kpi_per_participant = df.sum(axis=1) - 4
    df_with_kpi = pd.concat([df, kpi_per_participant], axis=1)
    df_with_kpi.columns = [*df_with_kpi.columns[:-1], 'kpi']
    return (
        df_with_kpi.round(2),
        kpi_per_participant.mean().round(2),
        kpi_per_participant.std(ddof=0).round(2),
    )


# ------- GRAPHICS -------


def plot_scale_means(mean_and_confidence_intervall_per_scale):
    """
    Plot the means of the scales.
    """
    barWidth = 0.3
    bars = mean_and_confidence_intervall_per_scale['mean'].values
    interval_height = []

    for i in range(len(mean_and_confidence_intervall_per_scale['confidence_interval'].values)):
        interval_height.append(
            (
                    mean_and_confidence_intervall_per_scale['confidence_interval'].values[i][1]
                    - mean_and_confidence_intervall_per_scale['confidence_interval'].values[i][0]
            )
            / 2
        )

    x_position = [r + barWidth for r in range(len(bars))]

    plt.axhspan(1, 3.5, facecolor='green', alpha=0.25)
    plt.axhspan(1, -1, facecolor='yellow', alpha=0.25)
    plt.axhspan(-1, -3.5, facecolor='red', alpha=0.25)

    plt.bar(
        x_position,
        bars,
        width=barWidth,
        color='grey',
        yerr=interval_height,
        capsize=7,
    )

    plt.ylim([-3.5, 3.5])

    plt.xticks(
        [r + barWidth for r in range(len(bars))],
        mean_and_confidence_intervall_per_scale.index.values,
        rotation=45,
        ha='right',
    )
    plt.ylabel('scale ratings mean')
    plt.grid(axis='y', alpha=0.25)

    # Show graphic
    return plt.show()


def plot_scale_importance_ratings(mean_importance_ratings):
    """
    Plot the means of the importance rating.
    """
    barWidth = 0.3
    bars = mean_importance_ratings['mean'].values
    interval_height = []

    for i in range(len(mean_importance_ratings['confidence_interval'].values)):
        interval_height.append(
            (
                    mean_importance_ratings['confidence_interval'].values[i][1]
                    - mean_importance_ratings['confidence_interval'].values[i][0]
            )
            / 2
        )

    x_position = [r + barWidth for r in range(len(bars))]

    plt.bar(
        x_position,
        bars,
        width=barWidth,
        yerr=interval_height,
        capsize=7,
    )

    plt.ylim([-3.5, 3.5])

    plt.xticks(
        [r + barWidth for r in range(len(bars))],
        mean_importance_ratings.index.values,
        rotation=45,
        ha='right',
    )
    plt.ylabel('importance ratings mean')
    plt.grid(axis='y', alpha=0.25)

    # Show graphic
    return plt.show()

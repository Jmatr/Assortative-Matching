import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)

df = pd.read_csv('../Zhang_dataset.csv')


def get_table(n, educ1, educ2):
    """
    :param n: Cohort
    :param educ1: High Education Level
    :param educ2: Low Education Level
    :return: 2x2 Table
    """
    df_n = df[df['COHORT'] == n]

    df_a = df_n[(df_n['GENDER'] == 'Male') & (df_n[educ1] == True) & (df_n[f'{educ1}_SP'] == True)]
    df_b = df_n[(df_n['GENDER'] == 'Male') & (df_n[educ1] == True) & (df_n[f'{educ2}_SP'] == True)]
    df_c = df_n[(df_n['GENDER'] == 'Male') & (df_n[educ2] == True) & (df_n[f'{educ1}_SP'] == True)]
    df_d = df_n[(df_n['GENDER'] == 'Male') & (df_n[educ2] == True) & (df_n[f'{educ2}_SP'] == True)]

    arr = np.zeros((2, 2))
    arr[0, 0] = len(df_a)
    arr[0, 1] = len(df_b)
    arr[1, 0] = len(df_c)
    arr[1, 1] = len(df_d)

    print(f'Cohort {n}: {educ1} vs {educ2}')
    print(arr)

    return arr

def get_table_single(n, educ1, educ2):
    """
    :param n: Cohort
    :param educ1: High Education Level
    :param educ2: Low Education Level
    :return: 3x3 Table
    """
    df_n = df[df['COHORT'] == n]

    df_a = df_n[(df_n['GENDER'] == 'Male') & (df_n[educ1] == True) & (df_n[f'{educ1}_SP'] == True)]
    df_b = df_n[(df_n['GENDER'] == 'Male') & (df_n[educ1] == True) & (df_n[f'{educ2}_SP'] == True)]
    df_c = df_n[(df_n['GENDER'] == 'Male') & (df_n[educ1] == True) & (df_n['IsMarried'] == 0)]

    df_d = df_n[(df_n['GENDER'] == 'Male') & (df_n[educ2] == True) & (df_n[f'{educ1}_SP'] == True)]
    df_e = df_n[(df_n['GENDER'] == 'Male') & (df_n[educ2] == True) & (df_n[f'{educ2}_SP'] == True)]
    df_f = df_n[(df_n['GENDER'] == 'Male') & (df_n[educ2] == True) & (df_n['IsMarried'] == 0)]

    df_g = df_n[(df_n['GENDER'] == 'Female') & (df_n[educ1] == True) & (df_n['IsMarried'] == 0)]
    df_h = df_n[(df_n['GENDER'] == 'Female') & (df_n[educ2] == True) & (df_n['IsMarried'] == 0)]

    arr = np.zeros((3, 3))
    arr[0, 0] = len(df_a)
    arr[0, 1] = len(df_b)
    arr[0, 2] = len(df_c)
    arr[1, 0] = len(df_d)
    arr[1, 1] = len(df_e)
    arr[1, 2] = len(df_f)
    arr[2, 0] = len(df_g)
    arr[2, 1] = len(df_h)

    print(f'Cohort {n}: {educ1} vs {educ2}')
    print(arr)

    return arr


def get_NT_index(table):
    a, b, c, d = table[0, 0], table[0, 1], table[1, 0], table[1, 1]
    total_mass = a + b + c + d
    # Normalized Trace (NT)
    if b * c == 0:
        NT = 1 if a + d > 0 else 0
    elif a * d == 0:
        NT = 0
    else:
        NT = (a + d) / total_mass
    return NT


def get_LRH_index(table):
    a, b, c, d = table[0, 0], table[0, 1], table[1, 0], table[1, 1]
    total_mass = a + b + c + d
    LR1 = (a * total_mass) / ((a + b) * (a + c)) if (a + b) > 0 and (a + c) > 0 else 0
    return LR1


def get_LRL_index(table):
    a, b, c, d = table[0, 0], table[0, 1], table[1, 0], table[1, 1]
    total_mass = a + b + c + d
    LR2 = (d * total_mass) / ((d + b) * (d + c)) if (d + b) > 0 and (d + c) > 0 else 0
    return LR2


def get_ALR_index(table):
    a, b, c, d = table[0, 0], table[0, 1], table[1, 0], table[1, 1]
    total_mass = a + b + c + d
    # weight1 = (a + b) * (a + c) / ((a + b) * (a + c) + (d + b) * (d + c))
    # weight2 = (d + b) * (d + c) / ((a + b) * (a + c) + (d + b) * (d + c))
    # ALR = weight1 * get_LRH_index(table) + weight2 * get_LRL_index(table)
    ALR = ((a + d) / total_mass) / ((a + b) / total_mass * (a + c) / total_mass + (d + b) / total_mass * (d + c) / total_mass)
    return ALR


def get_OR_index(table):
    """
    Get odds ratio index of table
    :param table: 2x2 table
    :return: odds ratio
    """
    a, b, c, d = table[0, 0], table[0, 1], table[1, 0], table[1, 1]
    OR = (a * d) / (b * c) if b > 0 and c > 0 else np.inf
    return OR


def get_LOR_index(table):
    """
    Get log odds ratio index of table
    :param table: 2x2 table
    :return: log odds ratio
    """
    LOR = np.log(get_OR_index(table))
    return LOR


def get_Q_index(table):
    """
    Get Yule’s Q, Coefficient of association index of table
    :param table: 2x2 table
    :return: Yule’s Q, Coefficient of association index
    """
    OR = get_OR_index(table)
    Yule_Q = (OR - 1) / (OR + 1) if OR != np.inf else 1
    return Yule_Q


def get_Y_index(table):
    """
    Get Yule’s Y, Coefficient of colligation index of table
    :param table: 2x2 table
    :return: Yule’s Y, Coefficient of colligation index
    """
    OR = get_OR_index(table)
    Yule_Y = (np.sqrt(OR) - 1) / (np.sqrt(OR) + 1) if OR != np.inf else 1
    return Yule_Y


def get_Corr_index(table):
    """
    Get Correlation index of table
    :param table: 2x2 table
    :return: Correlation index
    """
    a, b, c, d = table[0, 0], table[0, 1], table[1, 0], table[1, 1]
    # Correlation (Corr)
    numerator_corr = (a * d) - (b * c)
    denominator_corr = np.sqrt((a + b) * (c + d) * (a + c) * (b + d))
    Corr = numerator_corr / denominator_corr if denominator_corr > 0 else np.nan
    return Corr


def get_Chi_sq_index(table):
    """
    Get Chi square index of table
    :param table: 2x2 table
    :return: Chi square index
    """
    Corr = get_Corr_index(table)
    Spearman = Corr ** 2 if not np.isnan(Corr) else np.nan
    return Spearman


def get_PR_index(table):
    """
    Get Pure-random Normalization index of table
    :param table: 2x2 table
    :return: Pure-random Normalization index
    """
    a, b, c, d = table[0, 0], table[0, 1], table[1, 0], table[1, 1]
    max_bc = max(b, c)
    numerator_pr = (a * d) - (b * c)
    denominator_pr = (max_bc + d) * (a + max_bc)
    PR = numerator_pr / denominator_pr if denominator_pr > 0 else np.nan
    return PR


def get_NT_Single_index(table):
    """
    Get Normalized Trace index of table
    :param table: 2x2 table
    :return: Normalized Trace index
    """
    a, b, c, d, e, f, g, h = table[0, 0], table[0, 1], table[0, 2], table[1, 0], table[1, 1], table[1, 2], table[2, 0], table[2, 1]
    NT_single = (a * 2 + e * 2) / ((a + b + d + e) * 2 + (c + f + g + h))
    # NT_single = (a + e) / (a + b + c + d + e + f + g + h)
    return NT_single


def plot_2x2_tables(years, educ1, educ2):
    """
    Plot 2x2 tables for the given years.

    :param years: List of years for which to generate and plot 2x2 tables.
    :param educ1: High Education Level.
    :param educ2: Low Education Level.
    """
    fig, axes = plt.subplots(1, len(years), figsize=(len(years) * 5, 6))

    if len(years) == 1:
        axes = [axes]  # Ensure `axes` is iterable even for a single year

    for ax, year in zip(axes, years):
        # Generate the 2x2 table for the given year
        table = get_table(year, educ1, educ2)

        # Plot the table as a heatmap
        im = ax.matshow(table, cmap="viridis")

        # Add labels and annotations
        for (i, j), val in np.ndenumerate(table):
            ax.text(j, i, f"{val}", ha="center", va="center", color="white")

        ax.set_title(f"Cohort: {year}")
        ax.set_xticks(range(2))
        ax.set_yticks(range(2))
        ax.set_xticklabels([educ1, educ2])
        ax.set_yticklabels([educ1, educ2])

    # Add a colorbar
    # fig.colorbar(im, ax=axes, orientation="vertical", fraction=0.02, pad=0.04)
    plt.tight_layout()
    plt.show()


cohorts = [1930, 1940, 1950, 1960, 1970, 1980]
educ1 = "CA"
educ2 = "CB"

results = []

# Loop through cohorts and compute indices
for cohort in cohorts:
    table = get_table(cohort, educ1, educ2)
    table_single = get_table_single(cohort, educ1, educ2)
    results.append({
        "Cohort": cohort,
        "NT": get_NT_index(table),
        # "Normalized_NT": get_NT_index(table) / (1 + get_NT_index(table)),
        "OR": get_OR_index(table),
        "LOR": get_LOR_index(table),
        "QOR": get_Q_index(table),
        "YOR": get_Y_index(table),
        "NT_single": get_NT_Single_index(table_single),
        # "Normalized_NT_single": get_NT_Single_index(table_single) / (1 + get_NT_Single_index(table_single)),
        "Agg_LR": get_ALR_index(table),
        # Logistic Transformation
        "Normalized_Agg_LR": get_ALR_index(table) / (1 + get_ALR_index(table)),
        "LRH": get_LRH_index(table),
        # Logistic Transformation
        "Normalized_LRH": get_LRH_index(table) / (1 + get_LRH_index(table)),
        "LRL": get_LRL_index(table),
        # Logistic Transformation
        "Normalized_LRL": get_LRL_index(table) / (1 + get_LRL_index(table)),
    })

# plot_2x2_tables(cohorts, educ1, educ2)

# Convert results to a DataFrame
df_result = pd.DataFrame(results)

# Save to CSV
df_result.to_csv("../cohort_indices.csv", index=False)

# Display the DataFrame
print(df_result)

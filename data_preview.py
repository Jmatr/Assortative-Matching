import pandas as pd
import matplotlib.pyplot as plt

# Load & filter March CPS, married 35–44
pd.set_option('display.max_columns', None)
df = pd.read_csv('cps_00006.csv')
df = df[
    (df['MONTH'] == 3) &
    (df['EDUC'].notna()) & (df['EDUC'] != 999) &
    (df['SPLOC'] > 0) &
    (df['AGE'].between(35, 44))
    ]


# Four‐category education bucketing
def educ_bucket(ed):
    if ed <= 60:
        return 'Less than HS'
    elif 70 <= ed <= 73:
        return 'HS graduate'
    elif 80 <= ed <= 110:
        return 'Some college'
    elif ed >= 111:
        return 'Bachelor+'
    else:
        return pd.NA


df['educ_cat'] = df['EDUC'].apply(educ_bucket)
df['sp_educ_cat'] = df['EDUC_SP'].apply(educ_bucket)
df = df.dropna(subset=['educ_cat', 'sp_educ_cat'])

# Cohort assignment by birth‐year
df['BIRTH_YEAR'] = df['YEAR'] - df['AGE']


def birth_to_cohort(by):
    if 1930 <= by <= 1939: return 1930
    if 1940 <= by <= 1949: return 1940
    if 1950 <= by <= 1959: return 1950
    if 1960 <= by <= 1969: return 1960
    if 1970 <= by <= 1979: return 1970
    if 1980 <= by <= 1989: return 1980
    return pd.NA


df['COHORT'] = df['BIRTH_YEAR'].apply(birth_to_cohort)

# Category ordering
cats = ['Less than HS', 'HS graduate', 'Some college', 'Bachelor+']

# Loop cohorts
for cohort in sorted(df['COHORT'].dropna().unique()):
    sub_m = df[(df['COHORT'] == cohort) & (df['SEX'] == 1)]

    # joint counts matrix
    ct = pd.crosstab(
        sub_m['educ_cat'],
        sub_m['sp_educ_cat']
    ).reindex(index=cats, columns=cats, fill_value=0)

    # normalize so whole table sums to 1
    joint = ct / ct.values.sum()

    # print table
    print(f"\n--- Cohort {cohort} — Male joint distribution ---")
    print(joint.round(3).to_string())

    # plot heatmap
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(joint.values, aspect='auto', vmin=0, vmax=joint.values.max())
    ax.set_xticks(range(len(cats)))
    ax.set_xticklabels(cats, rotation=45, ha='right')
    ax.set_yticks(range(len(cats)))
    ax.set_yticklabels(cats)
    ax.set_title(f'Cohort {cohort} — Male joint P(own, spouse)')
    ax.set_xlabel('Spouse education')
    ax.set_ylabel('Own education')
    for i in range(len(cats)):
        for j in range(len(cats)):
            ax.text(j, i, f"{joint.values[i, j]:.2f}",
                    ha='center', va='center',
                    color='white' if joint.values[i, j] > joint.values.max() / 2 else 'black',
                    fontsize=8)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label='Joint P')
    plt.tight_layout()
    plt.show()

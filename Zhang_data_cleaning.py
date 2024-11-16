import pandas as pd
pd.set_option('display.max_columns', None)

df = pd.read_csv('../cps_dataset.csv')
df['IsMarried'] = df['SPLOC'].apply(lambda x: 1 if x > 0 else 0)
df['GENDER'] = df['SEX'].map({1: 'Male', 2: 'Female'})
df['BIRTH_YEAR'] = df['YEAR'] - df['AGE']

df_clean = df.loc[(df['MONTH'] == 3) & (df['EDUC'].notnull()) & (df['EDUC'] != 999)]
df_clean = df_clean[['YEAR', 'SERIAL', 'BIRTH_YEAR', 'AGE', 'GENDER', 'EDUC', 'AGE_SP', 'EDUC_SP', 'IsMarried']]
df_clean.rename(columns={'SERIAL': 'HOUSEHOLD'}, inplace=True)
df_clean = df_clean[(df_clean['YEAR'].isin([1974, 1984, 1994, 2004, 2014, 2024]))
                      & (df_clean['AGE'].between(35, 44)) & (df_clean['AGE_SP'].between(35, 44) | df_clean['AGE_SP'].isnull())]
df_clean.rename(columns={'YEAR': 'COHORT'}, inplace=True)
year_to_cohort = {1974: 1930, 1984: 1940, 1994: 1950, 2004: 1960, 2014: 1970, 2024: 1980}
df_clean['COHORT'] = df_clean['COHORT'].map(year_to_cohort)

df_clean['HSB'] = df_clean['EDUC'] <= 73
df_clean['CA'] = df_clean['EDUC'] >= 111
df_clean['SC'] = (df_clean['EDUC'] > 73) & (df_clean['EDUC'] < 111)
df_clean['CB'] = df_clean['EDUC'] < 111
df_clean['SCA'] = df_clean['EDUC'] > 73

df_clean['HSB_SP'] = df_clean['EDUC_SP'] <= 73
df_clean['CA_SP'] = df_clean['EDUC_SP'] >= 111
df_clean['SC_SP'] = (df_clean['EDUC_SP'] > 73) & (df_clean['EDUC_SP'] < 111)
df_clean['CB_SP'] = df_clean['EDUC_SP'] < 111
df_clean['SCA_SP'] = df_clean['EDUC_SP'] > 73


def assign_cohort(birth_year):
    if 1930 <= birth_year <= 1939:
        return 1930
    elif 1940 <= birth_year <= 1949:
        return 1940
    elif 1950 <= birth_year <= 1959:
        return 1950
    elif 1960 <= birth_year <= 1969:
        return 1960
    elif 1970 <= birth_year <= 1979:
        return 1970
    else:
        return None


df_clean.to_csv('../Zhang_dataset.csv', header=True, index=False)
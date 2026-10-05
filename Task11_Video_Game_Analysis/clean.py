"""Cleaning pipeline for Video Game Industry Analysis (Task 11)."""
import pandas as pd, numpy as np

RAW = '/home/claude/data/Video_Games_Sales_as_at_22_Dec_2016.csv'
log = []
df = pd.read_csv(RAW)
n0 = len(df); log.append(('Raw rows loaded', n0, ''))

# 1. Column names -> consistent style
df = df.rename(columns={'Name':'Name','Year_of_Release':'Year','NA_Sales':'NA_Sales','EU_Sales':'EU_Sales',
                        'JP_Sales':'JP_Sales','Other_Sales':'Other_Sales','Global_Sales':'Global_Sales'})

# 2. Text hygiene
for c in ['Name','Publisher','Developer','Genre','Platform','Rating']:
    df[c] = df[c].astype('string').str.strip()
log.append(('Name values with stray whitespace trimmed', int((pd.read_csv(RAW).Name.dropna().str.strip()!=pd.read_csv(RAW).Name.dropna()).sum()), 'e.g. trailing spaces in Name / Publisher'))

# 3. Rows with no Name and no Genre are unusable
bad = df['Name'].isna() & df['Genre'].isna()
log.append(('Rows dropped: missing Name AND Genre', int(bad.sum()), 'Both are Genesis 1993 rows, cannot be identified'))
df = df[~bad].copy()

# 4. Invalid release years (dataset snapshot is Dec-2016)
inv = df['Year'] > 2016
log.append(('Invalid Year set to NaN (>2016)', int(inv.sum()), 'Impossible for a Dec-2016 snapshot (2017 / 2020 values)'))
df.loc[inv,'Year'] = np.nan

# 5. Duplicates: same Name + Platform (and compatible Year) = split sales row -> merge, don't lose sales
sales = ['NA_Sales','EU_Sales','JP_Sales','Other_Sales','Global_Sales']
df['_k'] = df['Name'].str.lower() + '|' + df['Platform']
merged = 0; drop_idx = []
for k, g in df[df.duplicated('_k', keep=False)].groupby('_k'):
    yrs = g['Year'].dropna().unique()
    if len(yrs) > 1:      # different years = genuinely different releases (e.g. NFS Most Wanted 2005 vs 2012)
        continue
    keep = g.sort_values('Global_Sales', ascending=False).index[0]
    for c in sales: df.loc[keep, c] = g[c].sum()
    for c in ['Year','Publisher','Developer','Rating']:
        if pd.isna(df.loc[keep, c]) and g[c].notna().any(): df.loc[keep, c] = g[c].dropna().iloc[0]
    drop_idx += [i for i in g.index if i != keep]; merged += 1
df = df.drop(index=drop_idx).drop(columns='_k')
log.append(('Duplicate Name+Platform rows merged (sales summed)', len(drop_idx), f'{merged} games; kept distinct releases with different years'))

# 6. Missing categorical values
mp = df['Publisher'].isna().sum(); df['Publisher'] = df['Publisher'].fillna('Unknown')
log.append(('Missing Publisher -> "Unknown"', int(mp), ''))
md = df['Developer'].isna().sum(); df['Developer'] = df['Developer'].fillna('Unknown')
log.append(('Missing Developer -> "Unknown"', int(md), ''))

# 7. Standardise Publisher spelling variants
pub_map = {'Square Enix':'Square Enix','SquareSoft':'Square Enix','Square':'Square Enix','Square EA':'Square Enix',
           'Sony Computer Entertainment America':'Sony Computer Entertainment',
           'Sony Computer Entertainment Europe':'Sony Computer Entertainment',
           'Sony Oznline Entertainment':'Sony Online Entertainment','Activision Value':'Activision',
           'Codemasters Online':'Codemasters','Ubisoft Annecy':'Ubisoft'}
before = df['Publisher'].nunique()
df['Publisher'] = df['Publisher'].replace(pub_map)
log.append(('Publisher variants consolidated', before - df['Publisher'].nunique(), 'Square/SquareSoft->Square Enix, Sony CE America/Europe->Sony CE, etc.'))

# 8. Rating: legacy K-A == E; RP (rating pending) -> missing
n_ka = (df['Rating']=='K-A').sum(); n_rp = (df['Rating']=='RP').sum()
df['Rating'] = df['Rating'].replace({'K-A':'E'}); df.loc[df['Rating']=='RP','Rating'] = pd.NA
log.append(('Rating: K-A merged into E; RP set to NaN', int(n_ka+n_rp), ''))

# 9. Data types
df['Year'] = df['Year'].astype('Int64')
for c in ['Critic_Count','User_Count']: df[c] = df[c].astype('Int64')
for c in ['Name','Platform','Genre','Publisher','Developer','Rating']: df[c] = df[c].astype('category' if c in ['Platform','Genre','Rating'] else 'string')

# 10. Feature engineering
df['User_Score_100'] = (df['User_Score']*10).round(1)               # same 0-100 scale as critics
df['Score_Gap'] = df['Critic_Score'] - df['User_Score_100']
maker = {'PS':'Sony','PS2':'Sony','PS3':'Sony','PS4':'Sony','PSP':'Sony','PSV':'Sony',
         'NES':'Nintendo','SNES':'Nintendo','N64':'Nintendo','GC':'Nintendo','Wii':'Nintendo','WiiU':'Nintendo',
         'GB':'Nintendo','GBA':'Nintendo','DS':'Nintendo','3DS':'Nintendo',
         'XB':'Microsoft','X360':'Microsoft','XOne':'Microsoft',
         'SAT':'Sega','DC':'Sega','GEN':'Sega','SCD':'Sega','GG':'Sega','PC':'PC'}
df['Platform_Maker'] = df['Platform'].astype(str).map(maker).fillna('Other')
handheld = {'GB','GBA','DS','3DS','PSP','PSV','GG','WS','NG'}
df['Platform_Type'] = np.where(df['Platform']=='PC','PC', np.where(df['Platform'].astype(str).isin(handheld),'Handheld','Console'))
df['Decade'] = (df['Year']//10*10).astype('Int64').astype('string')+'s'
df.loc[df['Year'].isna(),'Decade'] = pd.NA
df['Critic_Band'] = pd.cut(df['Critic_Score'],[0,50,60,70,80,90,100],labels=['0-49','50-59','60-69','70-79','80-89','90+'])
df['Has_Scores'] = df['Critic_Score'].notna() & df['User_Score'].notna()
log.append(('Score columns left missing (NOT imputed)', int(df['Critic_Score'].isna().sum()), 'Imputing would invent ratings; score analysis uses only rated games'))

# 11. Validity checks
chk = (df[['NA_Sales','EU_Sales','JP_Sales','Other_Sales']].sum(axis=1) - df['Global_Sales']).abs()
log.append(('Rows where regions != Global by >0.05M', int((chk>0.05).sum()), 'Differences <=0.02M are rounding; Global kept as reported'))
assert (df[sales]>=0).all().all() and df['Critic_Score'].dropna().between(0,100).all() and df['User_Score'].dropna().between(0,10).all()

df = df.reset_index(drop=True)
log.append(('Final rows', len(df), f'{n0-len(df)} rows removed in total'))
df.to_csv('data/cleaned_video_games.csv', index=False)
pd.DataFrame(log, columns=['Step','Rows_affected','Note']).to_csv('data/cleaning_log.csv', index=False)
print(pd.DataFrame(log, columns=['Step','Rows_affected','Note']).to_string()); print(df.dtypes); print(df.shape, df.Global_Sales.sum())

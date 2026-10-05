"""Interactive Video Game Industry Dashboard.  Run:  streamlit run app.py"""
from pathlib import Path
import pandas as pd, plotly.express as px, streamlit as st

st.set_page_config(page_title='Video Game Industry Dashboard', layout='wide')
CSV = next(p for p in [Path(__file__).parent/'cleaned_video_games.csv', Path(__file__).parent.parent/'data'/'cleaned_video_games.csv'] if p.exists())

@st.cache_data
def load():
    return pd.read_csv(CSV)
df = load()

st.title('Video Game Industry Dashboard')
st.caption('Global sales in millions of units | source: Video_Games_Sales_as_at_22_Dec_2016 (cleaned)')

# ---- Sidebar filters ----
sb = st.sidebar; sb.header('Filters')
genres = sb.multiselect('Genre', sorted(df.Genre.unique()), default=[])
makers = sb.multiselect('Platform maker', sorted(df.Platform_Maker.unique()), default=[])
plats = sb.multiselect('Platform', sorted(df.Platform.unique()), default=[])
yr = sb.slider('Release year', 1980, 2016, (1980, 2016))
inc_na = sb.checkbox('Include games with unknown year', value=True)
ratings = sb.multiselect('ESRB rating', ['E','E10+','T','M'], default=[])
f = df.copy()
if genres:  f = f[f.Genre.isin(genres)]
if makers:  f = f[f.Platform_Maker.isin(makers)]
if plats:   f = f[f.Platform.isin(plats)]
if ratings: f = f[f.Rating.isin(ratings)]
f = f[f.Year.between(*yr) | (f.Year.isna() & inc_na)]
if f.empty: st.warning('No games match the filters.'); st.stop()

tot = f.Global_Sales.sum()
top = lambda col: f.groupby(col).Global_Sales.sum().sort_values(ascending=False)
c = st.columns(6)
c[0].metric('Total games (releases)', f'{len(f):,}'); c[1].metric('Total sales (M)', f'{tot:,.1f}')
c[2].metric('Top genre', top('Genre').index[0]); c[3].metric('Top platform', top('Platform').index[0])
c[4].metric('Top publisher', top('Publisher').index[0]); c[5].metric('Avg sales / release (M)', f'{f.Global_Sales.mean():.2f}')

tab1, tab2, tab3, tab4 = st.tabs(['Overview', 'Genre & Platform', 'Publishers & Games', 'Ratings vs Sales'])
with tab1:
    a, b = st.columns([2, 1])
    y = f.dropna(subset=['Year']).groupby('Year').agg(Sales=('Global_Sales','sum'), Releases=('Name','count')).reset_index()
    a.plotly_chart(px.line(y, x='Year', y='Sales', markers=True, title='Sales trend by release year (M units)'), width='stretch')
    reg = f[['NA_Sales','EU_Sales','JP_Sales','Other_Sales']].sum().rename({'NA_Sales':'North America','EU_Sales':'Europe','JP_Sales':'Japan','Other_Sales':'Other'})
    b.plotly_chart(px.pie(values=reg.values, names=reg.index, hole=.5, title='Sales by region'), width='stretch')
    ry = f.dropna(subset=['Year']).groupby('Year')[['NA_Sales','EU_Sales','JP_Sales','Other_Sales']].sum().reset_index().melt('Year', var_name='Region', value_name='Sales')
    st.plotly_chart(px.area(ry, x='Year', y='Sales', color='Region', title='Regional sales over time (M units)'), width='stretch')
with tab2:
    a, b = st.columns(2)
    g = f.groupby('Genre').agg(Games=('Name','count'), Sales=('Global_Sales','sum')).reset_index(); g['Avg per release'] = g.Sales/g.Games
    a.plotly_chart(px.bar(g.sort_values('Sales'), x='Sales', y='Genre', orientation='h', title='Sales by genre (M units)'), width='stretch')
    b.plotly_chart(px.bar(g.sort_values('Avg per release'), x='Avg per release', y='Genre', orientation='h', title='Avg sales per release by genre (M)', color_discrete_sequence=['#E07B39']), width='stretch')
    p = top('Platform').head(12).reset_index()
    a.plotly_chart(px.bar(p.sort_values('Global_Sales'), x='Global_Sales', y='Platform', orientation='h', title='Top platforms (M units)'), width='stretch')
    hm = f.pivot_table(index='Genre', columns='Platform_Maker', values='Global_Sales', aggfunc='sum').fillna(0)
    b.plotly_chart(px.imshow(hm, text_auto='.0f', aspect='auto', color_continuous_scale='Blues', title='Genre x platform maker (M units)'), width='stretch')
with tab3:
    a, b = st.columns(2)
    pb = top('Publisher').head(10).reset_index()
    a.plotly_chart(px.bar(pb.sort_values('Global_Sales'), x='Global_Sales', y='Publisher', orientation='h', title='Top 10 publishers (M units)'), width='stretch')
    gm = f.groupby('Name').Global_Sales.sum().sort_values(ascending=False).head(10).reset_index()
    b.plotly_chart(px.bar(gm.sort_values('Global_Sales'), x='Global_Sales', y='Name', orientation='h', title='Top 10 titles, all platforms combined (M units)', color_discrete_sequence=['#E07B39']), width='stretch')
    st.dataframe(f.nlargest(25, 'Global_Sales')[['Name','Platform','Year','Genre','Publisher','Global_Sales']], width='stretch', hide_index=True)
with tab4:
    s = f.dropna(subset=['Critic_Score'])
    if len(s) < 10: st.info('Too few rated games for the current filters.')
    else:
        a, b = st.columns(2)
        a.plotly_chart(px.scatter(s, x='Critic_Score', y='Global_Sales', log_y=True, color='Genre', hover_name='Name', opacity=.5, title='Critic score vs sales (log scale)'), width='stretch')
        bands = s.groupby('Critic_Band', observed=True).Global_Sales.mean().reindex(['0-49','50-59','60-69','70-79','80-89','90+']).reset_index()
        b.plotly_chart(px.bar(bands, x='Critic_Band', y='Global_Sales', title='Avg sales per release by critic band (M)'), width='stretch')
        st.caption(f'Spearman correlation critic score vs sales: {s.Critic_Score.corr(s.Global_Sales, method="spearman"):.2f} (n={len(s):,}; only games with a score)')

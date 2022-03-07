import pandas as pd
df=pd.read_csv("https://raw.githubusercontent.com/syedmdfaruq/datasets/main/matches.csv")
import dash
import dash_auth
from dash import dcc,html
from dash.dependencies import Input,Output
import plotly.express as px
USERNAME_PASSWORD_PAIRS=[["faruq","faruq"]]
app=dash.Dash(__name__)
auth=dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)
server=app.server
app.layout=html.Div([html.Label("select_option_below"),dcc.Dropdown(["best_teams","best_player","all_win_by_runs","all_win_by_wickets","lucky_venue","toss_win"],id="dropdown1"),html.Div(id="1")],style={'width': '70%'})
a=df["season"].unique()
a.sort()
b=df[df["season"]==2008]["winner"].value_counts().sort_values(ascending=False)
fig1=px.bar(df,x=b.index,y=b.values,labels={"y":"matches_won"})
best_players=[]
n=[]
for i in a:
  c=df[df["season"]==i]["player_of_match"].value_counts().sort_values(ascending=False)
  best_players.append(c.index[0])
  n.append(c.values[0])
b1=df[df["season"]==2008].groupby("winner").sum().sort_values(by="win_by_runs",ascending=False)
fig31=px.bar(x=b1.index,y=b1["win_by_runs"],labels={"y":"all_matches_total_win_by_runs"})
b2=df[df["season"]==2008].groupby("winner").sum().sort_values(by="win_by_wickets",ascending=False)
fig32=px.bar(x=b2.index,y=b2["win_by_wickets"],labels={"y":"all_matches_total_win_by_wickets"})
ef=[]
for i in df[df["season"]==2008]["team1"].unique():
  ab=0
  cd=""
  for j in df[df["season"]==2008]["venue"].unique():
    if len(df[(df["season"]==2008)&(df["winner"]==i)&(df["venue"]==j)])>ab:
      ab=len(df[(df["season"]==2008)&(df["winner"]==i)&(df["venue"]==j)])
      cd=j
  ef.append([i,cd,ab])
fig4=px.bar(df,x=[i[0]+"("+i[1]+")" for i in ef],y=[i[2] for i in ef],labels={"y":"matches_won"})
new_df1=df[df["season"]==2008]
a1=[]
a2=[]
for i in new_df1["team1"].unique():
  a1.append(i)
  a2.append(len(new_df1[(new_df1["toss_winner"]==i)&(new_df1["winner"]==i)])/len(new_df1[new_df1["toss_winner"]==i]))
fig5=px.bar(df,x=a1,y=a2,labels={"y":"(matches_won_after_winning_tosses/tosses_won)"})
@app.callback(
    Output("1","children"),
    Input("dropdown1","value"))
def update_dropdown(selected):
  if selected=="best_teams":
    return html.Div([dcc.Graph(id="best_teams_graph",figure=fig1),dcc.Slider(
        df['season'].min(),
        df['season'].max(),
        step=None,
        value=df['season'].min(),
        marks={str(year): str(year) for year in a},
        id="year-slider1"
    )])
  if selected=="best_player":
    return html.Div([dcc.Graph(figure=px.bar(df,x=[str(a[i])+" "+best_players[i] for i in range(len(a))],y=n,labels={"y":"number_of_times_player_of_the_match"}))])
  if selected=="all_win_by_runs":
    return html.Div([dcc.Graph(id="win_by_runs_graph",figure=fig31),dcc.Slider(
        df['season'].min(),
        df['season'].max(),
        step=None,
        value=df['season'].min(),
        marks={str(year): str(year) for year in a},
        id="year-slider31")])
  if selected=="all_win_by_wickets":
    return html.Div([dcc.Graph(id="win_by_wickets_graph",figure=fig32),dcc.Slider(
        df['season'].min(),
        df['season'].max(),
        step=None,
        value=df['season'].min(),
        marks={str(year): str(year) for year in a},
        id="year-slider32")])
  if selected=="lucky_venue":
    return html.Div([dcc.Graph(id="lucky_venue_graph",figure=fig4),dcc.Slider(
        df['season'].min(),
        df['season'].max(),
        step=None,
        value=df['season'].min(),
        marks={str(year): str(year) for year in a},
        id="year-slider4"
    )]) 
  if selected=="toss_win":
    return html.Div([dcc.Graph(id="toss_win_graph",figure=fig5),dcc.Slider(
        df['season'].min(),
        df['season'].max(),
        step=None,
        value=df['season'].min(),
        marks={str(year): str(year) for year in a},
        id="year-slider5"
    )])
@app.callback(
    Output("best_teams_graph","figure"),
    Input("year-slider1","value"))
def update_figure1(year1):
  b=df[df["season"]==year1]["winner"].value_counts().sort_values(ascending=False)
  fig1=px.bar(df,x=b.index,y=b.values,labels={"y":"matches_won"})
  return fig1
@app.callback(Output("win_by_runs_graph","figure"),Input("year-slider31","value"))
def update_figure31(year31):
  b1=df[df["season"]==year31].groupby("winner").sum().sort_values(by="win_by_runs",ascending=False)
  fig31=px.bar(x=b1.index,y=b1["win_by_runs"],labels={"y":"all_matches_total_win_by_runs"})
  return fig31
@app.callback(Output("win_by_wickets_graph","figure"),Input("year-slider32","value"))
def update_figure32(year32):
  b2=df[df["season"]==year32].groupby("winner").sum().sort_values(by="win_by_wickets",ascending=False)
  fig32=px.bar(x=b2.index,y=b2["win_by_wickets"],labels={"y":"all_matches_total_win_by_wickets"})
  return fig32
@app.callback(
    Output("lucky_venue_graph","figure"),
    Input("year-slider4","value"))
def update_figure4(year4):
  ef=[]
  for i in df[df["season"]==year4]["team1"].unique():
    ab=0
    cd=""
    for j in df[df["season"]==year4]["venue"].unique():
      if len(df[(df["season"]==year4)&(df["winner"]==i)&(df["venue"]==j)])>ab:
        ab=len(df[(df["season"]==year4)&(df["winner"]==i)&(df["venue"]==j)])
        cd=j
    ef.append([i,cd,ab])
  fig4=px.bar(df,x=[i[0]+"("+i[1]+")" for i in ef],y=[i[2] for i in ef],labels={"y":"matches_won"})
  return fig4

@app.callback(
    Output("toss_win_graph","figure"),
    Input("year-slider5","value"))
def update_figure5(year5):
  new_df1=df[df["season"]==year5]
  a1=[]
  a2=[]
  for i in new_df1["team1"].unique():
    a1.append(i)
    a2.append(len(new_df1[(new_df1["toss_winner"]==i)&(new_df1["winner"]==i)])/len(new_df1[new_df1["toss_winner"]==i]))
  fig5=px.bar(df,x=a1,y=a2,labels={"y":"(matches_won_after_winning_tosses/tosses_won)"})
  return fig5
if __name__=="__main__":
  app.run_server(debug=True)

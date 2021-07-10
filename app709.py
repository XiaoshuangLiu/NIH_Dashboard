#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import plotly.express as px


# In[2]:


df = pd.read_csv('data/resultUQ_FULL.csv' )
df['new_name'] = df['full_institute_name']+'('+df['Acronym_institute_name']+')'
df['project_type'] = df.PROJECT_NUMBER.str[0]
df 


# In[3]:


df_d = pd.read_csv('data/Drug_hold.csv' )
# df_d['new_name'] = df_d['full_institute_name']+'('+df_d['Acronym_institute_name']+')'
df_d


# In[4]:


df_t = pd.read_csv('data/Target_hold.csv' )
# df_t['new_name'] = df_t['full_institute_name']+'('+df_t['Acronym_institute_name']+')'
df_t


# In[5]:


df_d_pmid = pd.read_csv('data/pmid_drug.csv' )
df_d_pmid


# In[6]:


df_t_pmid = pd.read_csv('data/pmid_target.csv' )
df_t_pmid


# In[7]:


def unique_pmid(df):
    total = df.PMID.nunique()
    total = '{:,}'.format(total)
    return total


# In[8]:


def unique_project(df):
    total = df.PROJECT_NUMBER.nunique()
    total = '{:,}'.format(total)
    return total


# In[9]:


def apy(df):
    total = df.ACTUAL_PROJECT_YEAR.nunique()
    total = '{:,}'.format(total)
    return total


# In[10]:


def total_funding(df):
    total = df.drop_duplicates('ACTUAL_PROJECT_YEAR').APY_COST_inf2018.sum()
    total = '${:,}'.format(total)
    return total


# In[11]:


def pmid_count_year_plot(df):
    new_df = df[df.PROJECT_NUMBER.notnull()].groupby('PUB_YEAR').PMID.nunique().reset_index()
    return new_df  


# In[12]:


def funding_yearly_plot(df):
    new_df = df.drop_duplicates('ACTUAL_PROJECT_YEAR').groupby('APY')['APY_COST_inf2018'].sum().reset_index()
    return new_df    


# In[13]:


def APY_yearly_plot(df):
    new_df = df.groupby('APY')['ACTUAL_PROJECT_YEAR'].nunique().reset_index()
    return new_df 


# In[14]:


def top_10_fund_ins(df):
    top10_cost_ins_total = df.drop_duplicates('ACTUAL_PROJECT_YEAR').groupby('new_name')['APY_COST_inf2018'].sum().reset_index().sort_values(by = 'APY_COST_inf2018',ascending = False)
    return top10_cost_ins_total.head(10)


# In[15]:


def top_10_productive_ins(df):
    top10_productive_ins_total = df.groupby('new_name')['PMID'].nunique().reset_index().sort_values(by = 'PMID',ascending = False)
    return top10_productive_ins_total.head(10)


# In[16]:


def top_10_fund_proj(df):
    top10_cost_proj_total = df.drop_duplicates('ACTUAL_PROJECT_YEAR').groupby('project_type')['APY_COST_inf2018'].sum().reset_index().sort_values(by = 'APY_COST_inf2018',ascending = False)
    return top10_cost_proj_total.head(10)


# In[17]:


def top_10_productive_proj(df):
    top10_productive_proj_total = df.groupby('project_type')['PMID'].nunique().reset_index().sort_values(by = 'PMID',ascending = False)
    return top10_productive_proj_total.head(10)


# In[18]:


def build_banner():
    return html.Div(
            id="header",
            children=[
                html.H3(
                    id='header-title',
                    children="NIH Funding Drug Innovation (NFDI)"),
            ]
        )


# In[19]:


def blocks(df):
    return html.Div([
               
                html.Div(children=[html.P("PMID", style={'textAlign': 'center', 'fontWeight': 'bold', 'color': '#6A6567','padding': '1rem','font-size': '16px',},),
                        html.P(style={'color': '#823737'}, children=['Total: {:,}'.format(df_d_pmid.PMID.nunique() + df_t_pmid.PMID.nunique()),
                                                                     html.Br(),
                                                                      'Target: {:,}'.format(df_t_pmid.PMID.nunique()),
                                                                      html.Br(),
                                                                      'Drug: {:,}'.format(df_d_pmid.PMID.nunique()),

                                                                     ])],
                         className="box2", style={
                            'backgroundColor':'#D9D5A9',
                            'height':'200px',
#                             'margin-left':'10px',
                            'text-align':'center',
                            'width':'20%',
                            'display':'inline-block'
                           },
                        
                        ),
                html.Div(children=[html.P("NIH Funded PMID", style={'textAlign': 'center', 'fontWeight': 'bold', 'color': '#6A6567','padding': '1rem','font-size': '16px'},),
                        html.P(style={'color': '#823737'}, children=['Total: {}'.format(unique_pmid(df)),
                                                                     html.Br(),
                                                                      'Target: {}'.format(unique_pmid(df_t)),
                                                                      html.Br(),
                                                                      'Drug: {}'.format(unique_pmid(df_d)),
                                                                     ])],
                        className="box2", style={
                                'backgroundColor':'#F7D7D7',
                                'height':'200px',
#                                 'margin-left':'10px',
                                'text-align':'center',
                                'width':'20%',
                                'display':'inline-block'
                               }),
                html.Div(children=[html.P("Project", style={'textAlign': 'center', 'fontWeight': 'bold', 'color': '#6A6567','padding': '1rem','font-size': '16px'},),
                        html.P(style={'color': '#823737'}, children=['Total: {}'.format(unique_project(df)),
                                                                     html.Br(),
                                                                      'Target: {}'.format(unique_project(df_t)),
                                                                      html.Br(),
                                                                      'Drug: {}'.format(unique_project(df_d)),

                                                                     ])],
                         className="box2", style={
                            'backgroundColor':'#FFF0E0',
                            'height':'200px',
#                             'margin-left':'10px',
                            'text-align':'center',
                            'width':'20%',
                            'display':'inline-block'
                           },
                        
                        ),
                html.Div(children=[html.P("Project Year", style={'textAlign': 'center', 'fontWeight': 'bold', 'color': '#6A6567','padding': '1rem','font-size': '16px'},),
                       html.P(style={'color': '#823737'}, children=[
                                                                   'Total: {}'.format(apy(df)),
                                                                    html.Br(),
                                                                   'Target: {}'.format(apy(df_t)),
                                                                    html.Br(),
                                                                   'Drug: {}'.format(apy(df_d)),])
                                  ],
                         className="box2", style={
                                'backgroundColor':'#D3DFF6',
                                'height':'200px',
#                                 'margin-left':'10px',
                                'text-align':'center',
                                'width':'20%',
                                'display':'inline-block'
                               }),
                html.Div(children=[html.P("Funding", style={'textAlign': 'center', 'fontWeight': 'bold', 'color': '#6A6567','padding': '1rem','font-size': '16px'},),
                        html.P(style={'color': '#823737'}, children=['Total: {}'.format(total_funding(df)),
                                                                      html.Br(),
                                                                      'Target: {}'.format(total_funding(df_t)),
                                                                      html.Br(),
                                                                      'Drug: {}'.format(total_funding(df_d)),
                                                                     ])],
                        className="box2", style={
                            'backgroundColor':'#F0DDEC',
                            'height':'200px',
#                             'margin-left':'10px',
                            'width':'20%',
                            'text-align':'center',
                            'display':'inline-block'
                            }),

                            ])


# In[20]:


#Tab1 Lineplot target data
pmid_count_year_plot_target = pmid_count_year_plot(df_t) # PUB_YEAR  PMID
pmid_count_year_plot_target
APY_yearly_plot_target = APY_yearly_plot(df_t) #APY  ACTUAL_PROJECT_YEAR
APY_yearly_plot_target
funding_yearly_plot_target = funding_yearly_plot(df_t) # APY  APY_COST_inf2018
funding_yearly_plot_target


# In[21]:


#Tab1 Lineplot drug data
pmid_count_year_plot_drug = pmid_count_year_plot(df_d) # PUB_YEAR PMID
pmid_count_year_plot_drug
APY_yearly_plot_drug = APY_yearly_plot(df_d)  # APY ACTUAL_PROJECT_YEAR
APY_yearly_plot_drug
funding_yearly_plot_drug =funding_yearly_plot(df_d) # APY  APY_COST_inf2018
funding_yearly_plot_drug


# In[22]:


# tab 1 lineplot
fig = make_subplots(
    rows=2, cols=3, subplot_titles=( "PMID Count by Year (Target)", "Project Year by Year (Target)", "NIH Funding Drug Innovation by Year (Target)",
                                     "PMID Count by Year (Drug)", "Project Year by Year (Drug)", "NIH Funding Drug Innovation by Year (Drug)"), vertical_spacing=0.4
)

#pmid
fig.add_trace(go.Scatter(x=pmid_count_year_plot_target['PUB_YEAR'], y=pmid_count_year_plot_target['PMID'], name = 'Target', line_color='red',mode='lines+markers',showlegend=False),row=1, col=1)
fig.add_trace(go.Scatter(x=APY_yearly_plot_target['APY'], y=APY_yearly_plot_target['ACTUAL_PROJECT_YEAR'],name = 'Target', line_color='red',mode='lines+markers',showlegend=False), row=1, col=2)
fig.add_trace(go.Scatter(x=funding_yearly_plot_target['APY'], y=funding_yearly_plot_target['APY_COST_inf2018'], name = 'Target',line_color='red' ,mode='lines+markers',showlegend=False),row=1, col=3)


fig.add_trace(go.Scatter(x=pmid_count_year_plot_drug['PUB_YEAR'], y=pmid_count_year_plot_drug['PMID'], name = 'Drug', line_color='blue',mode='lines+markers',showlegend=False),row=2, col=1)
fig.add_trace(go.Scatter(x=APY_yearly_plot_drug['APY'], y=APY_yearly_plot_drug['ACTUAL_PROJECT_YEAR'],name = 'Drug', line_color='blue',mode='lines+markers',showlegend=False), row=2, col=2)
fig.add_trace(go.Scatter(x=funding_yearly_plot_drug['APY'], y=funding_yearly_plot_drug['APY_COST_inf2018'], name = 'Drug',line_color='blue',mode='lines+markers',showlegend=False ),row=2, col=3)


# Update xaxis properties
fig.update_xaxes(title_text="Year", tick0 = 2000, dtick=5, tickangle = 45, row=1, col=2)
fig.update_xaxes(title_text="Year", tick0 = 2000, dtick=5, tickangle = 45, row=1, col=3)
fig.update_xaxes(title_text="Year", tick0 = 2000, dtick=5, tickangle = 45, row=2, col=1)
fig.update_xaxes(title_text="Year", tick0 = 2000, dtick=5, tickangle = 45, row=2, col=2)
fig.update_xaxes(title_text="Year", tick0 = 2000, dtick=5, tickangle = 45, row=2, col=3)

# Update yaxis properties
fig.update_yaxes(title_text="Amount",rangemode="tozero", row=1, col=1)
fig.update_yaxes(title_text="Count", rangemode="tozero", row=1, col=2)
fig.update_yaxes(title_text="Count", rangemode="tozero", row=1, col=3)
fig.update_yaxes(title_text="Amount",rangemode="tozero", row=2, col=1)
fig.update_yaxes(title_text="Count", rangemode="tozero", row=2, col=2)
fig.update_yaxes(title_text="Count", rangemode="tozero", row=2, col=3)
# fig.update_layout(showlegend=False)

# Update title and height
fig.update_layout(paper_bgcolor =  'rgba(0, 0, 0, 0)')

fig.show()


# In[23]:


top_10_fund_ins(df)


# In[24]:


# tab2  overview barplot 1
fig2_1_1 = go.Figure([go.Bar(y=top_10_fund_ins(df).sort_values('APY_COST_inf2018')['new_name'], x=top_10_fund_ins(df).sort_values('APY_COST_inf2018')['APY_COST_inf2018'],orientation='h')])
fig2_1_1.update_traces(marker_color='#719FB0')
fig2_1_1.update_xaxes(title_text="Amount")
# fig2_1_1.update_yaxes(automargin=True)
fig2_1_1.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top 10 NIH Funded Institutes')


# In[25]:


# tab2  overview barplot 2
fig2_1_2 = go.Figure([go.Bar(y=top_10_productive_ins(df).sort_values('PMID')['new_name'], x=top_10_productive_ins(df).sort_values('PMID')['PMID'],orientation='h')])
fig2_1_2.update_traces(marker_color='#719FB0')
fig2_1_2.update_xaxes(title_text="PMID Count")
# fig2_1_2.update_yaxes(automargin=True)
fig2_1_2.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top 10 Productive Institutes')


# In[26]:


# tab 2 prepare data for selected insitute
ins__checklist =list(df['new_name'].drop_duplicates()[:])
ins_checklist_df_total = df[df.new_name.isin(ins__checklist[0:3])]
ins_checklist_df_total


# In[27]:


# tab2  select institue barplot 1
fig2_2_1 = go.Figure([go.Bar(y=top_10_fund_ins(ins_checklist_df_total).sort_values('APY_COST_inf2018')['new_name'], x=top_10_fund_ins(ins_checklist_df_total).sort_values('APY_COST_inf2018')['APY_COST_inf2018'],orientation='h')])
fig2_2_1.update_traces(marker_color='#719FB0')
fig2_2_1.update_xaxes(title_text="Amount")
# fig2_2_1.update_yaxes(automargin=True)
fig2_2_1.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top 10 NIH Funded Institutes (Selected)')


# In[28]:


# tab2  select institue barplot 2
fig2_2_2 = go.Figure([go.Bar(y=top_10_productive_ins(ins_checklist_df_total).sort_values('PMID')['new_name'], x=top_10_productive_ins(ins_checklist_df_total).sort_values('PMID')['PMID'],orientation='h')])
fig2_2_2.update_traces(marker_color='#719FB0')
fig2_2_2.update_xaxes(title_text="PMID Count")
# fig2_2_2.update_yaxes(automargin=True)
fig2_2_2.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top 10 Productive Institutes (Selected)')


# In[29]:


# tab 2 prepare data for selected ins lineplot 1
selected_funding_yearly_plot_total = ins_checklist_df_total.drop_duplicates('ACTUAL_PROJECT_YEAR').groupby(by = ['new_name','APY']).APY_COST_inf2018.sum().reset_index()
selected_funding_yearly_plot_total


# In[30]:


# tab 2 prepare data for selected ins lineplot 2
selected_pmid_count_year_plot_total = ins_checklist_df_total.groupby(by = ['new_name','APY']).PMID.nunique().reset_index()
selected_pmid_count_year_plot_total


# In[31]:


# tab 2 selected ins lineplot 1
fig2_3_1 = px.line(selected_funding_yearly_plot_total, x="APY", y="APY_COST_inf2018", color='new_name', title = 'Funding by Year (Selected)', labels={"new_name": ""})
fig2_3_1.update_xaxes(title_text="Year")
fig2_3_1.update_yaxes(title_text="Amount")
fig2_3_1.update_layout(paper_bgcolor =  'rgba(0, 0, 0, 0)')
fig2_3_1.show()


# In[32]:


# tab 2 selected ins lineplot 2
fig2_3_2 = px.line(selected_pmid_count_year_plot_total, x="APY", y="PMID", color='new_name', title = 'PMID Count by Year (Selected)', labels={"new_name": ""})
fig2_3_2.update_xaxes(title_text="Year")
fig2_3_2.update_yaxes(title_text="PMID Count")
fig2_3_2.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)')
fig2_3_2.show()


# In[33]:


# tab 3 project barplot
fig3 = make_subplots(
    rows=1, cols=2, subplot_titles=("Top 10 NIH Funded Project Type", "Top 10 Productive Project Type")
)

# Add traces
fig3.add_trace(go.Bar(y=top_10_fund_proj(df).sort_values('APY_COST_inf2018')['project_type'], x=top_10_fund_proj(df).sort_values('APY_COST_inf2018')['APY_COST_inf2018'], orientation='h'), row=1, col=1)
fig3.add_trace(go.Bar(y=top_10_productive_proj(df).sort_values('PMID')['project_type'], x=top_10_productive_proj(df).sort_values('PMID')['PMID'],orientation='h'), row=1, col=2)

fig3.update_traces(marker_color='#719FB0',row=1, col=1)
fig3.update_traces(marker_color='#719FB0',row=1, col=2)
# Update xaxis properties2
fig3.update_xaxes(title_text="Amount", row=1, col=1)
fig3.update_xaxes(title_text="PMID Count", row=1, col=2)

# Update yaxis properties
# fig2.update_yaxes(title_text="Institutes", row=1, col=1)
# fig2.update_yaxes(title_text="Institutes", row=1, col=2)

# fig3.update_layout(autosize=False,width=1600,height=500,showlegend=False)

# Update title and height
# fig.update_layout(title_text="Customizing Subplot Axes", height=700)
fig3.update_layout(showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)')
fig3.show()


# In[34]:


# tab 3 prepare data for selected pro 
pro__checklist =list(df['project_type'].drop_duplicates()[:])
pro_checklist_df_total = df[df.project_type.isin(pro__checklist[0:3])]
pro_checklist_df_total


# In[35]:


# tab 3 selected project barplot
fig3_2 = make_subplots(
    rows=1, cols=2, subplot_titles=("Top NIH Funded Project Type (Selected)", "Top Productive Project Type (Selected)")
)

# Add traces
fig3_2.add_trace(go.Bar(y=top_10_fund_proj(pro_checklist_df_total).sort_values('APY_COST_inf2018')['project_type'], x=top_10_fund_proj(pro_checklist_df_total).sort_values('APY_COST_inf2018')['APY_COST_inf2018'], orientation='h'), row=1, col=1)
fig3_2.add_trace(go.Bar(y=top_10_productive_proj(pro_checklist_df_total).sort_values('PMID')['project_type'], x=top_10_productive_proj(pro_checklist_df_total).sort_values('PMID')['PMID'],orientation='h'), row=1, col=2)

fig3_2.update_traces(marker_color='#719FB0',row=1, col=1)
fig3_2.update_traces(marker_color='#719FB0',row=1, col=2)
# Update xaxis properties2
fig3_2.update_xaxes(title_text="Amount", row=1, col=1)
fig3_2.update_xaxes(title_text="PMID Count", row=1, col=2)

# Update yaxis properties
# fig2.update_yaxes(title_text="Institutes", row=1, col=1)
# fig2.update_yaxes(title_text="Institutes", row=1, col=2)

# fig3.update_layout(autosize=False,width=1600,height=500,showlegend=False)

# Update title and height
# fig.update_layout(title_text="Customizing Subplot Axes", height=700)
fig3_2.update_layout(showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)')
fig3_2.show()


# In[36]:


# tab 3 prepare data for selected pro lineplot1
selected_pro_funding_yearly_plot_total = pro_checklist_df_total.drop_duplicates('ACTUAL_PROJECT_YEAR').groupby(by = ['project_type','APY']).APY_COST_inf2018.sum().reset_index()
selected_pro_funding_yearly_plot_total


# In[37]:


# tab 3 prepare data for selected pro lineplot2
selected_pro_pmid_count_year_plot_total = pro_checklist_df_total.groupby(by = ['project_type','PUB_YEAR']).PMID.nunique().reset_index()
selected_pro_pmid_count_year_plot_total


# In[38]:


# tab 3 selected pro lineplot 1
fig3_3_1 = px.line(selected_pro_funding_yearly_plot_total, x="APY", y="APY_COST_inf2018", color='project_type', title = 'Funding by Year (Selected)', labels={"project_type": ""})
fig3_3_1.update_xaxes(title_text="Year")
fig3_3_1.update_yaxes(title_text="Amount")
fig3_3_1.update_layout(paper_bgcolor =  'rgba(0, 0, 0, 0)')
fig3_3_1.show()





# In[39]:


# tab 3 selected pro lineplot 2
fig3_3_2 = px.line(selected_pro_pmid_count_year_plot_total, x="PUB_YEAR", y="PMID", color='project_type', title = 'PMID Count by Year (Selected)', labels={"project_type": ""})
fig3_3_2.update_xaxes(title_text="Year")
fig3_3_2.update_yaxes(title_text="PMID Count")
fig3_3_2.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)')
fig3_3_2.show()


# In[40]:


def tab0():                                       
    return  dcc.Tab(id="INTRODUCTION",
                    label="INTRODUCTION",
                    value="tab0",
                    style = {
                            'fontWeight': 'bold',
                            'color': '#646464',
                            'align-items': 'center',
                            'justify-content': 'center',},
                    className="custom-tab",
                    selected_className="custom-tab--selected",
#                     children = [
#                         dcc.Graph(id='tab3_barplots',figure = fig3),]
                    )


# In[41]:


def tab1():
    return dcc.Tab(
            id="OVERVIEW",
            label="OVERVIEW",
            value="tab1",   
            style = {
                    'fontWeight': 'bold',
                    'color': '#646464',
                    'align-items': 'center',
                    'justify-content': 'center',},
            className="custom-tab",
            selected_className="custom-tab--selected",
            children=[
                html.Br(),
                html.P("Please input Target and Drug below", style={'font-size': '16px','textAlign': 'center','font-weight': 'bold'}),
                html.Div([
                    dcc.Input(id="input Target1", type='text', placeholder="input Target, for example: Car_T",style={'width':'20%', 'font-size': '16px',} ),
                    dcc.Input(id="input Drug1", type='text', placeholder="input Drug, for example BCell", style={'width':'20%','font-size': '16px',}),
                    
                ],style=dict(display='flex', justifyContent='center') ),
                html.Br(),
                html.Br(),
                html.Br(),
                blocks(df),
                html.Br(),
                html.Br(),
                dcc.Graph(id='lineplots',figure = fig,), 

                html.Footer(['Tech Notes © 2021 by Center for Analytics and Data Science (CADS) - Data Analytics Research Team (DART), Bentley University are licensed under ',
                        dcc.Link('CC BY 4.0', href='https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1', target='CC BY 4.0'),])
            ]
    )
                


# In[42]:


def tab2():
    return dcc.Tab(
                    id="INSTITUTE",
                    label="INSTITUTE",
                    value="tab2",
                    style = {'fontWeight': 'bold',
                            'color': '#646464',
                            'align-items': 'center',
                            'justify-content': 'center',},
                    className="custom-tab",
                    selected_className="custom-tab--selected",
                    children=[
                            html.P("Overview", style={'textAlign': 'center','font-weight': 'bold', 'font-size': '16px'}),
                            html.Hr(),  
                            html.Div([dcc.Graph(id="top_10_ins_barplot1", figure = fig2_1_1)], style = {'width': '70%', 'display': 'block', 'margin-left':'15%','margin-right':'15%'}),
                            html.Div([dcc.Graph(id="top_10_ins_barplot2", figure = fig2_1_2)], style = {'width': '70%', 'display': 'block', 'margin-left':'15%','margin-right':'15%'}),
                            html.Br(),
                            html.P("Select Institutes", style={'textAlign': 'center','font-weight': 'bold', 'font-size': '16px'}),
                            html.Hr(), 
                            html.Div([
#                                 dcc.Checklist(
#                                         id="all-or-none",
#                                         options=[{"label": "All", "value": "All"}],
#                                         value=['All'],
# #                                         labelStyle={"display": "inline-block"},
#                                             ),
                                dcc.Dropdown(
                                        id="ins_selected",
                                        options=[{"label": i, "value": i} for i in ins__checklist],
                                        value=ins__checklist[0:3],
                                        multi=True,
                                         ),], 
                                     style = {'width': '50%', 'display': 'inline-block', 'align-items': 'center', 'justify-content': 'center', 'margin-left':'25%','margin-right':'25%'}
                                         ),

                            html.Div([ 
                    
                                    dcc.Graph(id="selected_ins_barplot1", figure = fig2_2_1),],
                                    style = {'width': '70%', 'display': 'block', 'margin-left':'15%','margin-right':'15%'}),
                            html.Div([ 
                    
                                    dcc.Graph(id="selected_ins_barplot2", figure = fig2_2_2),],
                                    style = {'width': '70%', 'display': 'block', 'margin-left':'15%','margin-right':'15%'}),
                            html.Div([ 
                                    dcc.Graph(id="selected_ins_lineplot1", figure = fig2_3_1),
                            ],
                                    style = {'width': '70%', 'display': 'block', 'margin-left':'15%','margin-right':'15%'}),

                            html.Div([ 
                                     dcc.Graph(id="selected_ins_lineplot2", figure = fig2_3_2),  
                            ],style = {'width': '70%', 'display': 'block', 'margin-left':'15%','margin-right':'15%'}
                                    ),

                            html.Footer(['Tech Notes © 2021 by Center for Analytics and Data Science (CADS) - Data Analytics Research Team (DART), Bentley University are licensed under ',
                            dcc.Link('CC BY 4.0', href='https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1', target='CC BY 4.0'),])

                        ],
#         style = {'margin':'auto','width': "50%"},
                    )
#                                     ]
#                                         )
# #                     ])


# In[43]:


def tab3():                                       
    return  dcc.Tab(id="PROJECT",
                    label="PROJECT",
                    value="tab3",
                    style = {
                            'fontWeight': 'bold',
                            'color': '#646464',
                            'align-items': 'center',
                            'justify-content': 'center',},
                    className="custom-tab",
                    selected_className="custom-tab--selected",
                    children = [
                        dcc.Graph(id='tab3_barplots',figure = fig3),
                         html.Br(),
                            html.P("Select Project Type", style={'textAlign': 'center','font-weight': 'bold', 'font-size': '16px'}),
                            html.Hr(), 
                            html.Div([
                                dcc.Dropdown(
                                        id="pro_selected",
                                        options=[{"label": i, "value": i} for i in pro__checklist],
                                        value=pro__checklist[0:3],
                                        multi=True,
                                         ),], 
                                     style = {'width': '50%', 'display': 'inline-block', 'align-items': 'center', 'justify-content': 'center', 'margin-left':'25%','margin-right':'25%'}
                                         ),

                            html.Div([ 
                    
                                    dcc.Graph(id="selected_pro_barplot", figure = fig3_2),],
                                    style = {'width': '70%', 'display': 'block', 'margin-left':'15%','margin-right':'15%'}),
                            html.Div([ 
                                    dcc.Graph(id="selected_pro_lineplot1", figure = fig3_3_1),
                            ],
                                    style = {'width': '70%', 'display': 'block', 'margin-left':'15%','margin-right':'15%'}),

                        html.Div([ 
                                     dcc.Graph(id="selected_pro_lineplot2", figure = fig3_3_2),  
                            ],style = {'width': '70%', 'display': 'block', 'margin-left':'15%','margin-right':'15%'}
                                    ),
                        html.Footer(['Tech Notes © 2021 by Center for Analytics and Data Science (CADS) - Data Analytics Research Team (DART), Bentley University are licensed under ',
                        dcc.Link('CC BY 4.0', href='https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1', target='CC BY 4.0'),])
                    ],
                        
                    )


# In[44]:


def tab4():                                       
    return  dcc.Tab(id="map",
                    label="MAP",
                    value="tab4",
                    style = {
                            'fontWeight': 'bold',
                            'color': '#646464',
                            'align-items': 'center',
                            'justify-content': 'center',},
                    className="custom-tab",
                    selected_className="custom-tab--selected",
#                     children = [
#                         dcc.Graph(id='tab3_barplots',figure = fig3),]
                    )


# In[45]:


def tab5():                                       
    return  dcc.Tab(id="download",
                    label="DOWNLOAD",
                    value="tab5",
                    style = {
                            'fontWeight': 'bold',
                            'color': '#646464',
                            'align-items': 'center',
                            'justify-content': 'center',},
                    className="custom-tab",
                    selected_className="custom-tab--selected",
#                     children = [
#                         dcc.Graph(id='tab3_barplots',figure = fig3),]
                    )


# In[46]:


def tab6():                                       
    return  dcc.Tab(id="help",
                    label="HELP",
                    value="tab6",
                    style = {
                            'fontWeight': 'bold',
                            'color': '#646464',
                            'align-items': 'center',
                            'justify-content': 'center',},
                    className="custom-tab",
                    selected_className="custom-tab--selected",
#                     children = [
#                         dcc.Graph(id='tab3_barplots',figure = fig3),]
                    )


# In[47]:


def tab7():                                       
    return  dcc.Tab(id="aboutus",
                    label="ABOUT US",
                    value="tab7",
                    style = {
                            'fontWeight': 'bold',
                            'color': '#646464',
                            'align-items': 'center',
                            'justify-content': 'center',},
                    className="custom-tab",
                    selected_className="custom-tab--selected",
#                     children = [
#                         dcc.Graph(id='tab3_barplots',figure = fig3),]
                    )


# In[48]:


app = dash.Dash(
    __name__,
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=0.3'}],
)
app.title = "NIH Funding Drug Innovation (NFDI) "
# app.config["suppress_callback_exceptions"] = True
# app.css.append_css({
#     'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
# })


# In[49]:



app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),
#         id="app-container",
#         children=[
            html.Div(
            id="tabs",
            className="tabs",
            children=[dcc.Tabs(id="app-tabs",
                               value="tab0",
                               className="custom-tabs",
                               colors={"border": "#6B95B", "background": "#ACCCDD"},
                               children=[tab0(),
                                          tab1(), 
                                          tab2(), 
                                          tab3(),
                                          tab4(), 
                                          tab5(), 
                                          tab6(),
                                          tab7(),],
                                  ),
                         ]
                )
    ]
#     ]
)


# In[50]:


@app.callback(
    Output(component_id = 'selected_ins_barplot1', component_property = 'figure'),
    [Input(component_id = 'ins_selected', component_property = 'value')]
)
def update_2_2_1barplot(ins_selection):
    ins_checklist_df_total = df[df.new_name.isin(ins_selection)]
    fig2_2_1 = go.Figure([go.Bar(y=top_10_fund_ins(ins_checklist_df_total).sort_values('APY_COST_inf2018')['new_name'], x=top_10_fund_ins(ins_checklist_df_total).sort_values('APY_COST_inf2018')['APY_COST_inf2018'],orientation='h')])
    fig2_2_1.update_traces(marker_color='#719FB0')
    fig2_2_1.update_xaxes(title_text="Amount")
#     fig2_2_1.update_yaxes(automargin=True)
    fig2_2_1.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top 10 NIH Funded Institutes (Selected)')

    return fig2_2_1


# In[51]:


@app.callback(
    Output(component_id = 'selected_ins_barplot2', component_property = 'figure'),
    [Input(component_id = 'ins_selected', component_property = 'value')]
)
def update_2_2_2barplot(ins_selection):
    ins_checklist_df_total = df[df.new_name.isin(ins_selection)]

    fig2_2_2 = go.Figure([go.Bar(y=top_10_productive_ins(ins_checklist_df_total).sort_values('PMID')['new_name'], x=top_10_productive_ins(ins_checklist_df_total).sort_values('PMID')['PMID'],orientation='h')])
    fig2_2_2.update_traces(marker_color='#719FB0')
    fig2_2_2.update_xaxes(title_text="PMID Count")
#     fig2_2_2.update_yaxes(automargin=True)
    fig2_2_2.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top 10 Productive Institutes (Selected)')

    return fig2_2_2


# In[52]:


@app.callback(
    Output(component_id = 'selected_ins_lineplot1', component_property = 'figure'),
    [Input(component_id = 'ins_selected', component_property = 'value')]
)
def update_2_3_lineplot1(ins_selection):
    ins_checklist_df_total = df[df.new_name.isin(ins_selection)]

    selected_funding_yearly_plot_total = ins_checklist_df_total.drop_duplicates('ACTUAL_PROJECT_YEAR').groupby(by = ['new_name','APY']).APY_COST_inf2018.sum().reset_index()

    fig2_3_1 = px.line(selected_funding_yearly_plot_total, x="APY", y="APY_COST_inf2018", color='new_name', title = 'Funding by Year (Selected)', labels={"new_name": ""},)
    fig2_3_1.update_xaxes(title_text="Year")
    fig2_3_1.update_yaxes(title_text="Amount")
    fig2_3_1.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)')
    return fig2_3_1


# In[53]:


@app.callback(
    Output(component_id = 'selected_ins_lineplot2', component_property = 'figure'),
    [Input(component_id = 'ins_selected', component_property = 'value')]
)
def update_2_3_lineplot2(ins_selection):
    ins_checklist_df_total = df[df.new_name.isin(ins_selection)]
    selected_pmid_count_year_plot_total = ins_checklist_df_total.groupby(by = ['new_name','APY']).PMID.nunique().reset_index()
    
    fig2_3_2 = px.line(selected_pmid_count_year_plot_total, x="APY", y="PMID", color='new_name', title = 'PMID Count by Year (Selected)', labels={"new_name": ""})
    fig2_3_2.update_xaxes(title_text="Year")
    fig2_3_2.update_yaxes(title_text="PMID Count")
    fig2_3_2.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)')
    return fig2_3_2


# In[54]:


@app.callback(
    Output(component_id = 'selected_pro_barplot', component_property = 'figure'),
    [Input(component_id = 'pro_selected', component_property = 'value')]
)
def update_3_2_barplot(pro_selection):
    pro_checklist_df_total = df[df.project_type.isin(pro_selection)]
    
    fig3_2 = make_subplots(
    rows=1, cols=2, subplot_titles=("Top NIH Funded Project Type (Selected)", "Top Productive Project Type (Selected)")
    )

    # Add traces
    fig3_2.add_trace(go.Bar(y=top_10_fund_proj(pro_checklist_df_total).sort_values('APY_COST_inf2018')['project_type'], x=top_10_fund_proj(pro_checklist_df_total).sort_values('APY_COST_inf2018')['APY_COST_inf2018'], orientation='h'), row=1, col=1)
    fig3_2.add_trace(go.Bar(y=top_10_productive_proj(pro_checklist_df_total).sort_values('PMID')['project_type'], x=top_10_productive_proj(pro_checklist_df_total).sort_values('PMID')['PMID'],orientation='h'), row=1, col=2)

    fig3_2.update_traces(marker_color='#719FB0',row=1, col=1)
    fig3_2.update_traces(marker_color='#719FB0',row=1, col=2)
    # Update xaxis properties2
    fig3_2.update_xaxes(title_text="Amount", row=1, col=1)
    fig3_2.update_xaxes(title_text="PMID Count", row=1, col=2)

    fig3_2.update_layout(showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)')
    
    return fig3_2


# In[55]:


@app.callback(
    Output(component_id = 'selected_pro_lineplot1', component_property = 'figure'),
    [Input(component_id = 'pro_selected', component_property = 'value')]
)
def update_3_3_lineplot1(pro_selection):
    pro_checklist_df_total = df[df.project_type.isin(pro_selection)]
    selected_pro_funding_yearly_plot_total = pro_checklist_df_total.drop_duplicates('ACTUAL_PROJECT_YEAR').groupby(by = ['project_type','APY']).APY_COST_inf2018.sum().reset_index()
    fig3_3_1 = px.line(selected_pro_funding_yearly_plot_total, x="APY", y="APY_COST_inf2018", color='project_type', title = 'Funding by Year (Selected)', labels={"project_type": ""})
    fig3_3_1.update_xaxes(title_text="Year")
    fig3_3_1.update_yaxes(title_text="Amount")
    fig3_3_1.update_layout(paper_bgcolor =  'rgba(0, 0, 0, 0)')

    return fig3_3_1


# In[56]:


@app.callback(
    Output(component_id = 'selected_pro_lineplot2', component_property = 'figure'),
    [Input(component_id = 'pro_selected', component_property = 'value')]
)
def update_3_3_lineplot2(pro_selection):
    pro_checklist_df_total = df[df.project_type.isin(pro_selection)]
    selected_pro_pmid_count_year_plot_total = pro_checklist_df_total.groupby(by = ['project_type','PUB_YEAR']).PMID.nunique().reset_index()
    
    fig3_3_2 = px.line(selected_pro_pmid_count_year_plot_total, x="PUB_YEAR", y="PMID", color='project_type', title = 'PMID Count by Year (Selected)', labels={"project_type": ""})
    fig3_3_2.update_xaxes(title_text="Year")
    fig3_3_2.update_yaxes(title_text="PMID Count")
    fig3_3_2.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)')

    return fig3_3_2


# In[ ]:


server = app.server

# Run the server
if __name__ == "__main__":
    app.run_server(debug=False)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





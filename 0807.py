#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import plotly.express as px
import dash_bootstrap_components as dbc
import NIH_Funding_TEST
from NIH_Funding_TEST import NIH_Search_Drug

# import pandas as pd
# from pandas import DataFrame
# from Bio import Entrez
# from Bio.Entrez import efetch
# import csv   
# import os


# In[2]:


df = pd.read_csv('data/resultUQ_FULL.csv' )
# df['full_institute_name'] = df['full_institute_name']+'('+df['Acronym_institute_name']+')'
df


# In[3]:


df = pd.read_csv('data/resultUQ_FULL.csv' )
# df['full_institute_name'] = df['full_institute_name']+'('+df['Acronym_institute_name']+')'
df 


# In[4]:


df_d = pd.read_csv('data/Drug_hold.csv' )
# df_d['full_institute_name'] = df_d['full_institute_name']+'('+df_d['Acronym_institute_name']+')'
df_d


# In[5]:


df_t = pd.read_csv('data/Target_hold.csv' )
# df_t['full_institute_name'] = df_t['full_institute_name']+'('+df_t['Acronym_institute_name']+')'
df_t


# In[6]:


df_d_pmid = pd.read_csv('data/pmid_drug.csv' )
df_d_pmid


# In[7]:


df_t_pmid = pd.read_csv('data/pmid_target.csv' )
df_t_pmid


# In[8]:


def unique_pmid(df):
    total = df.PMID.nunique()
    total = '{:,}'.format(total)
    return total


# In[9]:


def unique_project(df):
    total = df.PROJECT_NUMBER.nunique()
    total = '{:,}'.format(total)
    return total


# In[10]:


def apy(df):
    total = df.ACTUAL_PROJECT_YEAR.nunique()
    total = '{:,}'.format(total)
    return total


# In[11]:


def total_funding(df):
    total = df.drop_duplicates('ACTUAL_PROJECT_YEAR').APY_COST_inf2018.sum()
    total = '${:,}'.format(total)
    return total


# In[12]:


def pmid_count_year_plot(df):
    new_df = df[df.PROJECT_NUMBER.notnull()].groupby('PUB_YEAR').PMID.nunique().reset_index()
    return new_df  


# In[13]:


def funding_yearly_plot(df):
    new_df = df.drop_duplicates('ACTUAL_PROJECT_YEAR').groupby('APY')['APY_COST_inf2018'].sum().reset_index()
    return new_df    


# In[14]:


def APY_yearly_plot(df):
    new_df = df.groupby('APY')['ACTUAL_PROJECT_YEAR'].nunique().reset_index()
    return new_df 


# In[15]:


def top_10_fund_ins(df):
    top10_cost_ins_total = df.drop_duplicates('ACTUAL_PROJECT_YEAR').groupby('full_institute_name')['APY_COST_inf2018'].sum().reset_index().sort_values(by = 'APY_COST_inf2018',ascending = False)
    return top10_cost_ins_total.head(10)


# In[16]:


def top_10_productive_ins(df):
    top10_productive_ins_total = df.groupby('full_institute_name')['PMID'].nunique().reset_index().sort_values(by = 'PMID',ascending = False)
    return top10_productive_ins_total.head(10)


# In[17]:


def top_10_fund_proj(df):
    top10_cost_proj_total = df.drop_duplicates('ACTUAL_PROJECT_YEAR').groupby('Grant_Type_Name')['APY_COST_inf2018'].sum().reset_index().sort_values(by = 'APY_COST_inf2018',ascending = False)
    return top10_cost_proj_total.head(10)


# In[18]:


def top_10_productive_proj(df):
    top10_productive_proj_total = df.groupby('Grant_Type_Name')['PMID'].nunique().reset_index().sort_values(by = 'PMID',ascending = False)
    return top10_productive_proj_total.head(10)


# In[19]:


def build_banner():
    return html.Div(
            id="header",
            children=[
                html.H3(
                    id='header-title',
                    children="NIH Funding Drug Innovation (NFDI)"),
            ]
        )


# In[20]:


def blocks(df_d_pmid, df_t_pmid, df_t, df_d, df):
    return html.Div([ 
                html.Div(id = 'block1', children=[html.P("PMID", style={'textAlign': 'center', 'fontWeight': 'bold', 'color': '#6A6567','padding': '1rem','font-size': '16px',},),
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
                html.Div(id = 'block2',children=[html.P("NIH Funded PMID", style={'textAlign': 'center', 'fontWeight': 'bold', 'color': '#6A6567','padding': '1rem','font-size': '16px'},),
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
                html.Div(id = 'block3', children=[html.P("Project", style={'textAlign': 'center', 'fontWeight': 'bold', 'color': '#6A6567','padding': '1rem','font-size': '16px'},),
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
                html.Div(id = 'block4',children=[html.P("Project Year", style={'textAlign': 'center', 'fontWeight': 'bold', 'color': '#6A6567','padding': '1rem','font-size': '16px'},),
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
                html.Div(id = 'block5',children=[html.P("Funding", style={'textAlign': 'center', 'fontWeight': 'bold', 'color': '#6A6567','padding': '1rem','font-size': '16px'},),
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


# In[21]:


# tab 1 lineplot

def tab1_fig(df_t, df_d):
    #Tab1 Lineplot target data
    pmid_count_year_plot_target = pmid_count_year_plot(df_t) # PUB_YEAR  PMID
    # pmid_count_year_plot_target
    APY_yearly_plot_target = APY_yearly_plot(df_t) #APY  ACTUAL_PROJECT_YEAR
    # APY_yearly_plot_target
    funding_yearly_plot_target = funding_yearly_plot(df_t) # APY  APY_COST_inf2018
    # funding_yearly_plot_target


    #Tab1 Lineplot drug data
    pmid_count_year_plot_drug = pmid_count_year_plot(df_d) # PUB_YEAR PMID
    # pmid_count_year_plot_drug
    APY_yearly_plot_drug = APY_yearly_plot(df_d)  # APY ACTUAL_PROJECT_YEAR
    # APY_yearly_plot_drug
    funding_yearly_plot_drug =funding_yearly_plot(df_d) # APY  APY_COST_inf2018
    # funding_yearly_plot_drug

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
    fig.update_xaxes(title_text="Year", tick0 = 2000, dtick=5, row=1, col=1)
    fig.update_xaxes(title_text="Year", tick0 = 2000, dtick=5, row=1, col=2)
    fig.update_xaxes(title_text="Year", tick0 = 2000, dtick=5, row=1, col=3)
    fig.update_xaxes(title_text="Year", tick0 = 2000, dtick=5, row=2, col=1)
    fig.update_xaxes(title_text="Year", tick0 = 2000, dtick=5, row=2, col=2)
    fig.update_xaxes(title_text="Year", tick0 = 2000, dtick=5, row=2, col=3)

    # Update yaxis properties
    fig.update_yaxes(title_text="Count",rangemode="tozero", row=1, col=1)
    fig.update_yaxes(title_text="Count", rangemode="tozero", row=1, col=2)
    fig.update_yaxes(title_text="Amount", rangemode="tozero", row=1, col=3)
    fig.update_yaxes(title_text="Count",rangemode="tozero", row=2, col=1)
    fig.update_yaxes(title_text="Count", rangemode="tozero", row=2, col=2)
    fig.update_yaxes(title_text="Amount", rangemode="tozero", row=2, col=3)
    # fig.update_layout(showlegend=False)

    # Update title and height
    fig.update_layout(paper_bgcolor =  'rgba(0, 0, 0, 0)')
    
    return fig


# In[22]:


# top_10_fund_ins(df)


# In[23]:


# tab2  overview barplot 1
def tab2_barplot1(df):
    fig2_1_1 = go.Figure([go.Bar(y=top_10_fund_ins(df).sort_values('APY_COST_inf2018')['full_institute_name'], x=top_10_fund_ins(df).sort_values('APY_COST_inf2018')['APY_COST_inf2018'],orientation='h')])
    fig2_1_1.update_traces(marker_color='#719FB0')
    fig2_1_1.update_xaxes(title_text="Amount")
    # fig2_1_1.update_yaxes(automargin=True)
    fig2_1_1.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top 10 NIH Funded Institutes')
    
    return fig2_1_1


# In[24]:


# tab2  overview barplot 2
def tab2_barplot2(df):
    fig2_1_2 = go.Figure([go.Bar(y=top_10_productive_ins(df).sort_values('PMID')['full_institute_name'], x=top_10_productive_ins(df).sort_values('PMID')['PMID'],orientation='h')])
    fig2_1_2.update_traces(marker_color='#719FB0')
    fig2_1_2.update_xaxes(title_text="PMID Count")
    # fig2_1_2.update_yaxes(automargin=True)
    fig2_1_2.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top 10 Productive Institutes')
    
    return fig2_1_2


# In[25]:


# tab 2 prepare data for selected insitute
ins__checklist =list(df['full_institute_name'].drop_duplicates()[:])
ins_checklist_df_total = df[df.full_institute_name.isin(ins__checklist[0:3])]
ins_checklist_df_total


# In[26]:


def tab2_selected_barplot1(ins_checklist_df_total):    
   
    # tab2  select institue barplot 1
    fig2_2_1 = go.Figure([go.Bar(y=top_10_fund_ins(ins_checklist_df_total).sort_values('APY_COST_inf2018')['full_institute_name'], x=top_10_fund_ins(ins_checklist_df_total).sort_values('APY_COST_inf2018')['APY_COST_inf2018'],orientation='h')])
    fig2_2_1.update_traces(marker_color='#719FB0')
    fig2_2_1.update_xaxes(title_text="Amount")
    # fig2_2_1.update_yaxes(automargin=True)
    fig2_2_1.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top NIH Funded Institutes (Selected)')
    
    return fig2_2_1


# In[27]:


# tab2  select institue barplot 2
def tab2_selected_barplot2(ins_checklist_df_total): 
    fig2_2_2 = go.Figure([go.Bar(y=top_10_productive_ins(ins_checklist_df_total).sort_values('PMID')['full_institute_name'], x=top_10_productive_ins(ins_checklist_df_total).sort_values('PMID')['PMID'],orientation='h')])
    fig2_2_2.update_traces(marker_color='#719FB0')
    fig2_2_2.update_xaxes(title_text="PMID Count")
    # fig2_2_2.update_yaxes(automargin=True)
    fig2_2_2.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top Productive Institutes (Selected)')
    
    return fig2_2_2


# In[28]:


def tab2_selected_lineplot1(ins_checklist_df_total):
    # tab 2 prepare data for selected ins lineplot 1
    selected_funding_yearly_plot_total = ins_checklist_df_total.drop_duplicates('ACTUAL_PROJECT_YEAR').groupby(by = ['full_institute_name','APY']).APY_COST_inf2018.sum().reset_index()
    # selected_funding_yearly_plot_total

    # tab 2 selected ins lineplot 1
    fig2_3_1 = px.line(selected_funding_yearly_plot_total, x="APY", y="APY_COST_inf2018", color='full_institute_name', title = 'Funding by Year (Selected)', labels={"full_institute_name": ""})
    fig2_3_1.update_xaxes(title_text="Year")
    fig2_3_1.update_yaxes(title_text="Amount")
    fig2_3_1.update_layout(paper_bgcolor =  'rgba(0, 0, 0, 0)')
    #fig2_3_1.show()
    
    return fig2_3_1


# In[29]:


def tab2_selected_lineplot2(ins_checklist_df_total):

    # tab 2 prepare data for selected ins lineplot 2
    selected_pmid_count_year_plot_total = ins_checklist_df_total.groupby(by = ['full_institute_name','APY']).PMID.nunique().reset_index()
#     selected_pmid_count_year_plot_total

    # tab 2 selected ins lineplot 2
    fig2_3_2 = px.line(selected_pmid_count_year_plot_total, x="APY", y="PMID", color='full_institute_name', title = 'PMID Count by Year (Selected)', labels={"full_institute_name": ""})
    fig2_3_2.update_xaxes(title_text="Year")
    fig2_3_2.update_yaxes(title_text="PMID Count")
    fig2_3_2.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)')
    #fig2_3_2.show()
    
    return fig2_3_2


# In[ ]:





# In[30]:



def tab3_barplot1(df):
    # tab3  overview barplot 1
    fig3_1_1 = go.Figure([go.Bar(y=top_10_fund_proj(df).sort_values('APY_COST_inf2018')['Grant_Type_Name'], x=top_10_fund_proj(df).sort_values('APY_COST_inf2018')['APY_COST_inf2018'], orientation='h')])
    fig3_1_1.update_traces(marker_color='#719FB0')
    fig3_1_1.update_xaxes(title_text="Amount")
    # fig2_1_1.update_yaxes(automargin=True)
    fig3_1_1.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top 10 NIH Funded Project Type')
    
    return fig3_1_1


# In[31]:


def tab3_barplot2(df):
    # tab3  overview barplot 2
    fig3_1_2 = go.Figure([go.Bar(y=top_10_productive_proj(df).sort_values('PMID')['Grant_Type_Name'], x=top_10_productive_proj(df).sort_values('PMID')['PMID'],orientation='h')])
    fig3_1_2.update_traces(marker_color='#719FB0')
    fig3_1_2.update_xaxes(title_text="PMID Count")
    # fig2_1_1.update_yaxes(automargin=True)
    fig3_1_2.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top 10 Productive Project Type')
    
    return fig3_1_2


# In[32]:


# tab 3 prepare data for selected pro 
pro__checklist =list(df['Grant_Type_Name'].drop_duplicates()[:])
pro_checklist_df_total = df[df.Grant_Type_Name.isin(pro__checklist[0:3])]
pro_checklist_df_total


# In[33]:


def tab3_selected_barplot1(pro_checklist_df_total):

    # tab3  select pro barplot 1
    fig3_2_1 = go.Figure([go.Bar(y=top_10_fund_proj(pro_checklist_df_total).sort_values('APY_COST_inf2018')['Grant_Type_Name'], x=top_10_fund_proj(pro_checklist_df_total).sort_values('APY_COST_inf2018')['APY_COST_inf2018'], orientation='h')])
    fig3_2_1.update_traces(marker_color='#719FB0')
    fig3_2_1.update_xaxes(title_text="Amount")
    # fig2_2_1.update_yaxes(automargin=True)
    fig3_2_1.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top NIH Funded Project Type (Selected)')
    
    return fig3_2_1


# In[34]:


def tab3_selected_barplot2(pro_checklist_df_total):
    
    # tab3  select pro barplot 2
    fig3_2_2 = go.Figure([go.Bar(y=top_10_productive_proj(pro_checklist_df_total).sort_values('PMID')['Grant_Type_Name'], x=top_10_productive_proj(pro_checklist_df_total).sort_values('PMID')['PMID'],orientation='h')])
    fig3_2_2.update_traces(marker_color='#719FB0')
    fig3_2_2.update_xaxes(title_text="PMID Count")
    # fig2_2_1.update_yaxes(automargin=True)
    fig3_2_2.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top Productive Project Type (Selected)')
    
    return fig3_2_2


# In[ ]:





# In[ ]:





# In[35]:


def tab3_selected_lineplot1(pro_checklist_df_total):
    
    # tab 3 prepare data for selected pro lineplot1
    selected_pro_funding_yearly_plot_total = pro_checklist_df_total.drop_duplicates('ACTUAL_PROJECT_YEAR').groupby(by = ['Grant_Type_Name','APY']).APY_COST_inf2018.sum().reset_index()
    # selected_pro_funding_yearly_plot_total
    # tab 3 selected pro lineplot 1
    fig3_3_1 = px.line(selected_pro_funding_yearly_plot_total, x="APY", y="APY_COST_inf2018", color='Grant_Type_Name', title = 'Funding by Year (Selected)', labels={"Grant_Type_Name": ""})
    fig3_3_1.update_xaxes(title_text="Year")
    fig3_3_1.update_yaxes(title_text="Amount")
    fig3_3_1.update_layout(paper_bgcolor =  'rgba(0, 0, 0, 0)')
    # fig3_3_1.show()
    
    return fig3_3_1





# In[36]:


def tab3_selected_lineplot2(pro_checklist_df_total):

    # tab 3 prepare data for selected pro lineplot2
    selected_pro_pmid_count_year_plot_total = pro_checklist_df_total.groupby(by = ['Grant_Type_Name','PUB_YEAR']).PMID.nunique().reset_index()
    # selected_pro_pmid_count_year_plot_total

    # tab 3 selected pro lineplot 2
    fig3_3_2 = px.line(selected_pro_pmid_count_year_plot_total, x="PUB_YEAR", y="PMID", color='Grant_Type_Name', title = 'PMID Count by Year (Selected)', labels={"Grant_Type_Name": ""})
    fig3_3_2.update_xaxes(title_text="Year")
    fig3_3_2.update_yaxes(title_text="PMID Count")
    fig3_3_2.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)')
    # fig3_3_2.show()

    return fig3_3_2


# In[37]:


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


# In[38]:


def tab1(df_d_pmid, df_t_pmid, df_t, df_d, df):
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
                html.Div([
                    
                    html.Div([
                        html.P("Please input Target below:", style={'font-size': '16px','textAlign': 'center','font-weight': 'bold','display': 'inline', "margin-right": "40px"}),
                        html.P("Please input Drug below:", style={'font-size': '16px','textAlign': 'center','font-weight': 'bold','display': 'inline'}),
                        dbc.Button("\u2753", id="modal_open1", n_clicks=0, color="link", style={'textAlign': 'center', 'align-items': 'center', 'justify-content': 'center'}),
                        dbc.Modal([
                                 dbc.ModalHeader("Header"),
                                 dbc.ModalBody(
                                     html.Div([html.P("This is the content of the modal"),
                                            dcc.Link("This is a link", href='https://www.google.com/', target="link"),
                                               html.Br(),
                                               html.Img(src=app.get_asset_url("3.jpg"))])
                                                 ),
                                dbc.ModalFooter(
                                        dbc.Button("Close", id="modal_close1", className="ml-auto", n_clicks=0)
                                    ),
                             ],id="modal1", is_open=False,size="xl", scrollable=True,style={'display': 'inline-block', 'align-items': 'center', 'justify-content': 'center',})]
                        
        
                        ,style={'display': 'inline-block', 'align-items': 'center', 'justify-content': 'center',}),
                    
                    html.Br(),
                    
                    html.Div([
                        dcc.Input(id="input Target", type='text', debounce=True, placeholder="Acetylcholinesterase or AD and amyloid or amyloid beta-protein precursor or Amyloid plaques or amyloid precursor protein or secretases or apolipoproteins-e or Presenilins or receptors, n-methyl-d-aspartate or tau proteins or TDP-43",style={ 'font-size': '16px','display': 'inline-block',"margin-right": "20px"}, ),
                        dcc.Store(id='target_output'),
                        dcc.Input(id="input Drug", type='text', debounce=True, placeholder="Aducanumab or Bapineuzumab or Crenezumab or Gantenerumab or Solanezumab",style={ 'font-size': '16px','display': 'inline-block'} ),
                        dcc.Store(id='drug_output'),                     
                             ], style={'display': 'inline-block',"margin-left": "20px",} ),
#                     html.Div(id='drug_output'), 
#                     html.Div(id='target_output'),
                    html.Br(),
                    html.Br(),
                    html.Div([html.Button(id='tab1_submit', type='submit', children='Submit'), ],style={'display': 'inline-block', 'align-items': 'center', 'justify-content': 'center',}),
                    dcc.Store(id='new_data'),
                    ], style={'textAlign': 'center','align-items': 'center', 'justify-content': 'center',}),
                    
                html.Br(),
                html.Br(),
                blocks(df_d_pmid, df_t_pmid, df_t, df_d, df),
                html.Br(),
                dcc.Graph(id='lineplots',figure = tab1_fig(df_t, df_d),), 

                html.Footer(['© 2021 by Center for Analytics and Data Science (CADS) - Data Analytics Research Team (DART), Bentley University are licensed under ',
                        dcc.Link('CC BY 4.0', href='https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1', target='CC BY 4.0'),
                        html.Img(src=app.get_asset_url("1.png")),
                        html.Img(src=app.get_asset_url("2.png"))])
            ]
    )      


# In[39]:


def tab2(df, ins_checklist_df_total):
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
                        html.Div([
                            html.P("Overview", style={'textAlign': 'center','font-weight': 'bold', 'font-size': '16px', 'display': 'inline',}),
                            dbc.Button("\u2753", id="modal_open2", n_clicks=0, color="link", style={'textAlign': 'center', 'align-items': 'center', 'justify-content': 'center'}),
                             dbc.Modal([
                                 dbc.ModalHeader("Header"),
                                 dbc.ModalBody(
                                     html.Div([html.P("This is the content of the modal"),
                                            dcc.Link("This is a link", href='https://www.google.com/', target="link"),
                                               html.Br(),
                                               html.Img(src=app.get_asset_url("3.jpg"))])
                                                 ),
                                dbc.ModalFooter(
                                        dbc.Button("Close", id="modal_close2", className="ml-auto", n_clicks=0)
                                    ),
                             ],id="modal2", is_open=False,size="xl", scrollable=True,style={'display': 'inline-block', 'align-items': 'center', 'justify-content': 'center',})
                        ], style={'textAlign': 'center','align-items': 'center', 'justify-content': 'center',}) ,   
                        
                            html.Hr(),  
                            html.Div([dcc.Graph(id="top_10_ins_barplot1", figure = tab2_barplot1(df))], style = {'width': '70%', 'display': 'block', 'margin-left':'15%','margin-right':'15%'}),
                            html.Div([dcc.Graph(id="top_10_ins_barplot2", figure = tab2_barplot2(df))], style = {'width': '70%', 'display': 'block', 'margin-left':'15%','margin-right':'15%'}),
                            html.Br(),
                            html.P("Select Institutes", style={'textAlign': 'center','font-weight': 'bold', 'font-size': '16px'}),
                            html.Hr(), 
                            html.Div([
                                dcc.Dropdown(
                                        id="ins_selected",
                                        options=[{"label": i, "value": i} for i in ins__checklist],
                                        value=ins__checklist[0:3],
                                        multi=True,
                                         ),], 
                                     style = {'width': '50%', 'display': 'inline-block', 'align-items': 'center', 'justify-content': 'center', 'margin-left':'25%','margin-right':'25%'}
                                         ),

                            html.Div([ 
                    
                                    dcc.Graph(id="selected_ins_barplot1", figure = tab2_selected_barplot1(ins_checklist_df_total)),],
                                    style = {'width': '70%', 'display': 'block', 'margin-left':'15%','margin-right':'15%'}),
                            html.Div([ 
                    
                                    dcc.Graph(id="selected_ins_barplot2", figure = tab2_selected_barplot2(ins_checklist_df_total)),],
                                    style = {'width': '70%', 'display': 'block', 'margin-left':'15%','margin-right':'15%'}),
                            html.Div([ 
                                    dcc.Graph(id="selected_ins_lineplot1", figure = tab2_selected_lineplot1(ins_checklist_df_total)),
                            ],
                                    style = {'width': '70%', 'display': 'block', 'margin-left':'15%','margin-right':'15%'}),

                            html.Div([ 
                                     dcc.Graph(id="selected_ins_lineplot2", figure = tab2_selected_lineplot2(ins_checklist_df_total)),  
                            ],style = {'width': '70%', 'display': 'block', 'margin-left':'15%','margin-right':'15%'}
                                    ),

                            html.Footer(['© 2021 by Center for Analytics and Data Science (CADS) - Data Analytics Research Team (DART), Bentley University are licensed under ',
                                        dcc.Link('CC BY 4.0', href='https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1', target='CC BY 4.0'),
                                        html.Img(src=app.get_asset_url("1.png")),
                                        html.Img(src=app.get_asset_url("2.png"))])

                        ],
#         style = {'margin':'auto','width': "50%"},
                    )
#                                     ]
#                                         )
# #                     ])


# In[40]:


def tab3(df, pro_checklist_df_total):                                       
    return  dcc.Tab(id="PROJECT",
                    label="PROJECT",
                    value="tab3",
                    style = {
                            'fontWeight': 'bold',
                            'color': '#646464',
                            'align-items': 'center',
                            'textAlign': 'center',
                            'justify-content': 'center',},
                    
                    className="custom-tab",
                    selected_className="custom-tab--selected",
                    children = [
                        html.Div([
                            html.P("Overview", style={'textAlign': 'center','font-weight': 'bold', 'font-size': '16px', 'display': 'inline',}),
                            dbc.Button("\u2753", id="modal_open3", n_clicks=0, color="link", style={'textAlign': 'center', 'align-items': 'center', 'justify-content': 'center'}),
                             dbc.Modal([
                                 dbc.ModalHeader("Header"),
                                 dbc.ModalBody(
                                     html.Div([html.P("This is the content of the modal"),
                                            dcc.Link("This is a link", href='https://www.google.com/', target="link"),
                                               html.Br(),
                                               html.Img(src=app.get_asset_url("3.jpg"))])
                                                 ),
                                dbc.ModalFooter(
                                        dbc.Button("Close", id="modal_close3", className="ml-auto", n_clicks=0)
                                    ),
                             ],id="modal3", is_open=False,size="xl", scrollable=True,style={'display': 'inline-block', 'align-items': 'center', 'justify-content': 'center',})
                        ], style={'textAlign': 'center','align-items': 'center', 'justify-content': 'center',}) , 
                        
                        
                        html.Hr(), 
                        html.Div([
                            dcc.Graph(id='tab3_barplots1',figure = tab3_barplot1(df))],
                            style = {'width': '70%', 'display': 'inline-block', 'margin-left':'15%','margin-right':'15%'}),
                        html.Div([
                            dcc.Graph(id='tab3_barplots2',figure = tab3_barplot2(df))],
                            style = {'width': '70%', 'display': 'inline-block', 'margin-left':'15%','margin-right':'15%'}),
                        
                        
#                         dcc.Graph(id='tab3_barplots1',figure = fig3_1_1),
#                         dcc.Graph(id='tab3_barplots2',figure = fig3_1_2),
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
                    
                                    dcc.Graph(id="selected_pro_barplot1", figure = tab3_selected_barplot1(pro_checklist_df_total)),],
                                    style = {'width': '70%', 'display': 'block', 'margin-left':'15%','margin-right':'15%'}),
                         html.Div([ 
                    
                                    dcc.Graph(id="selected_pro_barplot2", figure = tab3_selected_barplot2(pro_checklist_df_total)),],
                                    style = {'width': '70%', 'display': 'block', 'margin-left':'15%','margin-right':'15%'}),
                            html.Div([ 
                                    dcc.Graph(id="selected_pro_lineplot1", figure = tab3_selected_lineplot1(pro_checklist_df_total)),
                            ],
                                    style = {'width': '70%', 'display': 'block', 'margin-left':'15%','margin-right':'15%'}),

                        html.Div([ 
                                     dcc.Graph(id="selected_pro_lineplot2", figure = tab3_selected_lineplot2(pro_checklist_df_total)),  
                            ],style = {'width': '70%', 'display': 'block', 'margin-left':'15%','margin-right':'15%'}
                                    ),
                        html.Footer(['© 2021 by Center for Analytics and Data Science (CADS) - Data Analytics Research Team (DART), Bentley University are licensed under ',
                                    dcc.Link('CC BY 4.0', href='https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1', target='CC BY 4.0'),
                                    html.Img(src=app.get_asset_url("1.png")),
                                    html.Img(src=app.get_asset_url("2.png"))])
                    ],
                        
                    )


# In[41]:


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


# In[42]:


# user_info = pd.DataFrame(columns = ['Name', 'Affiliation', 'Email', 'Purpose'])


# In[43]:


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
                    children = [
                        html.Div([
                            html.P("Please privide your contact information to download data", style={'textAlign': 'center','font-weight': 'bold', 'font-size': '16px', 'display': 'inline',}),
                            dbc.Button("\u2753", id="modal_open4", n_clicks=0, color="link", style={'textAlign': 'center', 'align-items': 'center', 'justify-content': 'center'}),
                             dbc.Modal([
                                 dbc.ModalHeader("Header"),
                                 dbc.ModalBody(
                                     html.Div([html.P("This is the content of the modal"),
                                            dcc.Link("This is a link", href='https://www.google.com/', target="link"),
                                               html.Br(),
                                               html.Img(src=app.get_asset_url("3.jpg"))])
                                                 ),
                                dbc.ModalFooter(
                                        dbc.Button("Close", id="modal_close4", className="ml-auto", n_clicks=0)
                                    ),
                             ],id="modal4", is_open=False,size="xl", scrollable=True,style={'display': 'inline-block', 'align-items': 'center', 'justify-content': 'center',})
                        ], style={'textAlign': 'center','align-items': 'center', 'justify-content': 'center',}) ,   
                        
                            html.Hr(),  
                        
                        html.Div([
                    
                            html.Div([
                                html.P("Name:", style={'font-size': '16px'}),
                                dcc.Input(id="Name", type='text', placeholder="Name",style={ 'font-size': '16px',} ),
                                dcc.Store(id = 'Name_input')], 
                                style={'display': 'inline-block', "margin-right": "20px"} ),
                            html.Div([
                                html.P("Affiliation:", style={'font-size': '16px',}),
                                dcc.Input(id="Affiliation", type='text', placeholder="Affiliation",style={ 'font-size': '16px',} ),
                                dcc.Store(id = 'Affiliation_input')], 
                                style={'display': 'inline-block', "margin-right": "20px"} ),
                            html.Div([
                                html.P("Email:", style={'font-size': '16px',}),
                                dcc.Input(id="Email", type='text', placeholder="Email",style={ 'font-size': '16px',} ),
                                dcc.Store(id = 'Email_input')], 
                                style={'display': 'inline-block', "margin-right": "20px"} ),
                            html.Div([
                                html.P("Purpose:", style={'font-size': '16px',}),
                                dcc.Checklist(id = 'Purpose_checklist',options=[
                                    {'label': 'Research', 'value': 'Research'},
                                    {'label': 'Teaching', 'value': 'Teaching'},
                                    {'label': 'News/Report', 'value': 'News/Report'},
                                    {'label': 'Government Service', 'value': 'Government Service'},
                                    {'label': 'Other', 'value': 'Other'}
                                ],
                                    value=[],labelStyle={'display': 'inline-block'}
                                ),
                                dcc.Store(id = 'Purpose_input')
                                
                                ], 
                                style={'display': 'inline-block', } ),
        
                    ], style={'width': '100%', 'display': 'flex', 'justifyContent':'center'}),
                        
                        html.Br(),
                     
                        
                        
                        
                        html.Div([
#                             html.Button("Submit", id="user_info_Submit"),
                            dbc.Button("Submit", id="modal_open5", n_clicks=0, color="link", style={'textAlign': 'center', 'align-items': 'center', 'justify-content': 'center'}),
                             dbc.Modal([
                                 dbc.ModalHeader("Header"),
                                 dbc.ModalBody(
                                     html.Div([dbc.Button("Download", id="btn_csv", className="ml-auto", n_clicks=0),
                                     dcc.Download(id="download-file")])
                                     
                                 ),
                                 dbc.ModalFooter(
                                        dbc.Button("Close", id="modal_close5", className="ml-auto", n_clicks=0)
                                    ),
                             ],id="modal5", is_open=False,size="xl", scrollable=True,style={'display': 'inline-block', 'align-items': 'center', 'justify-content': 'center',})
                        ], style={'width': '100%', 'display': 'flex', 'justifyContent':'center'}),
                        
                        html.Br(),
                        
#                         html.Div([
#                             html.Button("Download File", id="btn_txt"),
#                             dcc.Download(id="download-file")
#                         ], style={'width': '100%', 'display': 'flex', 'justifyContent':'center'})
                        
                        ]
                    )


# In[44]:


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
                    children = [
                        html.Div([
                            html.P("Search Term", id="help_search", style={'textAlign': 'center','font-weight': 'bold', 'font-size': '16px'}),
                            html.Hr(), 
                        ]),
                        html.Div([
                            html.P("Institute", id="help_institute", style={'textAlign': 'center','font-weight': 'bold', 'font-size': '16px'}),
                            html.Hr(), 
                        ]),
                        html.Div([
                            html.P("Project/Grants", id="help_project", style={'textAlign': 'center','font-weight': 'bold', 'font-size': '16px'}),
                            html.Hr(), 
                        ]),
                        html.Div([
                            html.P("Graph/Plotly usage", id="help_graph", style={'textAlign': 'center','font-weight': 'bold', 'font-size': '16px'}),
                            html.Hr(), 
                        ]),
                        
                        html.Div([
                            html.P("Map", id="help_map", style={'textAlign': 'center','font-weight': 'bold', 'font-size': '16px'}),
                            html.Hr(), 
                        ]),
                        html.Div([
                            html.P("Download", id="help_download", style={'textAlign': 'center','font-weight': 'bold', 'font-size': '16px'}),
                            html.Hr(), 
                        ]),
                        
                        ]
                    )


# In[45]:


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
                    children = [
                       html.H1("Test", style={'textAlign': 'center','font-weight': 'bold', 'font-size': '16px'}),]
                    )


# In[46]:


app = dash.Dash(
    __name__,
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=0.3'},
              ],external_stylesheets = [dbc.themes.BOOTSTRAP]
)
app.title = "NIH Funding Drug Innovation (NFDI) "
# app.config["suppress_callback_exceptions"] = True
# app.css.append_css({
#     'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
# })


# In[47]:


def serve_layout(df_d_pmid, df_t_pmid, df_t, df_d, df, ins_checklist_df_total,pro_checklist_df_total):
    return html.Div(
    id="big-app-container",
    children=[
        build_banner(),
#         id="app-container",
#         children=[
            html.Div(
            id="tabs",
            className="tabs",
            children=[
                dcc.Store(id="store"), 
                
#                 html.Div(id="trigger"),
                dcc.Tabs(id="app-tabs",
                               value="tab0",
                               className="custom-tabs",
                               colors={"border": "#6B95B", "background": "#ACCCDD"},
                               children=[
                                        tab0(),
                                          tab1(df_d_pmid, df_t_pmid, df_t, df_d, df), 
                                          tab2(df, ins_checklist_df_total), 
                                          tab3(df, pro_checklist_df_total),
                                          tab4(), 
                                          tab5(), 
                                          tab6(),
                                          tab7(),],
                                  ),
                dcc.Store(id="user_info"), 
                html.Div(id = 'trigger')
                         ]
                )
    ]
#     ]
)


# In[48]:


app.layout = serve_layout(df_d_pmid, df_t_pmid, df_t, df_d, df, ins_checklist_df_total,pro_checklist_df_total)


# In[49]:



# app.layout = html.Div(
#     id="big-app-container",
#     children=[
#         build_banner(),
# #         id="app-container",
# #         children=[
#             html.Div(
#             id="tabs",
#             className="tabs",
#             children=[
#                 dcc.Store(id="store"), 
                
# #                 html.Div(id="trigger"),
#                 dcc.Tabs(id="app-tabs",
#                                value="tab0",
#                                className="custom-tabs",
#                                colors={"border": "#6B95B", "background": "#ACCCDD"},
#                                children=[
#                                         tab0(),
#                                           tab1(df_d_pmid, df_t_pmid, df_t, df_d, df), 
#                                           tab2(df, ins_checklist_df_total), 
#                                           tab3(df, pro_checklist_df_total),
#                                           tab4(), 
#                                           tab5(), 
#                                           tab6(),
#                                           tab7(),],
#                                   ),
#                 dcc.Store(id="user_info"), 
#                          ]
#                 )
#     ]
# #     ]
# )


# In[50]:


@app.callback(
    Output("modal1", "is_open"),
    [Input("modal_open1", "n_clicks"), Input("modal_close1", "n_clicks")],
    [State("modal1", "is_open")],
)
def toggle_modal1(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# In[51]:


@app.callback(
    Output("modal2", "is_open"),
    [Input("modal_open2", "n_clicks"), Input("modal_close2", "n_clicks")],
    [State("modal2", "is_open")],
)
def toggle_modal2(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# In[52]:


@app.callback(
    Output("modal3", "is_open"),
    [Input("modal_open3", "n_clicks"), Input("modal_close3", "n_clicks")],
    [State("modal3", "is_open")],
)
def toggle_modal3(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# In[53]:


@app.callback(
    Output("modal4", "is_open"),
    [Input("modal_open4", "n_clicks"), Input("modal_close4", "n_clicks")],
    [State("modal4", "is_open")],
)
def toggle_modal4(n1, n2, is_open):
    if n1 or n2:
        return not is_open


# In[54]:


@app.callback(
    Output("modal5", "is_open"),
    [Input("modal_open5", "n_clicks"), Input("modal_close5", "n_clicks")],
    [State("modal5", "is_open")],
)
def toggle_modal5(n1, n2, is_open):
    if n1 or n2:
        return not is_open


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[55]:


@app.callback(
    Output(component_id = 'selected_ins_barplot1', component_property = 'figure'),
    [Input(component_id = 'ins_selected', component_property = 'value')]
)
def update_2_2_1barplot(ins_selection):
    ins_checklist_df_total = df[df.full_institute_name.isin(ins_selection)]
    
    return tab2_selected_barplot1(ins_checklist_df_total)
    
#     fig2_2_1 = go.Figure([go.Bar(y=top_10_fund_ins(ins_checklist_df_total).sort_values('APY_COST_inf2018')['full_institute_name'], x=top_10_fund_ins(ins_checklist_df_total).sort_values('APY_COST_inf2018')['APY_COST_inf2018'],orientation='h')])
#     fig2_2_1.update_traces(marker_color='#719FB0')
#     fig2_2_1.update_xaxes(title_text="Amount")
# #     fig2_2_1.update_yaxes(automargin=True)
#     fig2_2_1.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top NIH Funded Institutes (Selected)')

#     return fig2_2_1


# In[56]:


@app.callback(
    Output(component_id = 'selected_ins_barplot2', component_property = 'figure'),
    [Input(component_id = 'ins_selected', component_property = 'value')]
)
def update_2_2_2barplot(ins_selection):
    ins_checklist_df_total = df[df.full_institute_name.isin(ins_selection)]

    return tab2_selected_barplot2(ins_checklist_df_total)
#     fig2_2_2 = go.Figure([go.Bar(y=top_10_productive_ins(ins_checklist_df_total).sort_values('PMID')['full_institute_name'], x=top_10_productive_ins(ins_checklist_df_total).sort_values('PMID')['PMID'],orientation='h')])
#     fig2_2_2.update_traces(marker_color='#719FB0')
#     fig2_2_2.update_xaxes(title_text="PMID Count")
# #     fig2_2_2.update_yaxes(automargin=True)
#     fig2_2_2.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top Productive Institutes (Selected)')

#     return fig2_2_2


# In[57]:


@app.callback(
    Output(component_id = 'selected_ins_lineplot1', component_property = 'figure'),
    [Input(component_id = 'ins_selected', component_property = 'value')]
)
def update_2_3_lineplot1(ins_selection):
    ins_checklist_df_total = df[df.full_institute_name.isin(ins_selection)]

    return tab2_selected_lineplot1(ins_checklist_df_total)

#     selected_funding_yearly_plot_total = ins_checklist_df_total.drop_duplicates('ACTUAL_PROJECT_YEAR').groupby(by = ['full_institute_name','APY']).APY_COST_inf2018.sum().reset_index()

#     fig2_3_1 = px.line(selected_funding_yearly_plot_total, x="APY", y="APY_COST_inf2018", color='full_institute_name', title = 'Funding by Year (Selected)', labels={"full_institute_name": ""},)
#     fig2_3_1.update_xaxes(title_text="Year")
#     fig2_3_1.update_yaxes(title_text="Amount")
#     fig2_3_1.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)')
#     return fig2_3_1


# In[58]:


@app.callback(
    Output(component_id = 'selected_ins_lineplot2', component_property = 'figure'),
    [Input(component_id = 'ins_selected', component_property = 'value')]
)
def update_2_3_lineplot2(ins_selection):
    ins_checklist_df_total = df[df.full_institute_name.isin(ins_selection)]
    
    return tab2_selected_lineplot2(ins_checklist_df_total)

#     selected_pmid_count_year_plot_total = ins_checklist_df_total.groupby(by = ['full_institute_name','APY']).PMID.nunique().reset_index()
    
#     fig2_3_2 = px.line(selected_pmid_count_year_plot_total, x="APY", y="PMID", color='full_institute_name', title = 'PMID Count by Year (Selected)', labels={"full_institute_name": ""})
#     fig2_3_2.update_xaxes(title_text="Year")
#     fig2_3_2.update_yaxes(title_text="PMID Count")
#     fig2_3_2.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)')
#     return fig2_3_2


# In[59]:


@app.callback(
    Output(component_id = 'selected_pro_barplot1', component_property = 'figure'),
    [Input(component_id = 'pro_selected', component_property = 'value')]
)
def update_3_2_1barplot(pro_selection):
    pro_checklist_df_total = df[df.Grant_Type_Name.isin(pro_selection)]
    
    return tab3_selected_barplot1(pro_checklist_df_total)
#     fig3_2_1 = go.Figure([go.Bar(y=top_10_fund_proj(pro_checklist_df_total).sort_values('APY_COST_inf2018')['Grant_Type_Name'], x=top_10_fund_proj(pro_checklist_df_total).sort_values('APY_COST_inf2018')['APY_COST_inf2018'], orientation='h')])
#     fig3_2_1.update_traces(marker_color='#719FB0')
#     fig3_2_1.update_xaxes(title_text="Amount")
#     # fig2_2_1.update_yaxes(automargin=True)
#     fig3_2_1.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top NIH Funded Project Type (Selected)')

#     return fig3_2_1


# In[60]:


@app.callback(
    Output(component_id = 'selected_pro_barplot2', component_property = 'figure'),
    [Input(component_id = 'pro_selected', component_property = 'value')]
)
def update_3_2_2barplot(pro_selection):
    
    pro_checklist_df_total = df[df.Grant_Type_Name.isin(pro_selection)]
    
    return tab3_selected_barplot2(pro_checklist_df_total)

#     fig3_2_2 = go.Figure([go.Bar(y=top_10_productive_proj(pro_checklist_df_total).sort_values('PMID')['Grant_Type_Name'], x=top_10_productive_proj(pro_checklist_df_total).sort_values('PMID')['PMID'],orientation='h')])
#     fig3_2_2.update_traces(marker_color='#719FB0')
#     fig3_2_2.update_xaxes(title_text="PMID Count")
#     # fig2_2_1.update_yaxes(automargin=True)
#     fig3_2_2.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top Productive Project Type (Selected)')

#     return fig3_2_2


# In[ ]:





# In[61]:


@app.callback(
    Output(component_id = 'selected_pro_lineplot1', component_property = 'figure'),
    [Input(component_id = 'pro_selected', component_property = 'value')]
)
def update_3_3_lineplot1(pro_selection):
    pro_checklist_df_total = df[df.Grant_Type_Name.isin(pro_selection)]
    
    return tab3_selected_lineplot1(pro_checklist_df_total)

#     selected_pro_funding_yearly_plot_total = pro_checklist_df_total.drop_duplicates('ACTUAL_PROJECT_YEAR').groupby(by = ['Grant_Type_Name','APY']).APY_COST_inf2018.sum().reset_index()
#     fig3_3_1 = px.line(selected_pro_funding_yearly_plot_total, x="APY", y="APY_COST_inf2018", color='Grant_Type_Name', title = 'Funding by Year (Selected)', labels={"Grant_Type_Name": ""})
#     fig3_3_1.update_xaxes(title_text="Year")
#     fig3_3_1.update_yaxes(title_text="Amount")
#     fig3_3_1.update_layout(paper_bgcolor =  'rgba(0, 0, 0, 0)')

#     return fig3_3_1


# In[62]:


@app.callback(
    Output(component_id = 'selected_pro_lineplot2', component_property = 'figure'),
    [Input(component_id = 'pro_selected', component_property = 'value')]
)
def update_3_3_lineplot2(pro_selection):
    pro_checklist_df_total = df[df.Grant_Type_Name.isin(pro_selection)]
    
    return tab3_selected_lineplot2(pro_checklist_df_total)

#     selected_pro_pmid_count_year_plot_total = pro_checklist_df_total.groupby(by = ['Grant_Type_Name','PUB_YEAR']).PMID.nunique().reset_index()
    
#     fig3_3_2 = px.line(selected_pro_pmid_count_year_plot_total, x="PUB_YEAR", y="PMID", color='Grant_Type_Name', title = 'PMID Count by Year (Selected)', labels={"Grant_Type_Name": ""})
#     fig3_3_2.update_xaxes(title_text="Year")
#     fig3_3_2.update_yaxes(title_text="PMID Count")
#     fig3_3_2.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)')

#     return fig3_3_2


# In[63]:


@app.callback(Output('user_info', 'data'),
              Input('modal_open5', 'n_clicks'),
              State('Name', 'value'),
              State('Affiliation', 'value'),
              State('Email', 'value'),
              State('Purpose_checklist', 'value'), prevent_initial_call=True )
def update_user_info(n_clicks, Name, Affiliation, Email,Purpose):
    user_info= pd.read_csv('user_info.csv')
    user_info.loc[len(user_info.index)] = [Name, Affiliation, Email,Purpose ] 
    user_info.to_csv('user_info.csv')
    return user_info


# In[65]:


@app.callback(Output('lineplots', 'figure'),
#               Output('block2', 'children'),
#               Output('block3', 'children'),
#               Output('block4', 'children'),
#               Output('block5', 'children'),
              [Input('tab1_submit', 'n_clicks')],
              [State('input Target', 'value'),
              State('input Drug', 'value')], 
              prevent_initial_call=True)
def update_data(n_clicks,search_term_target,search_term_drug):

    d = {'A': '\"""','search_term_target': [search_term_target],'B': '\"""', 'search_term_drug': [search_term_drug],'C': '\"""',}
    data = pd.DataFrame(data = d)
    data.to_csv('data.csv', index = None)
    
    new_data = pd.read_csv('data.csv')
    search_term_target = new_data.iloc[0]['A'] + new_data.iloc[0]['search_term_target'] + new_data.iloc[0]['B']
    search_term_target
    search_term_drug = new_data.iloc[0]['B']+ new_data.iloc[0]['search_term_drug'] + new_data.iloc[0]['C']
    search_term_drug
    
    print('1 target--------------------------------')
    print(search_term_target)
    print('2 drug--------------------------------')
    print(search_term_drug)
    
    NIH_Search_Drug(search_term_drug,search_term_target)
    
#     NIH_Search_Drug(search_term_target, search_term_drug)
    

    df = pd.read_csv('new_data/resultUQ_FULL.csv' )
#     print(df.head)
    df_d = pd.read_csv('new_data/Drug_hold.csv' )
#     print(df_d.head)
    df_t = pd.read_csv('new_data/Target_hold.csv' )
#     print(df_t.head)
    df_d_pmid = pd.read_csv('new_data/pmid_drug.csv' )
#     print(df_d_pmid.head)
    df_t_pmid = pd.read_csv('new_data/pmid_target.csv' )
#     print(df_t_pmid.head)
    
     # tab 2 prepare data for selected insitute
    ins__checklist =list(df['full_institute_name'].drop_duplicates()[:])
#     print(ins__checklist)
    ins_checklist_df_total = df[df.full_institute_name.isin(ins__checklist[0:3])]
#     print(ins_checklist_df_total)

    # tab 3 prepare data for selected pro 
    pro__checklist =list(df['Grant_Type_Name'].drop_duplicates()[:])
#     print(pro__checklist)
    pro_checklist_df_total = df[df.Grant_Type_Name.isin(pro__checklist[0:3])]
#     print(pro_checklist_df_total)
    print('==============================================================')
#     blocks(df_d_pmid, df_t_pmid, df_t, df_d, df)
    app.layout = serve_layout(df_d_pmid, df_t_pmid, df_t, df_d, df, ins_checklist_df_total,pro_checklist_df_total)
    
    


# In[70]:


@app.callback(
    Output("download-file", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(df.to_csv, "mydf.csv")


# In[ ]:





# In[ ]:





# In[ ]:


server = app.server

# Run the server
if __name__ == "__main__":
    app.run_server(debug=False)


# In[ ]:


print(user_info)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





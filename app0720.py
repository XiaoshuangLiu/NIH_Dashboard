#!/usr/bin/env python
# coding: utf-8

# In[2]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import plotly.express as px
import dash_bootstrap_components as dbc
# import NIH_Funding_Search
# from NIH_Funding_Search import NIH_Search_Drug


# In[3]:


df = pd.read_csv('data/resultUQ_FULL.csv' )
df['new_name'] = df['full_institute_name']+'('+df['Acronym_institute_name']+')'
df


# In[4]:


df = pd.read_csv('data/resultUQ_FULL.csv' )
df['new_name'] = df['full_institute_name']+'('+df['Acronym_institute_name']+')'
df 


# In[5]:


df_d = pd.read_csv('data/Drug_hold.csv' )
# df_d['new_name'] = df_d['full_institute_name']+'('+df_d['Acronym_institute_name']+')'
df_d


# In[6]:


df_t = pd.read_csv('data/Target_hold.csv' )
# df_t['new_name'] = df_t['full_institute_name']+'('+df_t['Acronym_institute_name']+')'
df_t


# In[7]:


df_d_pmid = pd.read_csv('data/pmid_drug.csv' )
df_d_pmid


# In[8]:


df_t_pmid = pd.read_csv('data/pmid_target.csv' )
df_t_pmid


# In[9]:


def unique_pmid(df):
    total = df.PMID.nunique()
    total = '{:,}'.format(total)
    return total


# In[10]:


def unique_project(df):
    total = df.PROJECT_NUMBER.nunique()
    total = '{:,}'.format(total)
    return total


# In[11]:


def apy(df):
    total = df.ACTUAL_PROJECT_YEAR.nunique()
    total = '{:,}'.format(total)
    return total


# In[12]:


def total_funding(df):
    total = df.drop_duplicates('ACTUAL_PROJECT_YEAR').APY_COST_inf2018.sum()
    total = '${:,}'.format(total)
    return total


# In[13]:


def pmid_count_year_plot(df):
    new_df = df[df.PROJECT_NUMBER.notnull()].groupby('PUB_YEAR').PMID.nunique().reset_index()
    return new_df  


# In[14]:


def funding_yearly_plot(df):
    new_df = df.drop_duplicates('ACTUAL_PROJECT_YEAR').groupby('APY')['APY_COST_inf2018'].sum().reset_index()
    return new_df    


# In[15]:


def APY_yearly_plot(df):
    new_df = df.groupby('APY')['ACTUAL_PROJECT_YEAR'].nunique().reset_index()
    return new_df 


# In[16]:


def top_10_fund_ins(df):
    top10_cost_ins_total = df.drop_duplicates('ACTUAL_PROJECT_YEAR').groupby('new_name')['APY_COST_inf2018'].sum().reset_index().sort_values(by = 'APY_COST_inf2018',ascending = False)
    return top10_cost_ins_total.head(10)


# In[17]:


def top_10_productive_ins(df):
    top10_productive_ins_total = df.groupby('new_name')['PMID'].nunique().reset_index().sort_values(by = 'PMID',ascending = False)
    return top10_productive_ins_total.head(10)


# In[18]:


def top_10_fund_proj(df):
    top10_cost_proj_total = df.drop_duplicates('ACTUAL_PROJECT_YEAR').groupby('Grant_Type_Name')['APY_COST_inf2018'].sum().reset_index().sort_values(by = 'APY_COST_inf2018',ascending = False)
    return top10_cost_proj_total.head(10)


# In[19]:


def top_10_productive_proj(df):
    top10_productive_proj_total = df.groupby('Grant_Type_Name')['PMID'].nunique().reset_index().sort_values(by = 'PMID',ascending = False)
    return top10_productive_proj_total.head(10)


# In[20]:


def build_banner():
    return html.Div(
            id="header",
            children=[
                html.H3(
                    id='header-title',
                    children="NIH Funding Drug Innovation (NFDI)"),
            ]
        )


# In[21]:


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


# In[22]:


#Tab1 Lineplot target data
pmid_count_year_plot_target = pmid_count_year_plot(df_t) # PUB_YEAR  PMID
pmid_count_year_plot_target
APY_yearly_plot_target = APY_yearly_plot(df_t) #APY  ACTUAL_PROJECT_YEAR
APY_yearly_plot_target
funding_yearly_plot_target = funding_yearly_plot(df_t) # APY  APY_COST_inf2018
funding_yearly_plot_target


# In[23]:


#Tab1 Lineplot drug data
pmid_count_year_plot_drug = pmid_count_year_plot(df_d) # PUB_YEAR PMID
pmid_count_year_plot_drug
APY_yearly_plot_drug = APY_yearly_plot(df_d)  # APY ACTUAL_PROJECT_YEAR
APY_yearly_plot_drug
funding_yearly_plot_drug =funding_yearly_plot(df_d) # APY  APY_COST_inf2018
funding_yearly_plot_drug


# In[24]:


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

fig.show()


# In[25]:


top_10_fund_ins(df)


# In[26]:


title1 = html.Div([
        html.P("Top 10 NIH Funded Institutes   ", 
               style={'display': 'inline', 'font-size': '16px',}
              ),
        html.Abbr(dcc.Link("\u2753", href='tab6', target="\u2753"),

                  title="Click here for help", style = {'display': 'inline'}),
         ],),


# In[27]:


# tab2  overview barplot 1
fig2_1_1 = go.Figure([go.Bar(y=top_10_fund_ins(df).sort_values('APY_COST_inf2018')['new_name'], x=top_10_fund_ins(df).sort_values('APY_COST_inf2018')['APY_COST_inf2018'],orientation='h')])
fig2_1_1.update_traces(marker_color='#719FB0')
fig2_1_1.update_xaxes(title_text="Amount")
# fig2_1_1.update_yaxes(automargin=True)
fig2_1_1.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top 10 NIH Funded Institutes'
                      )


# In[28]:


# tab2  overview barplot 2
fig2_1_2 = go.Figure([go.Bar(y=top_10_productive_ins(df).sort_values('PMID')['new_name'], x=top_10_productive_ins(df).sort_values('PMID')['PMID'],orientation='h')])
fig2_1_2.update_traces(marker_color='#719FB0')
fig2_1_2.update_xaxes(title_text="PMID Count")
# fig2_1_2.update_yaxes(automargin=True)
fig2_1_2.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top 10 Productive Institutes')


# In[29]:


# tab 2 prepare data for selected insitute
ins__checklist =list(df['new_name'].drop_duplicates()[:])
ins_checklist_df_total = df[df.new_name.isin(ins__checklist[0:3])]
ins_checklist_df_total


# In[30]:


# tab2  select institue barplot 1
fig2_2_1 = go.Figure([go.Bar(y=top_10_fund_ins(ins_checklist_df_total).sort_values('APY_COST_inf2018')['new_name'], x=top_10_fund_ins(ins_checklist_df_total).sort_values('APY_COST_inf2018')['APY_COST_inf2018'],orientation='h')])
fig2_2_1.update_traces(marker_color='#719FB0')
fig2_2_1.update_xaxes(title_text="Amount")
# fig2_2_1.update_yaxes(automargin=True)
fig2_2_1.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top NIH Funded Institutes (Selected)')


# In[31]:


# tab2  select institue barplot 2
fig2_2_2 = go.Figure([go.Bar(y=top_10_productive_ins(ins_checklist_df_total).sort_values('PMID')['new_name'], x=top_10_productive_ins(ins_checklist_df_total).sort_values('PMID')['PMID'],orientation='h')])
fig2_2_2.update_traces(marker_color='#719FB0')
fig2_2_2.update_xaxes(title_text="PMID Count")
# fig2_2_2.update_yaxes(automargin=True)
fig2_2_2.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top Productive Institutes (Selected)')


# In[32]:


# tab 2 prepare data for selected ins lineplot 1
selected_funding_yearly_plot_total = ins_checklist_df_total.drop_duplicates('ACTUAL_PROJECT_YEAR').groupby(by = ['new_name','APY']).APY_COST_inf2018.sum().reset_index()
selected_funding_yearly_plot_total


# In[33]:


# tab 2 prepare data for selected ins lineplot 2
selected_pmid_count_year_plot_total = ins_checklist_df_total.groupby(by = ['new_name','APY']).PMID.nunique().reset_index()
selected_pmid_count_year_plot_total


# In[34]:


# tab 2 selected ins lineplot 1
fig2_3_1 = px.line(selected_funding_yearly_plot_total, x="APY", y="APY_COST_inf2018", color='new_name', title = 'Funding by Year (Selected)', labels={"new_name": ""})
fig2_3_1.update_xaxes(title_text="Year")
fig2_3_1.update_yaxes(title_text="Amount")
fig2_3_1.update_layout(paper_bgcolor =  'rgba(0, 0, 0, 0)')
fig2_3_1.show()


# In[35]:


# tab 2 selected ins lineplot 2
fig2_3_2 = px.line(selected_pmid_count_year_plot_total, x="APY", y="PMID", color='new_name', title = 'PMID Count by Year (Selected)', labels={"new_name": ""})
fig2_3_2.update_xaxes(title_text="Year")
fig2_3_2.update_yaxes(title_text="PMID Count")
fig2_3_2.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)')
fig2_3_2.show()


# In[36]:


# tab3  overview barplot 1
fig3_1_1 = go.Figure([go.Bar(y=top_10_fund_proj(df).sort_values('APY_COST_inf2018')['Grant_Type_Name'], x=top_10_fund_proj(df).sort_values('APY_COST_inf2018')['APY_COST_inf2018'], orientation='h')])
fig3_1_1.update_traces(marker_color='#719FB0')
fig3_1_1.update_xaxes(title_text="Amount")
# fig2_1_1.update_yaxes(automargin=True)
fig3_1_1.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top 10 NIH Funded Project Type')


# In[37]:


# tab3  overview barplot 2
fig3_1_2 = go.Figure([go.Bar(y=top_10_productive_proj(df).sort_values('PMID')['Grant_Type_Name'], x=top_10_productive_proj(df).sort_values('PMID')['PMID'],orientation='h')])
fig3_1_2.update_traces(marker_color='#719FB0')
fig3_1_2.update_xaxes(title_text="PMID Count")
# fig2_1_1.update_yaxes(automargin=True)
fig3_1_2.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top 10 Productive Project Type')


# In[38]:


# # tab 3 project barplot
# fig3 = make_subplots(
#     rows=2, cols=1, subplot_titles=("Top 10 NIH Funded Project Type", "Top 10 Productive Project Type")
# )

# # Add traces
# fig3.add_trace(go.Bar(y=top_10_fund_proj(df).sort_values('APY_COST_inf2018')['Grant_Type_Name'], x=top_10_fund_proj(df).sort_values('APY_COST_inf2018')['APY_COST_inf2018'], orientation='h'), row=1, col=1)
# fig3.add_trace(go.Bar(y=top_10_productive_proj(df).sort_values('PMID')['Grant_Type_Name'], x=top_10_productive_proj(df).sort_values('PMID')['PMID'],orientation='h'), row=2, col=1)

# fig3.update_traces(marker_color='#719FB0',row=1, col=1)
# fig3.update_traces(marker_color='#719FB0',row=2, col=1)
# # Update xaxis properties2
# fig3.update_xaxes(title_text="Amount", row=1, col=1)
# fig3.update_xaxes(title_text="PMID Count", row=2, col=1)

# # Update yaxis properties
# # fig2.update_yaxes(title_text="Institutes", row=1, col=1)
# # fig2.update_yaxes(title_text="Institutes", row=1, col=2)

# # fig3.update_layout(autosize=False,width=1600,height=500,showlegend=False)

# # Update title and height
# # fig.update_layout(title_text="Customizing Subplot Axes", height=700)
# fig3.update_layout(showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)')
# fig3.show()


# In[39]:


# tab 3 prepare data for selected pro 
pro__checklist =list(df['Grant_Type_Name'].drop_duplicates()[:])
pro_checklist_df_total = df[df.Grant_Type_Name.isin(pro__checklist[0:3])]
pro_checklist_df_total


# In[40]:


# tab3  select pro barplot 1
fig3_2_1 = go.Figure([go.Bar(y=top_10_fund_proj(pro_checklist_df_total).sort_values('APY_COST_inf2018')['Grant_Type_Name'], x=top_10_fund_proj(pro_checklist_df_total).sort_values('APY_COST_inf2018')['APY_COST_inf2018'], orientation='h')])
fig3_2_1.update_traces(marker_color='#719FB0')
fig3_2_1.update_xaxes(title_text="Amount")
# fig2_2_1.update_yaxes(automargin=True)
fig3_2_1.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top NIH Funded Project Type (Selected)')


# In[41]:


# tab3  select pro barplot 2
fig3_2_2 = go.Figure([go.Bar(y=top_10_productive_proj(pro_checklist_df_total).sort_values('PMID')['Grant_Type_Name'], x=top_10_productive_proj(pro_checklist_df_total).sort_values('PMID')['PMID'],orientation='h')])
fig3_2_2.update_traces(marker_color='#719FB0')
fig3_2_2.update_xaxes(title_text="PMID Count")
# fig2_2_1.update_yaxes(automargin=True)
fig3_2_2.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top Productive Project Type (Selected)')


# In[42]:


# # tab 3 selected project barplot
# fig3_2 = make_subplots(
#     rows=2, cols=1, subplot_titles=("Top NIH Funded Project Type (Selected)", "Top Productive Project Type (Selected)")
# )

# # Add traces
# fig3_2.add_trace(go.Bar(y=top_10_fund_proj(pro_checklist_df_total).sort_values('APY_COST_inf2018')['Grant_Type_Name'], x=top_10_fund_proj(pro_checklist_df_total).sort_values('APY_COST_inf2018')['APY_COST_inf2018'], orientation='h'), row=1, col=1)
# fig3_2.add_trace(go.Bar(y=top_10_productive_proj(pro_checklist_df_total).sort_values('PMID')['Grant_Type_Name'], x=top_10_productive_proj(pro_checklist_df_total).sort_values('PMID')['PMID'],orientation='h'), row=2, col=1)

# fig3_2.update_traces(marker_color='#719FB0',row=1, col=1)
# fig3_2.update_traces(marker_color='#719FB0',row=2, col=1)
# # Update xaxis properties2
# fig3_2.update_xaxes(title_text="Amount", row=1, col=1)
# fig3_2.update_xaxes(title_text="PMID Count", row=2, col=1)

# # Update yaxis properties
# # fig2.update_yaxes(title_text="Institutes", row=1, col=1)
# # fig2.update_yaxes(title_text="Institutes", row=1, col=2)

# # fig3.update_layout(autosize=False,width=1600,height=500,showlegend=False)

# # Update title and height
# # fig.update_layout(title_text="Customizing Subplot Axes", height=700)
# fig3_2.update_layout(showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)')
# fig3_2.show()


# In[43]:


# tab 3 prepare data for selected pro lineplot1
selected_pro_funding_yearly_plot_total = pro_checklist_df_total.drop_duplicates('ACTUAL_PROJECT_YEAR').groupby(by = ['Grant_Type_Name','APY']).APY_COST_inf2018.sum().reset_index()
selected_pro_funding_yearly_plot_total


# In[44]:


# tab 3 prepare data for selected pro lineplot2
selected_pro_pmid_count_year_plot_total = pro_checklist_df_total.groupby(by = ['Grant_Type_Name','PUB_YEAR']).PMID.nunique().reset_index()
selected_pro_pmid_count_year_plot_total


# In[45]:


# tab 3 selected pro lineplot 1
fig3_3_1 = px.line(selected_pro_funding_yearly_plot_total, x="APY", y="APY_COST_inf2018", color='Grant_Type_Name', title = 'Funding by Year (Selected)', labels={"Grant_Type_Name": ""})
fig3_3_1.update_xaxes(title_text="Year")
fig3_3_1.update_yaxes(title_text="Amount")
fig3_3_1.update_layout(paper_bgcolor =  'rgba(0, 0, 0, 0)')
fig3_3_1.show()





# In[46]:


# tab 3 selected pro lineplot 2
fig3_3_2 = px.line(selected_pro_pmid_count_year_plot_total, x="PUB_YEAR", y="PMID", color='Grant_Type_Name', title = 'PMID Count by Year (Selected)', labels={"Grant_Type_Name": ""})
fig3_3_2.update_xaxes(title_text="Year")
fig3_3_2.update_yaxes(title_text="PMID Count")
fig3_3_2.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)')
fig3_3_2.show()


# In[47]:


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


# In[48]:


# def tab1():
#     return dcc.Tab(
#             id="OVERVIEW",
#             label="OVERVIEW",
#             value="tab1",   
#             style = {
#                     'fontWeight': 'bold',
#                     'color': '#646464',
#                     'align-items': 'center',
#                     'justify-content': 'center',},
#             className="custom-tab",
#             selected_className="custom-tab--selected",
#             children=[
#                 html.Br(),
#                 html.Div([
#                     html.P("Please input Target below   ", 
#                            style={'display': 'inline', 'font-size': '16px','textAlign': 'center','font-weight': 'bold'}
#                           ),
                    
#                     html.P("Please input Drug below   ", 
#                            style={'display': 'inline', 'font-size': '16px','textAlign': 'center','font-weight': 'bold'}
#                           ),
                    
#                     html.Abbr(dcc.Link("\u2753", href='tab6', target="\u2753"),                             
#                               title="Click here for help", style = {'display': 'inline'}),
#                      ], style = {'textAlign': 'center'}),
                
#                 html.Div([
#                     dcc.Input(id="input Target1", type='text', placeholder="Acetylcholinesterase or AD and amyloid or amyloid beta-protein precursor or Amyloid plaques or amyloid precursor protein or secretases or apolipoproteins-e or Presenilins or receptors, n-methyl-d-aspartate or tau proteins or TDP-43",style={'width':'20%', 'font-size': '16px',} ),
#                     dcc.Input(id="input Drug1", type='text', placeholder="Aducanumab or Bapineuzumab or Crenezumab or Gantenerumab or Solanezumab", style={'width':'20%','font-size': '16px',}),
                    
#                 ],style=dict(display='flex', justifyContent='center') ),
#                 html.Br(),
#                 html.Br(),
#                 html.Br(),
#                 blocks(df),
#                 html.Br(),
#                 html.Br(),
#                 dcc.Graph(id='lineplots',figure = fig,), 

#                 html.Footer(['© 2021 by Center for Analytics and Data Science (CADS) - Data Analytics Research Team (DART), Bentley University are licensed under ',
#                         dcc.Link('CC BY 4.0', href='https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1', target='CC BY 4.0'),
#                         html.Img(src=app.get_asset_url("1.png")),
#                         html.Img(src=app.get_asset_url("2.png"))])
#             ]
#     )
                


# In[49]:


# @app.callback(
#     Output("modal", "is_open"),
#     [Input("open", "n_clicks"), Input("close", "n_clicks")],
#     [State("modal", "is_open")],
# )
# def toggle_modal(n1, n2, is_open):
#     if n1 or n2:
#         return not is_open
#     return is_open


# In[50]:


# modal = html.Div(
#     [
#         dbc.Button("Open modal", id="open", n_clicks=0),
#         dbc.Modal(
#             [
#                 dbc.ModalHeader("Header"),
#                 dbc.ModalBody("This is the content of the modal"),
#                 dbc.ModalFooter(
#                     dbc.Button(
#                         "Close", id="close", className="ml-auto", n_clicks=0
#                     )
#                 ),
#             ],
#             id="modal",
#             is_open=False,
#         ),
#     ]
# )


# In[51]:


# def tab1():
#     return dcc.Tab(
#             id="OVERVIEW",
#             label="OVERVIEW",
#             value="tab1",   
#             style = {
#                     'fontWeight': 'bold',
#                     'color': '#646464',
#                     'align-items': 'center',
#                     'justify-content': 'center',},
#             className="custom-tab",
#             selected_className="custom-tab--selected",
#             children=[
#                 html.Br(),
#                 html.Div([
                    
#                     html.Div([
#                         html.P("Please input Target below:", style={'font-size': '16px','textAlign': 'center','font-weight': 'bold', 'marginBottom': '0.5em'}),
#                         dcc.Input(id="input Target", type='text', placeholder="Acetylcholinesterase or AD and amyloid or amyloid beta-protein precursor or Amyloid plaques or amyloid precursor protein or secretases or apolipoproteins-e or Presenilins or receptors, n-methyl-d-aspartate or tau proteins or TDP-43",
#                                   style={ 'font-size': '16px','marginTop': '0.1em'} ),], 
#                         style={'display': 'inline-block', "margin-right": "20px"} ),
                    
#                     html.Div([
#                         html.P("Please input Drug below:", style={'font-size': '16px','textAlign': 'center','font-weight': 'bold','display': 'inline'}),
#                         dbc.Button("help", id="open", n_clicks=0, color="link",size="sm"),
#                              dbc.Modal([
#                                  dbc.ModalHeader("Header"),
#                                  dbc.ModalBody(
#                                      html.Div([html.P("This is the content of the modal"),
#                                                  dcc.Link("link", href='tab6', target="link"),
#                                                html.Img(src=app.get_asset_url("2.png"))])
#                                                  ),
#                                 dbc.ModalFooter(
#                                         dbc.Button("Close", id="close", className="ml-auto", n_clicks=0)
#                                     ),
#                              ],id="modal", is_open=False,size="xl", scrollable=True,),
#                         html.Br(),
#                         dcc.Input(id="input Drug", type='text', placeholder="Aducanumab or Bapineuzumab or Crenezumab or Gantenerumab or Solanezumab",style={ 'font-size': '16px'} ),], 
#                         style={'display': 'inline-block',"margin-left": "20px"} ),
                    
#                     html.Div([
#                         html.P("", style={'font-size': '16px','textAlign': 'center','font-weight': 'bold'}),
#                         html.Br(),
#                         html.Button(id='tab1_submit', type='submit', children='Submit'),
                        
#                              ], style={'display': 'inline-block',"margin-left": "20px"} ),
    
#                     ], style={'width': '100%', 'display': 'flex', 'justifyContent':'center'}),
                    
#                 html.Br(),
#                 html.Br(),
#                 blocks(df),
#                 html.Br(),
#                 html.Br(),
#                 dcc.Graph(id='lineplots',figure = fig,), 

#                 html.Footer(['© 2021 by Center for Analytics and Data Science (CADS) - Data Analytics Research Team (DART), Bentley University are licensed under ',
#                         dcc.Link('CC BY 4.0', href='https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1', target='CC BY 4.0'),
#                         html.Img(src=app.get_asset_url("1.png")),
#                         html.Img(src=app.get_asset_url("2.png"))])
#             ]
#     )      


# In[ ]:





# In[ ]:





# In[52]:


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
                        dcc.Input(id="input Target", type='text', placeholder="Acetylcholinesterase or AD and amyloid or amyloid beta-protein precursor or Amyloid plaques or amyloid precursor protein or secretases or apolipoproteins-e or Presenilins or receptors, n-methyl-d-aspartate or tau proteins or TDP-43",style={ 'font-size': '16px','display': 'inline-block',"margin-right": "20px"}, ),
                        html.Div(id='target_output',style={ 'font-size': '16px','display': 'inline-block'},),
                        dcc.Input(id="input Drug", type='text', placeholder="Aducanumab or Bapineuzumab or Crenezumab or Gantenerumab or Solanezumab",style={ 'font-size': '16px','display': 'inline-block'} ),
                        html.Div(id='drug_output',style={ 'font-size': '16px','display': 'inline-block',"margin-right": "20px"},),                     
                             ], style={'display': 'inline-block',"margin-left": "20px",} ),
                    html.Br(),
                    html.Br(),
                    html.Div([html.Button(id='tab1_submit', type='submit', children='Submit'), ],style={'display': 'inline-block', 'align-items': 'center', 'justify-content': 'center',})
    
                    ], style={'textAlign': 'center','align-items': 'center', 'justify-content': 'center',}),
                    
                html.Br(),
                html.Br(),
                blocks(df),
                html.Br(),
                dcc.Graph(id='lineplots',figure = fig,), 

                html.Footer(['© 2021 by Center for Analytics and Data Science (CADS) - Data Analytics Research Team (DART), Bentley University are licensed under ',
                        dcc.Link('CC BY 4.0', href='https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1', target='CC BY 4.0'),
                        html.Img(src=app.get_asset_url("1.png")),
                        html.Img(src=app.get_asset_url("2.png"))])
            ]
    )      


# In[53]:


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
                            html.Div([dcc.Graph(id="top_10_ins_barplot1", figure = fig2_1_1)], style = {'width': '70%', 'display': 'block', 'margin-left':'15%','margin-right':'15%'}),
                            html.Div([dcc.Graph(id="top_10_ins_barplot2", figure = fig2_1_2)], style = {'width': '70%', 'display': 'block', 'margin-left':'15%','margin-right':'15%'}),
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
                                     style={'width': '100%', 'display': 'flex', 'justifyContent':'center'}
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


# In[54]:


def tab3():                                       
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
                            dcc.Graph(id='tab3_barplots1',figure = fig3_1_1)],
                            style = {'width': '70%', 'display': 'inline-block', 'margin-left':'15%','margin-right':'15%'}),
                        html.Div([
                            dcc.Graph(id='tab3_barplots2',figure = fig3_1_2)],
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
                    
                                    dcc.Graph(id="selected_pro_barplot1", figure = fig3_2_1),],
                                    style = {'width': '70%', 'display': 'block', 'margin-left':'15%','margin-right':'15%'}),
                         html.Div([ 
                    
                                    dcc.Graph(id="selected_pro_barplot2", figure = fig3_2_2),],
                                    style = {'width': '70%', 'display': 'block', 'margin-left':'15%','margin-right':'15%'}),
                            html.Div([ 
                                    dcc.Graph(id="selected_pro_lineplot1", figure = fig3_3_1),
                            ],
                                    style = {'width': '70%', 'display': 'block', 'margin-left':'15%','margin-right':'15%'}),

                        html.Div([ 
                                     dcc.Graph(id="selected_pro_lineplot2", figure = fig3_3_2),  
                            ],style = {'width': '70%', 'display': 'block', 'margin-left':'15%','margin-right':'15%'}
                                    ),
                        html.Footer(['© 2021 by Center for Analytics and Data Science (CADS) - Data Analytics Research Team (DART), Bentley University are licensed under ',
                                    dcc.Link('CC BY 4.0', href='https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1', target='CC BY 4.0'),
                                    html.Img(src=app.get_asset_url("1.png")),
                                    html.Img(src=app.get_asset_url("2.png"))])
                    ],
                        
                    )


# In[55]:


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


# In[56]:


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
                                dcc.Input(id="Name", type='text', placeholder="Name",style={ 'font-size': '16px',} ),], 
                                style={'display': 'inline-block', "margin-right": "20px"} ),
                            html.Div([
                                html.P("Affiliation:", style={'font-size': '16px',}),
                                dcc.Input(id="Affiliation", type='text', placeholder="Affiliation",style={ 'font-size': '16px',} ),], 
                                style={'display': 'inline-block', "margin-right": "20px"} ),
                            html.Div([
                                html.P("Email:", style={'font-size': '16px',}),
                                dcc.Input(id="Email", type='text', placeholder="Email",style={ 'font-size': '16px',} ),], 
                                style={'display': 'inline-block', "margin-right": "20px"} ),
                            html.Div([
                                html.P("Purpose:", style={'font-size': '16px',}),
                                dcc.Checklist(options=[
                                    {'label': 'Research', 'value': 'Research'},
                                    {'label': 'Teaching', 'value': 'Teaching'},
                                    {'label': 'News/Report', 'value': 'News/Report'},
                                    {'label': 'Government Service', 'value': 'Government Service'},
                                    {'label': 'Other', 'value': 'Other'}
                                ],
                                    value=[],labelStyle={'display': 'inline-block'}
                                )
                                
                                ], 
                                style={'display': 'inline-block', } ),
        
                    ], style={'width': '100%', 'display': 'flex', 'justifyContent':'center'}),
                        
                        html.Br(),
                     
                        
                        
                        
                        html.Div([
                            html.Button("Submit", id="Submit"),
                        ], style={'width': '100%', 'display': 'flex', 'justifyContent':'center'}),
                        
                        html.Br(),
                        
                        html.Div([
                            html.Button("Download File", id="btn_txt"),
                            dcc.Download(id="download-file")
                        ], style={'width': '100%', 'display': 'flex', 'justifyContent':'center'})
                        
                        ]
                    )


# In[57]:


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


# In[58]:


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


# In[59]:


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


# In[60]:



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


# In[61]:


@app.callback(
    Output("modal1", "is_open"),
    [Input("modal_open1", "n_clicks"), Input("modal_close1", "n_clicks")],
    [State("modal1", "is_open")],
)
def toggle_modal1(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# In[62]:


@app.callback(
    Output("modal2", "is_open"),
    [Input("modal_open2", "n_clicks"), Input("modal_close2", "n_clicks")],
    [State("modal2", "is_open")],
)
def toggle_modal2(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# In[63]:


@app.callback(
    Output("modal3", "is_open"),
    [Input("modal_open3", "n_clicks"), Input("modal_close3", "n_clicks")],
    [State("modal3", "is_open")],
)
def toggle_modal3(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# In[64]:


@app.callback(
    Output("modal4", "is_open"),
    [Input("modal_open4", "n_clicks"), Input("modal_close4", "n_clicks")],
    [State("modal4", "is_open")],
)
def toggle_modal4(n1, n2, is_open):
    if n1 or n2:
        return not is_open


# In[ ]:





# In[65]:


@app.callback(Output('target_output', 'children'),
              Input('input Target', 'value'))
def target_output_1(value):
    search_term_target = value
    return search_term_target


# In[66]:


@app.callback(Output('drug_output', 'children'),
              Input('input Drug', 'value'))
def drug_output_1(value):
    search_term_drug = value
    return search_term_drug


# In[ ]:





# In[67]:


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
    fig2_2_1.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top NIH Funded Institutes (Selected)')

    return fig2_2_1


# In[68]:


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
    fig2_2_2.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top Productive Institutes (Selected)')

    return fig2_2_2


# In[69]:


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


# In[70]:


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


# In[71]:


@app.callback(
    Output(component_id = 'selected_pro_barplot1', component_property = 'figure'),
    [Input(component_id = 'pro_selected', component_property = 'value')]
)
def update_3_2_1barplot(pro_selection):
    pro_checklist_df_total = df[df.Grant_Type_Name.isin(pro_selection)]
    
    fig3_2_1 = go.Figure([go.Bar(y=top_10_fund_proj(pro_checklist_df_total).sort_values('APY_COST_inf2018')['Grant_Type_Name'], x=top_10_fund_proj(pro_checklist_df_total).sort_values('APY_COST_inf2018')['APY_COST_inf2018'], orientation='h')])
    fig3_2_1.update_traces(marker_color='#719FB0')
    fig3_2_1.update_xaxes(title_text="Amount")
    # fig2_2_1.update_yaxes(automargin=True)
    fig3_2_1.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top NIH Funded Project Type (Selected)')

    return fig3_2_1


# In[72]:


@app.callback(
    Output(component_id = 'selected_pro_barplot2', component_property = 'figure'),
    [Input(component_id = 'pro_selected', component_property = 'value')]
)
def update_3_2_2barplot(pro_selection):
    
    pro_checklist_df_total = df[df.Grant_Type_Name.isin(pro_selection)]
    
    fig3_2_2 = go.Figure([go.Bar(y=top_10_productive_proj(pro_checklist_df_total).sort_values('PMID')['Grant_Type_Name'], x=top_10_productive_proj(pro_checklist_df_total).sort_values('PMID')['PMID'],orientation='h')])
    fig3_2_2.update_traces(marker_color='#719FB0')
    fig3_2_2.update_xaxes(title_text="PMID Count")
    # fig2_2_1.update_yaxes(automargin=True)
    fig3_2_2.update_layout(autosize=True,showlegend=False,paper_bgcolor =  'rgba(0, 0, 0, 0)', title = 'Top Productive Project Type (Selected)')

    return fig3_2_2


# In[ ]:





# In[73]:


@app.callback(
    Output(component_id = 'selected_pro_lineplot1', component_property = 'figure'),
    [Input(component_id = 'pro_selected', component_property = 'value')]
)
def update_3_3_lineplot1(pro_selection):
    pro_checklist_df_total = df[df.Grant_Type_Name.isin(pro_selection)]
    selected_pro_funding_yearly_plot_total = pro_checklist_df_total.drop_duplicates('ACTUAL_PROJECT_YEAR').groupby(by = ['Grant_Type_Name','APY']).APY_COST_inf2018.sum().reset_index()
    fig3_3_1 = px.line(selected_pro_funding_yearly_plot_total, x="APY", y="APY_COST_inf2018", color='Grant_Type_Name', title = 'Funding by Year (Selected)', labels={"Grant_Type_Name": ""})
    fig3_3_1.update_xaxes(title_text="Year")
    fig3_3_1.update_yaxes(title_text="Amount")
    fig3_3_1.update_layout(paper_bgcolor =  'rgba(0, 0, 0, 0)')

    return fig3_3_1


# In[74]:


@app.callback(
    Output(component_id = 'selected_pro_lineplot2', component_property = 'figure'),
    [Input(component_id = 'pro_selected', component_property = 'value')]
)
def update_3_3_lineplot2(pro_selection):
    pro_checklist_df_total = df[df.Grant_Type_Name.isin(pro_selection)]
    selected_pro_pmid_count_year_plot_total = pro_checklist_df_total.groupby(by = ['Grant_Type_Name','PUB_YEAR']).PMID.nunique().reset_index()
    
    fig3_3_2 = px.line(selected_pro_pmid_count_year_plot_total, x="PUB_YEAR", y="PMID", color='Grant_Type_Name', title = 'PMID Count by Year (Selected)', labels={"Grant_Type_Name": ""})
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





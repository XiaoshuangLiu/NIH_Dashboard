#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
import dash_core_components as dcc
import dash_html_components as html
# from dash.dependencies import Input, Output, ClientsideFunction
# import plotly.express as px
import numpy as np
import pandas as pd
# import pathlib
# import matplotlib.pyplot as plt
# import seaborn as sns
# import dash_table
# import textwrap


# In[2]:


app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "NIH contribution to research "
server = app.server
app.config["suppress_callback_exceptions"] = True


# In[3]:


df = pd.read_csv('data/avg_cost_df.csv' )
df 


# In[4]:


df['new_name'] = df['full_institute_name']+'('+df['Acronym_institute_name']+')'
df


# In[5]:


def unique_pmid(df):
    total = df.PMID.nunique()
    total = '{:,}'.format(total)
    return total


# In[6]:


def unique_project(df):
    total = df.PROJECT_NUMBER.nunique()
    total = '{:,}'.format(total)
    return total


# In[7]:


def apy(df):
    total = df.ACTUAL_PROJECT_YEAR.nunique()
    total = '{:,}'.format(total)
    return total


# In[8]:


def total_funding(df):
    total = df.avg_cost.sum()
    total = '${:,}'.format(total)
    return total


# In[9]:


def pmid_count_year_plot(df):
    new_df = df[df.PROJECT_NUMBER.notnull()].groupby('APY').PMID.nunique().reset_index()
    return new_df  


# In[10]:


def project_count_year_plot(df):
    new_df = df[df.PROJECT_NUMBER.notnull()].groupby('APY').PROJECT_NUMBER.nunique().reset_index()
    return new_df  


# In[11]:


def funding_yearly_plot(df):
    new_df = df.groupby('APY')['avg_cost'].sum().reset_index()
    return new_df    


# In[12]:


# new_df = df.groupby('APY')['ACTUAL_PROJECT_YEAR'].nunique().reset_index()
# new_df


# In[13]:


def APY_yearly_plot(df):
    new_df = df.groupby('APY')['ACTUAL_PROJECT_YEAR'].nunique().reset_index()
    return new_df 


# In[14]:


def top_10_fund_ins(df):
    top10_cost_ins_total = df.groupby('Acronym_institute_name')['avg_cost'].sum().reset_index().sort_values(by = 'avg_cost',ascending = False)
    top10_cost_ins_total['apy'] = df.groupby('Acronym_institute_name')['ACTUAL_PROJECT_YEAR'].nunique().reset_index().ACTUAL_PROJECT_YEAR
    top10_cost_ins_total['apy%'] = (top10_cost_ins_total.apy / top10_cost_ins_total.apy.sum() * 100).round(2)
    top10_cost_ins_total = top10_cost_ins_total.sort_values('avg_cost',ascending = False)
    top10_productive_ins_total = df.groupby('Acronym_institute_name')['PMID'].nunique().reset_index().sort_values(by = 'PMID',ascending = False)
    top10_cost_ins_total.merge(top10_productive_ins_total, on = 'Acronym_institute_name')
    return top10_cost_ins_total.sort_values('avg_cost',ascending = False).head(10)


# In[15]:


def top_10_productive_ins(df):
    top10_productive_ins_total = df.groupby('Acronym_institute_name')['PMID'].nunique().reset_index().sort_values(by = 'PMID',ascending = False)
    return top10_productive_ins_total.sort_values('PMID',ascending = False).head(10)


# In[16]:


def top_10_fund_proj(df):
    top10_cost_proj_total = df.groupby('PROJECT_NUMBER')['avg_cost'].sum().reset_index().sort_values(by = 'avg_cost',ascending = False)
    return top10_cost_proj_total.head(10)


# In[17]:


def top_10_productive_proj(df):
    top10_productive_proj_total = df.groupby('PROJECT_NUMBER')['PMID'].nunique().reset_index().sort_values(by = 'PMID',ascending = False)
    return top10_productive_proj_total.head(10)


# In[18]:


def build_banner():
    return html.Div(
            id="header",
            children=[
                html.H3(
                    id='herder-title',
                    children="NIH Contribution to Research"),
                html.P(
                    id="description",
                    children=dcc.Markdown(
                        children=(
                            '''
                            The analysis identifies NIH funding that contributed to publications directly related to two components of this product.''',
                        )
                    )
                )
            ]
        )


# In[19]:


def blocks(df):
    return html.Div([
               html.Div(children=[html.H4("Total Funding", style={'textAlign': 'center', 'fontWeight': 'bold', 'color': '#6A6567','padding': '1rem'},),
                        html.H2(style={'color': '#823737'}, children=['{}'.format(total_funding(df)),])],
                        className="box1", style={
                            'backgroundColor':'#D6D5C3',
                            'height':'200px',
                            'margin-left':'10px',
                            'width':'24%',
                            'text-align':'center',
                            'display':'inline-block'
                            }),

                html.Div(children=[html.H4("Unique Project", style={'textAlign': 'center', 'fontWeight': 'bold', 'color': '#6A6567','padding': '1rem'},),
                        html.H2(style={'color': '#823737'}, children=['{}'.format(unique_project(df)),])],
                         className="box2", style={
                            'backgroundColor':'#FFF0E0',
                            'height':'200px',
                            'margin-left':'10px',
                            'text-align':'center',
                            'width':'24%',
                            'display':'inline-block'
                           },
                        
                        ),
                html.Div(children=[html.H4("Unique PMID", style={'textAlign': 'center', 'fontWeight': 'bold', 'color': '#6A6567','padding': '1rem'},),
                        html.H2(style={'color': '#823737'}, children=['{}'.format(unique_pmid(df)),])],
                        className="box2", style={
                                'backgroundColor':'#F7D7D7',
                                'height':'200px',
                                'margin-left':'10px',
                                'text-align':'center',
                                'width':'24%',
                                'display':'inline-block'
                               }),
                html.Div(children=[html.H4("Total APY", style={'textAlign': 'center', 'fontWeight': 'bold', 'color': '#6A6567','padding': '1rem'},),
                        html.H2(style={'color': '#823737'}, children=['{}'.format(apy(df)),])],
                         className="box2", style={
                                'backgroundColor':'#D3DFF6',
                                'height':'200px',
                                'margin-left':'10px',
                                'text-align':'center',
                                'width':'24%',
                                'display':'inline-block'
                               }),
                            ])


# In[20]:


def description_card():
    """
    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
#             html.H5("NIH Funded Institute"),
#             html.H3("Welcome to the Dashboard"),
            html.Div(
                id="intro",
                children="This page summarizes the information of NIH's contribution to Institutions. By selecting the insititutes you are insterested, you can find the funding it received from NIH and the rearch achievement they made.",
            ),
        ],
    )


# In[21]:


from plotly.subplots import make_subplots
import plotly.graph_objects as go

# tab 1 lineplot
fig = make_subplots(
    rows=1, cols=4, subplot_titles=("NIH Contribution to Research by Year", "Project Count by Year", "PMID by Year", "APY by Year")
)

# Add traces
fig.add_trace(go.Scatter(x=funding_yearly_plot(df)['APY'], y=funding_yearly_plot(df)['avg_cost']), row=1, col=1)
fig.add_trace(go.Scatter(x=project_count_year_plot(df)['APY'], y=project_count_year_plot(df)['PROJECT_NUMBER']), row=1, col=2)
fig.add_trace(go.Scatter(x=pmid_count_year_plot(df)['APY'], y=pmid_count_year_plot(df)['PMID']), row=1, col=3)
fig.add_trace(go.Scatter(x=APY_yearly_plot(df)['APY'], y=APY_yearly_plot(df)['ACTUAL_PROJECT_YEAR']), row=1, col=4)

# Update xaxis properties
fig.update_xaxes(title_text="Year", row=1, col=1)
fig.update_xaxes(title_text="Year", row=1, col=2)
fig.update_xaxes(title_text="Year", row=1, col=3)
fig.update_xaxes(title_text="Year", row=1, col=4)

# Update yaxis properties
fig.update_yaxes(title_text="Amount", row=1, col=1)
fig.update_yaxes(title_text="Count", row=1, col=2)
fig.update_yaxes(title_text="Count", row=1, col=3)
fig.update_yaxes(title_text="Count", row=1, col=4)

fig.update_layout(showlegend=False)

# Update title and height
# fig.update_layout(title_text="Customizing Subplot Axes", height=700)

# fig.show()


# In[22]:


from plotly.subplots import make_subplots
import plotly.graph_objects as go

# tab 2 barplot
fig2 = make_subplots(
    rows=1, cols=2, subplot_titles=("Top 10 NIH Funded Institutes", "Top 10 Productive Institutes")
)

# Add traces
# fig2.add_trace(go.Bar(y=top_10_fund_ins(df)['full_institute_name'], x=top_10_fund_ins(df)['avg_cost'], orientation='h'), row=1, col=1)
# fig2.add_trace(go.Bar(y=top_10_productive_ins(df)['full_institute_name'], x=top_10_productive_ins(df)['PMID'],orientation='h'), row=1, col=2)


fig2.add_trace(go.Bar(x=top_10_fund_ins(df)['Acronym_institute_name'], y=top_10_fund_ins(df)['avg_cost']), row=1, col=1)
fig2.add_trace(go.Bar(x=top_10_productive_ins(df)['Acronym_institute_name'], y=top_10_productive_ins(df)['PMID']), row=1, col=2)


fig2.update_traces(marker_color='#C99171',row=1, col=1)
fig2.update_traces(marker_color='#878F6F',row=1, col=2)

# Update xaxis properties
fig2.update_yaxes(title_text="Amount", row=1, col=1)
fig2.update_yaxes(title_text="PMID count", row=1, col=2)


# Update yaxis properties
# fig2.update_yaxes(title_text="Institutes", row=1, col=1)
# fig2.update_yaxes(title_text="Institutes", row=1, col=2)

fig2.update_layout(autosize=False,width=1600,height=500,showlegend=False)

# Update title and height
# fig.update_layout(title_text="Customizing Subplot Axes", height=700)

fig2.show()


# In[23]:



# ins__checklist = ['National Cancer Institute', 'National Human Genome Research Institute','Food and Drug Administration']
# in_checklist_df = df[df.full_institute_name.isin(ins__check_list)]
# in_checklist_funding_plot = funding_yearly_plot(in_checklist_df)
# in_checklist_funding_plot

# project_count_year_plot(in_checklist_df)


# In[24]:


# tab 2-2 lineplot
# ins__check_list = df['full_institute_name'].drop_duplicates()

ins__checklist = ['National Cancer Institute', 'National Human Genome Research Institute','Food and Drug Administration']
in_checklist_df = df[df.full_institute_name.isin(ins__checklist)]

   
fig22 = make_subplots(
    rows=2, cols=1, subplot_titles=("Funding by Year", "PMID Count by Year")
)

# Add traces
fig22.add_trace(go.Scatter(y=funding_yearly_plot(in_checklist_df)['avg_cost'], x=funding_yearly_plot(in_checklist_df)['APY']), row=1, col=1)
fig22.add_trace(go.Scatter(y=pmid_count_year_plot(in_checklist_df)['PMID'], x=pmid_count_year_plot(in_checklist_df)['APY']), row=2, col=1)


# Update xaxis properties
fig22.update_xaxes(title_text="Year", row=1, col=1)
fig22.update_xaxes(title_text="Year", row=2, col=1)

# Update yaxis properties
fig22.update_yaxes(title_text="Amount", row=1, col=1)
fig22.update_yaxes(title_text="PMID count", row=2, col=1)

fig22.update_layout(autosize=False,width=1600,height=500,showlegend=False)

# Update title and height
# fig.update_layout(title_text="Customizing Subplot Axes", height=700)

fig22.show()


# In[25]:


# tab 3 barplot
fig3 = make_subplots(
    rows=1, cols=2, subplot_titles=("Top 10 NIH Funded Projects", "Top 10 Productive Projects")
)

# Add traces
fig3.add_trace(go.Bar(y=top_10_fund_proj(df).sort_values('avg_cost')['PROJECT_NUMBER'], x=top_10_fund_proj(df).sort_values('avg_cost')['avg_cost'], orientation='h'), row=1, col=1)
fig3.add_trace(go.Bar(y=top_10_productive_proj(df).sort_values('PMID')['PROJECT_NUMBER'], x=top_10_productive_proj(df).sort_values('PMID')['PMID'],orientation='h'), row=1, col=2)

fig3.update_traces(marker_color='#C99171',row=1, col=1)
fig3.update_traces(marker_color='#878F6F',row=1, col=2)
# Update xaxis properties2
fig3.update_xaxes(title_text="Amount", row=1, col=1)
fig3.update_xaxes(title_text="PMID count", row=1, col=2)

# Update yaxis properties
# fig2.update_yaxes(title_text="Institutes", row=1, col=1)
# fig2.update_yaxes(title_text="Institutes", row=1, col=2)

# fig3.update_layout(autosize=False,width=1600,height=500,showlegend=False)

# Update title and height
# fig.update_layout(title_text="Customizing Subplot Axes", height=700)
fig3.update_layout(showlegend=False)
fig3.show()


# In[26]:


# top_10_fund_proj(df).head(10)


# In[27]:


# top_10_productive_proj(df).head(10)


# In[28]:


# top_10_productive_proj(df).head(10).plot(kind='barh')


# In[29]:


ins_list = df['new_name'].drop_duplicates()
# ins_list


# In[30]:


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


# In[31]:


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
                html.I("Please select:"),
                dcc.Dropdown(
                    id = 'overview_dropdown',
                    options = [{'label': 'Both Target and Drug', 'value': 'total'  },
                              {'label': 'Target', 'value': 'target'},
                              {'label': 'Drug', 'value': 'Drug'}],
                    value = 'total'

                ),
                html.Br(),
                html.Br(),
                blocks(df),
                html.Br(),
                html.Br(),
                dcc.Graph(id='lineplots',figure = fig,),                             
            ]
        )


# In[32]:


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
                            html.Div(
                                    id="app-container_tab2",
                                    children=[
                                        # Left column
                                        html.Div(
                                            id="left-column",
                                            className="three columns",
                                            children=[description_card(), 
                                                        html.P("Select Institute", style={'textAlign': 'left','font-weight': 'bold'}),
                                                        dcc.Checklist(
                                                            id="ins_selected",
                                                            options=[{"label": i, "value": i} for i in ins_list],
                                                            value=ins_list[:],
                #                                             style={"display":"inline-flex", "flex-wrap":"wrap", "line-height":"28px"},
                                                        ), 
                                                     ],),
                                         html.Br(),
                                        # Right column
                                        html.Div(
                                            id="right-column",
                                            className="nine columns",
                                            children=[
                                                # popularity barplot
                                                html.Div(
                                                    id="barplot_section",
                                                    children=[
                                                        html.B("Overview"),
                                                        html.Hr(),
                                                        dcc.Graph(id="top_10_ins_barplot", figure = fig2),
                                                    ],
                                                ),
                                                 html.Br(),
                                                # top 10 track table
                                                html.Div(
                                                    id="table_section",
                                                    children=[
                                                        html.B("Selected institutes"),
                                                        html.Hr(),
                                                        dcc.Graph(id="selected_ins_lineplot", figure = fig22),
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ]
                                        )
                    ])


# In[33]:


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
                        dcc.Graph(id='tab3_barplots',figure = fig3),]
                    )


# In[34]:


app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),
        
        html.I("Please type the Target here, for example: CAR_T  "),
        dcc.Input(id="input1", type="text", placeholder="CAR_T",  value = '',style={'marginRight':'10px'}),
        html.Br(),
        html.I("Please enter the Drug you are interested here, for example: BCell  "),
#         html.I("Please enter the Drug you are interested here, for example: BCell  "),
        dcc.Input(id="input2", type="text", placeholder="BCell",  value = '',style={'marginRight':'10px'}),
        html.Br(),
        html.Br(),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                id="tabs",
                className="tabs",
                children=[dcc.Tabs(id="app-tabs",
                                    value="tab1",
                                    className="custom-tabs",
                                   colors={
        "border": "#6B95B",
#         "primary": "gold",
        "background": "#ACCCDD"},
                                    children=[tab1(), 
                                              tab2(), 
                                              tab3()]
                                  )
                         ]
                )])])


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





# In[ ]:





# In[ ]:





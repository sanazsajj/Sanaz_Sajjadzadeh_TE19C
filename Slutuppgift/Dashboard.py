import dash
from dash_html_components.Figure import Figure
import plotly.express as px
import pandas as pd
import dash_html_components as HTML
import dash_core_components as dcc
from dash.dependencies import Output, Input

app = dash.Dash(__name__)

#Läser in filerna som behövs
sverige_df = pd.read_csv("Regional_Daily_Cases.csv")
ålder_df = pd.read_csv("National_Total_Deaths_by_Age_Group.csv")

#Skapar variablar med informationen som behövs
antal = [ålder_df.head(6)["Total_Deaths"].sum(), ålder_df.iloc[6:10]["Total_Deaths"].sum()]
labels = ["Antal döda inte i riskgruppen", "Antal döda i riskgruppen"]
antal2 = [ålder_df["Total_ICU_Admissions"].sum(), ålder_df["Total_Deaths"].sum()]
labels2 = ["Kritisk vård", "Antal döda"]

#Skapar ett linjediagram
fig_line = px.line(sverige_df, x="Date", y="Sweden_Total_Daily_Cases")
fig_line.update_layout(
    title="Antal sjuka varje dag i Sverige",
    xaxis_title="Datum",
    yaxis_title="Antal sjuka")

fig_line.update_traces(
    line_color="purple")

#Skapar ett stapeldiagram
fig_bar = px.bar(ålder_df, x="Age_Group", y="Total_Cases")
fig_bar.update_layout(
    title="Antal sjuka för varje åldersgrupp",
    xaxis_title="Åldersgrupper",
    yaxis_title="Antal sjuka")

fig_bar.update_traces(
    marker_color="pink")

#Skapar ett stapeldiagram
fig_bar2 = px.bar(ålder_df, x=antal2, y=labels2)
fig_bar2.update_layout(
    title="Behövde kritisk vård/Antal döda",
    xaxis_title="Antal människor",
    yaxis_title = "")

fig_bar2.update_traces(
    marker_color=["purple", "pink"])

#Skapar ett cirkeldiagram
fig_pie = px.pie(ålder_df, values=antal, names=labels, color=labels, color_discrete_map={"Antal döda inte i riskgruppen":"pink",
"Antal döda i riskgruppen":"purple"})
fig_pie.update_layout(
    title="Antal döda i riskgruppen/inte i riskgruppen")

#Lägger in alla diagram i en lista
fig = [fig_line, fig_bar, fig_bar2, fig_pie]

app.layout = HTML.Div(children=[
    HTML.H1(children= "Statistik för covid-19"), #Ger dashboarden en titel

    #Skapar en dropdown
    dcc.Dropdown(
    id="drop",
    options = [dict(label = "Antal sjuka varje dag i Sverige", value="Antal sjuka varje dag i Sverige"),
                dict(label= "Antal sjuka för varje åldersgrupp", value="Antal sjuka för varje åldersgrupp"),
                dict(label= "Behövde kritisk vård/Antal döda", value="Behövde kritisk vård/Antal döda"),
                dict(label= "Antal döda i riskgruppen/inte i riskgruppen", value="Antal döda i riskgruppen/inte i riskgruppen")],
                value="Antal sjuka varje dag i Sverige",
                searchable = False, #Gör så att man inte kan söka i dropdownen
                clearable=False), #Gör så att man inte kan ta bort det i dropdownen
                
    dcc.Graph(
    id="graph", 
    figure = fig
    )
])

@app.callback(
    Output("graph", "figure",),
    [Input("drop", "value")]
)

#Skapar en funktion med en if-sats
def update_figure(value):
    #If-sats där en graf visas beroende på vad man väljer i dropdownen
    if value == "Antal sjuka varje dag i Sverige": 
        return fig[0] #Visar den första grafen i listan

    elif value == "Antal sjuka för varje åldersgrupp":
        return fig [1] #Visar den andra grafen i listan

    elif value == "Behövde kritisk vård/Antal döda":
        return fig [2] #Visar den tredje grafen i listan

    elif value == "Antal döda i riskgruppen/inte i riskgruppen":
        return fig [3] #Visar den sista grafen i listan


if __name__ == "__main__":
    app.run_server()
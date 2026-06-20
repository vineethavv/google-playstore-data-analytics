import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pytz

# PAGE CONFIG

st.set_page_config(
    page_title="Google Play Store Reviews Analytics",
    layout="wide"
)

# DARK THEME

st.markdown("""
<style>

.stApp {
    background-color: #050816;
    color: white;
}

.block-container {
    padding-top: 110px;
    padding-left: 2rem;
    padding-right: 2rem;
}

header {
    visibility: hidden;
}

h1, h2, h3 {
    color: white !important;
}

/* FIXED NAVBAR */

.navbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 80px;
    background-color: #111111;
    display: flex;
    align-items: center;
    padding-left: 20px;
    z-index: 999999;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.7);
}

.nav-title {
    color: white;
    font-size: 34px;
    font-weight: bold;
    margin-left: 20px;
}

</style>
""", unsafe_allow_html=True)

# NAVBAR

st.markdown("""
<div class="navbar">

<img src="https://upload.wikimedia.org/wikipedia/commons/7/78/Google_Play_Store_badge_EN.svg"
width="140">

<div class="nav-title">
Google Play Store Reviews Analytics
</div>

</div>
""", unsafe_allow_html=True)

# LOAD DATASETS

apps_df = pd.read_csv("Play Store Data.csv")
reviews_df = pd.read_csv("User Reviews.csv")
#st.write(reviews_df.columns.tolist())

# CLEAN APPS DATA

apps_df.drop_duplicates(inplace=True)

apps_df["Rating"] = pd.to_numeric(
    apps_df["Rating"],
    errors="coerce"
)

apps_df["Reviews"] = pd.to_numeric(
    apps_df["Reviews"],
    errors="coerce"
)

# INSTALLS

apps_df["Installs"] = (
    apps_df["Installs"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.replace("+", "", regex=False)
)

apps_df["Installs"] = pd.to_numeric(
    apps_df["Installs"],
    errors="coerce"
)

# PRICE

apps_df["Price"] = (
    apps_df["Price"]
    .astype(str)
    .str.replace("$", "", regex=False)
)

apps_df["Price"] = pd.to_numeric(
    apps_df["Price"],
    errors="coerce"
).fillna(0)

# SIZE CONVERSION

def convert_size(size):

    try:

        size = str(size)

        if "M" in size:
            return float(size.replace("M", ""))

        elif "k" in size:
            return float(size.replace("k", "")) / 1024

        else:
            return np.nan

    except:
        return np.nan

apps_df["Size_MB"] = apps_df["Size"].apply(convert_size)

# REVENUE

apps_df["Revenue"] = (
    apps_df["Installs"] * apps_df["Price"]
)

# DATE

apps_df["Last Updated"] = pd.to_datetime(
    apps_df["Last Updated"],
    errors="coerce"
)

# ANDROID VERSION

apps_df["Android Ver"] = (
    apps_df["Android Ver"]
    .astype(str)
    .str.extract(r'(\d+\.\d+)')[0]
)

apps_df["Android Ver"] = pd.to_numeric(
    apps_df["Android Ver"],
    errors="coerce"
)

# CLEAN REVIEWS DATA

reviews_df["Sentiment_Subjectivity"] = pd.to_numeric(
    reviews_df["Sentiment_Subjectivity"],
    errors="coerce"
)

st.header("Project Dashboard")

tab1, tab2 = st.tabs(["Training Tasks", "Internship Tasks"])

with tab1:
    apps_df = apps_df.dropna(subset=['Rating'])
    #Figure 1
    category_counts=apps_df['Category'].value_counts().nlargest(10)
    fig1=px.bar(
    x=category_counts.index,
    y=category_counts.values,
    labels={'x':'Category','y':'Count'},
    title='Top Categories on Play Store',
    color=category_counts.index,
    color_discrete_sequence=px.colors.sequential.Plasma,
    width=400,
    height=300
    )
    fig1.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    title_font={'size':16},
    xaxis=dict(title_font={'size':12}),
    yaxis=dict(title_font={'size':12}),
    margin=dict(l=10,r=10,t=30,b=10)
    )
    #fig1.update_traces(marker=dict(pattern=dict(line=dict(color='white',width=1))))
    st.plotly_chart(fig1, width="stretch")

    #Figure 2
    type_counts=apps_df['Type'].value_counts()
    fig2=px.pie(
    values=type_counts.values,
    names=type_counts.index,
    title='App Type Distribution',
    color_discrete_sequence=px.colors.sequential.RdBu,
    width=400,
    height=300
    )
    fig2.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    title_font={'size':16},
    margin=dict(l=10,r=10,t=30,b=10)
    )
    #fig1.update_traces(marker=dict(pattern=dict(line=dict(color='white',width=1))))
    st.plotly_chart(fig2, width="stretch")

    #Figure 3
    fig3=px.histogram(
    apps_df,
    x='Rating',
    nbins=20,
    title='Rating Distribution',
    color_discrete_sequence=['#636EFA'],
    width=400,
    height=300
    )
    fig3.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    title_font={'size':16},
    xaxis=dict(title_font={'size':12}),
    yaxis=dict(title_font={'size':12}),
    margin=dict(l=10,r=10,t=30,b=10)
    )
    #fig1.update_traces(marker=dict(pattern=dict(line=dict(color='white',width=1))))
    st.plotly_chart(fig3, width="stretch")

    #Figure 4
    sentiment_counts = reviews_df['Sentiment'].value_counts()
    fig4=px.bar(
    x=sentiment_counts.index,
    y=sentiment_counts.values,
    labels={'x':'Sentiment Score','y':'Count'},
    title='Sentiment Distribution',
    color=sentiment_counts.index,
    color_discrete_sequence=px.colors.sequential.RdPu,
    width=400,
    height=300
    )
    fig4.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    title_font={'size':16},
    xaxis=dict(title_font={'size':12}),
    yaxis=dict(title_font={'size':12}),
    margin=dict(l=10,r=10,t=30,b=10)
    )
    #fig1.update_traces(marker=dict(pattern=dict(line=dict(color='white',width=1))))
    st.plotly_chart(fig4, width="stretch")

    #Figure 5
    installs_by_category=apps_df.groupby('Category')['Installs'].sum().nlargest(10)
    fig5=px.bar(
    x=installs_by_category.index,
    y=installs_by_category.values,
    orientation='h',
    labels={'x':'Installs','y':'Category'},
    title='Installs by Category',
    color=installs_by_category.index,
    color_discrete_sequence=px.colors.sequential.Blues,
    width=400,
    height=300
    )
    fig5.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    title_font={'size':16},
    xaxis=dict(title_font={'size':12}),
    yaxis=dict(title_font={'size':12}),
    margin=dict(l=10,r=10,t=30,b=10)
    )
    #fig1.update_traces(marker=dict(pattern=dict(line=dict(color='white',width=1))))
    st.plotly_chart(fig5, width="stretch")

    # Updates Per Year Plot
    updates_per_year = apps_df['Last Updated'].dt.year.value_counts().sort_index()

    fig6 = px.line(
    x=updates_per_year.index,
    y=updates_per_year.values,
    labels={'x': 'Year', 'y': 'Number of Updates'},
    title='Number of Updates Over the Years',
    color_discrete_sequence=['#AB63FA'],
    width=400,
    height=300
    )

    fig6.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    title_font={'size':16},
    xaxis=dict(title_font={'size':12}),
    yaxis=dict(title_font={'size':12}),
    margin=dict(l=10,r=10,t=30,b=10)
    )

    st.plotly_chart(fig6, width="stretch")

    #Figure 7
    revenue_by_category = apps_df.groupby('Category')['Revenue'].sum().nlargest(10)

    fig7 = px.bar(
    x=revenue_by_category.index,
    y=revenue_by_category.values,
    labels={'x':'Category','y':'Revenue'},
    title='Revenue by Category',
    color=revenue_by_category.index,
    color_discrete_sequence=px.colors.sequential.Greens,
    width=400,
    height=300
    )

    fig7.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    title_font={'size':16},
    xaxis=dict(title_font={'size':12}),
    yaxis=dict(title_font={'size':12}),
    margin=dict(l=10,r=10,t=30,b=10)
    )

    st.plotly_chart(fig7, width="stretch")

    #Figure 8
    genre_counts = apps_df['Genres'].str.split(';', expand=True).stack().value_counts().nlargest(10)

    fig8 = px.bar(
    x=genre_counts.index,
    y=genre_counts.values,
    labels={'x':'Genre','y':'Count'},
    title='Top Genres',
    color=genre_counts.index,
    color_discrete_sequence=px.colors.sequential.OrRd,
    width=400,
    height=300
    )

    fig8.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    title_font={'size':16},
    xaxis=dict(title_font={'size':12}),
    yaxis=dict(title_font={'size':12}),
    margin=dict(l=10,r=10,t=30,b=10)
    )

    st.plotly_chart(fig8, width="stretch")

    #Figure 9
    fig9=px.scatter(
    apps_df,
    x='Last Updated',
    y='Rating',
    color='Type',
    title='Impact of Last Update on Rating',
    color_discrete_sequence=px.colors.qualitative.Vivid,
    width=400,
    height=300
    )
    fig9.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    title_font={'size':16},
    xaxis=dict(title_font={'size':12}),
    yaxis=dict(title_font={'size':12}),
    margin=dict(l=10,r=10,t=30,b=10)
    )
    #fig1.update_traces(marker=dict(pattern=dict(line=dict(color='white',width=1))))
    st.plotly_chart(fig9, width="stretch")

    #Figure 10
    fig10=px.box(
    apps_df,
    x='Type',
    y='Rating',
    color='Type',
    title='Rating for Paid vs Free Apps',
    color_discrete_sequence=px.colors.qualitative.Pastel,
    width=400,
    height=300
    )
    fig10.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    title_font={'size':16},
    xaxis=dict(title_font={'size':12}),
    yaxis=dict(title_font={'size':12}),
    margin=dict(l=10,r=10,t=30,b=10)
    )
    #fig1.update_traces(marker=dict(pattern=dict(line=dict(color='white',width=1))))
    st.plotly_chart(fig10, width="stretch")

with tab2:

    # MERGE DATASETS

    merged_df = pd.merge(
        apps_df,
        reviews_df,
        on="App",
        how="left"
    )

    # CATEGORY TRANSLATIONS
    translation_map = {
        "BEAUTY": "सौंदर्य",
        "BUSINESS": "வணிகம்",
        "DATING": "Partnersuche",
        "TRAVEL_AND_LOCAL": "Voyage et Local",
        "PRODUCTIVITY": "Productividad",
        "PHOTOGRAPHY": "写真"
    }

    merged_df["Category_Display"] = (
        merged_df["Category"].replace(translation_map)
    )

    def is_time_allowed(start_hour, end_hour):
        ist = pytz.timezone("Asia/Kolkata")
        current_hour = datetime.now(ist).hour
        return start_hour <= current_hour < end_hour

    col1, col2 = st.columns(2)
        # TASK 1 — BUBBLE CHART
    with col1:
            st.subheader("Bubble Chart")

            if is_time_allowed(17, 19):

                categories_needed = [
                    "GAME",
                    "BEAUTY",
                    "BUSINESS",
                    "COMICS",
                    "COMMUNICATION",
                    "DATING",
                    "ENTERTAINMENT",
                    "SOCIAL",
                    "EVENTS"
                ]

                df1 = merged_df[
                    (merged_df["Rating"] > 3.5) &
                    (merged_df["Reviews"] > 500) &
                    (merged_df["Installs"] > 50000) &
                    (merged_df["Sentiment_Subjectivity"] > 0.5) &
                    (~merged_df["App"].str.contains("S", case=False, na=False)) &
                    (merged_df["Category"].isin(categories_needed))
                ].copy()

                df1["Category_Display"] = df1["Category"].replace({
                    "BEAUTY": "सौंदर्य",
                    "BUSINESS": "வணிகம்",
                    "DATING": "Partnersuche"
                })


                if len(df1) > 0:

                    fig1 = px.scatter(
                        df1,
                        x="Size_MB",
                        y="Rating",
                        size="Installs",
                        color="Category_Display",
                        hover_name="App",
                        size_max=60,
                        template="plotly_white",
                        title="App Size vs Rating",
                        color_discrete_map={
                            "GAME": "pink",
                            "सौंदर्य": "#FFD700",
                            "வணிகம்": "#00FFFF",
                            "Partnersuche": "#ADFF2F"
                        }
                    )

                    fig1.update_traces(
                            marker=dict(
                            opacity=0.8,
                            line=dict(width=1, color="black")
                        )
                    )

                    fig1.update_layout(
                        xaxis_title="App Size (MB)",
                        yaxis_title="Average Rating",
                        yaxis=dict(range=[3.5, 5.0]),
                        paper_bgcolor="white",
                        plot_bgcolor="white",
                        font=dict(color="black")
                    )

                    st.plotly_chart(
                        fig1,
                        use_container_width=True
                    )

                else:
                    st.warning("No data available for selected filters.")

            else:
                st.warning("Available only between 5 PM to 7 PM IST")
    
        # TASK 2 — CHOROPLETH MAP
    with col2:
        st.subheader("Global Installs")

        if is_time_allowed(18, 20):

            df2 = merged_df.groupby(
                "Category"
            )["Installs"].sum().reset_index()

            df2 = df2[
                ~df2["Category"].str.startswith(
                    ("A", "C", "G", "S"),
                    na=False
                )
            ]

            df2 = df2.sort_values(
                by="Installs",
                ascending=False
            ).head(5)

            df2["Highlight"] = np.where(
                df2["Installs"] > 1000000,
                "Above 1M",
                "Below 1M"
            )

            countries = [
                "India",
                "United States",
                "Brazil",
                "Germany",
                "Canada"
            ]

            df2["Country"] = countries[:len(df2)]

            fig2 = px.choropleth(
                df2,
                locations="Country",
                locationmode="country names",
                color="Installs",
                hover_name="Category",
                hover_data=["Highlight"],
                template="plotly_dark",
                color_continuous_scale="Plasma",
                title="Global Installs by Category"
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

        else:
            st.warning("Available only between 6 PM to 8 PM IST")

    col3, col4 = st.columns(2)

        # TASK 3 — TIME SERIES
    with col3:
        st.subheader("Install Trends")

        if is_time_allowed(18, 21):

            df3 = merged_df[
                (~merged_df["App"].str.startswith(
                    ("x", "y", "z"),
                    na=False
                )) &
                (~merged_df["App"].str.contains(
                    "S",
                    case=False,
                    na=False
                )) &
                (merged_df["Reviews"] > 500) &
                (merged_df["Category"].str.startswith(
                    ("E", "C", "B"),
                    na=False
                ))
            ].copy()

            df3["Month"] = (
                df3["Last Updated"]
                .dt.to_period("M")
                .astype(str)
            )

            trend = df3.groupby(
                ["Month", "Category_Display"]
            )["Installs"].sum().reset_index()

            # MONTH OVER MONTH GROWTH
            trend["Growth"] = trend.groupby(
                "Category_Display"
                )["Installs"].pct_change()

            fig3 = px.line(
                trend,
                x="Month",
                y="Installs",
                color="Category_Display",
                markers=True,
                template="plotly_white",
                title="Install Trends"
            )

            # HIGHLIGHT >20% GROWTH
            growth_df = trend[
                trend["Growth"] > 0.20
            ]

            for _, row in growth_df.iterrows():

                fig3.add_vrect(
                    x0=row["Month"],
                    x1=row["Month"],
                    fillcolor="lightgreen",
                    opacity=0.3,
                    line_width=0
                )

            fig3.update_layout(
                paper_bgcolor="white",
                plot_bgcolor="white",
                font=dict(color="black")
            )

            st.plotly_chart(
                fig3,
                use_container_width=True
            )

        else:
            st.warning("Available only between 6 PM to 9 PM IST")

        # TASK 4 — STACKED AREA
    with col4:
        st.subheader("Stacked Area Chart")

        if is_time_allowed(16, 18):

            df4 = merged_df[
                (merged_df["Rating"] >= 4.2) &
                (~merged_df["App"].str.contains(
                    r"\d",
                    na=False
                )) &
                (merged_df["Reviews"] > 1000) &
                (merged_df["Size_MB"].between(20, 80)) &
                (merged_df["Category"].str.startswith(
                    ("T", "P"),
                    na=False
                ))
            ].copy()

            df4["Month"] = (
                df4["Last Updated"]
                .dt.to_period("M")
                .astype(str)
            )

            area = df4.groupby(
                ["Month", "Category_Display"]
            )["Installs"].sum().reset_index()

                # MONTH OVER MONTH GROWTH
            area["Growth"] = area.groupby(
                "Category_Display"
            )["Installs"].pct_change()

            fig4 = px.area(
                area,
                x="Month",
                y="Installs",
                color="Category_Display",
                template="plotly_white",
                title="Cumulative Installs"
            )

                # HIGHLIGHT >25% GROWTH
            growth_area = area[
                area["Growth"] > 0.25
            ]

            for _, row in growth_area.iterrows():

                fig4.add_vrect(
                    x0=row["Month"],
                    x1=row["Month"],
                    fillcolor="orange",
                    opacity=0.25,
                    line_width=0
                )

            fig4.update_layout(
                paper_bgcolor="white",
                plot_bgcolor="white",
                font=dict(color="black")
            )

            st.plotly_chart(
                fig4,
                width="stretch"
            )

        else:
            st.warning("Available only between 4 PM to 6 PM IST")

        # THIRD ROW
    col5, col6 = st.columns(2)
        # TASK 5 — GROUPED BAR
    with col5:
            st.subheader("Ratings vs Reviews")
            if is_time_allowed(15, 17):

                df5 = merged_df[
                    (merged_df["Rating"] >= 4.0) &
                    (merged_df["Size_MB"] >= 10)
                ]

                df5 = df5[
                    df5["Last Updated"].dt.month == 1
                ]

                top10 = (
                    df5.groupby("Category")["Installs"]
                    .sum()
                    .sort_values(ascending=False)
                    .head(10)
                    .index
                )

                df5 = df5[
                    df5["Category"].isin(top10)
                ]

                grouped = df5.groupby("Category").agg({
                    "Rating": "mean",
                    "Reviews": "sum"
                }).reset_index()

                fig5 = go.Figure()

                fig5.add_trace(go.Bar(
                    x=grouped["Category"],
                    y=grouped["Rating"],
                    name="Average Rating"
                ))

                fig5.add_trace(go.Bar(
                    x=grouped["Category"],
                    y=grouped["Reviews"],
                    name="Total Reviews"
                ))

                fig5.update_layout(
                    barmode="group",
                    template="plotly_dark",
                    title="Ratings vs Reviews"
                )

                st.plotly_chart(
                    fig5,
                    use_container_width=True
                )

            else:
                st.warning("Available only between 3 PM to 5 PM IST")


        # TASK 6 — DUAL AXIS
    with col6:
        st.subheader("Free vs Paid")

        if is_time_allowed(13, 14):

            df6 = merged_df[
                (merged_df["Installs"] > 10000) &
                (merged_df["Revenue"] > 10000) &
                (merged_df["Android Ver"] > 4.0) &
                (merged_df["Size_MB"] > 15) &
                (merged_df["Content Rating"] == "Everyone") &
                (merged_df["App"].str.len() <= 30)
            ]

            top3 = (
                df6.groupby("Category")["Installs"]
                .sum()
                .sort_values(ascending=False)
                .head(3)
                .index
            )

            df6 = df6[
                df6["Category"].isin(top3)
            ]

            grouped = df6.groupby("Type").agg({
                "Installs": "mean",
                "Revenue": "mean"
            }).reset_index()

            fig6 = go.Figure()

            fig6.add_trace(go.Bar(
                x=grouped["Type"],
                y=grouped["Installs"],
                name="Average Installs"
            ))

            fig6.add_trace(go.Scatter(
                x=grouped["Type"],
                y=grouped["Revenue"],
                mode="lines+markers",
                name="Revenue",
                yaxis="y2"
            ))

            fig6.update_layout(
                template="plotly_dark",
                title="Free vs Paid Apps",
                yaxis2=dict(
                    overlaying="y",
                    side="right"
                )
            )

            st.plotly_chart(
                fig6,
                width="stretch"
            )

        else:
            st.warning("Available only between 1 PM to 2 PM IST")
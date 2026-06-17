import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from matplotlib.pyplot import title
from streamlit_option_menu import option_menu
import os
import re
import io



FILE_NAME="user.csv"

def load_data(file):
    df = pd.read_csv(file)
    df["Postal Cod"] = np.where(df["Postal Cod"].isnull(), 0, df["Postal Cod"])
    return df

if not os.path.exists(FILE_NAME):
    df=pd.DataFrame(columns=["First Name","Last Name","Phone","Email","User Name","Password"])
    df.to_csv(FILE_NAME,index=False)

df=pd.read_csv(FILE_NAME)

if "logged_in" not in st.session_state:
    st.session_state["logged_in"]=False
if "username" not in st.session_state:
    st.session_state["username"]=""


if "logged_in"  in st.query_params:
   st.session_state.logged_in=True
   st.session_state.username=st.query_params.get("user","")


def signup_page():


    with st.form("Sign Up form",):

        st.header("👤 Sign Up")
        c1,c2=st.columns(2)
        firstname = c1.text_input("First Name")
        lastname = c2.text_input("Last Name")
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        username = st.text_input("User Name")
        password = st.text_input("password", type="password")
        re_password = st.text_input("Confirm Password", type="password")

        submit = st.form_submit_button("Register")

        if submit:
            if not firstname or not lastname or not phone or not email or not username or not password or not re_password:
                st.warning("Please fill all fields")
            elif password!=re_password:
                st.error("Passwords  And re_Password do not match")
            elif not re.search(r"[0-9]",password):
                st.error("Passwords Must Contain At Least One Numbers")
            elif not re.search(r"[A-Z]",password):
                st.error("Passwords Must Contain At Least One Characters")
            elif not re.search(r"[$%&*£!@?^]",password):
                st.error("Passwords Must Contain At Least One Symbols")
            elif not re.match(r"^\d{10}$",phone):
                st.error("Phone Number Must Be 10 Digits")
            elif username in df["User Name"].values:
                st.error("Username Already Exists")
            elif email in df["Email"].values:
                st.error("Email Already Exists")
            else:
                new_user={
                    "First Name":firstname,
                    "Last Name":lastname,
                    "Phone":phone,
                    "Email":email,
                    "User Name":username,
                    "Password":password,

                }
                df=pd.concat([df,pd.DataFrame([new_user])],ignore_index=True)
                df.to_csv(FILE_NAME,index=False)
                st.success("Registered Successfully")

def login_page():
    st.header("🔐 Login")

    with st.form("Login form"):
        username = st.text_input("Username")
        password = st.text_input("Password",type="password")

        submit = st.form_submit_button("Login")

        if submit:

          user=df[(df["User Name"]==username) & (df["Password"]==password)]

          if not user.empty:
             st.success("Logged in Successfully")

             st.session_state["logged_in"]=True
             st.session_state["user"]=username

             st.query_params["logged_in"]=True
             st.query_params["user"]=username

             st.rerun()


          else:
             st.warning("Enter Valid Username And Password")

def login_signup_background():
    st.markdown("""
   

   
     <style>h1,h2,h3{text-align:center;}
    
    
    
     .stApp{
    
        background-image:url("https://images.unsplash.com/photo-1707924962886-12ad20367315?q=80&w=1332&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size:cover;
        background-position:center;
        background-attachment:scroll;
    
        }
     </style>
    """,unsafe_allow_html=True)

def dashboard():

    st.set_page_config(page_title="Dashboard",layout="centered",page_icon="📊")

    with st.sidebar:
        st.markdown("---")
        st.subheader("Welcome to Intelligent Sales Analytics Dashboard📊")
        username = st.session_state.get("username", "User")
        st.markdown(f"""
        <style>
        .sidebar-footer {{
            
            position:fixed ;
            bottom: 10px;
            left: 0;
            width: 300px;
            padding: 10px;
            text-align: center;
            color: white;
           
        }}
        </style>

        <div class="sidebar-footer">
            👤 Logged in as <br><b>{username}</b>
        </div>
        """, unsafe_allow_html=True)
        st.divider()
        st.sidebar.markdown("""
            <style>h1,h2,h3{text-align:center;}
            .stApp{
                   background-image:url("https://img.freepik.com/free-vector/gradient-abstract-wireframe-background_23-2149009903.jpg?semt=ais_hybrid&w=740&q=80");
                   background-size:cover;
                   background-position:center;
                   background-attachment:inherit;
                   }
            </style>
            """, unsafe_allow_html=True)
        file = st.file_uploader("Upload Your File", type=["csv", "xlsx"])
        st.divider()
        st.title("Navigation")
        selected=option_menu("Main Menu",["Dataset","Overview","Data Visualization","Customer Insights","Sales Analysis","Data Assistant","Logout"],
                             icons=["database","graph-up",  "bar-chart-line", "people", "cash-stack", "robot", "box-arrow-right"],
                             menu_icon="grid",
                             styles={
                                 "container": {"background-color": "#03045e"},
                                 "icon":{"color":"red"},
                                 "nav-link-selected":{"background-color":"#2b9eb3","font-weight": "bold"},
                                 "nav-link":{"--hover-color": "#3e92cc"},
                                    },

                             default_index=0,
                             orientation="vertical")

    if selected=="Dataset":
        st.divider()
        st.title("Dataset Explorer")
        st.divider()
        if file is not None:
            df = load_data(file)




            col1, col2, col3 = st.columns(3)
            col1.metric("Total Rows", df.shape[0])
            col2.metric("Total Columns", df.shape[1])
            col3.metric("Total Null Values", df.isnull().sum().sum())

            st.divider()
            st.subheader("Select Columns")
            select_columns = st.multiselect("Select Columns:", df.columns, default=df.columns)
            filtered_df=df[select_columns]

            st.divider()
            st.subheader("Search datasets")
            search_value = st.text_input("search value")

            if search_value:
                filtered_df = filtered_df[
                    filtered_df.astype(str).apply(lambda row: row.str.contains(search_value, case=False).any(), axis=1)]


            st.divider()
            st.subheader("column filter")

            col1, col2 = st.columns(2)

            with col1:
                filtered_columns = st.selectbox("select columns", filtered_df.columns)
            with col2:
                filtered_value = st.selectbox("select value", filtered_df[filtered_columns].dropna().unique())
            if st.button("apply filter"):
                filtered_df = filtered_df[filtered_df[filtered_columns] == filtered_value]

            st.divider()


            st.subheader("Row Display")

            row = st.slider("select row", 0, len(filtered_df), 10)

            st.divider()
            st.subheader("Dataset Tables")

            st.dataframe(filtered_df.head(row), use_container_width=True)

            if st.checkbox("view full dataset"):
                st.subheader("Full Dataset")
                st.dataframe(filtered_df, use_container_width=True)

            st.divider()
            st.subheader("Columns State")
            st.dataframe(df.describe(include='all'),use_container_width=True)



        else:
            st.info("No File Selected")

    elif selected=="Overview":
        st.divider()
        st.title("Overview")
        st.divider()
        if file is not None:
            df = load_data(file)

            # KPI
            total_sales=df["Sales"].sum()
            total_orders=len(df["Order ID"].unique())
            total_customers=len(df["Customer ID"].unique())
            avr_sales=df["Sales"].mean()

            col1, col2, col3,col4 = st.columns(4)
            with col1:
                st.metric("Total Sales", f"₹ {total_sales/1_00_000:,.2f} L","Target:25 L")
            with col2:
                st.metric("Total Orders", f"{total_orders:}")
            with col3:
                st.metric("Total Customers", f"{total_customers:}")
            with col4:
                st.metric("Average Sale", f"₹ {avr_sales:,.0f}")
            st.divider()
            col1, col2 = st.columns(2)
            with col1:
                # TOP & WORST INSIGHTS
                category_sum=df.groupby("Category")["Sales"].sum().reset_index()
                top_category = category_sum.sort_values(by="Sales", ascending=False).iloc[0]
                st.subheader("Top Category  By Sales")
                st.success(f"🛒 Top Category : {top_category['Category']}")

            with col2:
                # TOP CUSTOMER
                st.subheader("Top Customer By Sales")
                top_customer = df.groupby("Customer Name")["Sales"].sum().idxmax()
                st.info(f"👤 Top Customer : {top_customer}")



            with st.sidebar:
                st.subheader("Select Filters")
                #SIDEBAR
                region=st.multiselect("Select Region", df["Region"].unique(),default=df["Region"].unique())

                category=st.multiselect("Select Category", df["Category"].unique(),default=df["Category"].unique())

                segment=st.multiselect("Select Segment", df["Segment"].unique(),default=df["Segment"].unique())

                df_filtered=df[(df["Region"].isin(region)) & (df["Category"].isin(category)) & (df["Segment"].isin(segment))]

            def value_format(value):
                if value >= 1_00_00_000:
                    return f"₹ {value / 1_00_00_000:.2f} Cr"
                elif value >= 1_00_000:
                    return f"₹ {value / 1_00_000:.2f} L"
                elif value >= 1_000:
                    return f"₹ {value / 1_000:.2f} K"
                else:
                    return f"₹ {value:.2f}"


            #CATEGORY PERFORMANCE
            st.divider()
            category_perf=df_filtered.groupby("Category")["Sales"].sum().reset_index().sort_values(by="Sales",ascending=False)
            category_perf["Sales"]=category_perf["Sales"].apply(value_format)
            category_perf.index=range(1,len(category_perf)+1)
            st.subheader("Category Performance By Sales")
            st.dataframe(category_perf, use_container_width=True)

            #REGION PERFORMANCE
            st.divider()
            region_perf=df_filtered.groupby("Region")["Sales"].sum().reset_index().sort_values(by="Sales",ascending=False)
            region_perf["Sales"]=region_perf["Sales"].apply(value_format)
            region_perf.index=range(1,len(region_perf)+1)
            st.subheader("Region Performance By Sales")
            st.dataframe(region_perf, use_container_width=True)



            # BUSINESS STATEMENTS
            st.divider()
            st.subheader("Business Performance")

            business_per = df_filtered.groupby(["Region", "Category", "Segment"])["Sales"].sum().reset_index()
            business_per["Sales"] = business_per["Sales"].apply(value_format)
            business_per.sort_values(by="Sales", ascending=False)
            business_per.index = range(1, len(business_per) + 1)
            with st.expander("Business Performance"):
                st.dataframe(business_per, use_container_width=True)
        else:
         st.info("Please Upload File")

    elif selected=="Data Visualization":

        st.divider()
        st.title("Data Visualization")
        st.divider()
        if file is not None:
            df = load_data(file)


            tab1,tab2,tab3=st.tabs([" 📊 Simple Chart"," 🚀 Advanced Chart"," Build Your Chart"])
            with tab1:
                st.subheader("Category Performance By Sales")
                category_chart=df.groupby("Category")["Sales"].sum().reset_index()
                fig1=px.line(category_chart,x="Category",y="Sales",template="ggplot2")
                st.plotly_chart(fig1,use_container_width=True)
                st.divider()
                st.subheader("Region Performance By Sales")
                region_chart=df.groupby("Region")["Sales"].sum().reset_index()
                fig2=px.bar(region_chart,x="Region",y="Sales",template="ggplot2",color="Region")
                st.plotly_chart(fig2,use_container_width=True)
                st.divider()

                st.subheader("Sales by Segment")
                segment_sales=df.groupby("Segment")["Sales"].sum().reset_index()
                fig3=px.pie(segment_sales,names="Segment",values="Sales",template="plotly_dark")
                st.plotly_chart(fig3,use_container_width=True)
                st.divider()


                st.subheader("Ship Mode by Sales")
                ship_sales=df.groupby("Ship Mode")["Sales"].sum().reset_index()
                fig4=px.bar(ship_sales,x="Ship Mode",y="Sales",template="plotly_dark",color="Ship Mode")
                st.plotly_chart(fig4,use_container_width=True)
                st.divider()



            with tab2:
                st.subheader("TreeMap:Category  → Sub-Category  → Product Name")
                st.divider()
                fig1=px.treemap(df,
                               path=["Category","Sub-Category","Product Name"],
                               values="Sales",
                               color="Sales",
                               color_continuous_scale="Viridis",
                               hover_name="Category",
                               hover_data={"Sales": True}

                               )
                st.plotly_chart(fig1,use_container_width=True,width=600,height=600)
                st.divider()



                st.subheader("Sunburst: Region → State  → City")
                fig2=px.sunburst(df,
                                 path=["Region","State","City"],
                                 values="Sales",
                                 color="Sales",
                                 color_continuous_scale="Turbo",)
                st.plotly_chart(fig2,use_container_width=True,width=600,height=600)
                st.divider()

                st.subheader("Sales Trend")
                df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d-%m-%Y")
                trend = df.groupby("Order Date")["Sales"].sum().reset_index()

                fig3 = px.line(trend, x="Order Date", y="Sales", template="ggplot2")
                st.plotly_chart(fig3, use_container_width=True)
                st.divider()

                cat_region_sales = df.pivot_table(index="Region", columns="Category",
                                       values="Sales", aggfunc="sum")

                st.subheader("Category vs Region Sales Heatmap")
                fig4 = px.imshow(cat_region_sales, text_auto=True,
                                color_continuous_scale="Blues",
                                title="")
                st.plotly_chart(fig4, use_container_width=True)
                st.divider()

                st.subheader("Sales Distribution by Category")
                fig5=px.box(df,x="Category",y="Sales",template="plotly_dark",color="Category")
                st.plotly_chart(fig5,use_container_width=True,width=600,height=600)
                st.divider()

            with tab3:

                st.title("Build Your Chart")
                st.divider()
                st.subheader("Select X And Y Axis :")
                col1, col2 = st.columns(2)
                with col1:
                    x_axis = st.selectbox("X Axis", df.columns)
                with col2:
                    y_axis = st.selectbox("Y Axis", df.select_dtypes(include='number').columns)

                chart_type = st.selectbox("Chart Type", ["Bar", "Line", "Scatter"])
                if x_axis and y_axis and x_axis != y_axis:
                    button = st.button("Generate Chart")
                    if chart_type and button:
                        if chart_type == "Bar":
                            fig = px.bar(df, x=x_axis, y=y_axis, labels={x_axis: f"{x_axis}", y_axis: f"{y_axis}"},
                                         template="plotly_dark", color=x_axis)
                        elif chart_type == "Line":
                            fig = px.line(df, x=x_axis, y=y_axis, labels={x_axis: f"{x_axis}", y_axis: f"{y_axis}"},
                                          template="plotly_dark", color=x_axis)
                        elif chart_type == "Scatter":
                            fig = px.scatter(df, x=x_axis, y=y_axis, labels={x_axis: f"{x_axis}", y_axis: f"{y_axis}"},
                                             template="plotly_dark", color=x_axis)
                        st.divider()
                        st.subheader(f"{x_axis} VS {y_axis}")
                        st.plotly_chart(fig, use_container_width=True)
                        st.divider()
                    else:
                        st.info("Please Select Chart Type And Click The Button")
                else:
                    st.info("Please Select x-axis And y-axis Or Select x-axis And y-axis different")
        else:
            st.info("Please Upload File")

    elif selected=="Customer Insights":
        st.divider()
        st.title("Customer Insights")
        st.divider()
        if file is not None:
            df = load_data(file)

            def value_format(value):
                if value >= 1_00_00_000:
                    return f"₹ {value / 1_00_00_000:.2f} Cr"
                elif value >= 1_00_000:
                    return f"₹ {value / 1_00_000:.2f} L"
                elif value >= 1_000:
                    return f"₹ {value / 1_000:.2f} K"
                else:
                    return f"₹ {value:.2f}"



            repeat = df.groupby("Customer ID")["Order ID"].nunique()
            repeat_customer = (repeat > 1).sum()

            st.subheader("Repeat Customer")

            st.success(f"Total Repeat Customer Are : {repeat_customer}")

            st.divider()
            col1,col2=st.columns(2)
            with col1:
                st.subheader("Top And Lowest Segment By Sales")
                segment_sum = df.groupby("Segment")["Sales"].sum().reset_index()
                top_segment = segment_sum.sort_values(by="Sales", ascending=False).iloc[0]
                low_segment = segment_sum.sort_values(by="Sales").iloc[0]

                st.success(f"🧩 Top Segment : {top_segment['Segment']}")
                st.warning(f" 🧩 Lowest Segment : {low_segment['Segment']}")

            with col2:
                # TOP REGION
                st.subheader("Top And Lowest Region By Sales")
                top_region = df.groupby("Region")["Sales"].sum().idxmax()
                low_region = df.groupby("Region")["Sales"].sum().idxmin()

                st.success(f"🌍 Top Region  : {top_region}")
                st.warning(f"🌍 Lowest Region : {low_region}")


            st.divider()
            top_customers=df.groupby("Customer Name")["Sales"].sum().sort_values(ascending=False).head(5).reset_index()
            top_customers.index=range(1,len(top_customers)+1)
            top_customers["Sales"]=top_customers["Sales"].apply(value_format)

            st.subheader("Top 5 Customers By Sales")
            st.dataframe(top_customers,use_container_width=True)

            # Segment Performance
            st.divider()
            segment_perf = df.groupby("Segment")["Sales"].sum().reset_index().sort_values(by="Sales",ascending=False)
            segment_perf["Sales"] = segment_perf["Sales"].apply(value_format)
            segment_perf.index = range(1, len(segment_perf) + 1)
            st.subheader("Segment Performance By Sales")
            st.dataframe(segment_perf, use_container_width=True)

            st.divider()
            region_wise_customers=df.groupby("Region")["Customer ID"].nunique().reset_index().rename(columns={"Customer ID": "Total Customers"})
            region_wise_customers.sort_values(by="Total Customers", ascending=False)
            region_wise_customers.index=range(1,len(region_wise_customers)+1)
            st.subheader("Customer By Region")
            st.dataframe(region_wise_customers, use_container_width=True)

            st.divider()
            def days(x):
                if x<=0:
                    return f"{x:,.3f} Day"
                elif x>0:
                    return f"{x:,.1f} Days"
                else:
                    return f"{x:,.1f} Days"

            df["Ship Delay"] = (pd.to_datetime(df["Ship Date"], format="%d-%m-%Y") - pd.to_datetime(df["Order Date"], format="%d-%m-%Y")).dt.days
            avg_delay_by_mode = df.groupby("Ship Mode")["Ship Delay"].mean().reset_index()
            avg_delay_by_mode.index = range(1, len(avg_delay_by_mode) + 1)
            avg_delay_by_mode["Ship Delay"] = avg_delay_by_mode["Ship Delay"].apply(days)
            st.subheader("Average Delay By Mode")
            st.dataframe(avg_delay_by_mode, use_container_width=True)

            st.divider()
            city_wise_customers=df.groupby("City")["Customer ID"].nunique().reset_index().sort_values(by="Customer ID",ascending=False).head(5)
            city_wise_customers=city_wise_customers.rename(columns={"Customer ID": "Total Customers"})
            city_wise_customers.index=range(1,len(city_wise_customers)+1)
            st.subheader("Top 5 City By Customers")
            st.dataframe(city_wise_customers, use_container_width=True)

            st.markdown("---")


        else:
            st.info("Please Upload File")

    elif selected=="Sales Analysis":
        st.divider()
        st.title("Sales Analysis")
        st.divider()
        if file is not None:
            df = load_data(file)

            def value_format(value):
                if value >= 1_00_00_000:
                    return f"₹ {value / 1_00_00_000:.2f} Cr"
                elif value >= 1_00_000:
                    return f"₹ {value / 1_00_000:.2f} L"
                elif value >= 1_000:
                    return f"₹ {value / 1_000:.2f} K"
                else:
                    return f"₹ {value:.2f}"

            total_sales=df["Sales"].sum()
            total_orders=df["Order ID"].nunique()
            avr_sales=df["Sales"].mean()

            col1,col2,col3=st.columns(3)
            col1.metric("Total Sales",f" ₹ {total_sales/1_00_000:,.0f} L")
            col2.metric("Total Orders",f"  {total_orders:}")
            col3.metric("Average Sales",f" ₹ {avr_sales:.0f}")
            st.divider()

            top_sub_cat_sales = df.groupby("Sub-Category")["Sales"].sum().reset_index()
            top_sub_category = top_sub_cat_sales.sort_values(by="Sales", ascending=False).iloc[0]
            low_sub_category = top_sub_cat_sales.sort_values(by="Sales").iloc[0]

            st.subheader("Top And Lowest Sub-Category by Sales")
            col1, col2 = st.columns(2)
            with col1:
                st.success(f" ↪️🛒 Top Sub-Category : {top_sub_category['Sub-Category']}")
            with col2:
                st.warning(f" ↪️🛒 Lowest Sub-Category : {low_sub_category['Sub-Category']}")
            st.divider()


            st.subheader("Top 5 City By Sales")
            city_sales=df.groupby("City")["Sales"].sum().reset_index().sort_values(by="Sales", ascending=False).head(5)
            city_sales.index=range(1,len(city_sales)+1)
            city_sales["Sales"]=city_sales["Sales"].apply(value_format)

            st.dataframe(city_sales, use_container_width=True)
            st.divider()

            st.subheader("Top 5 State By Sales")
            state_sales=df.groupby("State")["Sales"].sum().reset_index().sort_values(by="Sales",ascending=False).head(5)
            state_sales.index=range(1,len(state_sales)+1)
            state_sales["Sales"]=state_sales["Sales"].apply(value_format)

            st.dataframe(state_sales, use_container_width=True)
            st.divider()

            st.subheader("Monthly Sales")
            df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d-%m-%Y")
            df["Month"] = df["Order Date"].dt.to_period("M")
            monthly_sales = df.groupby("Month")["Sales"].sum().reset_index()
            monthly_sales.index=range(1,len(monthly_sales)+1)
            monthly_sales["Sales"]=monthly_sales["Sales"].apply(value_format)
            st.dataframe(monthly_sales, use_container_width=True)
            st.divider()

            product_sales = df.groupby("Product Name")["Sales"].sum().reset_index()
            top_product = product_sales.sort_values(by="Sales", ascending=False).head(5)
            top_product.index=range(1,len(top_product)+1)
            top_product["Sales"]=top_product["Sales"].apply(value_format)


            top_sub_cat = top_sub_cat_sales.sort_values(by="Sales",ascending=False).head(5)
            top_sub_cat.index=range(1,len(top_sub_cat)+1)
            top_sub_cat["Sales"]=top_sub_cat["Sales"].apply(value_format)

            st.subheader("Top 5 Sub-Category by Sales")
            st.dataframe(top_sub_cat, use_container_width=True)
            st.divider()

            st.subheader("Top 5 Product Name By Sales")
            st.dataframe(top_product, use_container_width=True)
            st.divider()




        else:
            st.info("Please Upload File")

    elif selected=="Data Assistant":
        st.divider()
        st.title("Data Assistant")
        st.divider()
        if file is not None:
            df = load_data(file)

            def value_format(value):
                if value >= 1_00_00_000:
                    return f"₹ {value / 1_00_00_000:.2f} Cr"
                elif value >= 1_00_000:
                    return f"₹ {value / 1_00_000:.2f} L"
                elif value >= 1_000:
                    return f"₹ {value / 1_000:.2f} K"
                else:
                    return f"₹ {value:.2f}"
            search = st.chat_input(" Asked Question About The Dataset And Get Visual Representation ")
            st.info("""    
                         Try:
                       - total sales  
                       - top category  
                       - top customer  
                       - top product 
                       - region performance  
                       - sales trend  
                       - segment analysis  
                       - ship mode
                       - monthly sales
                       """)
            st.divider()
            if search:
                q=search.lower()
                if "total sales" in q:
                    total=df["Sales"].sum()
                    st.success(f"💰 Total Sales :  ₹ {total/1_00_000:,.0f} L ")

                elif "top category" in q:
                    category_sales=df.groupby("Category")["Sales"].sum()
                    top_category=category_sales.idxmax()
                    low_category=category_sales.idxmin()
                    st.success(f" 🛒 Top Category: {top_category}")
                    st.warning(f" 🛒 Lowest Category: {low_category}")
                    st.divider()
                    category_df=category_sales.reset_index()


                    st.subheader("Category VS Sales Chart")
                    fig=px.bar(category_df, x="Category", y="Sales", color="Category", barmode="group")
                    st.plotly_chart(fig, use_container_width=True)
                    st.divider()
                    category_df["Sales"] = category_df["Sales"].apply(value_format)
                    category_df.index = range(1, len(category_df) + 1)
                    st.subheader("Category Sales Data")
                    st.dataframe(category_df, use_container_width=True)

                elif "top customer" in q:
                    customer_sales=df.groupby("Customer Name")["Sales"].sum()
                    top_customer=customer_sales.idxmax()
                    st.success(f" 👤 Top Customer: {top_customer}")


                    customer_df=customer_sales.reset_index().sort_values(by="Sales",ascending=False).head(10)

                    st.divider()
                    st.subheader("Top 10 Customers by Sales Chart")
                    fig=px.bar(customer_df, x="Customer Name", y="Sales", color="Customer Name")
                    st.plotly_chart(fig, use_container_width=True)
                    st.divider()
                    st.subheader("Top 10 Customers by Sales Data")
                    customer_df["Sales"] = customer_df["Sales"].apply(value_format)
                    customer_df.index = range(1, len(customer_df) + 1)
                    st.dataframe(customer_df, use_container_width=True)

                elif "top product" in q:
                    product_sales=df.groupby("Product Name")["Sales"].sum()
                    top_product=product_sales.idxmax()
                    st.success(f"  Top Product: {top_product}")

                    product_df=product_sales.reset_index().sort_values(by="Sales",ascending=False).head(10)

                    st.divider()
                    st.subheader("Top 10 Products By Sales Chart")
                    fig=px.bar(product_df,x="Product Name"  ,y="Sales", color="Product Name")
                    st.plotly_chart(fig, use_container_width=True)
                    st.divider()
                    st.subheader("Top 10 Products by Sales Data")
                    product_df.index = range(1, len(product_df) + 1)
                    product_df["Sales"] = product_df["Sales"].apply(value_format)
                    st.dataframe(product_df, use_container_width=True)

                elif "region performance" in q:
                    region_sales=df.groupby("Region")["Sales"].sum()
                    top_region=region_sales.idxmax()
                    st.success(f" 🌍 Top Region: {top_region}")

                    region_df=region_sales.reset_index()

                    st.divider()
                    st.subheader(" Regions by Sales Chart")
                    fig=px.bar(region_df,x="Region" ,y="Sales", color="Region")
                    st.plotly_chart(fig, use_container_width=True)
                    st.divider()
                    st.subheader("Regions by Sales Data")
                    region_df.index = range(1, len(region_df) + 1)
                    region_df["Sales"] = region_df["Sales"].apply(value_format)
                    st.dataframe(region_df, use_container_width=True)

                elif "sales trend" in q:
                    df["Order Date"]=pd.to_datetime(df["Order Date"], format="%d-%m-%Y")
                    trend=df.groupby("Order Date")["Sales"].sum().reset_index()
                    trend.index=range(1,len(trend)+1)
                    st.subheader("Order Date VS Sales Chart")
                    fig=px.bar(trend, x="Order Date", y="Sales", color="Order Date")
                    st.plotly_chart(fig, use_container_width=True)
                    st.divider()
                    st.subheader("Trends Data")
                    st.dataframe(trend, use_container_width=True)

                elif "segment analysis" in q:
                    segment_sales=df.groupby("Segment")["Sales"].sum().reset_index()

                    st.subheader("Segment VS Sales Chart")
                    fig=px.bar(segment_sales, x="Segment", y="Sales", color="Segment")
                    st.plotly_chart(fig, use_container_width=True)
                    st.divider()
                    st.subheader("Segment And Sales Data")
                    segment_sales.index = range(1, len(segment_sales) + 1)
                    segment_sales["Sales"] = segment_sales["Sales"].apply(value_format)
                    st.dataframe(segment_sales, use_container_width=True)

                elif "ship mode" in q:
                    ship_sales=df.groupby("Ship Mode")["Sales"].sum().reset_index()
                    top_ship=ship_sales.loc[ship_sales["Sales"].idxmax(),"Ship Mode"]
                    st.success(f" 🚚 Top Ship Mode: {top_ship}")

                    st.subheader("Ship Mode VS Sales Chart")
                    fig=px.pie(ship_sales, values="Sales", names="Ship Mode")
                    st.plotly_chart(fig, use_container_width=True)
                    ship_sales["Sales"]=ship_sales["Sales"].apply(value_format)
                    ship_sales.index = range(1, len(ship_sales) + 1)
                    st.subheader("ship mode Sales Date")
                    st.dataframe(ship_sales, use_container_width=True)

                elif "monthly sales" in q:
                    df["Order Date"]=pd.to_datetime(df["Order Date"], format="%d-%m-%Y")
                    df["YearMonth"] = df["Order Date"].dt.to_period("M").astype(str)
                    monthly_sales=df.groupby("YearMonth")["Sales"].sum().reset_index()
                    top_month=monthly_sales.loc[monthly_sales["Sales"].idxmax()]
                    low_month=monthly_sales.loc[monthly_sales["Sales"].idxmin()]

                    st.success(f"  Top Month: {top_month['YearMonth']} , Sales ₹ {top_month['Sales']/1_00_000:,.2f} L")
                    st.warning(f"Lowest Month:{low_month['YearMonth']} , Sales ₹ {low_month['Sales']/1_000:,.2f} K")

                    st.subheader("Year Wise Monthly Sales Chart")
                    fig=px.scatter(monthly_sales, x="YearMonth", y="Sales", color="YearMonth")
                    st.plotly_chart(fig, use_container_width=True)
                    st.divider()



                else:
                    st.warning("Question Not Recognized ,Please Try In Above")

        else:
            st.info("Please Upload File")

    elif selected=="Logout":
            st.session_state.logged_in=False
            st.session_state.username=""

            st.query_params.clear()
            st.success("Log Out Successful")
            st.rerun()

if st.session_state.logged_in:
    dashboard()

else:
    login_signup_background()
    st.set_page_config(page_title="User Authentication", layout="centered",page_icon="🔒")

    st.title("🔒 User Authentication")
    tab1,tab2=st.tabs([" 📋✓ SIGN_UP"," 🚪 LOGIN"])
    with tab1:
        signup_page()
    with tab2:
        login_page()

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="VANI Premium",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CSS
# =====================================================
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
}
.block-container {
    padding-top: 3rem;
}
div[data-testid="metric-container"]{
    background:#111827;
    padding:14px;
    border-radius:14px;
    border:1px solid #333;
}
.stChatMessage{
    border-radius:14px;
    padding:10px;
}
.title{
    text-align:center;
    color:#00ffd5;
    font-size:34px;
    font-weight:bold;
    line-height:1.4;
    margin-top:10px;
    margin-bottom:0px;
}
.sub{
    text-align:center;
    color:white;
    margin-bottom:20px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION
# =====================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = ""

if "role" not in st.session_state:
    st.session_state.role = ""

if "history" not in st.session_state:
    st.session_state.history = []

# =====================================================
# USERS
# =====================================================
users = {
    "admin": {"password":"1234","role":"Admin"},
    "recruiter": {"password":"daffodil","role":"Recruiter"},
    "paras": {"password":"vani123","role":"Developer"}
}

# =====================================================
# LOGIN PAGE
# =====================================================
if not st.session_state.logged_in:

    st.markdown("""
    <div class='title'>🌼 Daffodil × VANI</div>
    <div class='sub'>Secure Analytics Portal</div>
    """, unsafe_allow_html=True)

    c1,c2,c3 = st.columns([1,2,1])

    with c2:
        user = st.text_input("User ID")
        pwd = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):

            if user in users:

                if pwd == users[user]["password"]:

                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.session_state.role = users[user]["role"]
                    st.rerun()

                else:
                    st.error("Wrong Password")

            else:
                st.error("User Not Found")

# =====================================================
# MAIN APP
# =====================================================
else:

    # -------------------------------------------------
    # HEADER
    # -------------------------------------------------
    h1,h2 = st.columns([5,1])

    with h1:
        st.markdown("""
        <div class='title'>🤖 VANI Premium Dashboard</div>
        <div class='sub'>Voice Assisted Neural Intelligence</div>
        """, unsafe_allow_html=True)

    with h2:
        st.success(st.session_state.user)
        st.caption(st.session_state.role)

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user = ""
            st.session_state.role = ""
            st.rerun()

    # -------------------------------------------------
    # FILE UPLOAD
    # -------------------------------------------------
    files = st.file_uploader(
        "📂 Upload Excel Files",
        type=["xlsx","xls"],
        accept_multiple_files=True
    )

    if files:

        all_data = []

        for file in files:
            df = pd.read_excel(file)
            df["Source_File"] = file.name
            all_data.append(df)

        data = pd.concat(all_data, ignore_index=True)

        # =================================================
        # SMART SIDEBAR 2.0
        # =================================================
        st.sidebar.title("📊 Smart Controls")

        filter_col1 = st.sidebar.selectbox(
            "Filter Column 1",
            ["None"] + list(data.columns)
        )

        if filter_col1 != "None":

            values1 = st.sidebar.multiselect(
                "Values",
                data[filter_col1].dropna().unique()
            )

            if values1:
                data = data[data[filter_col1].isin(values1)]

        filter_col2 = st.sidebar.selectbox(
            "Filter Column 2",
            ["None"] + list(data.columns)
        )

        if filter_col2 != "None":

            values2 = st.sidebar.multiselect(
                "Values 2",
                data[filter_col2].dropna().unique()
            )

            if values2:
                data = data[data[filter_col2].isin(values2)]

        num_cols = data.select_dtypes(include="number").columns.tolist()

        x_axis = st.sidebar.selectbox(
            "X Axis",
            data.columns
        )

        if num_cols:
            y_axis = st.sidebar.selectbox(
                "Y Axis",
                num_cols
            )
        else:
            y_axis = None

        chart_type = st.sidebar.selectbox(
            "Chart Type",
            [
                "Line Chart",
                "Bar Chart",
                "Histogram",
                "Scatter Plot",
                "Pie Chart",
                "Area Chart"
            ]
        )

        csv = data.to_csv(index=False).encode("utf-8")

        st.sidebar.download_button(
            "📥 Download CSV",
            csv,
            "filtered_data.csv",
            "text/csv"
        )

        st.success("Files Uploaded Successfully ✅")

        # =================================================
        # SMART PROMPTS
        # =================================================
        st.markdown("### 💡 Suggested Actions")

        p1,p2,p3 = st.columns(3)

        selected_prompt = None

        with p1:
            if st.button("💰 Highest Sales"):
                selected_prompt = "highest sales"

        with p2:
            if st.button("📊 Summary Report"):
                selected_prompt = "summary report"

        with p3:
            if st.button("👀 Preview"):
                selected_prompt = "preview"

        # =================================================
        # LAYOUT
        # =================================================
        left,right = st.columns([2,1])

        # =================================================
        # CHAT PANEL
        # =================================================
        with left:

            for msg in st.session_state.history:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

            typed = st.chat_input("Ask VANI about your data...")

            user_input = selected_prompt if selected_prompt else typed

            if user_input:

                st.session_state.history.append(
                    {"role":"user","content":user_input}
                )

                query = user_input.lower()
                response = ""

                # ---------------------------------------------
                # COMMANDS
                # ---------------------------------------------
                if "rows" in query:
                    response = f"📌 Total Rows : {data.shape[0]}"

                elif "columns" in query:
                    response = "\n".join(
                        [f"• {col}" for col in data.columns]
                    )

                elif "preview" in query:

                    rows = []

                    for i,row in data.head().iterrows():

                        rows.append(f"📌 Record {i+1}")

                        for col in data.columns:
                            rows.append(f"{col} : {row[col]}")

                        rows.append("")

                    response = "\n".join(rows)

                elif "summary report" in query:

                    num = data.select_dtypes(include="number")

                    if num.empty:
                        response = "No numeric columns found."

                    else:
                        desc = num.describe()

                        lines = []

                        for col in desc.columns:

                            lines.append(f"\n📊 {col}")

                            for idx in desc.index:
                                val = round(desc.loc[idx,col],2)
                                lines.append(f"{idx} : {val}")

                        response = "\n".join(lines)

                elif "highest sales" in query:

                    if "Sales" in data.columns:
                        response = f"💰 Highest Sales : ₹{data['Sales'].max()}"
                    else:
                        response = "Sales column not found."

                else:

                    response = """
Try Commands:

rows
columns
preview
summary report
highest sales
"""

                # SAVE CHAT
                st.session_state.history.append(
                    {"role":"assistant","content":response}
                )

                with st.chat_message("assistant"):
                    st.write(response)

                    st.components.v1.html(f"""
                    <script>
                    var msg = new SpeechSynthesisUtterance(`{response}`);
                    window.speechSynthesis.speak(msg);
                    </script>
                    """)

        # =================================================
        # RIGHT PANEL
        # =================================================
        with right:

            st.subheader("📊 Live Metrics")

            st.metric("Rows", data.shape[0])
            st.metric("Columns", data.shape[1])

            if num_cols:
                st.metric(
                    "Average",
                    round(data[num_cols].mean().mean(),2)
                )

            st.subheader("📈 Dynamic Chart")

            if num_cols and y_axis:

                fig, ax = plt.subplots(figsize=(6,4))

                try:

                    if chart_type == "Line Chart":
                        data[y_axis].plot(
                            kind="line",
                            marker="o",
                            ax=ax
                        )

                    elif chart_type == "Bar Chart":
                        data[y_axis].head(20).plot(
                            kind="bar",
                            ax=ax
                        )

                    elif chart_type == "Histogram":
                        data[y_axis].plot(
                            kind="hist",
                            bins=20,
                            ax=ax
                        )

                    elif chart_type == "Scatter Plot":

                        if len(num_cols) >= 2:
                            ax.scatter(
                                data[num_cols[0]],
                                data[num_cols[1]]
                            )

                    elif chart_type == "Pie Chart":
                        data[y_axis].head(5).plot(
                            kind="pie",
                            autopct="%1.1f%%",
                            ax=ax
                        )
                        ax.set_ylabel("")

                    elif chart_type == "Area Chart":
                        data[y_axis].head(20).plot(
                            kind="area",
                            ax=ax
                        )

                    st.pyplot(fig)

                except:
                    st.warning("Unable to create chart.")

    else:
        st.info("📂 Upload Excel files to begin.")

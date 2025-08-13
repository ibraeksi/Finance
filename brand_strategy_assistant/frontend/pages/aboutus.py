import streamlit as st
import sys, os
from modules.navbar import navbar

rootpath = os.path.join(os.getcwd())
imagepath = rootpath + "/modules/images/"

def aboutus():
    st.session_state.update(st.session_state)
    navbar()

    st.set_page_config(
        page_title="Value Mapping",
        page_icon=":moneybag:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("Our Leadership Team")
    st.markdown("Meet the creators behind the Brand Strategy AI Assistant")

    # Team Members
    team = [
        {
            "title": "Chief Executive Officer (CEO)",
            "name": "Vivien Daszkowski",
            "image": imagepath + "vividsz.jpg",
            "In-Project Role": "Founder of the core idea, led the presentation, and established the main workflows for the team.",
            "Real-World Role":
            """Vivien did her Master’s degree in Management and worked at the intersection of business and tech
            - as Managing Director of a spin-off of a strategy consultancy.""",
            "github": "https://github.com/Vivi-dsz",
            "linkedin": "https://www.linkedin.com/in/vivien-daszkowski/"
        },
        {
            "title": "Chief Technology Officer (CTO)",
            "name": "Ibrahim Eksi",
            "image": imagepath + "ibraeksi.jpg",
            "In-Project Role": "Owns the scraping pipeline setup, frontend, and supports the broader technical infrastructure.",
            "Real-World Role":
            """Ibrahim is a Mechanical Engineer with 6 years of experience in vehicle safety simulations followed by 2+ years experience as a data analyst.""",
            "github": "https://github.com/ibraeksi",
            "linkedin": "https://www.linkedin.com/in/ibrahim-eksi/"
        },
        {
            "title": "Chief Product Officer (CPO)",
            "name": "Liana Gilmanova",
            "image": imagepath + "gilmali.png",
            "In-Project Role": "Focused on product development — created the system diagram and proposed the initial MVP structure.",
            "Real-World Role":
            """Liana is a Product Manager with 8 years experience in building and scaling Customer facing Products across 18 countries
            and complex cross-functional teams.""",
            "github": "https://github.com/gilmali",
            "linkedin": "https://www.linkedin.com/in/ligilmanova/"
        },
        {
            "title": "Chief Innovation Officer (CIO)",
            "name": "Elnaz Roshan, Ph.D.",
            "image": imagepath + "elnroshan.jpg",
            "In-Project Role": "Responsible for the AI model development and integration, ensuring metrics and functions are intelligent.",
            "Real-World Role":
            """Elnaz is a Climate Economics with 10+ years of experience in evaluating climate transition
            forward-looking optimization modeling, and leading small teams.""",
            "github": "https://github.com/elnroshan",
            "linkedin": "https://www.linkedin.com/in/elnaz-roshan/"
        },

    ]

    # Layout 2x2
    def chunk_list(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    # Display in 2x2 layout
    for row in chunk_list(team, 2):
        cols = st.columns(2)
        for idx, member in enumerate(row):
            st.empty()
            with cols[idx]:
                left, right = st.columns([2, 4], vertical_alignment="top")
                with left:
                    st.image(member["image"], width=150)
                with right:
                    st.markdown(f"## {member['name']}")
                    st.markdown(f"###### :rainbow[{member['title']}]")
                    st.markdown(f"[GitHub]({member['github']}) | [LinkedIn]({member['linkedin']})")

                st.markdown("**In-Project Role**")
                st.write(member["In-Project Role"])

                st.markdown("**Real-World Role**")
                st.write(member["Real-World Role"])
                st.write("         ")

if __name__ == '__main__':
    aboutus()

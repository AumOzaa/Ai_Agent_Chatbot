import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="My Portfolio", page_icon="🌟", layout="wide")

tab1, tab2, tab3 = st.tabs(["🏠 Home", "📂 Projects", "📝 Blog"])

with tab1:
    st.write("Welcome to my portfolio!")

with tab2:
    st.write("Here are my projects...")

with tab3:
    st.write("Here are my blog posts...")


# --- HEADER ---
st.title("👋 Hi, I'm Aum Oza")
st.subheader("AI/ML Enthusiast | Aspiring Engineer | Tech Explorer")
st.write("Welcome to my portfolio! Here you can learn more about me, my skills, and my projects.")

# --- ABOUT SECTION ---
st.header("About Me")
st.write("""
I'm passionate about Artificial Intelligence and Machine Learning.  
Currently exploring DSA in Java, deep learning, and building cool projects.  
I also enjoy writing about my learning journey on X (Twitter).
""")

# --- SKILLS ---
st.header("Skills")
skills = ["Python", "Java", "Streamlit", "Machine Learning", "Data Visualization"]
st.write(", ".join(skills))

# --- PROJECTS ---
st.header("Projects")
st.markdown("""
- 📊 **Stock Market Dashboard** – Built with Streamlit & Pandas.  
- 🤖 **Chatbot with LangChain** – AI-powered assistant using LLMs.  
- 🧮 **Sorting Visualizer** – DSA sorting algorithms explained visually in Python.  
""")

# --- CONTACT ---
st.header("Contact Me")
st.write("📧 Email: your_email@example.com")  
st.write("[💼 LinkedIn](https://linkedin.com/in/yourprofile)")  
st.write("[🐦 Twitter](https://twitter.com/yourhandle)")  

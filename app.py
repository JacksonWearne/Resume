import streamlit as st
import yaml
from pathlib import Path

# ---------- Paths ----------
BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "Data" / "resume.yml"
ASSETS_DIR = BASE_DIR / "assets"


# ----help----
@st.cache_data
def load_resume():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def show_header(resume):
    left, right = st.columns([3, 1])

    with left:
        st.title(resume["name"])
        st.subheader(resume["title"])
        st.write(resume["summary"])

        # Contact info
        contact = []
        if resume.get("location"):
            contact.append(f"📍 {resume['location']}")
        if resume.get("email"):
            contact.append(f"✉️ [{resume['email']}](mailto:{resume['email']})")
        if resume.get("website"):
            contact.append(f"🌐 [Website]({resume['website']})")
        if resume.get("linkedin"):
            contact.append(f"💼 [LinkedIn]({resume['linkedin']})")
        if resume.get("github"):
            contact.append(f"💻 [GitHub]({resume['github']})")

        st.markdown(" • ".join(contact))

    with right:
        profile_img = ASSETS_DIR / "profile.jpg"
        if profile_img.exists():
            st.image(str(profile_img), use_container_width=True)

        pdf_path = ASSETS_DIR / "resume.pdf"
        if pdf_path.exists():
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
            st.download_button(
                label="📄 Download PDF",
                data=pdf_bytes,
                file_name="resume.pdf",
                mime="application/pdf",
            )


def show_skills(resume):
    if "skills" not in resume:
        return

    st.header("Skills")
    cols = st.columns(len(resume["skills"]))
    for col, skill_group in zip(cols, resume["skills"]):
        with col:
            st.subheader(skill_group["name"])
            st.write(", ".join(skill_group["items"]))


def show_experience(resume):
    if "experience" not in resume:
        return

    st.header("Experience")
    for exp in resume["experience"]:
        st.subheader(f"{exp['role']} — {exp['company']}")
        st.caption(f"{exp['location']} • {exp['start']}–{exp['end']}")
        for bullet in exp["bullets"]:
            st.markdown(f"- {bullet}")
        st.markdown("---")


def show_education(resume):
    if "education" not in resume:
        return

    st.header("Education")
    for edu in resume["education"]:
        st.subheader(f"{edu['degree']} — {edu['school']}")
        st.caption(f"{edu['location']} • {edu['start']}–{edu['end']}")
        for bullet in edu["bullets"]:
            st.markdown(f"- {bullet}")
        st.markdown("---")


def show_projects(resume):
    if "projects" not in resume:
        return

    st.header("Projects")
    for proj in resume["projects"]:
        name = proj["name"]
        link = proj.get("link")
        if link:
            st.subheader(f"[{name}]({link})")
        else:
            st.subheader(name)
        for bullet in proj["bullets"]:
            st.markdown(f"- {bullet}")
        st.markdown("---")


def show_interests(resume):
    if "interests" not in resume:
        return

    st.header("Interests")
    st.write(", ".join(resume["interests"]))


# ---------- Main ----------
def main():
    st.set_page_config(
        page_title="Resume | Jackson Wearne",
        page_icon="📊",
        layout="wide",
    )

    resume = load_resume()

    # Sidebar navigation
    st.sidebar.title("Navigation")
    section = st.sidebar.radio(
        "Go to",
        ["Overview", "Experience", "Education", "Projects", "Interests"],
    )

    if section == "Overview":
        show_header(resume)
        show_skills(resume)
    elif section == "Experience":
        show_header(resume)
        show_experience(resume)
    elif section == "Education":
        show_header(resume)
        show_education(resume)
    elif section == "Projects":
        show_header(resume)
        show_projects(resume)
    elif section == "Interests":
        show_header(resume)
        show_interests(resume)


if __name__ == "__main__":
    main()

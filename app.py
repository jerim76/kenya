import streamlit as st
from datetime import datetime
import re
import base64
import pandas as pd

# Custom CSS with local fallback
background_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
st.markdown(f"""
<style>
    :root {{
        --primary: #26A69A;
        --accent: #FF6F61;
        --light: #e6f3f5;
        --dark: #2c3e50;
    }}
    .stApp {{
        background-color: var(--light);
        background-image: url('{background_image}');
        color: var(--dark);
        padding: 10px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    h1, h2, h3, h4 {{
        color: var(--dark);
    }}
    .card {{
        background: white;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}
    .btn {{
        background: var(--primary);
        color: white !important;
        padding: 10px 20px;
        border-radius: 6px;
        border: none;
        cursor: pointer;
        text-decoration: none;
        font-weight: 600;
        display: inline-block;
        transition: background-color 0.3s ease;
    }}
    .btn:hover {{
        background: var(--accent);
    }}
    .section-header {{
        margin-top: 40px;
        margin-bottom: 15px;
        border-bottom: 3px solid var(--primary);
        padding-bottom: 5px;
    }}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="SafeSpace Organisation", page_icon="🧠", layout="wide")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "mood_history" not in st.session_state:
    st.session_state.mood_history = []
if "counseling_form_data" not in st.session_state:
    st.session_state.counseling_form_data = {"name": "", "email": "", "phone": "", "type": "Online"}
if "volunteer_form_data" not in st.session_state:
    st.session_state.volunteer_form_data = {"name": "", "email": "", "phone": "", "role": "Any"}
if "partnership_form_data" not in st.session_state:
    st.session_state.partnership_form_data = {"name": "", "email": "", "phone": "", "type": "Partner"}

# Utility functions
def get_download_link(file_content, file_name):
    try:
        b64 = base64.b64encode(file_content.encode()).decode()
        return f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}" class="btn">Download CSV</a>'
    except Exception:
        st.error("Error generating download link.")
        return ""

def export_mood_history():
    try:
        df = pd.DataFrame(st.session_state.mood_history, columns=["Date", "Mood", "Note"])
        df["Date"] = df["Date"].apply(lambda x: x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime) else x)
        return df.to_csv(index=False)
    except Exception:
        st.error("Error exporting mood history.")
        return ""

# Chatbot knowledge base
knowledge_base = [
    {"question": r"what is safespace organisation\??", "answer": "SafeSpace Organisation is a non-profit dedicated to providing holistic mental health care, support, and education since 2023."},
    {"question": r"what services do you offer\??", "answer": "Our services include individual counseling, group therapy, crisis intervention, and online counseling accessible to all."},
    {"question": r"how can i contact you\??", "answer": "You can reach us by phone at +254 781 095 919 or email info@safespaceorganisation.org."},
    {"question": r"what are your hours\??", "answer": "We operate Monday to Friday, 9 AM to 5 PM, and Saturdays from 10 AM to 2 PM to accommodate your needs."},
    {"question": r"how much does it cost\??", "answer": "Our counseling sessions are affordably priced, ranging from KSh 500 to KSh 2,000 depending on the service."},
    {"question": r"who are the founders\??", "answer": "SafeSpace was founded by Jerim Owino and Hamdi Roble with a vision to increase mental health accessibility."},
    {"question": r"what events are coming up\??", "answer": "Upcoming events include stress management workshops and community outreach programs. Check our Events section for dates."},
    {"question": r"how can i volunteer\??", "answer": "We welcome volunteers passionate about mental health. Please register via our Volunteer form to get involved."},
    {"question": r"what is the crisis line\??", "answer": "Our crisis support line is available at +254 781 095 919 from 8 AM to 7 PM EAT."},
    {"question": r"how can i partner with you\??", "answer": "Partnership inquiries can be made through our Partnership form. We collaborate with institutions to expand mental health services."},
    {"default": "I’m sorry, I didn’t understand that. You can ask about our services, contact info, hours, fees, events, volunteering, or partnerships."}
]

def get_chatbot_response(query):
    query = query.lower()
    for entry in knowledge_base:
        if "question" in entry and re.search(entry["question"], query):
            return entry["answer"]
    return knowledge_base[-1]["default"]

# HEADER
st.markdown("<h1 style='text-align:center; margin-bottom:0;'>SafeSpace Organisation</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px; margin-top:5px;'>Empowering Minds, Nurturing Hope Since 2023</p>", unsafe_allow_html=True)

# HERO SECTION
st.markdown("<div id='hero'></div>", unsafe_allow_html=True)
st.markdown("<h2 class='section-header' style='text-align:center;'>Healing Minds, Restoring Lives</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; max-width:700px; margin:auto;'>SafeSpace offers confidential and compassionate counseling services tailored to the unique needs of individuals, groups, and communities. We believe every person deserves access to mental wellness and support without stigma.</p>", unsafe_allow_html=True)
cols = st.columns(2)
with cols[0]:
    st.markdown("<a href='#services' class='btn'>Explore Our Services</a>", unsafe_allow_html=True)
with cols[1]:
    st.markdown("<a href='#about' class='btn'>Learn About Us</a>", unsafe_allow_html=True)

# ABOUT SECTION
st.markdown("<div id='about'></div>", unsafe_allow_html=True)
st.markdown("## About SafeSpace Organisation")
st.markdown("""
<div class='card'>
<p>Founded in 2023 by Jerim Owino and Hamdi Roble, SafeSpace Organisation is committed to breaking barriers around mental health in Kenya and beyond. With a dedicated team of 15 experienced mental health professionals, we provide accessible, culturally sensitive, and evidence-based care to diverse populations.</p>
<p>Our vision is a society where mental health is prioritized equally with physical health, and our mission is to empower individuals to achieve emotional well-being through counseling, education, and community engagement.</p>
</div>
""", unsafe_allow_html=True)

# SERVICES SECTION
st.markdown("<div id='services'></div>", unsafe_allow_html=True)
st.markdown("## Our Services")
services = [
    {"title": "Individual Counseling", "desc": "One-on-one personalized therapy sessions designed to address your unique mental health challenges, promote emotional healing, and develop coping strategies."},
    {"title": "Group Therapy", "desc": "Facilitated group sessions that provide peer support, foster shared understanding, and encourage collective growth in a safe and supportive environment."},
    {"title": "Online Counseling", "desc": "Convenient and confidential virtual counseling options allowing clients to access professional support from the comfort of their homes or workplaces."},
    {"title": "Crisis Intervention", "desc": "Immediate support for individuals experiencing mental health crises, ensuring safety and connecting them to appropriate resources."},
    {"title": "Workshops & Training", "desc": "Educational sessions focused on mental health awareness, stress management, and resilience building for individuals, schools, and organizations."}
]
for service in services:
    st.markdown(f"<div class='card'><h3>{service['title']}</h3><p>{service['desc']}</p></div>", unsafe_allow_html=True)

with st.form("counseling_form", clear_on_submit=True):
    st.markdown("### Register for Counseling")
    name = st.text_input("Full Name", key="counseling_name")
    email = st.text_input("Email", key="counseling_email")
    phone = st.text_input("Phone", key="counseling_phone")
    submit = st.form_submit_button("Register")
    if submit:
        if name and re.match(r"[^@]+@[^@]+\.[^@]+", email) and phone:
            st.session_state.counseling_form_data = {"name": name, "email": email, "phone": phone, "type": "Online"}
            st.success(f"Thank you, {name}! Your counseling registration has been received. We will contact you shortly at {email}.")
            st.session_state.counseling_form_data = {"name": "", "email": "", "phone": "", "type": "Online"}
        else:
            st.error("Please fill all fields with a valid email.")

# TESTIMONIALS SECTION
st.markdown("<div id='testimonials'></div>", unsafe_allow_html=True)
st.markdown("## Testimonials")
testimonials = [
    {"text": "'The support I received was life-changing. Compassionate and professional care at its best.'", "author": "Jane K."},
    {"text": "'SafeSpace gave me hope and tools to manage my anxiety effectively. Highly recommend!'", "author": "Michael L."},
    {"text": "'The group therapy sessions helped me connect with others who understood my struggles.'", "author": "Faith M."}
]
for t in testimonials:
    st.markdown(f"<div class='card'><p><em>{t['text']}</em></p><p style='text-align:right; font-weight:bold;'>- {t['author']}</p></div>", unsafe_allow_html=True)

# EVENTS SECTION
st.markdown("<div id='events'></div>", unsafe_allow_html=True)
st.markdown("## Upcoming Events")
events = [
    {"title": "Stress Management Workshop", "date": "August 10, 2025", "location": "Nairobi Community Hall", "desc": "Learn practical techniques to manage stress and enhance mental wellness."},
    {"title": "Mental Health Awareness Campaign", "date": "September 15-20, 2025", "location": "Nationwide", "desc": "Join our outreach events to promote understanding and reduce stigma."},
    {"title": "Volunteer Training Seminar", "date": "October 5, 2025", "location": "SafeSpace Headquarters", "desc": "Comprehensive training for new volunteers passionate about mental health."}
]
for event in events:
    st.markdown(f"<div class='card'><h4>{event['title']}</h4><p><strong>Date:</strong> {event['date']}<br><strong>Location:</strong> {event['location']}</p><p>{event['desc']}</p></div>", unsafe_allow_html=True)

# PARTNERSHIPS SECTION
st.markdown("<div id='partnerships'></div>", unsafe_allow_html=True)
st.markdown("## Partnerships")
st.markdown("""
<div class='card'>
<h4>Kenyatta National Hospital</h4>
<p>Since 2024, we have partnered with Kenyatta National Hospital to provide seamless referrals and collaborative care for individuals requiring specialized mental health services.</p>
</div>
<div class='card'>
<h4>Ministry of Health</h4>
<p>Collaborating on nationwide mental health initiatives to improve accessibility and awareness across Kenya.</p>
</div>
<div class='card'>
<h4>Local NGOs & Community Groups</h4>
<p>Working with grassroots organizations to deliver mental health education and outreach programs directly to vulnerable populations.</p>
</div>
""", unsafe_allow_html=True)

with st.form("partnership_form", clear_on_submit=True):
    st.markdown("### Become a Partner")
    name = st.text_input("Full Name", key="partnership_name")
    email = st.text_input("Email", key="partnership_email")
    phone = st.text_input("Phone", key="partnership_phone")
    submit = st.form_submit_button("Register")
    if submit:
        if name and re.match(r"[^@]+@[^@]+\.[^@]+", email) and phone:
            st.session_state.partnership_form_data = {"name": name, "email": email, "phone": phone, "type": "Partner"}
            st.success(f"Thank you, {name}! Your partnership inquiry has been received. We will get back to you soon at {email}.")
            st.session_state.partnership_form_data = {"name": "", "email": "", "phone": "", "type": "Partner"}
        else:
            st.error("Please fill all fields with a valid email.")

# BLOG SECTION
st.markdown("<div id='blog'></div>", unsafe_allow_html=True)
st.markdown("## Blog")
blogs = [
    {"title": "Coping with Stress", "date": "July 20, 2025", "author": "Dr. Amina", "summary": "Effective tips and techniques to manage stress in daily life and maintain emotional balance."},
    {"title": "Understanding Anxiety Disorders", "date": "June 10, 2025", "author": "Hamdi Roble", "summary": "An overview of anxiety disorders, symptoms, and when to seek professional help."},
    {"title": "Building Resilience During Tough Times", "date": "May 5, 2025", "author": "Jerim Owino", "summary": "Strategies to develop mental resilience and bounce back from adversity."}
]
for blog in blogs:
    st.markdown(f"<div class='card'><h4>{blog['title']}</h4><p><em>{blog['date']} - by {blog['author']}</em></p><p>{blog['summary']}</p></div>", unsafe_allow_html=True)

# TRACKER SECTION
st.markdown("<div id='tracker'></div>", unsafe_allow_html=True)
st.markdown("## Mood Tracker")
st.markdown("""
Track your mood regularly to become more aware of your emotional wellbeing. Logging your mood helps you notice patterns and share important insights with your counselor.
""")
mood = st.slider("Mood (1 = Very low, 5 = Very high)", 1, 5, 3)
note = st.text_input("Add a note (optional)", key="mood_note")
if st.button("Log Mood"):
    st.session_state.mood_history.append({"Date": datetime.now(), "Mood": mood, "Note": note})
    st.success("Your mood has been logged successfully.")
if st.session_state.mood_history:
    st.markdown("### Recent Mood Logs")
    for entry in st.session_state.mood_history[-5:]:
        note_text = f" — {entry['Note']}" if entry['Note'] else ""
        st.write(f"- {entry['Date'].strftime('%Y-%m-%d %H:%M')}: Mood {entry['Mood']}/5{note_text}")
if st.button("Export Mood History as CSV"):
    csv = export_mood_history()
    if csv:
        st.markdown(get_download_link(csv, "mood_history.csv"), unsafe_allow_html=True)

# VOLUNTEER SECTION
st.markdown("<div id='volunteer'></div>", unsafe_allow_html=True)
st.markdown("## Volunteer")
st.markdown("""
Join our dedicated volunteer team and contribute your time and skills to support mental health outreach campaigns, community workshops, and administrative support. Volunteering with SafeSpace is a rewarding way to make a positive impact.
""")
st.markdown("""
**Volunteer Roles Include:**
- Outreach Support: Participate in 2-4 hour campaigns raising mental health awareness.
- Event Coordination: Help organize workshops and training sessions.
- Peer Support Assistance: Assist in group sessions and community engagement.
""")
with st.form("volunteer_form", clear_on_submit=True):
    st.markdown("### Volunteer Registration")
    name = st.text_input("Full Name", key="volunteer_name")
    email = st.text_input("Email", key="volunteer_email")
    phone = st.text_input("Phone", key="volunteer_phone")
    submit = st.form_submit_button("Register")
    if submit:
        if name and re.match(r"[^@]+@[^@]+\.[^@]+", email) and phone:
            st.session_state.volunteer_form_data = {"name": name, "email": email, "phone": phone, "role": "Any"}
            st.success(f"Thank you, {name}! You are now registered as a SafeSpace volunteer. We will contact you at {email} soon.")
            st.session_state.volunteer_form_data = {"name": "", "email": "", "phone": "", "role": "Any"}
        else:
            st.error("Please fill all fields with a valid email.")

# CONTACT SECTION
st.markdown("<div id='contact'></div>", unsafe_allow_html=True)
st.markdown("## Contact Us")
st.markdown("""
<div class='card'>
<p>We are located at Greenhouse Plaza, Nairobi. Our friendly team is ready to assist you with any inquiries or support.</p>
<ul>
<li><strong>Phone:</strong> +254 781 095 919</li>
<li><strong>Email:</strong> info@safespaceorganisation.org</li>
<li><strong>Office Hours:</strong> Monday - Friday: 9 AM - 5 PM, Saturday: 10 AM - 2 PM</li>
</ul>
<p>Follow us on social media for updates, events, and mental health tips.</p>
</div>
""", unsafe_allow_html=True)

# CHATBOT SECTION

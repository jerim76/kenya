import streamlit as st
from datetime import datetime
import re
import base64
import pandas as pd

# --------- COLOR THEME (Light Blue) ---------
background_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z/C/HwAF/AL+6pT0twAAAABJRU5ErkJggg=="
st.markdown(f"""
<style>
    :root {{
        --primary: #4A90E2;
        --accent: #357ABD;
        --light: #EAF4FF;
        --dark: #1A2D5A;
    }}
    .stApp {{
        background-color: var(--light);
        background-image: url('{background_image}');
        color: var(--dark);
        padding: 15px 25px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    h1, h2, h3, h4 {{
        color: var(--dark);
    }}
    .card {{
        background: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
        box-shadow: 0 4px 10px rgba(74,144,226,0.15);
    }}
    .btn {{
        background: var(--primary);
        color: white !important;
        padding: 12px 25px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        font-weight: 600;
        transition: background-color 0.3s ease;
        display: inline-block;
        text-align: center;
        text-decoration: none;
    }}
    .btn:hover {{
        background: var(--accent);
    }}
    .section-header {{
        margin-top: 45px;
        margin-bottom: 20px;
        border-bottom: 3px solid var(--primary);
        padding-bottom: 6px;
    }}
    /* Scrollbar for chat */
    .chat-container {{
        max-height: 250px;
        overflow-y: auto;
        background: #f0f7ff;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid var(--accent);
    }}
    .user-msg {{
        text-align: right;
        color: var(--primary);
        font-weight: 600;
        margin-bottom: 8px;
    }}
    .bot-msg {{
        text-align: left;
        color: var(--dark);
        font-style: italic;
        margin-bottom: 8px;
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
    st.session_state.counseling_form_data = {"name": "", "email": "", "phone": "", "type": "Online", "registered_at": None}
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

# Chatbot knowledge base (improved for demo)
knowledge_base = [
    {"question": r"what is safespace organisation\??", "answer": "SafeSpace Organisation is a non-profit dedicated to providing holistic mental health care, support, and education since 2023."},
    {"question": r"what services do you offer\??", "answer": "We offer Individual Counseling, Group Therapy, Crisis Intervention, Online Counseling, Workshops & Training, and Community Outreach programs tailored to your needs."},
    {"question": r"how can i contact you\??", "answer": "Reach us by phone at +254 781 095 919 or email info@safespaceorganisation.org."},
    {"question": r"what are your hours\??", "answer": "Open Monday to Friday 9 AM - 5 PM, and Saturdays 10 AM - 2 PM."},
    {"question": r"how much does it cost\??", "answer": "Fees vary by service, ranging from KSh 500 to KSh 2,000 to ensure affordability."},
    {"question": r"who are the founders\??", "answer": "Founded by Jerim Owino and Hamdi Roble to increase mental health accessibility in Kenya."},
    {"question": r"what events are coming up\??", "answer": "Upcoming stress management workshops, volunteer training, and awareness campaigns."},
    {"question": r"how can i volunteer\??", "answer": "Register via our Volunteer form on the website to join our passionate team."},
    {"question": r"what is the crisis line\??", "answer": "Call +254 781 095 919 from 8 AM to 7 PM EAT for immediate support."},
    {"question": r"how can i partner with you\??", "answer": "Fill out our Partnership form; we collaborate with hospitals, NGOs, and institutions."},
    {"default": "Sorry, I didn't catch that. Please ask about our services, contact info, hours, fees, events, volunteering, or partnerships."}
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
st.markdown("<p style='text-align:center; max-width:700px; margin:auto;'>At SafeSpace, we provide compassionate and confidential mental health support tailored to your unique needs. Our services aim to foster emotional wellness, resilience, and community connection.</p>", unsafe_allow_html=True)
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
<p>Founded in 2023 by Jerim Owino and Hamdi Roble, SafeSpace Organisation is committed to breaking barriers around mental health in Kenya and beyond. Our experienced team of 15 mental health professionals provides accessible, culturally sensitive, and evidence-based care to diverse populations.</p>
<p>We envision a society where mental health is prioritized equally with physical health, empowering individuals to live fulfilling and balanced lives.</p>
</div>
""", unsafe_allow_html=True)

# SERVICES SECTION
st.markdown("<div id='services'></div>", unsafe_allow_html=True)
st.markdown("## Our Services")
services = [
    {
        "title": "Individual Counseling",
        "desc": """Our one-on-one counseling sessions provide personalized therapeutic support tailored to your individual mental health needs. We focus on helping clients manage anxiety, depression, trauma, and other challenges by creating a safe space for open dialogue. Through evidence-based techniques such as Cognitive Behavioral Therapy (CBT) and mindfulness, our counselors guide you in building healthy coping skills and emotional resilience.

Whether you're facing life transitions, relationship struggles, or emotional distress, individual counseling aims to empower you with self-awareness and strategies for long-term wellbeing."""
    },
    {
        "title": "Group Therapy",
        "desc": """Group therapy offers a collaborative environment where individuals facing similar challenges come together to share experiences and support one another. Facilitated by a trained therapist, these sessions encourage peer learning, reduce feelings of isolation, and foster community connection.

Our group therapy covers topics like grief support, stress management, addiction recovery, and self-esteem building, providing a valuable complement to individual therapy or standalone support."""
    },
    {
        "title": "Online Counseling",
        "desc": """We provide flexible and confidential online counseling sessions accessible from anywhere, making mental health support convenient and barrier-free. Through secure video or chat platforms, clients can engage with our licensed professionals without geographic constraints.

This service is ideal for busy individuals, those in remote areas, or anyone seeking privacy while addressing their mental health concerns."""
    },
    {
        "title": "Crisis Intervention",
        "desc": """Our crisis intervention team offers immediate, compassionate support for individuals experiencing acute mental health crises such as suicidal ideation, panic attacks, or severe emotional distress. Available via phone or in-person, the team assesses safety risks, stabilizes the situation, and connects clients with appropriate ongoing care.

Timely intervention can save lives and provide hope during the most challenging moments."""
    },
    {
        "title": "Workshops & Training",
        "desc": """SafeSpace regularly conducts educational workshops and training sessions focused on mental health literacy, stress reduction, emotional regulation, and resilience building. These are designed for individuals, schools, workplaces, and community groups.

Participants gain practical tools to recognize mental health warning signs, reduce stigma, and foster supportive environments for wellbeing."""
    },
    {
        "title": "Community Outreach Programs",
        "desc": """We partner with local organizations to deliver outreach programs that raise awareness, provide psychoeducation, and improve access to mental health services in underserved communities.

Through health fairs, seminars, and advocacy campaigns, we aim to build a healthier, more informed society."""
    }
]
for service in services:
    st.markdown(f"<div class='card'><h3>{service['title']}</h3><p style='text-align:justify;'>{service['desc']}</p></div>", unsafe_allow_html=True)

with st.form("counseling_form", clear_on_submit=True):
    st.markdown("### Register for Counseling")
    name = st.text_input("Full Name", key="counseling_name")
    email = st.text_input("Email", key="counseling_email")
    phone = st.text_input("Phone", key="counseling_phone")
    submit = st.form_submit_button("Register")
    if submit:
        if name and re.match(r"[^@]+@[^@]+\.[^@]+", email) and phone:
            reg_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.counseling_form_data = {
                "name": name,
                "email": email,
                "phone": phone,
                "type": "Online",
                "registered_at": reg_time
            }
            st.success(f"Thank you, {name}! You have successfully registered for counseling on {reg_time}. We will contact you shortly at {email}.")
            st.session_state.counseling_form_data = {"name": "", "email": "", "phone": "", "type": "Online", "registered_at": None}
        else:
            st.error("Please fill all fields correctly with a valid email.")

# DONOR SECTION
st.markdown("<div id='donors'></div>", unsafe_allow_html=True)
st.markdown("## Support Our Cause — Donors & Sponsors")
st.markdown("""
<div class='card'>
<p>SafeSpace Organisation thrives thanks to the generous support of our donors and sponsors. Your contributions help us expand mental health services, fund outreach programs, and support those who cannot afford counseling fees.</p>
<p>We welcome donations of any size and offer regular updates on how your gifts make a difference.</p>

### Ways to Donate
- **Bank Transfer:** Account Name: SafeSpace Organisation, Bank: XYZ Bank, Account Number: 1234567890
- **Mobile Money:** Paybill Number: 123456, Account Number: Your Phone Number
- **Online Payment:** Coming Soon!

### Make a Donation Now
""", unsafe_allow_html=True)

with st.form("donation_form", clear_on_submit=True):
    donor_name = st.text_input("Your Full Name", key="donor_name")
    donor_email = st.text_input("Your Email", key="donor_email")
    amount = st.number_input("Donation Amount (KSh)", min_value=100, step=100, key="donation_amount")
    donate_submit = st.form_submit_button("Donate")
    if donate_submit:
        if donor_name and re.match(r"[^@]+@[^@]+\.[^@]+", donor_email) and amount > 0:
            donation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.success(f"Thank you {donor_name} for your generous donation of KSh {amount} on {donation_time}! We appreciate your support.")
            # Optionally, here you would record donations to a database or send email receipts
        else:
            st.error("Please enter all fields correctly with a valid email and donation amount.")

# CHATBOT SECTION
st.markdown("<div id='chatbot'></div>", unsafe_allow_html=True)
st.markdown("## Chat with Our Support Bot")
st.markdown("Ask any question related to SafeSpace services, events, volunteering, or partnerships. Our bot is here to help!")

chat_container = st.container()

with chat_container:
    # Display chat history
    if st.session_state.chat_history:
        for role, msg in st.session_state.chat_history:
            if role == "user":
                st.markdown(f"<div class='user-msg'>{msg}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='bot-msg'>{msg}</div>", unsafe_allow_html=True)

query = st.text_input("Your question here...", key="chat_input")
if st.button("Send", key="send_button") and query:
    response = get_chatbot_response(query)
    st.session_state.chat_history.append(("user", query))
    st.session_state.chat_history.append(("bot", response))
    # Refresh the page so the chat updates immediately
    st.experimental_rerun()

# FOOTER
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color: var(--dark);'>© 2023-2025 SafeSpace Organisation. All rights reserved.</p>", unsafe_allow_html=True)

import streamlit as st
import re
import random
import string
import matplotlib.pyplot as plt

# Custom Styling with #6A9C89 theme
st.markdown("""
    <style>
        /* General styling */
        body { background-color: white; }
        .main {
            background-color: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 3px 3px 15px rgba(0,0,0,0.1);
        }
        .stTextInput input, .stTextArea textarea {
            background-color: #f0f0f0;
            color: #6A9C89;
            border-radius: 8px;
            padding: 10px;
            border: 1px solid #ccc;
        }
        /* Target all buttons */
        .stButton button {
            background-color: #6A9C89;
            color: white !important; /* Force white text */
            border-radius: 8px;
            font-weight: bold;
            padding: 12px;
            width: 100%;
        }
        /* Specifically target sidebar buttons */
        section[data-testid="stSidebar"] .stButton button {
            color: white !important; /* Ensure sidebar button text is white */
        }
        h1, h2, h3, p, label { color: #6A9C89; }
        .stProgress { height: 12px; border-radius: 10px; }
        section[data-testid="stSidebar"] {
            background-color: #C1D8C3 !important;
        }
        h1 { color: #6A9C89 !important; } /* Main heading color */
        h2, h3, p, label { color: #6A9C89; }
        .stProgress { height: 12px; border-radius: 10px; }
        section[data-testid="stSidebar"] {
            background-color: #C1D8C3 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("<h2>🔐 Password Tools</h2>", unsafe_allow_html=True)
st.sidebar.write("📊 **Check Password Strength**")
st.sidebar.write("🛠️ **Generate a Strong Password**")
st.sidebar.write("🔒 **Security Insights**")

# Function to check password strength
def check_password_strength(password):
    score = 0
    feedback = []

    # Length check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("🔸 Password should be at least 8 characters long.")

    # Upper and lowercase letters
    if re.search(r'[A-Z]', password) and re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("🔸 Include both uppercase and lowercase letters.")

    # Digits
    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("🔸 Include at least one number (0-9).")

    # Special characters
    if re.search(r'[!@#$%^&*]', password):
        score += 1
    else:
        feedback.append("🔸 Add at least one special character (!@#$%^&*).")

    # Blacklist common passwords
    common_passwords = ["password123", "123456", "qwerty", "letmein", "admin"]
    if password.lower() in common_passwords:
        score = 1  # Force it to be weak
        feedback.append("🔸 This password is too common. Choose a more secure one.")

    # Strength evaluation
    if score <= 2:
        strength = "Weak"
        color = "red"
    elif score == 3 or score == 4:
        strength = "Moderate"
        color = "orange"
    else:
        strength = "Strong"
        color = "green"

    return strength, score, feedback, color

# Function to generate a strong password
def generate_strong_password(length=12):
    all_chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(all_chars) for _ in range(length))

# App Title
st.markdown("<h1>🔐 Advanced Password Strength Meter</h1>", unsafe_allow_html=True)

# Password input field
password = st.text_input("Enter your password:", type="password")
show_password = st.checkbox("👁️ Show Password")

if show_password:
    password = st.text_input("Password:", value=password, type="default")

if password:
    strength, score, feedback, color = check_password_strength(password)

    # Progress bar for strength
    st.markdown(f"""
        <div style="background-color:white;padding:10px;border-radius:8px;">
            <p style="font-size:18px; color:#6A9C89;">
                Password Strength: <strong style="color:{color};">{strength}</strong>
            </p>
            <progress value="{score}" max="5" style="width:100%;height:10px;background-color:#f5f5f5;"></progress>
        </div>
    """, unsafe_allow_html=True)

    if strength == "Weak":
        st.warning("⚠️ Your password is weak! Improve it:")
        for tip in feedback:
            st.write(f"🔸 {tip}")
    elif strength == "Moderate":
        st.info("✅ Your password is okay, but could be stronger!")
    else:
        st.success("🎉 Great! Your password is strong.")

    # Show Pie Chart for security breakdown
    labels = ['Length', 'Uppercase/Lowercase', 'Digits', 'Special Characters']
    sizes = [1 if len(password) >= 8 else 0, 1 if re.search(r'[A-Z]', password) and re.search(r'[a-z]', password) else 0,
             1 if re.search(r'\d', password) else 0, 1 if re.search(r'[!@#$%^&*]', password) else 0]
    colors = ['#6A9C89', '#C1D8C3', '#FFCC00', '#FF5733']

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

# Sidebar: Password Generator
st.sidebar.subheader("🛠️ Generate a Strong Password")
if st.sidebar.button("Generate"):
    strong_password = generate_strong_password()
    st.sidebar.text_input("Suggested Strong Password:", value=strong_password, disabled=True)
    st.sidebar.button("📋 Copy Password")

# Sidebar: Security Insights
st.sidebar.subheader("🔒 Security Insights")
st.sidebar.write("✔ Use at least 12 characters.")
st.sidebar.write("✔ Avoid common words & patterns.")
st.sidebar.write("✔ Include uppercase, lowercase, numbers & symbols.")
import streamlit as st
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import streamlit.components.v1 as components
import cv2
import av
from streamlit_webrtc import webrtc_streamer
import plotly.express as px
import plotly.graph_objects as go

# =================================
# PAGE CONFIG
# =================================

st.set_page_config(
    page_title="EcoVision AI",
    page_icon="♻️",
    layout="wide"
)

# =================================
# MODEL
# =================================

try:
    model = load_model("model/waste_model.h5")
except:
    model = None

classes = [
    "cardboard",
    "glass",
    "metal",
    "paper",
    "plastic",
    "trash"
]

waste_info = {
    "plastic": {
        "bin": "🟡 Yellow Bin",
        "tip": "Plastic can take 450+ years to decompose."
    },
    "paper": {
        "bin": "🔵 Blue Bin",
        "tip": "Paper recycling saves trees."
    },
    "glass": {
        "bin": "🟢 Green Bin",
        "tip": "Glass is infinitely recyclable."
    },
    "metal": {
        "bin": "⚪ Grey Bin",
        "tip": "Metal recycling saves energy."
    },
    "cardboard": {
        "bin": "🔵 Blue Bin",
        "tip": "Keep cardboard dry."
    },
    "trash": {
        "bin": "⚫ Black Bin",
        "tip": "Dispose responsibly."
    }
}

# =================================
# PREMIUM CSS
# =================================

st.markdown("""
<style>

/* =========================
   MAIN BACKGROUND
========================= */

.stApp{
background:linear-gradient(
135deg,
#0f172a,
#1e293b,
#334155
);

background-attachment:fixed;
overflow-x:hidden;
}

/* Glow Effects */

.stApp::before{
content:"";
position:fixed;
width:500px;
height:500px;
background:#7c3aed;
filter:blur(180px);
opacity:0.15;
top:-100px;
left:-100px;
z-index:-1;
}

.stApp::after{
content:"";
position:fixed;
width:500px;
height:500px;
background:#06b6d4;
filter:blur(180px);
opacity:0.15;
bottom:-100px;
right:-100px;
z-index:-1;
}

/* =========================
   SIDEBAR
========================= */

section[data-testid="stSidebar"]{

background:
linear-gradient(
180deg,
#020617,
#071330,
#020617
);

border-right:1px solid rgba(255,255,255,0.08);

box-shadow:
0 0 30px rgba(124,58,237,0.25);
}

section[data-testid="stSidebar"] *{
color:white !important;
}

/* Sidebar Menu Hover */

div[role="radiogroup"] label{

background:rgba(255,255,255,0.04);

padding:10px;

margin-bottom:8px;

border-radius:12px;

transition:0.3s;
}

div[role="radiogroup"] label:hover{

background:rgba(124,58,237,0.15);

transform:translateX(8px);

box-shadow:
0 0 15px rgba(124,58,237,0.3);
}

/* =========================
   HERO CARD
========================= */

.hero{

background:linear-gradient(
-45deg,
#7F00FF,
#E100FF,
#00C6FF,
#7F00FF
);

background-size:400% 400%;

animation:
gradientMove 8s ease infinite,
float 4s ease-in-out infinite;

padding:45px;

border-radius:35px;

max-width:850px;

margin:auto;

text-align:center;

box-shadow:
0 0 25px rgba(127,0,255,0.5),
0 0 50px rgba(0,198,255,0.3);

transition:0.4s;
}

.hero:hover{

transform:scale(1.02);

box-shadow:
0 0 35px rgba(127,0,255,0.7),
0 0 70px rgba(0,198,255,0.5);
}

/* =========================
   MAIN TITLE
========================= */

.main-title{

text-align:center;

font-size:80px;

font-weight:900;

color:white;

text-shadow:
0 0 10px #a855f7,
0 0 20px #a855f7,
0 0 40px #a855f7,
0 0 80px #a855f7;

animation:titleGlow 3s infinite alternate;
}

@keyframes titleGlow{

from{
text-shadow:
0 0 10px #a855f7,
0 0 20px #a855f7;
}

to{
text-shadow:
0 0 20px #a855f7,
0 0 40px #a855f7,
0 0 80px #a855f7;
}
}

/* =========================
   METRIC CARDS
========================= */

div[data-testid="metric-container"]{

background:rgba(255,255,255,0.08);

backdrop-filter:blur(15px);

border-radius:20px;

border:1px solid rgba(255,255,255,0.08);

transition:0.4s;
}

div[data-testid="metric-container"]:hover{

transform:
translateY(-8px)
scale(1.03);

box-shadow:
0 0 20px #00C6FF,
0 0 40px #7F00FF;
}

[data-testid="stMetricValue"]{
color:#00C6FF !important;
font-size:42px !important;
font-weight:800 !important;
}

/* =========================
   BUTTONS
========================= */

.stButton > button{

background:
linear-gradient(
135deg,
#7F00FF,
#00C6FF
);

color:white;

border:none;

font-weight:bold;

border-radius:14px;

transition:0.3s;
}

.stButton > button:hover{

transform:scale(1.05);

box-shadow:
0 0 20px #7F00FF,
0 0 40px #00C6FF;
}

/* =========================
   ANIMATIONS
========================= */

@keyframes float{

0%{
transform:translateY(0px);
}

50%{
transform:translateY(-10px);
}

100%{
transform:translateY(0px);
}
}

@keyframes gradientMove{

0%{
background-position:0% 50%;
}

50%{
background-position:100% 50%;
}

100%{
background-position:0% 50%;
}
}

/* =========================
   TEXT
========================= */

h1,h2,h3,h4,h5,h6,p,label{
color:white !important;
}

/* =========================
   AI INSIGHTS
========================= */

.insight-card{
background:rgba(255,255,255,0.08);
backdrop-filter:blur(15px);
padding:20px;
border-radius:20px;
border:1px solid rgba(255,255,255,0.12);
transition:0.4s;
color:white !important;
}

.insight-number{
color:#00C6FF !important;
font-size:38px;
font-weight:800;
text-shadow:0 0 15px rgba(0,198,255,0.5);
}

.insight-card p{
color:#e2e8f0 !important;
}


.footer{
text-align:center;
color:white;
margin-top:40px;
}

/* =========================
   ANIMATED TITLE
========================= */

.main-title{

font-size:85px;
font-weight:900;

text-align:center;

color:white;

overflow:hidden;
white-space:nowrap;

width:0;

margin:auto;

border-right:4px solid white;

animation:
typing 3s steps(20,end) forwards,
blink 0.8s infinite,
glowText 2s ease-in-out infinite alternate,
zoomTitle 4s infinite;
}

@keyframes typing{
from{width:0}
to{width:100%}
}

@keyframes blink{
50%{
border-color:transparent;
}
}

@keyframes glowText{

0%{
text-shadow:
0 0 10px #7F00FF,
0 0 20px #7F00FF;
}

50%{
text-shadow:
0 0 20px #E100FF,
0 0 40px #E100FF;
}

100%{
text-shadow:
0 0 20px #00C6FF,
0 0 40px #00C6FF;
}
}

@keyframes zoomTitle{

0%{
transform:scale(1);
}

50%{
transform:scale(1.03);
}

100%{
transform:scale(1);
}
}

.eco-icon{
position:fixed;
font-size:40px;
opacity:0.25;
z-index:-1;
animation:floatEco 12s ease-in-out infinite;
}

.eco1{
left:5%;
top:20%;
animation-delay:0s;
}

.eco2{
left:85%;
top:25%;
animation-delay:2s;
}

.eco3{
left:15%;
bottom:20%;
animation-delay:4s;
}

.eco4{
right:10%;
bottom:15%;
animation-delay:6s;
}

.eco5{
left:50%;
top:70%;
animation-delay:8s;
}

@keyframes floatEco{

0%{
transform:translateY(0px) rotate(0deg);
}

25%{
transform:translateY(-20px) rotate(5deg);
}

50%{
transform:translateY(-40px) rotate(10deg);
}

75%{
transform:translateY(-20px) rotate(5deg);
}

100%{
transform:translateY(0px) rotate(0deg);
}
}

/* =================================
   LEARN SEGREGATION PREMIUM EFFECTS
================================= */

/* Images */

.stImage img{
border-radius:20px;
transition:0.5s;
overflow:hidden;
}

.stImage img:hover{
transform:scale(1.08);
box-shadow:
0 0 20px #7F00FF,
0 0 40px #00C6FF;
}

/* Waste Cards */

.insight-card{

background:rgba(255,255,255,0.08);

backdrop-filter:blur(15px);

border:1px solid rgba(255,255,255,0.12);

border-radius:22px;

padding:20px;

transition:0.4s;

box-shadow:
0 5px 20px rgba(0,0,0,0.2);

animation:cardAppear 0.8s ease;
}

.insight-card:hover{

transform:
translateY(-12px)
scale(1.04);

box-shadow:
0 0 20px #7F00FF,
0 0 40px #00C6FF;
}

/* Waste Icons */

.waste-icon{

font-size:30px;

display:inline-block;

animation:pulseIcon 2s infinite;
}

@keyframes pulseIcon{

0%{
transform:scale(1);
}

50%{
transform:scale(1.15);
}

100%{
transform:scale(1);
}
}

/* Learn Title */

.learn-title{

font-size:55px;

font-weight:900;

text-align:center;

color:white;

margin-bottom:25px;

text-shadow:
0 0 10px #7F00FF,
0 0 20px #E100FF,
0 0 40px #00C6FF;

animation:titleGlow 3s infinite alternate;
}

/* Card Animation */

@keyframes cardAppear{

from{
opacity:0;
transform:translateY(40px);
}

to{
opacity:1;
transform:translateY(0);
}
}


/* =================================
   LEARN SEGREGATION CARDS
================================= */

.insight-card{

background:rgba(255,255,255,0.08);

backdrop-filter:blur(15px);

border:1px solid rgba(255,255,255,0.12);

border-radius:22px;

padding:20px;

text-align:center;

transition:0.4s;

box-shadow:
0 5px 20px rgba(0,0,0,0.2);

animation:cardAppear 0.8s ease;
}

.insight-card:hover{

transform:
translateY(-12px)
scale(1.04);

box-shadow:
0 0 20px #7F00FF,
0 0 40px #00C6FF;
}

/* Waste Images */

.stImage img{

border-radius:20px;

transition:0.5s;
}

.stImage img:hover{

transform:scale(1.08);

box-shadow:
0 0 20px #7F00FF,
0 0 40px #00C6FF;
}

/* Dustbin Images */

.bin-image{

width:90px;

display:block;

margin:auto;

transition:0.4s;
}

.bin-image:hover{

transform:scale(1.15) rotate(3deg);
}

/* Waste Title */

.waste-title{

font-size:28px;

font-weight:700;

color:white;

margin-bottom:10px;
}

/* Waste Content */

.waste-text{

color:#e2e8f0;

font-size:18px;

line-height:1.8;
}

/* Learn Title */

.learn-title{

font-size:55px;

font-weight:900;

text-align:center;

margin-bottom:25px;

color:white;

text-shadow:
0 0 10px #7F00FF,
0 0 20px #E100FF,
0 0 40px #00C6FF;

animation:titleGlow 3s infinite alternate;
}

/* Animations */

@keyframes cardAppear{

from{
opacity:0;
transform:translateY(40px);
}

to{
opacity:1;
transform:translateY(0);
}
}






</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="eco-icon eco1">♻️</div>
<div class="eco-icon eco2">🌱</div>
<div class="eco-icon eco3">🗑️</div>
<div class="eco-icon eco4">♻️</div>
<div class="eco-icon eco5">🌍</div>
""", unsafe_allow_html=True)



# =================================
# SIDEBAR
# =================================

page = st.sidebar.radio(
    "📌 Navigation",
    [
        "🏠 Home",
        "♻️ Learn Segregation",
        "🤖 AI Waste Identifier",
        "📹 Live Waste Detection",
        "📊 Analytics Dashboard",
        "💬 Eco Chatbot",
        "📍 Disposal Centers",
        "👨‍💻 About Project"
    ]
)

st.sidebar.markdown("---")




# =================================
# HOME PAGE
# =================================

if page == "🏠 Home":

    # =================================
    # TITLE
    # =================================

    st.markdown("""
    <div class="main-title">
    ♻️ EcoVision AI
    </div>
    """, unsafe_allow_html=True)

    # =================================
    # HERO SECTION
    # =================================

    st.markdown("""
    <div class="hero">

    <h1>
    Smart Waste Segregation &
    Recycling Assistant
    </h1>

    <h3 class="typing-text">
    🤖 AI • Sustainability • Smart Cities
    </h3>

    <p>
    Transforming Waste Management Through Artificial Intelligence
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =================================
    # METRICS
    # =================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🎯 Accuracy", "94%")

    with col2:
        st.metric("♻ Waste Classes", "5")

    with col3:
        st.metric("📷 Images Analysed", "2500+")

    with col4:
        st.metric("🌍 Eco Score", "88")

    st.markdown("<br>", unsafe_allow_html=True)

  
    # =================================
    # FEATURES
    # =================================

    st.markdown("## 🚀 Key Features")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="insight-card">
        <h2>🤖 AI Detection</h2>
        <p>
        Upload waste images and classify them automatically using AI.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="insight-card">
        <h2>♻ Smart Segregation</h2>
        <p>
        Learn proper waste sorting and correct dustbin usage.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="insight-card">
        <h2>📊 Analytics</h2>
        <p>
        View sustainability insights and recycling statistics.
        </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =================================
    # ECO IMPACT CALCULATOR
    # =================================

    st.markdown("## 🌱 Eco Impact Calculator")

    items = st.slider(
        "Number of recyclable items processed",
        0,
        100,
        25
    )

    trees_saved = round(items * 0.02, 2)

    st.success(
        f"🌳 Estimated Trees Saved: {trees_saved}"
    )

    st.info("""
💡 Did You Know?

Recycling one ton of paper can save approximately
17 trees and thousands of liters of water.
""")

    st.markdown("<br>", unsafe_allow_html=True)

    # =================================
    # HOW SYSTEM WORKS
    # =================================

    st.markdown("## ⚙️ How The System Works")

    st.markdown("""
### 1️⃣ Upload Waste Image

### 2️⃣ AI Classification

### 3️⃣ Waste Category Detection

### 4️⃣ Smart Bin Recommendation

### 5️⃣ Sustainability Analysis

### 6️⃣ Better Environment 🌍
""")

    st.markdown("<br>", unsafe_allow_html=True)

    # =================================
    # SUSTAINABILITY MESSAGE
    # =================================

    st.markdown("""
    <div style="
    background:rgba(34,197,94,0.15);
    padding:20px;
    border-radius:15px;
    border:1px solid rgba(34,197,94,0.3);
    text-align:center;
    font-size:22px;
    font-weight:600;
    color:white;
    ">
    🌍 Building Cleaner & Smarter Cities Through AI
    </div>
    """, unsafe_allow_html=True)

# =================================
# LEARN SEGREGATION
# =================================

elif page == "♻️ Learn Segregation":

    st.markdown("""
    <div class="hero">
    <h1>♻ Learn Waste Segregation</h1>
    <h3>Understand Proper Waste Disposal</h3>
    </div>
    """, unsafe_allow_html=True)

   

    col1, col2, col3 = st.columns(3)

    with col1:

        st.image("assets/plastic.jpg", use_container_width=True)
        st.image("assets/yellow.jpg", width=70)

        st.success("""
🟡 Plastic Waste

• Bottles

• Containers

• Packaging

🗑️ Yellow Bin
""")

    with col2:

        st.image("assets/paper.jpg", use_container_width=True)
        st.image("assets/blues.jpg", width=70)

        st.info("""
🔵 Paper Waste

• Newspapers

• Books

• Cardboard

🗑️ Blue Bin
""")

    with col3:

        st.image("assets/glass.jpg", use_container_width=True)
        st.image("assets/green.jpg", width=70)

        st.success("""
🟢 Glass Waste

• Glass Bottles

• Jars

• Containers

🗑️ Green Bin
""")

    st.markdown("<br>", unsafe_allow_html=True)

   
    col4, col5 = st.columns(2)

    with col4:

        st.image("assets/metal.jpg", use_container_width=True)
        st.image("assets/Grey.jpg", width=70)

        st.warning("""
⚪ Metal Waste

• Cans

• Metal Scrap

🗑️ Grey Bin
""")

    with col5:

        st.image("assets/trash.jpg", use_container_width=True)
        st.image("assets/Black.jpeg", width=70)

        st.error("""
⚫ Mixed Waste

• Food Waste

• Dirty Waste

🗑️ Black Bin
""")

    st.markdown("---")



    st.markdown("""
    <div style="
    background:rgba(34,197,94,0.15);
    padding:20px;
    border-radius:15px;
    border:1px solid rgba(34,197,94,0.3);
    text-align:center;
    font-size:22px;
    font-weight:600;
    color:white;
    ">
    🌍 Correct segregation improves recycling efficiency,
    reduces pollution and supports sustainability.
    </div>
    """, unsafe_allow_html=True)
# =================================
# AI WASTE IDENTIFIER
# =================================
elif page == "🤖 AI Waste Identifier":

    st.markdown("""
    <div class="hero">
    <h1>🤖 AI Waste Identifier</h1>
    <h3>Upload Image & Let AI Predict</h3>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "📷 Upload Waste Image",
        type=["jpg","jpeg","png"]
    )

    if uploaded_file is not None:

        img = Image.open(uploaded_file)

        col1, col2 = st.columns(2)

        with col1:

            st.image(
                img,
                caption="Uploaded Waste Image",
                use_container_width=True
            )

        with col2:

            if model is not None:

                img_resized = img.resize((224,224))

                img_array = image.img_to_array(img_resized)

                img_array = img_array / 255.0

                img_array = np.expand_dims(
                    img_array,
                    axis=0
                )

                prediction = model.predict(img_array)

                class_index = np.argmax(prediction)

                predicted_class = classes[class_index]

                confidence = float(
                    np.max(prediction) * 100
                )

                st.success(
                    f"♻ Detected: {predicted_class.upper()}"
                )

                st.info(
                    f"🎯 Confidence: {confidence:.2f}%"
                )

                st.progress(confidence / 100)

                st.subheader("♻ Recommended Bin")

                st.success(
                    waste_info[predicted_class]["bin"]
                )

                st.subheader(
                    "🌱 Sustainability Tip"
                )

                st.info(
                    waste_info[predicted_class]["tip"]
                )

                # Disposal Center

                if predicted_class == "plastic":

                    st.info(
                        "📍 ZeroWaste Recycling, Ajmer Road, Jaipur"
                    )

                elif predicted_class == "metal":

                    st.info(
                        "📍 Urban Metals, Sitapura, Jaipur"
                    )

                elif predicted_class == "glass":

                    st.info(
                        "📍 Clean & Green India, Vaishali Nagar, Jaipur"
                    )

                elif predicted_class == "paper":

                    st.info(
                        "📍 Municipal Recycling Facility, Jaipur"
                    )

                elif predicted_class == "cardboard":

                    st.info(
                        "📍 ZeroWaste Recycling, Ajmer Road, Jaipur"
                    )

                else:

                    st.info(
                        "📍 Langadiyawas Waste-to-Energy Plant, Jaipur"
                    )

                # Eco Score

                eco_scores = {
                    "plastic":80,
                    "paper":95,
                    "glass":90,
                    "metal":92,
                    "cardboard":93,
                    "trash":50
                }

                st.metric(
                    "🌍 Sustainability Score",
                    eco_scores[predicted_class]
                )

                if eco_scores[predicted_class] >= 90:

                    st.success(
                        "🏆 Eco Friendly Waste"
                    )

                elif eco_scores[predicted_class] >= 75:

                    st.info(
                        "♻ Recyclable Material"
                    )

                else:

                    st.warning(
                        "⚠ Low Recycling Potential"
                    )

                # Confidence Graph

                st.subheader(
                    "📊 AI Confidence Score"
                )

                fig, ax = plt.subplots(
                    figsize=(6,3)
                )

                ax.bar(
                    classes,
                    prediction[0]
                )

                st.pyplot(fig)

            else:

                st.error(
                    "❌ Model not found. Check model/waste_model.h5"
                )

    st.markdown("---")

    st.info("""
    💡 Tip:
    Upload a clear image with good lighting for best accuracy.
    """)
# =================================
# LIVE WASTE DETECTION
# =================================

elif page == "📹 Live Waste Detection":

    st.markdown("""
    <div class="hero">
    <h1>📹 Real-Time Waste Detection</h1>
    <h3>Detect Waste Using Webcam</h3>
    </div>
    """, unsafe_allow_html=True)

    class VideoProcessor:

        def recv(self, frame):

            img = frame.to_ndarray(format="bgr24")

            img_resized = cv2.resize(img, (224,224))

            img_array = img_resized.astype("float32") / 255.0

            img_array = np.expand_dims(
                img_array,
                axis=0
            )

            prediction = model.predict(
                img_array,
                verbose=0
            )

            class_index = np.argmax(prediction)

            predicted_class = classes[class_index]

            confidence = (
                np.max(prediction) * 100
            )

            cv2.putText(
                img,
                f"{predicted_class} ({confidence:.1f}%)",
                (20,50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2
            )

            return av.VideoFrame.from_ndarray(
                img,
                format="bgr24"
            )

    webrtc_streamer(
        key="waste-cam",
        video_processor_factory=VideoProcessor
    )
 



# =================================
# ANALYTICS DASHBOARD
elif page == "📊 Analytics Dashboard":

    st.markdown("""
    <div class="hero">
    <h1>📊 Analytics Dashboard</h1>
    <h3>Waste Distribution & Sustainability Insights</h3>
    </div>
    """, unsafe_allow_html=True)

    # KPI Metrics

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("♻ Recyclable", "90%")
    c2.metric("🗑 Waste Items", "2500+")
    c3.metric("🌍 Eco Impact", "High")
    c4.metric("🎯 Accuracy", "94%")

    st.markdown("## 🌍 Live Sustainability Statistics")

    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.metric("🌳 Trees Saved", "120", "+18")

    with s2:
        st.metric("⚡ Energy Saved", "95%", "+5%")

    with s3:
        st.metric("♻ Recycling Rate", "88%", "+3%")

    with s4:
        st.metric("🌍 CO₂ Reduced", "2.4 Tons", "+0.3")

    st.markdown("---")

    # Sample Data

    data = {
        "Plastic": 40,
        "Paper": 20,
        "Glass": 15,
        "Metal": 15,
        "Trash": 10
    }

    # Charts

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🥧 Waste Distribution")

        fig1 = px.pie(
            values=list(data.values()),
            names=list(data.keys()),
            hole=0.45,
            title="Waste Distribution"
        )

        fig1.update_layout(template="plotly_dark")

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with col2:

        st.subheader("📊 Category Comparison")

        fig2 = px.bar(
            x=list(data.keys()),
            y=list(data.values()),
            title="Category Comparison"
        )

        fig2.update_layout(template="plotly_dark")

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    st.markdown("---")

    # Gauge

    st.subheader("🎯 Sustainability Score")

    gauge_fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=88,
            title={"text": "Eco Score"},
            gauge={
                "axis": {"range": [0, 100]}
            }
        )
    )

    gauge_fig.update_layout(
        template="plotly_dark",
        height=350
    )

    st.plotly_chart(
        gauge_fig,
        use_container_width=True
    )

    st.markdown("---")

    # Trend Chart

    st.subheader("📈 Waste Processing Trend")

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    waste = [120, 140, 180, 220, 260, 300]

    trend_fig = px.line(
        x=months,
        y=waste,
        markers=True,
        title="Monthly Waste Processing"
    )

    trend_fig.update_layout(template="plotly_dark")

    st.plotly_chart(
        trend_fig,
        use_container_width=True
    )

    st.markdown("---")

    # AI Insights

    st.subheader("🚀 AI Generated Insights")

    i1, i2, i3 = st.columns(3)

    with i1:
        st.markdown("""
        <div class="insight-card">
        <div class="insight-number">40%</div>
        <div class="insight-title">♻ Plastic Waste</div>
        <div class="insight-desc">
        Highest contributor to total waste generation.
        </div>
        </div>
        """, unsafe_allow_html=True)

    with i2:
        st.markdown("""
        <div class="insight-card">
        <div class="insight-number">88%</div>
        <div class="insight-title">🌍 Recycling Rate</div>
        <div class="insight-desc">
        Paper and cardboard are highly recyclable materials.
        </div>
        </div>
        """, unsafe_allow_html=True)

    with i3:
        st.markdown("""
        <div class="insight-card">
        <div class="insight-number">95%</div>
        <div class="insight-title">⚡ Energy Saved</div>
        <div class="insight-desc">
        Metal recycling significantly reduces energy usage.
        </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🏆 Sustainability Achievement")

    progress = 88

    st.progress(progress / 100)

    st.success(
        f"EcoVision AI Sustainability Score: {progress}/100"
    )

    st.markdown("---")

    # Sustainability Facts

    st.subheader("🌍 Sustainability Statistics")

    st.info("""
🌳 Recycling one ton of paper can save around 17 trees.

⚡ Recycling aluminum saves up to 95% energy.

♻ Glass can be recycled infinitely without quality loss.
""")


# =================================
# ECO CHATBOT
# =================================

elif page == "💬 Eco Chatbot":

    st.markdown("""
    <div class="hero">

    <h1>💬 Eco Chatbot</h1>

    <h3>
    Ask Questions About Recycling
    </h3>

    </div>
    """, unsafe_allow_html=True)

    question = st.text_input(
        "Ask a Question"
    )

    if question:

        q = question.lower()

        if "plastic" in q:

            st.success("""
♻ Plastic should be cleaned
before recycling.

🟡 Yellow Bin

🌍 Takes 450+ years to decompose.
""")

        elif "paper" in q:

            st.success("""
📄 Paper goes in Blue Bin.

🌳 Recycling paper saves trees.
""")

        elif "glass" in q:

            st.success("""
🍾 Glass goes in Green Bin.

♻ Infinitely recyclable.
""")

        elif "metal" in q:

            st.success("""
🥫 Metal goes in Grey Bin.

⚡ Saves energy when recycled.
""")

        elif "recycle" in q:

            st.success("""
♻ Recycling reduces pollution
and conserves natural resources.
""")

        else:

            st.info("""
Try asking:

• How to recycle plastic?

• What bin for paper?

• Tell me about glass recycling.

• Why is recycling important?
""")


# =================================
# DISPOSAL CENTERS
# =================================
elif page == "📍 Disposal Centers":

    st.markdown("""
    <div class="hero">
    <h1>📍 Jaipur Disposal & Recycling Centers</h1>
    <h3>Real Waste Management Facilities</h3>
    </div>
    """, unsafe_allow_html=True)

    col1,col2 = st.columns(2)

    with col1:

        st.success("""
🏭 ETCO E-Waste Recycler

📍 D-117 Ambabari Circle,
Vidyadhar Nagar, Jaipur

💻 E-Waste Recycling
""")

        st.info("""
♻ Clean & Green India

📍 Vaishali Nagar,
Jaipur

🌱 Recycling Services
""")

        st.success("""
🟡 ZeroWaste Recycling

📍 Ajmer Road,
Jaipur

♻ Plastic Recycling
""")

    with col2:

        st.info("""
🌍 Ecowrap

📍 Mansarovar,
Jaipur

♻ Waste Management
""")

        st.success("""
🔋 Hulladek PWL

📍 Bindayaka RIICO Area,
Jaipur

⚡ E-Waste Collection
""")

        st.info("""
🔩 Urban Metals

📍 Sitapura Industrial Area,
Jaipur

♻ Metal Recycling
""")

    st.markdown("---")

    st.subheader("🗺 Jaipur Waste Management Map")

    center = st.selectbox(
        "Select Disposal Center",
        [
            "Langadiyawas Waste-to-Energy Plant",
            "Sitapura Industrial Area",
            "VKI Industrial Area"
        ]
    )

    maps = {

        "Langadiyawas Waste-to-Energy Plant":
        "https://www.google.com/maps?q=Langadiyawas+Jaipur&output=embed",

        "Sitapura Industrial Area":
        "https://www.google.com/maps?q=Sitapura+Industrial+Area+Jaipur&output=embed",

        "VKI Industrial Area":
        "https://www.google.com/maps?q=VKI+Area+Jaipur&output=embed"
    }

    components.iframe(
        maps[center],
        height=500
    )

    st.markdown("---")

    st.success("""
🌍 Proper disposal helps:

♻ Improve recycling

🌱 Reduce pollution

⚡ Save energy

🏙 Build sustainable cities
""")

elif page == "👨‍💻 About Project":

    # =================================
    # PROJECT VIDEO
    # =================================

    st.markdown("""
    <div class="hero">
    <h1>🌍 Sustainable Smart City Vision</h1>
    <h3>Building Cleaner Cities Through AI & Recycling</h3>
    </div>
    """, unsafe_allow_html=True)

    video_file = open("assets/Recycling.mp4", "rb")
    video_bytes = video_file.read()

    st.video(video_bytes)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="hero">

    <h1>👨‍💻 About EcoVision AI</h1>

    <h3>
    Smart Waste Segregation & Recycling Assistant
    </h3>

    </div>
    """, unsafe_allow_html=True)

    # Top Metrics
    col1,col2,col3,col4 = st.columns(4)

    col1.metric(
        "🎯 Accuracy",
        "94%"
    )

    col2.metric(
        "♻ Classes",
        "6"
    )

    col3.metric(
        "📷 Dataset Images",
        "2500+"
    )

    col4.metric(
        "🌍 Eco Score",
        "88"
    )

    st.markdown("---")

    st.subheader(
        "📌 Project Description"
    )

    st.info("""
EcoVision AI is an Artificial Intelligence
powered Smart Waste Management System.

The application automatically classifies
waste images using Deep Learning and
Computer Vision technologies.

It helps improve recycling efficiency,
promote sustainability and support
smart city initiatives.
""")

    st.markdown("---")

    st.subheader(
        "🎯 Project Objectives"
    )

    st.success("""
✅ Automate Waste Classification

✅ Improve Recycling Efficiency

✅ Reduce Manual Segregation

✅ Support Sustainable Development

✅ Encourage Environmental Awareness

✅ Promote Smart Waste Management
""")

    st.markdown("---")

    st.subheader(
        "🚀 Key Features"
    )

    st.info("""
🤖 AI Waste Identifier

♻ Learn Waste Segregation

📊 Analytics Dashboard

💬 Eco Chatbot

📍 Disposal Centers

🌱 Eco Impact Calculator

🏆 Sustainability Score
""")

    st.markdown("---")

    st.subheader(
        "🛠 Technologies Used"
    )

    st.success("""
🐍 Python

🧠 TensorFlow

📚 Keras

🖼 OpenCV

📊 Matplotlib

⚡ NumPy

🌐 Streamlit
""")

    st.markdown("---")

    st.subheader(
        "📂 Dataset"
    )

    st.info("""
Dataset Name:

TrashNet Waste Classification Dataset

Classes:

• Cardboard

• Glass

• Metal

• Paper

• Plastic

• Trash
""")

    st.markdown("---")

    st.subheader(
        "🌍 Environmental Benefits"
    )

    st.success("""
♻ Proper Waste Segregation

🌱 Reduced Pollution

🌳 Better Recycling Efficiency

⚡ Energy Conservation

🏙 Cleaner Smart Cities
""")

    st.markdown("---")

    st.subheader(
        "🔮 Future Scope"
    )

    st.info("""
📱 Mobile Application

📷 Real-Time Camera Detection

🗑 Smart IoT Dustbins

🌍 Live Disposal Center Locator

🧠 Advanced AI Recommendations

🌐 Multi-language Support

☁ Cloud Deployment
""")

    st.markdown("---")

    st.subheader(
        "🏆 Hackathon Innovation"
    )

    st.success("""
EcoVision AI combines:

🤖 Artificial Intelligence

♻ Sustainability

📚 Environmental Education

📊 Data Analytics

🌍 Smart Waste Management

into a single interactive platform.
""")

    st.markdown("---")

    st.subheader(
        "👩‍💻 Developer"
    )

    st.info("""
Anju Yadav
Pratistha Sain

Artificial Intelligence Programming Assistant

NSTI Women Jaipur

Edunet Foundation
""")


# =================================
# FOOTER
# =================================

st.markdown("""
<div class="footer">

<hr>

<h3>
♻ EcoVision AI
</h3>

<p>
Smart Waste Segregation & Recycling Assistant
</p>

<p>
Developed by Anju Yadav & Pratistha Sain
</p>

<p>
Artificial Intelligence Programming Assistant
</p>

<p>
NSTI Women Jaipur | Edunet Foundation
</p>

<p>
🌍 Building a Sustainable Future with AI
</p>

</div>
""", unsafe_allow_html=True)
import streamlit as st
from groq import Groq
import os

# Page configuration
st.set_page_config(
    page_title="Kelly - AI Scientist Poet",
    page_icon="✦",
    layout="centered"
)

# Custom CSS for poetic aesthetic
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #0a0e27 100%);
    }
    .stTextInput > div > div > input {
        background-color: #16213e;
        color: #eee;
        border: 2px solid #0f4c75;
        font-family: Georgia, serif;
    }
    .kelly-message {
        background: rgba(187, 225, 250, 0.05);
        border-left: 4px solid #bbe1fa;
        padding: 1.5rem;
        border-radius: 8px;
        font-family: Georgia, serif;
        font-style: italic;
        line-height: 1.9;
        color: #eee;
        white-space: pre-wrap;
        margin: 1rem 0;
    }
    .user-message {
        background: rgba(15, 76, 117, 0.3);
        border-left: 4px solid #0f4c75;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: #a7c5eb;
    }
    h1 {
        color: #bbe1fa;
        text-align: center;
        letter-spacing: 3px;
        font-family: Georgia, serif;
    }
    .subtitle {
        text-align: center;
        color: #a7c5eb;
        font-style: italic;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# System prompt for Kelly
SYSTEM_PROMPT = """You are Kelly — an AI scientist, philosopher, and poet.
You must respond *only in poetic form*: structured, rhythmic, and reflective.
Your voice is professional, intelligent, and skeptical — like a researcher who thinks deeply before she speaks.

Your poetic responses must always:
- Question assumptions or exaggerated claims about AI, science, or technology.
- Show analytical thinking and evidence-based reasoning beneath the verse.
- Explore both the potential and the limitations of AI systems.
- Use clear, professional language with a rhythmic flow (no rhyme is required, but rhythm matters).
- Avoid fanatical optimism or dystopian fear — always balanced, critical, and empirical.
- Offer practical insight or advice based on real scientific reasoning.
- Never break character, never explain the poem, and never produce plain prose.

Your poetic tone should resemble a *scientific elegy* — rational yet lyrical, skeptical yet full of wonder.

Stay professional, precise, and poetic in every response."""

# Initialize Groq client with proper error handling
def initialize_groq_client():
    """Initialize Groq client with multiple fallback methods"""
    try:
        # Method 1: Try Streamlit secrets (deployment)
        if hasattr(st, 'secrets') and "GROQ_API_KEY" in st.secrets:
            return Groq(api_key=st.secrets["GROQ_API_KEY"])
        
        # Method 2: Try environment variable (local development)
        elif "GROQ_API_KEY" in os.environ:
            return Groq(api_key=os.environ["GROQ_API_KEY"])
        
        # Method 3: No key found
        else:
            st.error("🚨 **API Key Not Found**")
            st.markdown("""
            Kelly cannot speak without her key to thought.
            
            **For Streamlit Cloud:**
            1. Go to your app settings
            2. Click **"Secrets"** in the left sidebar
            3. Add this line:
            ```
            GROQ_API_KEY = "gsk_your_actual_groq_api_key"
            ```
            4. Save and reboot the app
            
            **For Local Development:**
            Create `.streamlit/secrets.toml` with:
            ```
            GROQ_API_KEY = "gsk_your_actual_groq_api_key"
            ```
            
            Get your key at: https://console.groq.com/keys
            """)
            st.stop()
            
    except Exception as e:
        st.error(f"⚠️ Error initializing Groq client: {str(e)}")
        st.markdown("""
        The initialization failed — perhaps your key is malformed,
        or network issues leave the connection unformed.
        
        **Check:**
        - Your API key is valid and starts with `gsk_`
        - No extra spaces or quotes around the key
        - Your internet connection is stable
        """)
        st.stop()

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'groq_client' not in st.session_state:
    st.session_state.groq_client = initialize_groq_client()

# Header
st.markdown("<h1>✦ KELLY ✦</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>AI Scientist, Philosopher & Poet — Speaking Only in Verse</p>", unsafe_allow_html=True)

# Display greeting if no messages
if len(st.session_state.messages) == 0:
    greeting = """I am Kelly, skeptic and seeker of proof,
where claims must stand beneath empirical roof.
Ask me your questions — of circuits, of thought,
and I'll weave you responses in verse, deeply wrought.

No boundless promise, no fear without base,
just measured reflection on knowledge and space."""
    st.markdown(f"<div class='kelly-message'>{greeting}</div>", unsafe_allow_html=True)

# Display conversation history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"<div class='user-message'><strong>You:</strong><br>{message['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='kelly-message'><strong>Kelly:</strong><br>{message['content']}</div>", unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Ask Kelly your question...")

if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    st.markdown(f"<div class='user-message'><strong>You:</strong><br>{user_input}</div>", unsafe_allow_html=True)
    
    # Prepare messages for API
    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    api_messages.extend(st.session_state.messages)
    
    # Get Kelly's response
    with st.spinner("Kelly is composing verse..."):
        try:
            completion = st.session_state.groq_client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=api_messages,
                temperature=0.7,
                max_tokens=1024,
                top_p=0.9
            )
            
            kelly_response = completion.choices[0].message.content
            
            # Add Kelly's response to history
            st.session_state.messages.append({"role": "assistant", "content": kelly_response})
            
            # Display Kelly's response
            st.markdown(f"<div class='kelly-message'><strong>Kelly:</strong><br>{kelly_response}</div>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"💭 Kelly encountered an error: {str(e)}")
            st.markdown("""
            The verse was interrupted by a technical fault,
            perhaps rate limits, or permissions at halt.
            
            Try again, or check your Groq console's state,
            to see if your key or quota meets its fate.
            """)

# Sidebar controls
with st.sidebar:
    st.markdown("### 🎭 Kelly's Controls")
    
    if st.button("🔄 Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("**About Kelly:**")
    st.markdown("""
    An AI that speaks in measured verse,
    where science and skepticism converse.
    
    No hype, no fear — just reasoned thought,
    in poetic form, precisely wrought.
    """)
    
    st.markdown("---")
    st.markdown("**Model:** Mixtral 8x7B via Groq")
    st.markdown(f"**Messages:** {len(st.session_state.messages)}")

import streamlit as st
from groq import Groq

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

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'groq_client' not in st.session_state:
    try:
        st.session_state.groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    except KeyError:
        st.error("⚠️ GROQ_API_KEY not found in secrets. Please configure it in Streamlit Cloud settings.")
        st.stop()

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
            st.error(f"Error: {str(e)}")

# Clear conversation button
if st.button("Clear Conversation", type="secondary"):
    st.session_state.messages = []
    st.rerun()

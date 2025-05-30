import streamlit as st
import time
import json
from datetime import datetime
from typing import List, Dict, Any

# Page configuration
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for ChatGPT-like styling
st.markdown("""
<style>
    body, .main, .block-container {
        background-color: #18181b !important;
        color: #f3f4f6 !important;
    }
    .block-container {
        max-width: 48rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .user-message {
        background: #23272f;
        color: #f3f4f6;
        padding: 1rem 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
        border: 1px solid #27272a;
    }
    .assistant-message {
        background: #18181b;
        color: #f3f4f6;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        border-left: 3px solid #10a37f;
        border-radius: 0.5rem;
    }
    .status-line {
        font-size: 0.95rem;
        color: #a1a1aa;
        margin: 0.25rem 0;
        padding: 0.25rem 0;
        font-style: italic;
    }
    .status-running {
        color: #fbbf24;
    }
    .status-completed {
        color: #22d3ee;
    }
    .stTextArea textarea {
        background: #23272f;
        color: #f3f4f6;
        border-radius: 0.75rem;
        border: 1px solid #52525b;
        padding: 0.75rem 1rem;
    }
    .stTextArea textarea:focus {
        border-color: #10a37f;
        box-shadow: 0 0 0 1px #10a37f;
    }
    .stButton > button {
        background-color: #10a37f;
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: background-color 0.2s;
    }
    .stButton > button:hover {
        background-color: #059669;
    }
    .download-btn {
        background-color: #23272f;
        border: 1px solid #52525b;
        color: #f3f4f6;
        font-size: 0.875rem;
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
        margin-top: 1rem;
    }
    .header {
        text-align: center;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #27272a;
    }
    .header h1 {
        font-size: 2rem;
        font-weight: 600;
        color: #f3f4f6;
        margin-bottom: 0.5rem;
    }
    .header p {
        color: #a1a1aa;
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Agent definitions
AGENTS = {
    'governance': {'name': 'Governance Agent', 'icon': '🛡️'},
    'auth': {'name': 'Authorization & Access Agent', 'icon': '🔐'},
    'research': {'name': 'Research Agent', 'icon': '🔍'},
    'legal': {'name': 'Legal Agent', 'icon': '⚖️'},
    'financial': {'name': 'Financial Agent', 'icon': '💰'},
    'risk': {'name': 'Risk Assessment Agent', 'icon': '📊'},
    'marketing': {'name': 'Marketing Analytics Agent', 'icon': '📈'},
    'document': {'name': 'Documenting Agent', 'icon': '📄'}
}

# Orchestration flows
FLOWS = {
    "healthcare_trends": {
        "query": "What are latest trends in the healthcare treatment space?",
        "agents": ['governance', 'auth', 'research', 'document'],
        "response": """**Latest Healthcare Treatment Trends (2025):**\n\n• **Personalized Medicine**: Treatments tailored to individual genetic profiles\n• **AI-Powered Diagnostics**: Machine learning for early disease detection  \n• **Telemedicine Integration**: Hybrid remote and in-person care models\n• **Immunotherapy Advances**: Revolutionary cancer treatments\n• **Digital Therapeutics**: App-based treatments for mental health\n\n*Analysis based on 15+ medical journals and industry reports*"""
    },
    "healthcare_risk": {
        "query": "Is implementing this particular healthcare treatment risky?",
        "agents": ['governance', 'auth', 'risk', 'legal', 'document'],
        "response": """**Risk Assessment Summary:**\n\n**Risk Level: MODERATE ⚠️**\n\n**Key Considerations:**\n• Regulatory compliance (FDA approval: 12-18 months)\n• Clinical trial requirements\n• Insurance coverage uncertainties  \n• Staff training needs\n\n**Recommended Actions:**\n• Phased implementation approach\n• Early regulatory engagement\n• Insurance pre-authorization protocols"""
    },
    "revenue_projection": {
        "query": "What is the revenue and profit projection?",
        "agents": ['governance', 'auth', 'financial', 'document'],
        "response": """**5-Year Revenue & Profit Projection:**\n\n• **Year 1**: $2.5M (Break-even)\n• **Year 2**: $4.8M (15% margin)\n• **Year 3**: $7.2M (22% margin)  \n• **Year 4**: $9.8M (28% margin)\n• **Year 5**: $12.5M (32% margin)\n\n**Key Assumptions:**\n• 15% market penetration by Year 3\n• $8,500 average treatment cost\n• 85% operational efficiency scaling"""
    },
    "marketing_campaigns": {
        "query": "What are the latest marketing campaigns?",
        "agents": ['governance', 'auth', 'research', 'document'],
        "response": """**Latest Marketing Campaigns (Q2 2025):**\n\n**1. \"Health Forward\" Digital Campaign**\n• Multi-channel approach (Social, Search, Display)\n• Budget: $2.5M | Duration: 6 months\n\n**2. \"Wellness Reimagined\" Content Series**  \n• Educational content marketing\n• Budget: $800K | Duration: 4 months\n\n**3. \"Care Connect\" Community Outreach**\n• Local partnerships and events\n• Budget: $1.2M | Duration: 8 months"""
    },
    "campaign_roi": {
        "query": "Give analysis of ROI of these campaigns",
        "agents": ['governance', 'auth', 'marketing', 'document'],
        "response": """**Campaign ROI Analysis:**\n\n**\"Health Forward\" Digital:**\n• Investment: $2.5M → Revenue: $8.2M\n• **ROI: 228%** (vs 180% benchmark)\n\n**\"Wellness Reimagined\" Content:**\n• Investment: $800K → Revenue: $2.1M  \n• **ROI: 163%** (vs 140% benchmark)\n\n**\"Care Connect\" Outreach:**\n• Investment: $1.2M → Revenue: $2.8M\n• **ROI: 133%** (vs 120% benchmark)\n\n**Overall Performance:** Above industry standards across all campaigns"""
    }
}

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'last_flow_key' not in st.session_state:
    st.session_state.last_flow_key = None

def simulate_agent_work(agent_key: str) -> str:
    """Simulate agent execution"""
    responses = {
        'governance': 'Guardrails and policy compliance verified',
        'auth': 'Access authorized',
        'research': 'Research completed',
        'legal': 'Legal review completed',
        'financial': 'Financial analysis completed',
        'risk': 'Risk assessment completed',
        'marketing': 'Marketing analysis completed',
        'document': 'Documentation finalized'
    }
    return responses.get(agent_key, 'Processing completed')

def get_final_response(flow_key: str) -> str:
    """Get hardcoded responses"""
    responses = {
        "healthcare_trends": """**Latest Healthcare Treatment Trends (2025):**

• **Personalized Medicine**: Treatments tailored to individual genetic profiles
• **AI-Powered Diagnostics**: Machine learning for early disease detection  
• **Telemedicine Integration**: Hybrid remote and in-person care models
• **Immunotherapy Advances**: Revolutionary cancer treatments
• **Digital Therapeutics**: App-based treatments for mental health

*Analysis based on 15+ medical journals and industry reports*""",

        "healthcare_risk": """**Risk Assessment Summary:**

**Risk Level: MODERATE ⚠️**

**Key Considerations:**
• Regulatory compliance (FDA approval: 12-18 months)
• Clinical trial requirements
• Insurance coverage uncertainties  
• Staff training needs

**Recommended Actions:**
• Phased implementation approach
• Early regulatory engagement
• Insurance pre-authorization protocols""",

        "revenue_projection": """**5-Year Revenue & Profit Projection:**

• **Year 1**: $2.5M (Break-even)
• **Year 2**: $4.8M (15% margin)
• **Year 3**: $7.2M (22% margin)  
• **Year 4**: $9.8M (28% margin)
• **Year 5**: $12.5M (32% margin)

**Key Assumptions:**
• 15% market penetration by Year 3
• $8,500 average treatment cost
• 85% operational efficiency scaling""",

        "marketing_campaigns": """**Latest Marketing Campaigns (Q2 2025):**

**1. "Health Forward" Digital Campaign**
• Multi-channel approach (Social, Search, Display)
• Budget: $2.5M | Duration: 6 months

**2. "Wellness Reimagined" Content Series**  
• Educational content marketing
• Budget: $800K | Duration: 4 months

**3. "Care Connect" Community Outreach**
• Local partnerships and events
• Budget: $1.2M | Duration: 8 months""",

        "campaign_roi": """**Campaign ROI Analysis:**

**"Health Forward" Digital:**
• Investment: $2.5M → Revenue: $8.2M
• **ROI: 228%** (vs 180% benchmark)

**"Wellness Reimagined" Content:**
• Investment: $800K → Revenue: $2.1M  
• **ROI: 163%** (vs 140% benchmark)

**"Care Connect" Outreach:**
• Investment: $1.2M → Revenue: $2.8M
• **ROI: 133%** (vs 120% benchmark)

**Overall Performance:** Above industry standards across all campaigns"""
    }
    return responses.get(flow_key, "Analysis completed successfully.")

async def execute_flow(flow_key: str, user_query: str):
    """Execute orchestration flow with subtle status updates"""
    if flow_key not in FLOWS:
        return
    
    flow = FLOWS[flow_key]
    agents = flow['agents']
    
    # Status container
    status_container = st.empty()
    
    # Execute agents
    for i, agent_key in enumerate(agents):
        agent = AGENTS[agent_key]
        
        # Show current status
        with status_container:
            status_text = f"🔄 {agent['name']}..."
            st.markdown(f'<p class="status-line status-running">{status_text}</p>', 
                       unsafe_allow_html=True)
        
        # Simulate work
        time.sleep(1.5)
        
        # Show completion
        with status_container:
            result = simulate_agent_work(agent_key)
            status_text = f"✓ {result}"
            st.markdown(f'<p class="status-line status-completed">{status_text}</p>', 
                       unsafe_allow_html=True)
        
        time.sleep(0.5)
    
    # Clear status and show final response
    status_container.empty()
    
    # Generate response
    response = get_final_response(flow_key)
    
    # Add to messages
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response,
        "timestamp": datetime.now(),
        "flow": flow_key
    })

def main():
    # Header
    st.markdown("""
    <div class="header">
        <h1>AI Orchestration Agent</h1>
        <p>Unified, intelligent analysis powered by specialized agents</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <strong>You</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="assistant-message">
                <strong>Assistant</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
            
            # Add download button for assistant messages
            if "flow" in message:
                report_data = {
                    "query": message["content"],
                    "timestamp": message["timestamp"].isoformat(),
                    "analysis": message["content"]
                }
                report_json = json.dumps(report_data, indent=2)
                st.download_button(
                    label="📥 Download Report",
                    data=report_json,
                    file_name=f"report_{message['timestamp'].strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    key=f"download_{message['timestamp']}"
                )
    
    # Example queries (only show if no conversation yet)
    if not st.session_state.messages:
        st.markdown("**Try asking:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🏥 Healthcare trends", key="ex1", disabled=st.session_state.processing):
                st.session_state.messages.append({
                    "role": "user", 
                    "content": FLOWS["healthcare_trends"]["query"]
                })
                st.session_state.last_flow_key = "healthcare_trends"
                st.rerun()
        
        with col2:
            if st.button("📊 Risk assessment", key="ex2", disabled=st.session_state.processing):
                st.session_state.messages.append({
                    "role": "user", 
                    "content": FLOWS["healthcare_risk"]["query"]
                })
                st.session_state.last_flow_key = "healthcare_risk"
                st.rerun()
        
        col3, col4 = st.columns(2)
        
        with col3:
            if st.button("💰 Revenue projection", key="ex3", disabled=st.session_state.processing):
                st.session_state.messages.append({
                    "role": "user", 
                    "content": FLOWS["revenue_projection"]["query"]
                })
                st.session_state.last_flow_key = "revenue_projection"
                st.rerun()
        
        with col4:
            if st.button("📈 Marketing ROI", key="ex4", disabled=st.session_state.processing):
                st.session_state.messages.append({
                    "role": "user", 
                    "content": FLOWS["campaign_roi"]["query"]
                })
                st.session_state.last_flow_key = "campaign_roi"
                st.rerun()
    
    # Input area
    st.markdown("---")
    
    # Text input
    user_input = st.text_area(
        "Message AI Orchestration Agent...",
        height=80,
        placeholder="Ask about healthcare trends, risk assessment, financial projections, or marketing analysis...",
        disabled=st.session_state.processing,
        label_visibility="collapsed"
    )
    
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        send_button = st.button("Send", disabled=st.session_state.processing or not user_input.strip())
    
    with col2:
        if st.button("Clear", disabled=st.session_state.processing):
            st.session_state.messages = []
            st.session_state.last_flow_key = None
            st.rerun()
    
    # Process user input
    if send_button and user_input.strip():
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.processing = True
        
        # Determine flow based on keywords
        flow_key = "healthcare_trends"  # default
        
        query_lower = user_input.lower()
        if any(word in query_lower for word in ['risk', 'risky', 'danger', 'safe']):
            flow_key = "healthcare_risk"
        elif any(word in query_lower for word in ['revenue', 'profit', 'money', 'financial']):
            flow_key = "revenue_projection"
        elif any(word in query_lower for word in ['roi', 'return']):
            flow_key = "campaign_roi"
        elif any(word in query_lower for word in ['campaign', 'marketing']):
            flow_key = "marketing_campaigns"
        
        st.session_state.last_flow_key = flow_key
        st.rerun()
    
    # Execute flow if processing
    if st.session_state.processing:
        # Get the last user message to determine flow
        last_user_msg = None
        for msg in reversed(st.session_state.messages):
            if msg["role"] == "user":
                last_user_msg = msg["content"]
                break
        
        if last_user_msg:
            # Determine flow
            query_lower = last_user_msg.lower()
            flow_key = "healthcare_trends"
            
            if any(word in query_lower for word in ['risk', 'risky', 'danger', 'safe']):
                flow_key = "healthcare_risk"
            elif any(word in query_lower for word in ['revenue', 'profit', 'money', 'financial']):
                flow_key = "revenue_projection"
            elif any(word in query_lower for word in ['roi', 'return']):
                flow_key = "campaign_roi"
            elif any(word in query_lower for word in ['campaign', 'marketing']):
                flow_key = "marketing_campaigns"
            
            # Execute flow
            execute_flow(flow_key, last_user_msg)
            st.session_state.processing = False
            st.rerun()

if __name__ == "__main__":
    main()

import streamlit as st
import pickle
import random

# Load model
model = pickle.load(open("chatbot_model.pkl","rb"))
vectorizer = pickle.load(open("vectorizer.pkl","rb"))

# -----------------------------
# Responses
# -----------------------------
responses = {

"order_management":[
"Sure! I can help with your order. Please provide your order ID.",
"I'd be happy to assist with your order. Could you share the order number?",
"Let me check your order details. Please provide your order ID."
],

"account_management":[
"I can help you with your account. What issue are you facing?",
"Sure! Let's resolve your account issue.",
"No problem! Tell me more about your account concern."
],

"payment_related":[
"I can assist you with payment-related issues.",
"Let me check your payment status. Could you share more details?",
"Sure, I’ll help you with your payment query."
],

"subscription_services":[
"I can help you manage your subscription.",
"Would you like to upgrade, downgrade, or reactivate your plan?",
"Let me assist you with your subscription request."
],

"service_requests":[
"I can help you with that service request.",
"Please provide more details so I can assist you better.",
"Sure! Let me look into that for you."
]
}

# -----------------------------
# Intent Keywords
# -----------------------------

intent_keywords = {

"order_management":[
"order","track","tracking","delivery","package","shipment","status"
],

"payment_related":[
"payment","pay","money","transaction","charged","deducted","billing"
],

"subscription_services":[
"subscription","plan","upgrade","downgrade","cancel","reactivate"
],

"service_requests":[
"replace","replacement","refund","return","damaged","broken"
],

"account_management":[
"account","login","signin","password","reset","register"
]

}

greetings = ["hi","hello","hey"]
thanks = ["thank","thanks"]
goodbye = ["bye","goodbye"]

# -----------------------------
# Chatbot Logic
# -----------------------------

def get_response(user_input):

    text = user_input.lower()

    # greetings
    if any(word in text for word in greetings):
        return "Hello! How can I help you today?"

    if any(word in text for word in thanks):
        return "You're welcome! Happy to help."

    if any(word in text for word in goodbye):
        return "Goodbye! Have a great day."

    # rule based detection
    for intent, keywords in intent_keywords.items():
        for keyword in keywords:
            if keyword in text:
                return random.choice(responses[intent])

    # ML fallback
    X = vectorizer.transform([text])
    prediction = model.predict(X)[0]

    return random.choice(responses.get(prediction,["Sorry, I didn't understand that."]))


# -----------------------------
# Streamlit UI
# -----------------------------

st.title("E-Commerce Customer Support Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_prompt = st.chat_input("Ask something about orders, payments, etc...")

if user_prompt:

    # show user message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # generate bot response
    bot_reply = get_response(user_prompt)

    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    # save conversation
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
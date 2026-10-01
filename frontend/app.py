import streamlit as st
from api import send_message
from styles import apply_styles


# =================================================
# APPLY STYLES
# =================================================

apply_styles()


# =================================================
# SESSION STATE
# =================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "language" not in st.session_state:
    st.session_state.language = "English"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Medicine status
if "morning_taken" not in st.session_state:
    st.session_state.morning_taken = False

if "afternoon_taken" not in st.session_state:
    st.session_state.afternoon_taken = False

if "night_taken" not in st.session_state:
    st.session_state.night_taken = False


# =================================================
# HELPER FUNCTION
# =================================================

def go_to(page):
    st.session_state.page = page
    st.rerun()


# =================================================
# HOME PAGE
# =================================================

if st.session_state.page == "home":

    st.title("💛 NERAVU")

    st.markdown(
        """
        <p style="
            text-align: center;
            font-size: 24px;
            margin-bottom: 10px;
        ">
            Your friendly AI companion
        </p>

        <p style="
            text-align: center;
            font-size: 18px;
        ">
            Here to listen, remind and help you every day 💛
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # =================================================
    # LANGUAGE
    # =================================================

    st.subheader("🌐 Choose your language")

    st.selectbox(
        "Preferred language",
        [
            "English",
            "ಕನ್ನಡ",
            "हिन्दी",
            "தமிழ்",
            "తెలుగు"
        ],
        key="language"
    )

    st.divider()

    # =================================================
    # WELCOME MESSAGE
    # =================================================

    st.success(
        "👋 Welcome to Neravu! "
        "How can I help you today?"
    )

    st.divider()

    # =================================================
    # MAIN OPTIONS
    # =================================================

    st.subheader("💛 How can Neravu help you?")

    col1, col2 = st.columns(2)

    # -------------------------------------------------
    # TALK
    # -------------------------------------------------

    with col1:

        if st.button(
            "💬 Talk to Neravu",
            key="talk_button",
            use_container_width=True
        ):

            go_to("chat")

    # -------------------------------------------------
    # MEDICINES
    # -------------------------------------------------

    with col2:

        if st.button(
            "💊 My Medicines",
            key="medicine_button",
            use_container_width=True
        ):

            go_to("medicines")

    st.write("")

    col3, col4 = st.columns(2)

    # -------------------------------------------------
    # FAMILY
    # -------------------------------------------------

    with col3:

        if st.button(
            "👨‍👩‍👧 Family & Caregiver",
            key="family_button",
            use_container_width=True
        ):

            go_to("family")

    # -------------------------------------------------
    # EMERGENCY
    # -------------------------------------------------

    with col4:

        if st.button(
            "🚨 Emergency Help",
            key="emergency_button",
            use_container_width=True
        ):

            go_to("emergency")

    st.divider()

    # =================================================
    # QUICK STATUS
    # =================================================

    st.subheader("📋 Today's Status")

    morning = "✅ Taken" if st.session_state.morning_taken else "⏳ Pending"
    afternoon = "✅ Taken" if st.session_state.afternoon_taken else "⏳ Pending"
    night = "✅ Taken" if st.session_state.night_taken else "⏳ Pending"

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🌅 Morning",
            morning
        )

    with col2:
        st.metric(
            "☀️ Afternoon",
            afternoon
        )

    with col3:
        st.metric(
            "🌙 Night",
            night
        )

    st.divider()

    # =================================================
    # VOICE ASSISTANT
    # =================================================

    st.subheader("🎙️ Voice Assistant")

    st.info(
        "You will be able to talk to Neravu using your voice. "
        "Voice recognition will be connected during final integration."
    )

    if st.button(
        "🎙️ Start Voice Conversation",
        key="voice_home",
        use_container_width=True
    ):

        go_to("voice")


# =================================================
# CHAT PAGE
# =================================================

elif st.session_state.page == "chat":

    st.title("💬 Talk to Neravu")

    st.markdown(
        """
        <p style="
            text-align: center;
            font-size: 22px;
        ">
            💛 Hello! I'm Neravu.<br>
            I'm here to listen and help you.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # =================================================
    # NAVIGATION
    # =================================================

    if st.button(
        "⬅️ Back to Home",
        key="chat_back_button",
        use_container_width=True
    ):

        go_to("home")

    if st.button(
        "🧹 Clear Chat",
        key="clear_chat_button",
        use_container_width=True
    ):

        st.session_state.messages = []
        st.rerun()

    st.divider()

    # =================================================
    # CHAT HISTORY
    # =================================================

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    # =================================================
    # TEXT INPUT
    # =================================================

    user_message = st.chat_input(
        "Type your message here..."
    )

    if user_message:

        with st.chat_message("user"):
            st.write(user_message)

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_message
            }
        )

        try:

            response = send_message(
                user_message,
                st.session_state.language
            )

            bot_response = response["reply"]

        except Exception as e:

            st.error(
                f"Could not connect to Neravu: {e}"
            )

            bot_response = (
                "Sorry, I couldn't connect "
                "to Neravu's server right now."
            )

        with st.chat_message("assistant"):
            st.write(bot_response)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": bot_response
            }
        )


# =================================================
# MEDICINES PAGE
# =================================================

elif st.session_state.page == "medicines":

    st.title("💊 My Medicines")

    st.markdown(
        """
        <p style="
            text-align: center;
            font-size: 22px;
        ">
            Here are your medicines for today.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # =================================================
    # BACK
    # =================================================

    if st.button(
        "⬅️ Back to Home",
        key="medicine_back_button",
        use_container_width=True
    ):

        go_to("home")

    st.divider()

    st.subheader("📅 Today's Medicines")

    # =================================================
    # MORNING
    # =================================================

    st.markdown("### 🌅 Morning")

    st.write("💊 **Medicine:** Morning Medicine")
    st.write("⏰ **Time:** 9:00 AM")

    if st.session_state.morning_taken:

        st.success("✅ Medicine Taken")

        if st.button(
            "↩️ Mark as Not Taken",
            key="morning_undo",
            use_container_width=True
        ):

            st.session_state.morning_taken = False
            st.rerun()

    else:

        st.warning("⏳ Medicine Pending")

        if st.button(
            "✓ Mark as Taken",
            key="morning_taken",
            use_container_width=True
        ):

            st.session_state.morning_taken = True
            st.rerun()

    st.divider()

    # =================================================
    # AFTERNOON
    # =================================================

    st.markdown("### ☀️ Afternoon")

    st.write("💊 **Medicine:** Afternoon Medicine")
    st.write("⏰ **Time:** 1:00 PM")

    if st.session_state.afternoon_taken:

        st.success("✅ Medicine Taken")

        if st.button(
            "↩️ Mark as Not Taken",
            key="afternoon_undo",
            use_container_width=True
        ):

            st.session_state.afternoon_taken = False
            st.rerun()

    else:

        st.warning("⏳ Medicine Pending")

        if st.button(
            "✓ Mark as Taken",
            key="afternoon_taken",
            use_container_width=True
        ):

            st.session_state.afternoon_taken = True
            st.rerun()

    st.divider()

    # =================================================
    # NIGHT
    # =================================================

    st.markdown("### 🌙 Night")

    st.write("💊 **Medicine:** Night Medicine")
    st.write("⏰ **Time:** 8:00 PM")

    if st.session_state.night_taken:

        st.success("✅ Medicine Taken")

        if st.button(
            "↩️ Mark as Not Taken",
            key="night_undo",
            use_container_width=True
        ):

            st.session_state.night_taken = False
            st.rerun()

    else:

        st.warning("⏳ Medicine Pending")

        if st.button(
            "✓ Mark as Taken",
            key="night_taken",
            use_container_width=True
        ):

            st.session_state.night_taken = True
            st.rerun()

    st.divider()

    # =================================================
    # MEDICINE SUMMARY
    # =================================================

    completed = sum(
        [
            st.session_state.morning_taken,
            st.session_state.afternoon_taken,
            st.session_state.night_taken
        ]
    )

    st.subheader("📊 Today's Progress")

    st.write(
        f"**{completed} out of 3 medicines completed.**"
    )

    if completed == 3:
        st.success("🎉 All medicines have been taken today!")
    else:
        st.warning(
            "Please remember to take your pending medicines."
        )


# =================================================
# FAMILY & CAREGIVER PAGE
# =================================================

elif st.session_state.page == "family":

    st.title("👨‍👩‍👧 Family & Caregiver")

    st.markdown(
        """
        <p style="
            text-align: center;
            font-size: 22px;
        ">
            Stay connected with your family and caregivers 💛
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # =================================================
    # BACK
    # =================================================

    if st.button(
        "⬅️ Back to Home",
        key="family_back_button",
        use_container_width=True
    ):

        go_to("home")

    st.divider()

    # =================================================
    # FAMILY MEMBER
    # =================================================

    st.subheader("👤 Family Member")

    st.info(
        """
        **Name:** Family Member

        **Relationship:** Son / Daughter

        **Phone:** Contact information will be connected later.
        """
    )

    if st.button(
        "📞 Contact Family Member",
        key="family_contact",
        use_container_width=True
    ):

        st.info(
            "📱 Calling functionality will be connected later."
        )

    st.divider()

    # =================================================
    # CAREGIVER
    # =================================================

    st.subheader("👨‍⚕️ Caregiver Information")

    st.info(
        """
        **Name:** Primary Caregiver

        **Role:** Caregiver

        **Availability:** Available for assistance
        """
    )

    if st.button(
        "📞 Contact Caregiver",
        key="caregiver_contact",
        use_container_width=True
    ):

        st.info(
            "📱 Calling functionality will be connected later."
        )

    st.divider()

    # =================================================
    # MEDICINE STATUS
    # =================================================

    st.subheader("💊 Medicine Status")

    if st.session_state.morning_taken:
        st.write("🌅 Morning medicine — ✅ Taken")
    else:
        st.write("🌅 Morning medicine — ⏳ Pending")

    if st.session_state.afternoon_taken:
        st.write("☀️ Afternoon medicine — ✅ Taken")
    else:
        st.write("☀️ Afternoon medicine — ⏳ Pending")

    if st.session_state.night_taken:
        st.write("🌙 Night medicine — ✅ Taken")
    else:
        st.write("🌙 Night medicine — ⏳ Pending")

    st.divider()

    # =================================================
    # RECENT UPDATES
    # =================================================

    st.subheader("🔔 Recent Updates")

    st.write("✓ Neravu is ready to assist.")

    if st.session_state.morning_taken:
        st.write("✓ Morning medicine completed.")

    if st.session_state.afternoon_taken:
        st.write("✓ Afternoon medicine completed.")

    if st.session_state.night_taken:
        st.write("✓ Night medicine completed.")

    if len(st.session_state.messages) > 0:
        st.write("✓ Neravu conversation recorded.")

    st.divider()

    st.success(
        "💛 Your family and caregiver information "
        "will be connected to the Neravu database later."
    )


# =================================================
# EMERGENCY PAGE
# =================================================

elif st.session_state.page == "emergency":

    st.title("🚨 Emergency Help")

    st.markdown(
        """
        <p style="
            text-align: center;
            font-size: 23px;
        ">
            Don't worry. Neravu is here to help.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # =================================================
    # BACK
    # =================================================

    if st.button(
        "⬅️ Back to Home",
        key="emergency_back",
        use_container_width=True
    ):

        go_to("home")

    st.divider()

    # =================================================
    # EMERGENCY MESSAGE
    # =================================================

    st.error(
        "🚨 If you are experiencing a serious emergency, "
        "please contact your local emergency service "
        "or a trusted person immediately."
    )

    st.subheader("📞 Emergency Contacts")

    # -------------------------------------------------
    # FAMILY
    # -------------------------------------------------

    st.write("👨‍👩‍👧 **Family Member**")

    if st.button(
        "📞 Contact Family",
        key="emergency_family",
        use_container_width=True
    ):

        st.info(
            "Emergency calling will be connected later."
        )

    # -------------------------------------------------
    # CAREGIVER
    # -------------------------------------------------

    st.write("👨‍⚕️ **Caregiver**")

    if st.button(
        "📞 Contact Caregiver",
        key="emergency_caregiver",
        use_container_width=True
    ):

        st.info(
            "Emergency calling will be connected later."
        )

    st.divider()

    # =================================================
    # EMERGENCY INFORMATION
    # =================================================

    st.subheader("🆘 What should I do?")

    st.write(
        """
        1. Stay calm.
        2. Contact a trusted family member or caregiver.
        3. If the situation is serious, contact your local emergency service.
        4. Do not ignore severe symptoms or dangerous situations.
        """
    )

    st.divider()

    st.info(
        "💛 Neravu provides assistance and information, "
        "but it is not a replacement for emergency medical services."
    )


# =================================================
# VOICE PAGE
# =================================================

elif st.session_state.page == "voice":

    st.title("🎙️ Voice Conversation")

    st.markdown(
        """
        <p style="
            text-align: center;
            font-size: 22px;
        ">
            Talk naturally with Neravu 💛
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # =================================================
    # BACK
    # =================================================

    if st.button(
        "⬅️ Back to Home",
        key="voice_back",
        use_container_width=True
    ):

        go_to("home")

    st.divider()

    # =================================================
    # VOICE UI
    # =================================================

    st.subheader("🎙️ Voice Assistant")

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:30px;
            border:2px solid #FFD700;
            border-radius:20px;
            margin:10px 0;
        ">
            <div style="font-size:70px;">🎙️</div>

            <p style="
                font-size:24px;
                color:white;
            ">
                Press the button below to start talking
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "🎙️ Start Listening",
        key="start_voice",
        use_container_width=True
    ):

        st.info(
            "🎙️ Voice recognition will be connected "
            "during final integration."
        )

    st.divider()

    # =================================================
    # VOICE LANGUAGE
    # =================================================

    st.subheader("🌐 Voice Language")

    st.write(
        f"Current language: **{st.session_state.language}**"
    )

    st.write(
        "Neravu will support multilingual voice interaction "
        "after the voice backend is connected."
    )

    st.divider()

    # =================================================
    # VOICE FEATURES
    # =================================================

    st.subheader("✨ Voice Features")

    st.write("🎙️ Speak naturally")
    st.write("🌐 Multiple languages")
    st.write("💬 AI conversation")
    st.write("💊 Medicine reminders")
    st.write("🆘 Emergency assistance")


# =================================================
# FALLBACK
# =================================================

else:

    st.session_state.page = "home"
    st.rerun()
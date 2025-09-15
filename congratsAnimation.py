import streamlit as st
import streamlit.components.v1 as components

# ---------------------------------------------------------------
# Animate confetti and show incentive result


def animate_confetti(final_incentive):
    st.markdown("---")

    # Submit button to trigger the animation
    if st.button("Submit"):
        if final_incentive > 0:
            # Beautiful congrats message with formatted incentive
            st.markdown(f"""
                <div style='text-align: center; padding: 30px 0;'>
                    <h1 style='font-size: 48px; color: #4CAF50; margin-bottom: 10px;'>🎉 Congratulations! 🎉</h1>
                    <h2 style='font-size: 32px; color: #444;'>Your Incentive:</h2>
                    <h2 style='font-size: 36px; color: green; font-weight: bold;'>৳ {final_incentive:,.0f} 🏆</h2>
                    <p style="color: red;"><strong>Note:</strong> This is a preliminary estimate. The final amount may differ based on actual calculations.</p>

                </div>
            """, unsafe_allow_html=True)

            # Confetti JS animation
            components.html("""
                <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.4.0/dist/confetti.browser.min.js"></script>
                <script>
                confetti({
                    particleCount: 200,
                    spread: 100,
                    origin: { y: 0.6 }
                });
                </script>
            """, height=0)

            # Moving emojis with CSS animation
            st.markdown("""
                <style>
                .emoji-container {
                    position: relative;
                    height: 150px;
                    overflow: hidden;
                    margin-top: 30px;
                }
                .emoji {
                    font-size: 32px;
                    position: absolute;
                    animation: float 6s infinite linear;
                }
                @keyframes float {
                    0% { top: 100%; left: 10%; }
                    25% { top: 75%; left: 40%; }
                    50% { top: 50%; left: 70%; }
                    75% { top: 25%; left: 40%; }
                    100% { top: 0%; left: 10%; }
                }
                </style>

                <div class="emoji-container">
                    <div class="emoji">🎈</div>
                    <div class="emoji" style="animation-delay: 1s;">🎉</div>
                    <div class="emoji" style="animation-delay: 2s;">✨</div>
                    <div class="emoji" style="animation-delay: 3s;">🥳</div>
                    <div class="emoji" style="animation-delay: 4s;">🎊</div>
                </div>
            """, unsafe_allow_html=True)

            # Optional Streamlit balloons
            st.balloons()
        else:
            st.warning(
                "Please complete your incentive calculation before submitting.")

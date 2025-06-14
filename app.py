import streamlit as st
import cv2
import tempfile
import numpy as np

st.set_page_config(page_title="Vertical Leap Analyzer", layout="centered")
st.title("🦘 Vertical Leap Analyzer")

video_file = st.file_uploader("Upload your jump video", type=["mp4", "mov", "avi"])

if video_file:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file.read())

    cap = cv2.VideoCapture(tfile.name)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    st.write(f"🎞️ FPS: {fps:.2f}, Total Frames: {total_frames}")

    # Sliders to choose takeoff and landing frames
    takeoff_frame = st.slider("Select Takeoff Frame", 0, total_frames - 1, 0)
    landing_frame = st.slider("Select Landing Frame", 0, total_frames - 1, total_frames - 1)

    def get_frame(frame_number):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        if not ret:
            return None
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

    col1, col2 = st.columns(2)
    with col1:
        frame1 = get_frame(takeoff_frame)
        if frame1 is not None:
            st.image(frame1, caption="Takeoff Frame", use_column_width=True)
    with col2:
        frame2 = get_frame(landing_frame)
        if frame2 is not None:
            st.image(frame2, caption="Landing Frame", use_column_width=True)

    # Physics calculation
    if landing_frame > takeoff_frame:
        time_in_air = (landing_frame - takeoff_frame) / fps
        g = 9.81  # gravity in m/s²
        jump_height = 0.5 * g * (time_in_air / 2)**2  # height = 0.5 * g * (t/2)^2

        st.markdown(f"🕒 Time in air: `{time_in_air:.3f}` seconds")
        st.success(f"🦖 Estimated Jump Height: `{jump_height:.2f}` meters")
    else:
        st.warning("👀 Landing frame must come after takeoff.")

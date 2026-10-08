        st.metric("Overall ATS score", f"{result.overall_score}/100", score_label(result.overall_score),
                  delta_color="off")
        st.progress(result.overall_score / 100)
    with right:
        st.subheader("Summary")
        st.write(result.summary)

    st.subheader("Score breakdown")
    cols = st.columns(4)
    breakdown = [
        ("Keywords", result.keyword_score),
        ("Formatting", result.formatting_score),
        ("Content", result.content_score),
        ("Impact", result.impact_score),
    ]
    for col, (label, value) in zip(cols, breakdown):
        with col:
            st.metric(label, f"{value}/100")
            st.progress(value / 100)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Strengths")
        if result.strengths:
            for s in result.strengths:
                st.markdown(f"- {s}")
        else:
            st.write("None identified.")
    with c2:
        st.subheader("Missing keywords")
        if result.missing_keywords:
            st.write(", ".join(f"`{k}`" for k in result.missing_keywords))
        else:
            st.write("None identified.")

    st.subheader("Recommended improvements")
    order = {"High": 0, "Medium": 1, "Low": 2}
    icons = {"High": "🔴", "Medium": "🟠", "Low": "🟢"}
    for imp in sorted(result.improvements, key=lambda i: order[i.priority]):
        with st.expander(f"{icons[imp.priority]} {imp.priority} · {imp.area}", expanded=imp.priority == "High"):
            st.markdown(f"**Issue:** {imp.issue}")
            st.markdown(f"**Fix:** {imp.suggestion}")

    st.download_button(
        "Download report (JSON)",
        data=result.model_dump_json(indent=2),
        file_name="ats_report.json",
        mime="application/json",
    )


# --------------------------------------------------------------------------
# App
# --------------------------------------------------------------------------
def main() -> None:
    st.set_page_config(page_title="ATS Resume Checker", page_icon="📄", layout="wide")
    st.title("📄 ATS Resume Checker")
    st.caption("Upload your resume to get an ATS score and specific ways to improve it.")

    api_key = get_api_key()
    with st.sidebar:
        st.header("Settings")
        if not api_key:
            api_key = st.text_input("Gemini API key", type="password",
                                    help="Get a free key at https://aistudio.google.com/apikey")
        else:
            st.success("API key loaded")
        st.caption(f"Model: `{get_model()}`")
        st.caption("Your resume is sent to the Gemini API for analysis and is not stored by this app.")

    uploaded = st.file_uploader("Resume", type=["pdf", "docx", "txt"])
    job_description = st.text_area(
        "Job description (optional)",
        height=160,
        placeholder="Paste a job description to score keyword match for a specific role.",
    )

    if st.button("Analyze resume", type="primary", disabled=uploaded is None):
        if not api_key:
            st.error("Please provide a Gemini API key in the sidebar.")
            return
        data = uploaded.getvalue()
        if len(data) > MAX_FILE_MB * 1024 * 1024:
            st.error(f"File is larger than {MAX_FILE_MB} MB.")
            return
        try:
            text = extract_text(uploaded.name, data)
        except ValueError as exc:
            st.error(str(exc))
            return
        except Exception:
            st.error("Could not read this file. It may be corrupted.")
            return
        if len(text) < 100:
            st.error("Could not extract enough text. If this is a scanned/image PDF, "
                     "upload a text-based PDF or a DOCX instead.")
            return

        cache_key = hashlib.sha256((text + "||" + job_description).encode()).hexdigest()
        cache = st.session_state.setdefault("cache", {})
        if cache_key in cache:
            st.session_state["result"] = cache[cache_key]
        else:
            with st.spinner("Analyzing your resume..."):
                try:
                    result = analyze_resume(text, job_description, api_key, get_model())
                except Exception as exc:
                    st.error(f"Analysis failed: {exc}")
                    return
            cache[cache_key] = result
            st.session_state["result"] = result

    if "result" in st.session_state:
        render_result(st.session_state["result"])


if __name__ == "__main__":
    main()

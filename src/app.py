import streamlit as st
import tempfile
import json
import sys
import os
import matplotlib.pyplot as plt

# Fix path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.services.orchestrator import TestOrchestrator

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="AI Test Generator",
    layout="wide"
)

# ---------------------------
# HEADER
# ---------------------------
st.title("🤖 AI-Based API Test Generator")
st.markdown("## 🚀 AI-Powered API Testing Platform")
st.caption("Transforming API specifications into intelligent test suites")

st.divider()

# ---------------------------
# FILE UPLOAD
# ---------------------------
uploaded_file = st.file_uploader("📂 Upload Swagger/OpenAPI JSON", type=["json"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    st.success("✅ File uploaded successfully!")

    # ---------------------------
    # GENERATE BUTTON
    # ---------------------------
    if st.button("🚀 Generate & Execute Tests"):
        try:
            with st.spinner("Processing API, generating and executing tests..."):
                orchestrator = TestOrchestrator(temp_path)
                results = orchestrator.run()

                st.session_state["results"] = results

            st.success("✅ Test cases generated and executed successfully!")

        except Exception as e:
            import traceback
            st.error(f"❌ Error: {str(e)}")
            st.text(traceback.format_exc())

# ---------------------------
# DISPLAY RESULTS + DASHBOARD
# ---------------------------
if "results" in st.session_state:
    results = st.session_state["results"]

    st.divider()
    st.subheader("📊 Execution Dashboard")

    total_tests = 0
    passed = 0
    failed = 0

    for suite in results:
        total_tests += suite["total_tests"]
        for res in suite.get("execution", []):
            if res["status"] == "PASS":
                passed += 1
            elif res["status"] == "FAIL":
                failed += 1

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tests", total_tests)
    col2.metric("Passed", passed)
    col3.metric("Failed", failed)

    # ---------------------------
    # GRAPH VISUALIZATION
    # ---------------------------
    st.subheader("📈 Test Results Visualization")

    labels = ["Passed", "Failed"]
    values = [passed, failed]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%')
    ax.set_title("Test Execution Results")

    st.pyplot(fig)

    st.divider()

    # ---------------------------
    # DISPLAY TESTS WITH STATUS
    # ---------------------------
    for suite in results:
        with st.expander(f"🔹 {suite['endpoint']} ({suite['total_tests']} tests)"):

            execution_map = {
                res["test_id"]: res for res in suite.get("execution", [])
            }

            for tc in suite["test_cases"]:
                exec_result = execution_map.get(tc["test_id"], {})

                status = exec_result.get("status", "N/A")

                if status == "PASS":
                    st.markdown(f"🟢 **{tc['test_id']} — {tc['title']}**")
                elif status == "FAIL":
                    st.markdown(f"🔴 **{tc['test_id']} — {tc['title']}**")
                else:
                    st.markdown(f"⚪ **{tc['test_id']} — {tc['title']}**")

                st.write(f"Category: {tc['category']}")
                st.write(f"Expected: {tc['expected']}")
                st.write(f"Status: {status}")
                st.markdown("---")

    # ---------------------------
    # PERFORMANCE TESTING (k6)
    # ---------------------------
    st.divider()
    st.subheader("⚡ Performance Testing (k6)")

    if st.button("Run Performance Test"):
        try:
            from src.performance.k6_runner import K6Runner

            endpoints = [suite["endpoint"] for suite in results]

            with st.spinner("Running load test..."):
                k6 = K6Runner()
                output = k6.run_test(endpoints)

            st.text_area("k6 Output", output, height=300)

        except Exception as e:
            st.error(f"Error running k6: {str(e)}")

    # ---------------------------
    # DOWNLOAD SECTION
    # ---------------------------
    st.divider()
    st.subheader("⬇️ Download Results")

    # JSON download
    json_data = json.dumps(results, indent=4)

    st.download_button(
        label="📥 Download JSON",
        data=json_data,
        file_name="test_results.json",
        mime="application/json"
    )

    # Text download
    text_output = ""
    for suite in results:
        text_output += f"\n=== {suite['endpoint']} ===\n"
        for tc in suite["test_cases"]:
            text_output += f"\n[{tc['test_id']}] {tc['title']}\n"
            text_output += f"Category: {tc['category']}\n"
            text_output += f"Expected: {tc['expected']}\n"

            exec_result = next(
                (r for r in suite.get("execution", []) if r["test_id"] == tc["test_id"]),
                {}
            )
            text_output += f"Status: {exec_result.get('status', 'N/A')}\n"

    st.download_button(
        label="📄 Download Text",
        data=text_output,
        file_name="test_results.txt",
        mime="text/plain"
    )
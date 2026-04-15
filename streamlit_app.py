import streamlit as st
import json
import pandas as pd
import os

# -------------------------------
# Page Config (must be first Streamlit command)
# -------------------------------
st.set_page_config(page_title="WAD Assignment-5", layout="wide")

st.title("WAD Assignment-5")
st.subheader("Manasa Gunnam (2023000055)")

# -------------------------------
# Load JSON Files (Safe + Correct Path)
# -------------------------------
BASE_DIR = os.path.dirname(__file__)

def load_json(file):
    try:
        path = os.path.join(BASE_DIR, file)
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"{file} not found!")
        return []

students_data = load_json('students.json')
course_data = load_json('courseAnalytics.json')
products_data = load_json('products.json')

# -------------------------------
# Sidebar Navigation
# -------------------------------
option = st.sidebar.selectbox(
    "Select Task",
    ["Student Records", "Course Analytics", "Product App"]
)

# -------------------------------
# 1. Student Records
# -------------------------------
if option == "Student Records":
    st.header("Student Academic Records")

    df = pd.DataFrame(students_data)
    st.subheader("All Students")
    st.dataframe(df)

    st.subheader("Students with CGPA > 8.0")
    high_cgpa = df[df["cgpa"] > 8.0]
    st.dataframe(high_cgpa)

# -------------------------------
# 2. Course Analytics
# -------------------------------
elif option == "Course Analytics":
    st.header("Course Analytics")

    if not course_data:
        st.warning("No course data available")
    else:
        students = course_data["students"]
        df = pd.DataFrame(students)

        st.subheader("All Students")
        st.dataframe(df)

        st.subheader("Students at Academic Risk")

        risk_students = []
        reasons = []

        for s in students:
            reason = []
            if s["attendance_percentage"] < 75:
                reason.append("Low Attendance")
            if s["internal_marks"] < 40:
                reason.append("Low Internal Marks")

            if reason:
                risk_students.append(s["name"])
                reasons.append(", ".join(reason))

        risk_df = pd.DataFrame({
            "Name": risk_students,
            "Reason": reasons
        })

        st.dataframe(risk_df)

        # Averages
        st.subheader("Class Averages")

        avg_internal = df["internal_marks"].mean()

        all_assignments = []
        for s in students:
            all_assignments.extend(s["assignment_scores"])

        avg_assignment = sum(all_assignments) / len(all_assignments)

        st.write("Average Internal Marks:", round(avg_internal, 2))
        st.write("Average Assignment Score:", round(avg_assignment, 2))

# -------------------------------
# 3. Product App
# -------------------------------
elif option == "Product App":
    st.header("Product Management App")

    if "products" not in st.session_state:
        st.session_state.products = products_data

    products = st.session_state.products
    df = pd.DataFrame(products)

    st.subheader("All Products")

    if not df.empty:
        category = st.selectbox(
            "Filter by Category",
            ["All"] + list(df["category"].unique())
        )

        if category != "All":
            filtered_df = df[df["category"] == category]
        else:
            filtered_df = df

        st.dataframe(filtered_df)

        # Average Rating
        st.subheader("Average Rating")
        avg_rating = df["rating"].mean()
        st.write(round(avg_rating, 2))
    else:
        st.warning("No products available")

    # Add Product
    st.subheader("Add New Product")

    name = st.text_input("Product Name")
    price = st.number_input("Price", min_value=0.0)
    category_input = st.text_input("Category")
    rating = st.slider("Rating", 0.0, 5.0, 3.0)

    if st.button("Add Product"):
        new_product = {
            "product_id": len(products) + 1,
            "product_name": name,
            "price": price,
            "category": category_input,
            "rating": rating
        }

        st.session_state.products.append(new_product)
        st.success("Product Added Successfully!")

        st.rerun()

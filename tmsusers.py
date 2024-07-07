import streamlit as st
import pandas as pd
import plotly.express as px
import openpyxl

st.set_page_config(page_title="TEMSCO",page_icon=":factory:",layout="wide")
header = st.container()
header.image('logo.png', width=100) 

# Title of the web app
# أضف CSS لجعل العنوان في منتصف الصفحة
st.markdown("""
    <style>
    .title {
        text-align: center;
        font-size: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title of the web app
with header:
    st.markdown("<h1 class='title'> التمساح الدولية للتصنيع والتجارة - تمسكو </h1>", unsafe_allow_html=True)

st.markdown('<style>div.block-container{padding-top:3rem;}</style>', unsafe_allow_html=True)


# تحميل البيانات
data = pd.read_excel('TMS_users.xlsx', engine='openpyxl')

# تحويل كود الموظف إلى أرقام صحيحة
data['كود الموظف'] = pd.to_numeric(data['كود الموظف'], errors='coerce').astype('Int')

# Filter DataFrame based on selected date range
col1, col2 = st.columns((2, 2))

# إجمالي عدد المستخدمين
total_users = len(data)
st.write(f"### إجمالي عدد المستخدمين: {total_users}")

# الشريط الجانبي للفلاتر
st.sidebar.title('Choose filter :')
department_filter = st.sidebar.multiselect('اختر الادارة', data['الإدارة'].unique())
role_filter = st.sidebar.multiselect('اختر المسمى الوظيفي', data['المسمى'].unique())
user_filter = st.sidebar.multiselect('اختر المستخدم', data['اسم الموظف'].unique())

# تطبيق الفلاتر
filtered_data = data
if department_filter:
    filtered_data = filtered_data[filtered_data['الإدارة'].isin(department_filter)]
if role_filter:
    filtered_data = filtered_data[filtered_data['المسمى'].isin(role_filter)]
if user_filter:
    filtered_data = filtered_data[filtered_data['اسم الموظف'].isin(user_filter)]

# عرض البيانات المصفاة
st.write("##")
st.write(filtered_data)


with col1:
    # توزيع الموظفين حسب القسم
    st.write("### توزيع الموظفين حسب القسم")
    department_counts = filtered_data['الإدارة'].value_counts().reset_index()
    department_counts.columns = ['الإدارة', 'Count']
    fig = px.bar(department_counts, x='الإدارة', y='Count', title='توزيع الموظفين حسب القسم')
    st.plotly_chart(fig)

with col2:
    # توزيع الموظفين حسب الوظيفة
    st.write("### توزيع الموظفين حسب الوظيفة")
    role_counts = filtered_data['المسمى'].value_counts().reset_index()
    role_counts.columns = ['المسمى', 'Count']
    fig = px.pie(role_counts, values='Count', names='المسمى', title='توزيع الموظفين حسب الدور')
    st.plotly_chart(fig)

with col1:
    # توزيع الموظفين حسب النظام
    st.write("### توزيع الموظفين حسب النظام")
    module_counts = filtered_data['النظام'].value_counts().reset_index()
    module_counts.columns = ['Module', 'Count']
    fig = px.scatter(module_counts, x='Module', y='Count', title='توزيع الموظفين حسب الوحدة')
    st.plotly_chart(fig)

with col2:
    # توزيع المستخدمين باستخدام هيستوجرام
    st.write("### توزيع المستخدمين")
    fig = px.histogram(filtered_data, x='اسم الموظف', title='توزيع المستخدمين')
    st.plotly_chart(fig)

# زر لتصدير البيانات المصفاة إلى ملف Excel
st.write("## Export to Excel")
if st.button('تصدير إلى Excel'):
    filtered_data.to_excel('filtered_data.xlsx', index=False)
    st.success('تم تصدير البيانات بنجاح!')

# بدء تشغيل تطبيق Streamlit
if __name__ == '__main__':
    st.sidebar.title(" ")
    st.sidebar.markdown(" ")

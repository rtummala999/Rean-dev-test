import requests
import streamlit as st
import pandas as pd
from io import StringIO


def get_response_from_route(route, input_text):
    response = requests.post(f"http://localhost:8000/{route}/invoke",
                             json={'input': {'text': input_text}})
    return response.json()['output']['content']


def get_combined_response(input_text):
    try:
        emotions_info = get_response_from_route("/emotions", input_text)
        return emotions_info
    except Exception as e:
        return str(e)


st.title('REAN TESTING')
disease = st.text_input("Enter the disease you want FAQs for:")

if disease:
    faq_response = get_combined_response(disease)

    # Parsing the response to extract FAQ data
    faq_lines = faq_response.split("\n")
    faq_data = []
    for i in range(len(faq_lines)):
        if faq_lines[i].startswith('|') and not faq_lines[i].startswith('| **FAQ**'):
            faq_row = faq_lines[i].strip('|').split('|')
            faq_data.append([faq_row[0].strip(), faq_row[1].strip()])

    # Creating a DataFrame from the parsed FAQ data
    faq_df = pd.DataFrame(faq_data, columns=["FAQ", "Answer"])

    # Display DataFrame
    st.write(f"FAQ on {disease} and Diet:")
    st.dataframe(faq_df)

    # Convert DataFrame to CSV
    csv = faq_df.to_csv(index=False)

    # Provide option to download CSV
    st.download_button(label="Download FAQ as CSV", data=csv, file_name=f'{disease}_faq.csv', mime='text/csv')

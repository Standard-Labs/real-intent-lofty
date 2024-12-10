import streamlit as st
import pandas as pd


# Define global variables for column mappings
COLUMN_MAPPINGS = {
    "first_name": "First Name",
    "last_name": "Last Name",
    "email_1": "Email",
    "phone_1": "Phone",
    "phone_1_dnc": "Phone DNC Status",
    "address": "Mailing Street Address",
    "city": "Mailing City",
    "state": "Mailing State",
    "zip_code": "Mailing Zip Code",
    "insight": "Insight" # would have to manually denote this column as "Import as Note" in Lofty,
}

def format_phone_number(phone_number):
    try:
        phone_number = str(int(phone_number))
        return f"{phone_number[:3]}-{phone_number[3:6]}-{phone_number[6:]}" if len(phone_number) == 10 else phone_number
    except Exception as e:
        return phone_number

def main():
    st.title('Real Intent to Lofty Converter')

    st.info("""
    Upload a CSV file. The app will convert your Real Intent CSV into a format that can be imported into Lofty.
    """)

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        # Check if required columns are in the dataframe
        missing_columns = [col for col in COLUMN_MAPPINGS.keys() if col not in df.columns]
        
        if not missing_columns:
            df = df[list(COLUMN_MAPPINGS.keys())].rename(columns=COLUMN_MAPPINGS)

            # Phones in ###-###-#### format
            if 'Phone' in df.columns:
                df['Phone'] = df['Phone'].apply(format_phone_number)

            # From Lofty Docs: To mark as DNC, any of the following three options will work: yes/DNC/out
            if 'Phone DNC Status' in df.columns:
                df['Phone DNC Status'] = df['Phone DNC Status'].apply(lambda x: "DNC" if x else "") 

            df["Source"] = "Real Intent"

            # Display the resulting dataframe
            st.write("Converted DataFrame:")
            st.write(df)
            
            # Download the converted dataframe as CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download converted CSV",
                data=csv,
                file_name='converted_file.csv',
                mime='text/csv',
            )
        else:
            st.write(f"The uploaded file does not contain the required columns: {', '.join(missing_columns)}.")


if __name__ == "__main__":
    main()

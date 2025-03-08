import pandas as pd
import streamlit as st

# Τίτλος εφαρμογής
st.title("📦 Sistem Automatizat de Comenzi")

# Επιλογή χρονικού διαστήματος για παραγγελία
weeks = st.slider("Alegeți perioada de stocare (în săptămâni)", 1.0, 3.0, 2.0, 0.5)

# Μεταφόρτωση αρχείου από τον χρήστη
uploaded_file = st.file_uploader("Încărcați un fișier Excel/CSV", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Ανίχνευση τύπου αρχείου και ανάγνωση
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    # Έλεγχος αν περιέχει τις σωστές στήλες
    required_columns = {"cod", "Nume", "Stock", "SALES", "Rest Comenzi"}
    if not required_columns.issubset(df.columns):
        st.error("Fișierul trebuie să conțină coloanele: cod, Nume, Stock, SALES, Rest Comenzi")
    else:
        # Υπολογισμός προτεινόμενης παραγγελίας με δυναμικό χρονικό διάστημα
        df["Comandă recomandată"] = df.apply(
            lambda row: max((weeks * row["SALES"] + row["Rest Comenzi"]) - row["Stock"], row["Rest Comenzi"]),
            axis=1
        )
        
        # Στρογγυλοποίηση των τιμών
        df["Comandă recomandată"] = df["Comandă recomandată"].round().astype(int)
        
        # Εμφάνιση δεδομένων
        st.write("### Rezultate Calcul", df)
        
        # Εξαγωγή σε Excel
        st.download_button(
            label="📥 Descărcați rezultatele în Excel",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="comenzi_recomandate.csv",
            mime="text/csv"
        )

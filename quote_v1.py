import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Key Innovations Inc.",
    page_icon="https://tscstatic.keyinnovations.ca/logo/logo_1T895ONEIG.png"
)
st.image("https://tscstatic.keyinnovations.ca/logo/logo_1T895ONEIG.png", width=150)
st.title('Quoting System')
st.subheader('Key Innovation Inc.')


# Select the clothing method
st.text('Which method are you using to calculate the price?')

option = st.selectbox(
    "Select an option:", 
    ["Choose Option", "Embroidery", "Screen Print", "Embroidery & Screen Print"]
)


# DataFrame for pricing 
data = {
    "Quantity": ["0-11", "12-17", "18-23", "24-35", "36-59", "60-119", "120-239", "240-600"],
    "1-1,000": [5.00, 4.00, 3.25, 2.75, 2.25, 2.00, 1.75, 1.50],
    "1,000-2,000": [5.50, 4.40, 3.60, 3.05, 2.53, 2.27, 2.01, 1.75],
    "2,001-3,000": [6.00, 4.80, 3.95, 3.35, 2.81, 2.54, 2.27, 2.00],
    "3,001-4,000": [6.50, 5.20, 4.30, 3.65, 3.09, 2.81, 2.53, 2.25],
    "4,001-5,000": [7.00, 5.60, 4.65, 3.95, 3.37, 3.08, 2.79, 2.50],
    "5,001-6,000": [7.50, 6.00, 5.00, 4.25, 3.65, 3.35, 3.05, 2.75],
    "6,001-7,000": [8.00, 6.40, 5.35, 4.55, 3.93, 3.62, 3.31, 3.00],
    "7,001-8,000": [8.50, 6.80, 5.70, 4.85, 4.21, 3.89, 3.57, 3.25],
    "8,001-9,000": [9.00, 7.20, 6.05, 5.15, 4.49, 4.16, 3.83, 3.50],
    "9,001-10,000": [9.50, 7.60, 6.40, 5.45, 4.77, 4.43, 4.09, 3.75],
    "10,001-11,000": [10.00, 8.00, 6.75, 5.75, 5.05, 4.70, 4.35, 4.00],
    "11,001-12,000": [10.50, 8.40, 7.10, 6.05, 5.33, 4.97, 4.61, 4.25],
    "12,001-13,000": [11.00, 8.80, 7.45, 6.35, 5.61, 5.24, 4.87, 4.50],
    "13,001-14,000": [11.50, 9.20, 7.80, 6.65, 5.89, 5.51, 5.13, 4.75],
    "14,001-15,000": [12.00, 9.60, 8.15, 6.95, 6.17, 5.78, 5.39, 5.00],
    "15,001-16,000": [12.50, 10.00, 8.50, 7.25, 6.45, 6.05, 5.65, 5.25],
    "16,001-17,000": [13.00, 10.40, 8.85, 7.55, 6.73, 6.32, 5.91, 5.50],
    "17,001-18,000": [13.50, 10.80, 9.20, 7.85, 7.01, 6.59, 6.17, 5.75],
    "18,001-19,000": [14.00, 11.20, 9.55, 8.15, 7.29, 6.86, 6.43, 6.00],
    "19,001-20,000": [14.50, 11.60, 9.90, 8.45, 7.57, 7.13, 6.69, 6.25]
}
df = pd.DataFrame(data)

net_value = 0

if option == 'Embroidery':
    if "entries" not in st.session_state:
        st.session_state.entries = []

    st.subheader("Enter Item Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        quantity = st.number_input("Enter Quantity", min_value=1, step=1, key="quantity")

    with col2:
        stitch_count = st.selectbox(
            "Select Stitch Count",
            options=list(df.columns[1:]),  
            key="stitch_count"
        )

    with col3:
        item_price = st.number_input('Item Cost (Fixed)', min_value=0.0, step=0.01, key="item_price")

    use_manual_margin = st.checkbox("Use Manual Margin")

    # ✅ Ensure selected_range & stitch_price are always calculated
    selected_range = next((key for key, val in {
        "0-11": range(0, 12), "12-17": range(12, 18), "18-23": range(18, 24),
        "24-35": range(24, 36), "36-59": range(36, 60), "60-119": range(60, 120),
        "120-239": range(120, 240), "240-600": range(240, 601)
    }.items() if quantity in val), "240-600")

    stitch_price = df[df["Quantity"] == selected_range][stitch_count].values[0]

    # ✅ Calculate Net Value Before Margin Selection
    net_value = quantity * (item_price + stitch_price)

    # ✅ Apply Manual Margin if selected
    if use_manual_margin:
        margin_percentage = st.slider("Select Margin (%)", min_value=1.0, max_value=99.0, step=0.5, value=60.0, format="%.2f%%")
        margin = 1 - (margin_percentage / 100)  
    else:
        # ✅ Automatic Margin Selection
        margin_data = [
            (0, 0.4), (150, 0.5), (210, 0.525), (275, 0.55), (345, 0.575),
            (840, 0.6), (1563, 0.625), (2600, 0.65), (4290, 0.66), (6030, 0.67)
        ]
        margin = next((rate for threshold, rate in reversed(margin_data) if net_value >= threshold), 0.67)

    if st.button("➕ Add Entry"):
        if quantity and stitch_count and item_price:
            total_selling_price = net_value / (1 - margin)  
            entry = {
                "Quantity": quantity,
                "Stitch Count": stitch_count,
                "Item Price": item_price,
                "Stitch Price Per Unit": stitch_price,
                "Total Cost": net_value,
                "Margin": margin,
                "Selling Price": total_selling_price
            }
            st.session_state.entries.append(entry)

    if st.session_state.entries:
        st.subheader("Pricing Breakdown")

        for i, entry in enumerate(st.session_state.entries):
            unit_price = entry["Selling Price"] / entry["Quantity"]
            st.text("===========================================================================")

            st.write(f"### Entry {i+1}")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="📌 Quantity", value=entry["Quantity"])
            with col2:
                st.metric(label="🪡 Stitch Count", value=entry["Stitch Count"])
            with col3:
                st.metric(label="💰 Item Cost", value=f"${entry['Item Price']:.2f}")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="🪡 Stitch Price (per unit)", value=f"${entry['Stitch Price Per Unit']:.2f}")
            with col2:
                st.metric(label=f"📊 Unit Price (+{entry['Margin']*100:.2f}% Margin)", value=f"${unit_price:.2f}")
            with col3:
                st.metric(label="💰 Total Selling Price", value=f"${entry['Selling Price']:.2f}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"❌ Delete {i+1}", key=f"delete_{i}"):
                    del st.session_state.entries[i]
                    st.rerun()

        st.text("===========================================================================")
        st.subheader("Final Pricing Summary")

        total_cost = sum(entry['Total Cost'] for entry in st.session_state.entries)
        total_selling_price = sum(entry['Selling Price'] for entry in st.session_state.entries)  

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="📊 Total Cost", value=f"${total_cost:.2f}")
        with col2:
            st.metric(label="💸 Total Selling Price", value=f"${total_selling_price:.2f}")

        if st.button("🔄 Reset Entries"):
            st.session_state.entries = []
            st.rerun()

elif option == 'Screen Print':
    #st.text('You selected Screen Print.')
    # Define pricing DataFrame
    # Pricing Data: Structured from the cleaned data
    # Pricing Data
    pricing_data = {
        "1-Color ScreenPrint": pd.DataFrame({
            "Qty": ["below 6", "6 to 12", "13 - 18", "19 - 24", "25 - 36", "37 - 48","49 - 72", "73 - 96", "97 - 144", "145 - 288", "289 - 500", "Above 500"],
            "4x4": [6.91, 4.26, 3.80, 3.23, 2.62, 2.26, 1.92, 1.60, 1.34, 1.05, 0.79, 0.63],
            "12x12": [9.74, 5.70, 5.01, 4.12, 3.23, 2.68, 2.24, 1.75, 1.41, 1.19, 0.92, 0.75],
            "14x16": [11.05, 6.73, 5.83, 4.75, 3.76, 3.19, 2.72, 2.21, 1.85, 1.55, 1.18, 1],
            "Darks": [0.3, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.2, 0.1, 0.1, 0.1],
            "Fleece": [0.55, 0.55, 0.55, 0.55, 0.55, 0.45, 0.45, 0.45, 0.45, 0.40, 0.40, 0.40],
            "90% Poly+": [0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.4, 0.4, 0.4, 0.25, 0.25, 0.25],
            "Sleeves & Legs":[0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35]
        }),
        "2-Color ScreenPrint": pd.DataFrame({
            "Qty": ["below 6", "6 to 12", "13 - 18", "19 - 24", "25 - 36", "37 - 48","49 - 72", "73 - 96", "97 - 144", "145 - 288", "289 - 500", "Above 500"],
            "4x4": [10.24, 6.63, 5.67, 4.48, 3.58, 3.10, 2.46, 2.06, 1.62, 1.40, 1.05, 0.88],
            "12x12": [15.58, 9.62, 8.06, 6.18, 4.80, 4.20, 3.36, 2.51, 2.05, 1.62, 1.31, 1.08],
            "14x16": [17.95, 11.74, 9.70, 7.25, 5.76, 5.02, 4.09, 2.89, 2.41, 2.03, 1.72, 1.51],
            "Darks": [0.4, 0.4, 0.4, 0.4, 0.4, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2],
            "Fleece": [0.55, 0.55, 0.55, 0.55, 0.55, 0.45, 0.45, 0.45, 0.45, 0.40, 0.40, 0.40],
            "90% Poly+": [0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.4, 0.4, 0.4, 0.25, 0.25, 0.25],
            "Sleeves & Legs":[0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35]
        }),
        "3-Color ScreenPrint": pd.DataFrame({
            "Qty": ["below 6", "6 to 12", "13 - 18", "19 - 24", "25 - 36", "37 - 48","49 - 72", "73 - 96", "97 - 144", "145 - 288", "289 - 500", "Above 500"],
            "4x4": [14.99, 9.38, 7.85, 6.02, 4.77, 3.93, 3.35, 2.72, 2.30, 1.78, 1.51, 1.32],
            "12x12": [24.02, 14.32, 11.85, 8.89, 7.02, 5.71, 4.74, 3.41, 2.81, 2.43, 2.04, 1.75],
            "14x16": [27.50, 16.54, 13.72, 10.32, 8.26, 6.91, 5.64, 4.27, 3.60, 3.01, 2.63, 2.24],
            "Darks": [0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.4, 0.4, 0.4, 0.3, 0.3, 0.3],
            "Fleece": [0.55, 0.55, 0.55, 0.55, 0.55, 0.45, 0.45, 0.45, 0.45, 0.40, 0.40, 0.40],
            "90% Poly+": [0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.4, 0.4, 0.4, 0.25, 0.25, 0.25],
            "Sleeves & Legs":[0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35]
            }),
        "4-Color ScreenPrint": pd.DataFrame({
            "Qty": ["below 6", "6 to 12", "13 - 18", "19 - 24", "25 - 36", "37 - 48","49 - 72", "73 - 96", "97 - 144", "145 - 288", "289 - 500", "Above 500"],
            "4x4": [17.58, 10.86, 9.15, 7.07, 5.52, 4.69, 3.92, 3.32, 2.85, 2.15, 2.01, 1.80],
            "12x12": [28.67, 17.00, 14.13, 10.69, 8.36, 7.08, 5.64, 4.35, 3.62, 2.77, 2.42, 2.29],
            "14x16": [33.32, 19.67, 17.09, 13.87, 9.82, 8.45, 6.85, 5.36, 4.62, 3.47, 3.12, 2.91],
            "Darks": [0.6, 0.6, 0.6, 0.6, 0.6, 0.5, 0.5, 0.5, 0.5, 0.4, 0.4, 0.4],
            "Fleece": [0.55, 0.55, 0.55, 0.55, 0.55, 0.45, 0.45, 0.45, 0.45, 0.40, 0.40, 0.40],
            "90% Poly+": [0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.4, 0.4, 0.4, 0.25, 0.25, 0.25],
            "Sleeves & Legs":[0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35]
            }),
        "5-Color ScreenPrint": pd.DataFrame({
            "Qty": ["below 6", "6 to 12", "13 - 18", "19 - 24", "25 - 36", "37 - 48","49 - 72", "73 - 96", "97 - 144", "145 - 288", "289 - 500", "Above 500"],
            "4x4": [22.22, 12.98, 10.85, 8.26, 6.45, 5.47, 4.58, 3.82, 3.35, 2.51, 2.36, 2.22],
            "12x12": [36.63, 20.84, 17.16, 12.74, 9.90, 8.45, 6.53, 5.25, 4.34, 3.14, 2.77, 2.71],
            "14x16": [43.00, 24.07, 20.28, 15.68, 11.71, 10.00, 8.09, 6.45, 5.36, 3.98, 3.53, 3.26],
            "Darks": [0.75, 0.75, 0.75, 0.75, 0.75, 0.6, 0.6, 0.6, 0.6, 0.5, 0.5, 0.5],
            "Fleece": [0.55, 0.55, 0.55, 0.55, 0.55, 0.45, 0.45, 0.45, 0.45, 0.40, 0.40, 0.40],
            "90% Poly+": [0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.4, 0.4, 0.4, 0.25, 0.25, 0.25],
            "Sleeves & Legs":[0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35]
            }),
        "6-Color ScreenPrint": pd.DataFrame({
            "Qty": ["below 6", "6 to 12", "13 - 18", "19 - 24", "25 - 36", "37 - 48","49 - 72", "73 - 96", "97 - 144", "145 - 288", "289 - 500", "Above 500"],
            "4x4": [26.13, 15.18, 12.59, 9.47, 7.41, 6.23, 4.90, 4.43, 3.85, 2.96, 2.70, 2.57],
            "12x12": [43.39, 24.70, 20.53, 13.01, 11.46, 9.81, 7.51, 6.19, 5.10, 3.60, 3.05, 2.91],
            "14x16": [51.21, 28.57, 23.48, 17.40, 13.62, 11.52, 9.30, 7.63, 6.19, 4.58, 3.88, 3.68],
            "Darks": [0.85, 0.85, 0.85, 0.85, 0.85, 0.7, 0.7, 0.7, 0.7, 0.6, 0.6, 0.6],
            "Fleece": [0.55, 0.55, 0.55, 0.55, 0.55, 0.45, 0.45, 0.45, 0.45, 0.40, 0.40, 0.40],
            "90% Poly+": [0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.4, 0.4, 0.4, 0.25, 0.25, 0.25],
            "Sleeves & Legs":[0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35]
            }),
    }


    # --- Margin Matrix ---
    margin_data = [
        (0, 0.4), (150, 0.5), (210, 0.525), (275, 0.55), (345, 0.575),
        (840, 0.6), (1563, 0.625), (2600, 0.65), (4290, 0.66), (6030, 0.67)
    ]

    # --- Session State Initialization ---
    if "entries_screenprint" not in st.session_state:
        st.session_state.entries_screenprint = []

    # --- User Inputs ---
    col1, col2, col3, col4 = st.columns(4)
    selected_type = col1.selectbox("Select Screen Print Type", pricing_data.keys())
    selected_size = col2.selectbox("Select Print Size", ["4x4", "12x12", "14x16"])
    quantity = col3.number_input("Enter Quantity", min_value=1, step=1)
    selected_options = col4.multiselect("Select Options", ["Darks", "Fleece", "90% Poly+", "Sleeves & Legs"])
    item_cost = st.number_input("Enter Base Item Cost", min_value=0.0, step=0.01)

    use_manual_margin = st.checkbox("Use Manual Margin")

    # --- Determine the Price Tier Based on Quantity ---
    df = pricing_data[selected_type]
    selected_range = next((row["Qty"] for _, row in df.iterrows() if quantity <= int(row["Qty"].split()[-1])), "Above 500")

    # --- Fetch the Price Per Unit ---
    row = df[df["Qty"] == selected_range]
    if not row.empty and item_cost > 0:
        base_price = row[selected_size].values[0]
        unit_price_before_margin = base_price + item_cost

        # --- Apply Additional Costs ---
        for option in selected_options:
            unit_price_before_margin += row[option].values[0]

        # --- Calculate Total Cost Before Margin ---
        total_cost = unit_price_before_margin * quantity

        # --- Apply Manual or Automatic Margin ---
        if use_manual_margin:
            margin_percentage = st.slider("Select Margin (%)", min_value=1.0, max_value=99.0, step=0.5, value=60.0, format="%.2f%%")
            margin = 1 - (margin_percentage / 100)
        else:
            margin = next((rate for threshold, rate in reversed(margin_data) if total_cost >= threshold), 0.67)

        # --- Calculate Selling Prices ---
        total_selling_price = total_cost / margin
        unit_price_after_margin = total_selling_price / quantity

        # --- Add Entry Button ---
        if st.button("➕ Add Entry"):
            entry = {
                "Quantity": quantity,
                "Print Type": selected_type,
                "Print Size": selected_size,
                "Options": ", ".join(selected_options) if selected_options else "None",
                "Item Cost": item_cost,
                "Base Price Per Unit": base_price,
                "Total Cost": total_cost,
                "Margin": margin,
                "Unit Price After Margin": unit_price_after_margin,
                "Total Selling Price": total_selling_price
            }
            st.session_state.entries_screenprint.append(entry)

    # --- Display Pricing Breakdown ---
    if st.session_state.entries_screenprint:
        st.subheader("Pricing Breakdown")

        for i, entry in enumerate(st.session_state.entries_screenprint):
            st.text("===========================================================================")

            st.write(f"### Entry {i+1}")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(label="📌 Quantity", value=entry["Quantity"])
            with col2:
                st.metric(label="🖨️ Print Type", value=entry["Print Type"][:7])
            with col3:
                st.metric(label="📏 Print Size", value=entry["Print Size"])
            with col4:
                st.metric(label="⚙️ Options", value=entry["Options"]) 

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(label="💰 Item Cost", value=f"${entry['Item Cost']:.2f}")
            with col2:
                st.metric(label="🖨️ Base Price Per Unit", value=f"${entry['Base Price Per Unit']:.2f}")
            with col3:
                st.metric(label=f"📊 Unit Price (+{(1 - entry['Margin']) * 100:.2f}% Margin)", value=f"${entry['Unit Price After Margin']:.2f}")
            with col4:
                st.metric(label="💸 Total Selling Price", value=f"${entry['Total Selling Price']:.2f}")



            if st.button(f"❌ Delete {i+1}", key=f"delete_{i}"):
                del st.session_state.entries_screenprint[i]
                st.rerun()

    # --- Final Pricing Summary ---
    if st.session_state.entries_screenprint:
        st.text("===========================================================================")
        st.subheader("Final Pricing Summary")

        total_cost_final = sum(entry['Total Cost'] for entry in st.session_state.entries_screenprint)
        total_selling_price_final = sum(entry['Total Selling Price'] for entry in st.session_state.entries_screenprint)

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="📊 Total Cost", value=f"${total_cost_final:.2f}")
        with col2:
            st.metric(label="💸 Total Selling Price", value=f"${total_selling_price_final:.2f}")

        if st.button("🔄 Reset Entries"):
            st.session_state.entries_screenprint = []
            st.rerun()


elif option == 'Embroidery & Screen Print':
    pass

def footer():
    st.markdown(
        """
        <style>
        @media (max-width: 768px) {
            .footer { 
                display: none; 
            }
        }
        
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            background-color: #f8f9fa;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            border-top: 1px solid #e7e7e7;
        }
        .footer a {
            color: #007bff;
            text-decoration: none;
            margin: 0 10px;
        }
        </style>
        <div class="footer">
            &copy; 2025 Key Innovations Inc. All rights reserved. 
            <br>
            Follow us on:
            <a href="https://www.linkedin.com/company/keyinnovations" target="_blank">LinkedIn</a> |
            <a href="https://twitter.com/keyinnovations" target="_blank">Twitter</a> |
            <a href="https://www.instagram.com/key.innovations/" target="_blank">Instagram</a>
            <a href="https://www.facebook.com/KeyInnovations/" target="_blank">Facebook</a>
        </div>
        """,
        unsafe_allow_html=True
    )

footer()


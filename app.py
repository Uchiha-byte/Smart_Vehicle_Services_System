import streamlit as st
import sqlite3
import os
from dotenv import load_dotenv
from datetime import datetime
import plotly.express as px
import pandas as pd
import uuid

# Load environment variables
load_dotenv('api.env')

# Configure page with dark theme
st.set_page_config(
    page_title="Vehicle Service System",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load external CSS
with open('static/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Custom CSS for dark theme
st.markdown("""
<style>
    /* Dark theme colors */
    :root {
        --background-color: #0E1117;
        --secondary-background-color: #262730;
        --text-color: #FAFAFA;
        --accent-color: #FF4B4B;
    }
    
    .main {
        background-color: var(--background-color);
        color: var(--text-color);
        padding: 0rem 1rem;
    }
    
    .service-card {
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #2E2E2E;
        margin: 10px 0;
        background-color: var(--secondary-background-color);
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        transition: transform 0.2s;
        color: var(--text-color);
    }
    
    .service-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        border: 1px solid var(--accent-color);
    }
    
    .stButton>button {
        width: 100%;
        background-color: var(--accent-color);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #FF6B6B;
    }
    
    .stTextInput>div>div>input {
        background-color: var(--secondary-background-color);
        color: var(--text-color);
        border: 1px solid #2E2E2E;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-color) !important;
    }
    
    .css-145kmo2 {
        color: var(--text-color) !important;
    }
    
    /* Dark theme for data editor */
    .stDataFrame {
        background-color: var(--secondary-background-color);
    }
    
    /* Dark theme for select boxes */
    .stSelectbox>div>div {
        background-color: var(--secondary-background-color);
        color: var(--text-color);
    }
</style>
""", unsafe_allow_html=True)

# Initialize database
def init_db():
    conn = sqlite3.connect('vehicle_service.db')
    c = conn.cursor()
    
    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS staff
                 (staff_id TEXT PRIMARY KEY, name TEXT, duty TEXT, salary REAL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS inventory
                 (part_id TEXT PRIMARY KEY, name TEXT, quantity INTEGER, price REAL, status TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS bookings
                 (booking_id TEXT PRIMARY KEY, customer_name TEXT, vehicle_type TEXT,
                  vehicle_number TEXT, service_type TEXT, booking_date DATE,
                  time_slot TEXT, status TEXT, description TEXT)''')
    
    conn.commit()
    conn.close()

def show_admin_dashboard():
    st.title("Admin Dashboard")
    
    # Create tabs for different admin functions
    tabs = st.tabs(["Staff Management", "Inventory Management", "Booking Management"])
    
    with tabs[0]:  # Staff Management
        st.header("Staff Management")
        st.write("Here you can manage staff members")
        
        # Add staff form
        with st.form("add_staff_form"):
            staff_name = st.text_input("Staff Name")
            staff_duty = st.selectbox("Duty", ["Mechanic", "Helper", "Manager", "Receptionist"])
            staff_salary = st.number_input("Salary", min_value=0.0, step=1000.0)
            submit_staff = st.form_submit_button("Add Staff")
            
            if submit_staff and staff_name and staff_salary > 0:
                conn = sqlite3.connect('vehicle_service.db')
                c = conn.cursor()
                c.execute("INSERT INTO staff (staff_id, name, duty, salary) VALUES (?, ?, ?, ?)",
                         (str(uuid.uuid4()), staff_name, staff_duty, staff_salary))
                conn.commit()
                conn.close()
                st.success("Staff member added successfully!")
        
        # Display staff list
        conn = sqlite3.connect('vehicle_service.db')
        staff_df = pd.read_sql_query("SELECT * FROM staff", conn)
        conn.close()
        
        if not staff_df.empty:
            st.write("Current Staff Members:")
            st.dataframe(staff_df)
    
    with tabs[1]:  # Inventory Management
        st.header("Inventory Management")
        st.write("Here you can manage parts inventory")
        
        # Add inventory form
        with st.form("add_inventory_form"):
            part_name = st.text_input("Part Name")
            quantity = st.number_input("Quantity", min_value=0, step=1)
            price = st.number_input("Price", min_value=0.0, step=100.0)
            status = st.selectbox("Status", ["In Stock", "Low Stock", "Out of Stock"])
            submit_inventory = st.form_submit_button("Add Part")
            
            if submit_inventory and part_name and price > 0:
                conn = sqlite3.connect('vehicle_service.db')
                c = conn.cursor()
                c.execute("INSERT INTO inventory (part_id, name, quantity, price, status) VALUES (?, ?, ?, ?, ?)",
                         (str(uuid.uuid4()), part_name, quantity, price, status))
                conn.commit()
                conn.close()
                st.success("Part added successfully!")
        
        # Display inventory list
        conn = sqlite3.connect('vehicle_service.db')
        inventory_df = pd.read_sql_query("SELECT * FROM inventory", conn)
        conn.close()
        
        if not inventory_df.empty:
            st.write("Current Inventory:")
            st.dataframe(inventory_df)
    
    with tabs[2]:  # Booking Management
        st.header("Booking Management")
        st.write("Here you can view and manage bookings")
        
        # Display bookings
        conn = sqlite3.connect('vehicle_service.db')
        bookings_df = pd.read_sql_query("SELECT * FROM bookings", conn)
        conn.close()
        
        if not bookings_df.empty:
            st.write("Current Bookings:")
            st.dataframe(bookings_df)
        else:
            st.info("No bookings available")

def show_booking_history(customer_name=None):
    st.header("Your Booking History")
    if not customer_name:
        customer_name = st.text_input("Enter your name to view bookings")
    
    if customer_name:
        conn = sqlite3.connect('vehicle_service.db')
        customer_bookings = pd.read_sql_query(
            "SELECT * FROM bookings WHERE customer_name=? ORDER BY booking_date DESC", 
            conn, 
            params=(customer_name,)
        )
        conn.close()
        
        if not customer_bookings.empty:
            for _, booking in customer_bookings.iterrows():
                status_class = f"status-{booking['status'].lower()}"
                st.markdown(f"""
                <div class="booking-card">
                    <h4>Booking ID: {booking['booking_id']}</h4>
                    <p><strong>Date:</strong> {booking['booking_date']}</p>
                    <p><strong>Vehicle:</strong> {booking['vehicle_type']}</p>
                    <p><strong>Service Type:</strong> {booking['service_type']}</p>
                    <p><strong>Time Slot:</strong> {booking['time_slot']}</p>
                    <p><strong>Status:</strong> <span class="booking-status {status_class}">{booking['status']}</span></p>
                    <details>
                        <summary>Service Details</summary>
                        <p>{booking['description'].replace(chr(10), '<br>')}</p>
                    </details>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("You have no bookings yet")
    else:
        st.info("Please enter your name to view your booking history")

def get_vehicle_data():
    return {
        "Car": {
            "Categories": [
                "Hatchback",
                "Sedan",
                "SUV",
                "MPV",
                "Electric",
                "Pickup"
            ],
            "Models": {
                "Hatchback": [
                    "Alto", "WagonR", "Swift", "Baleno", "Celerio", "S-Presso", "Ignis",
                    "Tiago", "Altroz", "Punch", "Nano",
                    "i10", "i20", "Grand i10", "Santro",
                    "Jazz", "Brio", "Amaze",
                    "Sonet",
                    "Polo", "Virtus"
                ],
                "Sedan": [
                    "Dzire", "Ciaz", "SX4",
                    "Tigor", "Indigo", "Manza",
                    "Verna", "Aura", "Elantra", "Sonata",
                    "Camry", "Corolla", "Etios",
                    "City", "Civic", "Accord",
                    "Carens",
                    "Vento",
                    "Rapid", "Superb", "Octavia"
                ],
                "SUV": [
                    "Brezza", "Grand Vitara", "Ertiga", "XL6", "Jimny", "Fronx",
                    "Nexon", "Harrier", "Safari", "Gravitas",
                    "XUV700", "XUV300", "Scorpio", "Bolero", "Thar", "XUV400",
                    "Creta", "Venue", "Alcazar", "Tucson", "Kona Electric",
                    "Fortuner", "Urban Cruiser", "Land Cruiser",
                    "WR-V", "Elevate", "CR-V",
                    "Seltos", "Carnival", "EV6",
                    "Taigun", "T-Roc",
                    "Kodiaq", "Karoq",
                    "Hector", "Astor", "Gloster", "Comet"
                ],
                "MPV": [
                    "Eeco", "Omni",
                    "Innova", "Vellfire",
                    "BR-V",
                    "Starex"
                ],
                "Electric": [
                    "eVX",
                    "Nexon EV", "Tigor EV",
                    "e2o", "eVerito",
                    "bZ4X",
                    "ZS EV"
                ],
                "Pickup": [
                    "Bolero Pickup", "Jeeto", "Bolero Maxi Truck"
                ]
            },
            "Brands": [
                "Maruti Suzuki",
                "Tata",
                "Mahindra",
                "Hyundai",
                "Toyota",
                "Honda",
                "Kia",
                "Volkswagen",
                "Skoda",
                "MG"
            ]
        },
        "Motorcycle": {
            "Categories": [
                "Commuter",
                "Sports",
                "Scooter",
                "Adventure",
                "Classic",
                "Cruiser",
                "Modern Classic",
                "Naked",
                "Perak",
                "Bobber"
            ],
            "Models": {
                "Commuter": [
                    "Shine", "Unicorn", "Livo", "SP 125", "CB Shine", "Dream Yuga",
                    "Pulsar 150", "Platina", "CT 100", "Pulsar 125", "Pulsar NS160",
                    "Apache RTR 160", "Sport", "Star City", "Radeon",
                    "FZ", "FZ-S", "FZ-X", "FZ25",
                    "Intruder", "Access 125",
                    "Splendor", "HF Deluxe", "Passion", "Glamour", "Xtreme"
                ],
                "Sports": [
                    "CBR 150R", "CBR 250R", "CBR 650R", "CB300R",
                    "Pulsar 220F", "Dominar 400", "Pulsar NS200", "Pulsar RS200",
                    "Apache RR 310", "Apache RTR 200", "Apache RTR 180",
                    "R15", "MT-15", "MT-03",
                    "Gixxer", "Gixxer SF", "V-Strom 250",
                    "Xtreme 160R", "Karizma", "Xpulse",
                    "S1000RR", "M1000RR"
                ],
                "Scooter": [
                    "Activa", "Dio", "Jazz", "Grazia", "Aviator",
                    "Chetak", "Platina 110",
                    "Jupiter", "NTorq", "Scooty Pep+", "Scooty Zest",
                    "Fascino", "Ray ZR", "Aerox 155",
                    "Maestro Edge", "Pleasure+", "Destini"
                ],
                "Adventure": [
                    "CB200X", "CB500X",
                    "Adventure 400",
                    "Himalayan", "Scram 411",
                    "Adventure 390", "Adventure 250", "390 Adventure",
                    "V-Strom 650",
                    "GS 310", "F850GS"
                ],
                "Classic": [
                    "Classic 350", "Classic 500", "Classic 650",
                    "Jawa", "Jawa 42"
                ],
                "Cruiser": [
                    "Meteor 350", "Thunderbird", "Super Meteor 650"
                ],
                "Modern Classic": [
                    "Interceptor 650", "Continental GT 650"
                ],
                "Naked": [
                    "Duke 125", "Duke 250",
                    "G310R"
                ],
                "Perak": [
                    "Perak"
                ],
                "Bobber": [
                    "42 Bobber"
                ]
            ],
            "Brands": [
                "Honda",
                "Bajaj",
                "TVS",
                "Royal Enfield",
                "KTM",
                "Yamaha",
                "Suzuki",
                "Hero",
                "Jawa",
                "BMW"
            ]
        }
    }

def search_vehicle(query, vehicle_type=None):
    """Search for vehicles based on query string and optional vehicle type"""
    vehicle_data = get_vehicle_data()
    results = []
    
    # Determine which vehicle types to search
    search_types = [vehicle_type] if vehicle_type else vehicle_data.keys()
    
    for v_type in search_types:
        if v_type not in vehicle_data:
            continue
            
        for brand, categories in vehicle_data[v_type].items():
            for category, models in categories.items():
                for model in models:
                    # Search in brand, category, and model names
                    if (query.lower() in brand.lower() or 
                        query.lower() in category.lower() or 
                        query.lower() in model.lower()):
                        results.append({
                            'type': v_type,
                            'brand': brand,
                            'category': category,
                            'model': model
                        })
    return results

def get_repair_types():
    return {
        "Car": {
            "Engine": [
                "Engine Overhaul",
                "Piston Replacement",
                "Cylinder Head Repair",
                "Timing Belt Replacement",
                "Engine Mount Replacement"
            ],
            "Transmission": [
                "Clutch Replacement",
                "Gearbox Repair",
                "Automatic Transmission Service",
                "Differential Repair",
                "Drive Shaft Replacement"
            ],
            "Brakes": [
                "Brake Pad Replacement",
                "Brake Disc Replacement",
                "Brake Caliper Repair",
                "Brake Line Replacement",
                "ABS System Repair"
            ],
            "Suspension": [
                "Shock Absorber Replacement",
                "Spring Replacement",
                "Control Arm Replacement",
                "Ball Joint Replacement",
                "Wheel Bearing Replacement"
            ],
            "Electrical": [
                "Battery Replacement",
                "Alternator Repair",
                "Starter Motor Replacement",
                "ECU Repair",
                "Wiring Harness Repair"
            ],
            "AC": [
                "AC Compressor Replacement",
                "AC Condenser Repair",
                "AC Evaporator Replacement",
                "AC Gas Refill",
                "AC Control Unit Repair"
            ],
            "Body": [
                "Dent Removal",
                "Paint Work",
                "Panel Replacement",
                "Glass Replacement",
                "Bumper Repair"
            ]
        },
        "Motorcycle": {
            "Engine": [
                "Engine Overhaul",
                "Piston Replacement",
                "Cylinder Head Repair",
                "Valve Adjustment",
                "Engine Mount Replacement"
            ],
            "Transmission": [
                "Clutch Replacement",
                "Gearbox Repair",
                "Chain & Sprocket Replacement",
                "Primary Drive Repair",
                "Gear Shifter Repair"
            ],
            "Brakes": [
                "Brake Pad Replacement",
                "Brake Disc Replacement",
                "Brake Caliper Repair",
                "Brake Line Replacement",
                "ABS System Repair"
            ],
            "Suspension": [
                "Front Fork Repair",
                "Rear Shock Replacement",
                "Swing Arm Repair",
                "Wheel Bearing Replacement",
                "Steering Head Bearing Replacement"
            ],
            "Electrical": [
                "Battery Replacement",
                "Alternator Repair",
                "Starter Motor Replacement",
                "ECU Repair",
                "Wiring Harness Repair"
            ],
            "Body": [
                "Fairing Repair",
                "Paint Work",
                "Panel Replacement",
                "Mirror Replacement",
                "Seat Repair"
            ]
        }
    }

def show_initial_booking_form():
    st.header("Book a Service")
    with st.form("initial_booking_form"):
        customer_name = st.text_input("Your Name")
        vehicle_number = st.text_input("Vehicle Number")
        
        # Vehicle Type Selection
        vehicle_type = st.selectbox("Vehicle Type", ["Car", "Motorcycle"])
        
        # Last service details
        col1, col2 = st.columns(2)
        with col1:
            last_service_date = st.date_input("Last Service Date (if any)", value=None)
        with col2:
            last_service_km = st.number_input("Odometer Reading (KM)", min_value=0)
        
        submit_initial = st.form_submit_button("Continue to Service Selection")
        
        if submit_initial and customer_name and vehicle_number:
            # Store the initial details in session state
            st.session_state.booking_details = {
                'customer_name': customer_name,
                'vehicle_number': vehicle_number,
                'vehicle_type': vehicle_type,
                'last_service_date': last_service_date,
                'last_service_km': last_service_km
            }
            st.session_state.current_page = 'car_service' if vehicle_type == "Car" else 'bike_service'
            st.rerun()

def show_car_service_form():
    st.header("Car Service Booking")
    
    # Get the initial booking details from session state
    booking_details = st.session_state.get('booking_details', {})
    if not booking_details:
        st.error("Please start from the initial booking form")
        if st.button("Go Back"):
            st.session_state.current_page = 'book_service'
            st.rerun()
        return
    
    with st.form("car_service_form"):
        # Get vehicle data
        vehicle_data = get_vehicle_data()
        repair_types = get_repair_types()
        
        # Add search functionality
        search_query = st.text_input("Search for your vehicle (brand, category, or model)")
        if search_query:
            search_results = search_vehicle(search_query, "Car")
            if search_results:
                st.write("Search Results:")
                for result in search_results:
                    st.write(f"- {result['brand']} {result['model']} ({result['category']})")
            else:
                st.info("No matching vehicles found")
        
        # Brand Selection
        vehicle_brand = st.selectbox("Brand", vehicle_data["Car"]["Brands"])
        
        # Category Selection
        vehicle_category = st.selectbox("Category", vehicle_data["Car"]["Categories"])
        
        # Model Selection
        models = vehicle_data["Car"]["Models"][vehicle_category]
        vehicle_model = st.selectbox("Model", models)
        
        service_type = st.selectbox("Service Type", ["Regular Maintenance", "Repair", "Washing", "Inspection", "Custom"])
        
        # Dynamic service options based on type
        if service_type == "Regular Maintenance":
            service_items = st.multiselect("Maintenance Items", [
                "Engine Oil Change",
                "Oil Filter Replacement",
                "Air Filter Cleaning/Replacement",
                "Coolant Check/Top-up",
                "Brake Fluid Check",
                "Wheel Alignment",
                "Wheel Balancing",
                "Tire Rotation",
                "Battery Check",
                "AC Service",
                "General Inspection"
            ])
        elif service_type == "Repair":
            repair_categories = list(repair_types["Car"].keys())
            selected_repair_category = st.selectbox("Repair Category", repair_categories)
            repair_items = repair_types["Car"][selected_repair_category]
            service_items = st.multiselect("Repair Items", repair_items)
        elif service_type == "Washing":
            service_items = st.multiselect("Washing Services", [
                "Basic Wash (Exterior)",
                "Premium Wash (Exterior + Interior)",
                "Deep Cleaning",
                "Interior Vacuuming",
                "Dashboard Polishing",
                "Seat Cleaning",
                "Carpet Cleaning",
                "Waxing & Polishing",
                "Ceramic Coating",
                "Underbody Wash"
            ])
        elif service_type == "Inspection":
            service_items = st.multiselect("Inspection Items", [
                "Pre-purchase Inspection",
                "Annual Safety Check",
                "Insurance Inspection",
                "Warranty Inspection",
                "Performance Check",
                "Emission Test",
                "Brake System Inspection",
                "Suspension Inspection",
                "Electrical System Check",
                "AC System Check"
            ])
        
        booking_date = st.date_input("Preferred Date", min_value=datetime.today())
        time_slot = st.selectbox("Preferred Time Slot", 
                               ["09:00 AM - 11:00 AM", 
                                "11:00 AM - 01:00 PM",
                                "02:00 PM - 04:00 PM",
                                "04:00 PM - 06:00 PM"])
        
        additional_notes = st.text_area("Additional Notes (Optional)")
        
        submit_booking = st.form_submit_button("Book Service")
        
        if submit_booking:
            try:
                # Prepare service description
                service_description = f"Vehicle: {vehicle_brand} {vehicle_model} ({vehicle_category})\n"
                if booking_details.get('last_service_date'):
                    service_description += f"Last Service: {booking_details['last_service_date']}, {booking_details['last_service_km']} KM\n"
                if service_items:
                    service_description += f"Service Items: {', '.join(service_items)}\n"
                if additional_notes:
                    service_description += f"Additional Notes: {additional_notes}"
                
                conn = sqlite3.connect('vehicle_service.db')
                c = conn.cursor()
                c.execute("""
                    INSERT INTO bookings 
                    (booking_id, customer_name, vehicle_type, vehicle_number, 
                     service_type, booking_date, time_slot, status, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (str(uuid.uuid4()), booking_details['customer_name'], 
                      f"Car - {vehicle_brand} {vehicle_model}", 
                      booking_details['vehicle_number'], service_type, 
                      booking_date, time_slot, "Pending", service_description))
                conn.commit()
                conn.close()
                st.success("Service booked successfully!")
                
                # Clear session state and return to home
                st.session_state.booking_details = None
                st.session_state.current_page = 'home'
                st.rerun()
                
        except Exception as e:
                st.error(f"An error occurred while booking: {str(e)}")
                conn.rollback()
            finally:
                if 'conn' in locals():
                    conn.close()

def show_bike_service_form():
    st.header("Motorcycle Service Booking")
    
    # Get the initial booking details from session state
    booking_details = st.session_state.get('booking_details', {})
    if not booking_details:
        st.error("Please start from the initial booking form")
        if st.button("Go Back"):
            st.session_state.current_page = 'book_service'
            st.rerun()
            return
    
    with st.form("bike_service_form"):
        # Get vehicle data
        vehicle_data = get_vehicle_data()
        repair_types = get_repair_types()
        
        # Add search functionality
        search_query = st.text_input("Search for your vehicle (brand, category, or model)")
        if search_query:
            search_results = search_vehicle(search_query, "Motorcycle")
            if search_results:
                st.write("Search Results:")
                for result in search_results:
                    st.write(f"- {result['brand']} {result['model']} ({result['category']})")
            else:
                st.info("No matching vehicles found")
        
        # Brand Selection
        vehicle_brand = st.selectbox("Brand", vehicle_data["Motorcycle"]["Brands"])
        
        # Category Selection
        vehicle_category = st.selectbox("Category", vehicle_data["Motorcycle"]["Categories"])
        
        # Model Selection
        models = vehicle_data["Motorcycle"]["Models"][vehicle_category]
        vehicle_model = st.selectbox("Model", models)
        
        service_type = st.selectbox("Service Type", ["Regular Maintenance", "Repair", "Washing", "Inspection", "Custom"])
        
        # Dynamic service options based on type
        if service_type == "Regular Maintenance":
            service_items = st.multiselect("Maintenance Items", [
                "Engine Oil Change",
                "Oil Filter Replacement",
                "Air Filter Cleaning",
                "Chain Cleaning and Lubrication",
                "Brake Pad Check",
                "Clutch Adjustment",
                "Spark Plug Check/Replacement",
                "Battery Check",
                "General Inspection"
            ])
        elif service_type == "Repair":
            repair_categories = list(repair_types["Motorcycle"].keys())
            selected_repair_category = st.selectbox("Repair Category", repair_categories)
            repair_items = repair_types["Motorcycle"][selected_repair_category]
            service_items = st.multiselect("Repair Items", repair_items)
        elif service_type == "Washing":
            service_items = st.multiselect("Washing Services", [
                "Basic Wash",
                "Premium Wash",
                "Chain Cleaning",
                "Deep Cleaning",
                "Polishing",
                "Ceramic Coating",
                "Engine Cleaning"
            ])
        elif service_type == "Inspection":
            service_items = st.multiselect("Inspection Items", [
                "Pre-purchase Inspection",
                "Annual Safety Check",
                "Insurance Inspection",
                "Warranty Inspection",
                "Performance Check",
                "Emission Test",
                "Brake System Inspection",
                "Suspension Inspection",
                "Electrical System Check"
            ])
        
        booking_date = st.date_input("Preferred Date", min_value=datetime.today())
        time_slot = st.selectbox("Preferred Time Slot", 
                               ["09:00 AM - 11:00 AM", 
                                "11:00 AM - 01:00 PM",
                                "02:00 PM - 04:00 PM",
                                "04:00 PM - 06:00 PM"])
        
        additional_notes = st.text_area("Additional Notes (Optional)")
        
        submit_booking = st.form_submit_button("Book Service")
        
        if submit_booking:
            try:
                # Prepare service description
                service_description = f"Vehicle: {vehicle_brand} {vehicle_model} ({vehicle_category})\n"
                if booking_details.get('last_service_date'):
                    service_description += f"Last Service: {booking_details['last_service_date']}, {booking_details['last_service_km']} KM\n"
                if service_items:
                    service_description += f"Service Items: {', '.join(service_items)}\n"
                if additional_notes:
                    service_description += f"Additional Notes: {additional_notes}"
                
                conn = sqlite3.connect('vehicle_service.db')
                c = conn.cursor()
                c.execute("""
                    INSERT INTO bookings 
                    (booking_id, customer_name, vehicle_type, vehicle_number, 
                     service_type, booking_date, time_slot, status, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (str(uuid.uuid4()), booking_details['customer_name'], 
                      f"Motorcycle - {vehicle_brand} {vehicle_model}", 
                      booking_details['vehicle_number'], service_type, 
                      booking_date, time_slot, "Pending", service_description))
                conn.commit()
                conn.close()
                st.success("Service booked successfully!")
                
                # Clear session state and return to home
                st.session_state.booking_details = None
                st.session_state.current_page = 'home'
                st.rerun()
                
            except Exception as e:
                st.error(f"An error occurred while booking: {str(e)}")
                conn.rollback()
            finally:
                if 'conn' in locals():
                    conn.close()

def show_customer_dashboard():
    st.title("Vehicle Service System")
    
    # Initialize the current page in session state if not exists
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    
    # Back button for all pages except home
    if st.session_state.current_page != 'home':
        if st.button('🏠 Back to Home', use_container_width=True):
            st.session_state.current_page = 'home'
            st.rerun()
    
    # Show the appropriate page based on current_page
    if st.session_state.current_page == 'home':
        # Welcome message
        st.markdown("### Welcome to Vehicle Service System")
        st.write("Select a service to proceed:")
        
        # Create three rows of cards with 2 cards each
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)
        row3_col1, row3_col2 = st.columns(2)
        
        with row1_col1:
            st.markdown("""
            <div class="service-card">
                <h3>📝 Book Service</h3>
                <p>Schedule a new service appointment for your vehicle</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Book Service", key="book_service", use_container_width=True):
                st.session_state.current_page = 'book_service'
                st.rerun()
        
        with row1_col2:
            st.markdown("""
            <div class="service-card">
                <h3>📋 Booking History</h3>
                <p>View your past and upcoming service bookings</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("View History", key="booking_history", use_container_width=True):
                st.session_state.current_page = 'booking_history'
                st.rerun()
        
        with row2_col1:
            st.markdown("""
            <div class="service-card">
                <h3>🔍 Service Status</h3>
                <p>Track the status of your current service</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Check Status", key="service_status", use_container_width=True):
                st.session_state.current_page = 'service_status'
                st.rerun()
        
        with row2_col2:
            st.markdown("""
            <div class="service-card">
                <h3>💰 Cost Calculator</h3>
                <p>Estimate the cost of your service</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Calculate Cost", key="cost_calculator", use_container_width=True):
                st.session_state.current_page = 'cost_calculator'
                st.rerun()
        
        with row3_col1:
            st.markdown("""
            <div class="service-card">
                <h3>💬 Chat Support</h3>
                <p>Get instant help from our support team</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Start Chat", key="chat_support", use_container_width=True):
                st.session_state.current_page = 'chat_support'
                st.rerun()
        
        with row3_col2:
            st.markdown("""
            <div class="service-card">
                <h3>ℹ️ Service Information</h3>
                <p>View our service packages and offerings</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("View Services", key="service_info", use_container_width=True):
                st.session_state.current_page = 'service_info'
                st.rerun()
        
        # Display service highlights at the bottom
        st.markdown("---")
        st.subheader("Our Services")
        highlights_col1, highlights_col2 = st.columns(2)
        
        with highlights_col1:
            st.markdown("### 🚗 Car Services")
            st.write("- Regular Maintenance")
            st.write("- Repair Services")
            st.write("- Body Work")
        
        with highlights_col2:
            st.markdown("### 🏍️ Bike Services")
            st.write("- Periodic Services")
            st.write("- Repairs & Parts")
            st.write("- Performance Tuning")
    
    elif st.session_state.current_page == 'book_service':
        show_initial_booking_form()
    
    elif st.session_state.current_page == 'car_service':
        show_car_service_form()
    
    elif st.session_state.current_page == 'bike_service':
        show_bike_service_form()
    
    elif st.session_state.current_page == 'booking_history':
        show_booking_history(st.session_state.get('customer_name', None))
    
    elif st.session_state.current_page == 'service_status':
        show_service_status()
    
    elif st.session_state.current_page == 'cost_calculator':
        show_service_calculator()
    
    elif st.session_state.current_page == 'chat_support':
        show_chatbot()
    
    elif st.session_state.current_page == 'service_info':
        st.header("Service Information")
        
        # Car Services
        st.subheader("🚗 Car Services")
        car_services_tab1, car_services_tab2 = st.tabs(["Regular Maintenance", "Repairs"])
        
        with car_services_tab1:
            st.markdown("""
            #### Basic Service (₹2,000)
            - Engine Oil Change
            - Oil Filter Replacement
            - General Inspection
            
            #### Standard Service (₹4,000)
            - All Basic Service Items
            - Air Filter Cleaning
            - Brake Check
            - Wheel Alignment
            
            #### Premium Service (₹6,000)
            - All Standard Service Items
            - Complete Diagnostics
            - Detailed Inspection
            - Interior Cleaning
            """)
        
        with car_services_tab2:
            st.markdown("""
            #### Available Repair Services
            - Engine Repair
            - Transmission Service
            - Brake System Repair
            - Suspension Work
            - Electrical Systems
            - AC Service & Repair
            - Body Work & Painting
            
            *Actual costs will be provided after inspection*
            """)
        
        # Bike Services
        st.subheader("🏍️ Bike Services")
        bike_services_tab1, bike_services_tab2 = st.tabs(["Regular Maintenance", "Repairs"])
        
        with bike_services_tab1:
            st.markdown("""
            #### Basic Service (₹1,000)
            - Engine Oil Change
            - Chain Lubrication
            - Basic Inspection
            
            #### Standard Service (₹2,000)
            - All Basic Service Items
            - Air Filter Cleaning
            - Brake Adjustment
            - Chain Adjustment
            
            #### Premium Service (₹3,000)
            - All Standard Service Items
            - Complete Diagnostics
            - Deep Cleaning
            - Performance Tuning
            """)
        
        with bike_services_tab2:
            st.markdown("""
            #### Available Repair Services
            - Engine Work
            - Chain & Sprocket Replacement
            - Clutch Repair
            - Brake System Service
            - Electrical Repairs
            - Tire Services
            - Paint Work
            
            *Actual costs will be provided after inspection*
            """)

def main():
    init_db()
    
    # Main title
    st.markdown("<h1 style='text-align: center;'>Vehicle Service System</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create two columns for the buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Admin Access", use_container_width=True):
            st.session_state['current_view'] = 'admin'
            
    with col2:
        if st.button("Customer Access", use_container_width=True):
            st.session_state['current_view'] = 'customer'
    
    # Show the appropriate dashboard based on button click
    if 'current_view' in st.session_state:
        if st.session_state['current_view'] == 'admin':
            show_admin_dashboard()
        elif st.session_state['current_view'] == 'customer':
            show_customer_dashboard()

if __name__ == "__main__":
    main() 
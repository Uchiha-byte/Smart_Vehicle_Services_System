import streamlit as st
import sqlite3
import os
from dotenv import load_dotenv
from datetime import datetime
import plotly.express as px
import pandas as pd
import uuid
import google.generativeai as genai
from typing import Dict, List, Optional

# Load environment variables
load_dotenv('api.env')

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    st.error("Gemini API key not found. Please check your api.env file.")
    st.stop()

try:
    genai.configure(api_key=GEMINI_API_KEY)
    # Initialize Gemini model with gemini-1.5-flash
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error initializing Gemini API: {str(e)}")
    st.stop()

def get_auto_assist_response(prompt: str, context: Optional[Dict] = None) -> str:
    """
    Get AI-powered suggestions and insights using Gemini API.
    
    Args:
        prompt (str): The user's input or query
        context (Dict, optional): Additional context for better responses
        
    Returns:
        str: AI-generated response
    """
    try:
        # Prepare the full prompt with context
        full_prompt = f"""
        You are an automotive service expert AI assistant. Provide clear, concise responses in bullet points.
        
        Context: {context if context else 'No additional context provided'}
        
        User Query: {prompt}
        
        Please provide your response in this format:
        • Main point 1\n\n
        • Main point 2\n\n
        • Main point 3\n\n
        
        Keep each point brief and easy to understand.
        Make sure each bullet point is on a separate line with a blank line between them.
        """
        
        # Generate response with error handling
        try:
            response = model.generate_content(full_prompt)
            if response and hasattr(response, 'text'):
                return response.text
            else:
                return "I apologize, but I received an invalid response from the AI service. Please try again later."
        except Exception as e:
            st.error(f"Error generating AI response: {str(e)}")
            return "I apologize, but I'm currently unable to provide AI assistance. Please try again later or contact our support team."
    except Exception as e:
        return f"Error getting AI response: {str(e)}"

def get_service_recommendations(vehicle_type: str, vehicle_model: str, service_history: List[Dict]) -> str:
    """
    Get AI-powered service recommendations based on vehicle details and history.
    
    Args:
        vehicle_type (str): Type of vehicle (Car/Motorcycle)
        vehicle_model (str): Model of the vehicle
        service_history (List[Dict]): List of previous service records
        
    Returns:
        str: AI-generated service recommendations
    """
    try:
        prompt = f"""
        Based on the following vehicle information, provide service recommendations in bullet points:
        
        Vehicle Type: {vehicle_type}
        Vehicle Model: {vehicle_model}
        Service History: {service_history}
        
        Please provide your response in this format:
        
        Recommended Maintenance:\n\n
        • Item 1\n\n
        • Item 2\n\n
        
        Common Issues to Watch:\n\n
        • Issue 1\n\n
        • Issue 2\n\n
        
        Preventive Tips:\n\n
        • Tip 1\n\n
        • Tip 2\n\n
        
        Keep each point brief and actionable.
        Make sure each bullet point is on a separate line with a blank line between them.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error getting service recommendations: {str(e)}"

def get_diagnostic_insights(symptoms: str, vehicle_details: Dict) -> str:
    """
    Get AI-powered diagnostic insights based on reported symptoms.
    
    Args:
        symptoms (str): Reported vehicle symptoms/issues
        vehicle_details (Dict): Vehicle information
        
    Returns:
        str: AI-generated diagnostic insights
    """
    try:
        prompt = f"""
        Based on the following symptoms and vehicle details, provide diagnostic insights in bullet points:
        
        Symptoms: {symptoms}
        Vehicle Details: {vehicle_details}
        
        Please provide your response in this format:
        
        Likely Causes:\n\n
        • Cause 1\n\n
        • Cause 2\n\n
        
        Severity Assessment:\n\n
        • Level: [Low/Medium/High]\n\n
        • Immediate Action Required: [Yes/No]\n\n
        
        Recommended Actions:\n\n
        • Action 1\n\n
        • Action 2\n\n
        
        Safety Considerations:\n\n
        • Consideration 1\n\n
        • Consideration 2\n\n
        
        Keep each point clear and concise.
        Make sure each bullet point is on a separate line with a blank line between them.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error getting diagnostic insights: {str(e)}"

def get_staff_assistance(task: str, context: Dict) -> str:
    """
    Get AI-powered assistance for staff members.
    
    Args:
        task (str): The task or query from staff
        context (Dict): Additional context about the task
        
    Returns:
        str: AI-generated assistance
    """
    try:
        prompt = f"""
        As a service center staff assistant, provide guidance in bullet points:
        
        Task: {task}
        Context: {context}
        
        Please provide your response in this format:
        
        Step-by-Step Guidance:\n\n
        • Step 1\n\n
        • Step 2\n\n
        
        Best Practices:\n\n
        • Practice 1\n\n
        • Practice 2\n\n
        
        Common Pitfalls:\n\n
        • Pitfall 1\n\n
        • Pitfall 2\n\n
        
        Quality Check Points:\n\n
        • Check 1\n\n
        • Check 2\n\n
        
        Keep each point brief and practical.
        Make sure each bullet point is on a separate line with a blank line between them.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error getting staff assistance: {str(e)}"

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
                  time_slot TEXT, status TEXT, description TEXT, last_service_date DATE,
                  last_service_km INTEGER, service_items TEXT, additional_notes TEXT)''')
    
    conn.commit()
    conn.close()

def show_admin_dashboard():
    st.title("Admin Dashboard")
    
    # Create tabs for different admin functions
    tabs = st.tabs(["Staff Management", "Inventory Management", "Booking Management", "AI Assistant"])
    
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
        st.write("Manage your inventory here")
        
        # Add inventory form
        with st.form("add_inventory_form"):
            item_name = st.text_input("Item Name")
            quantity = st.number_input("Quantity", min_value=0, step=1)
            price = st.number_input("Price", min_value=0.0, step=0.01)
            submit_inventory = st.form_submit_button("Add Item")
            
            if submit_inventory and item_name and quantity > 0 and price > 0:
                conn = sqlite3.connect('vehicle_service.db')
                c = conn.cursor()
                c.execute("INSERT INTO inventory (item_id, name, quantity, price) VALUES (?, ?, ?, ?)",
                         (str(uuid.uuid4()), item_name, quantity, price))
                conn.commit()
                conn.close()
                st.success("Item added successfully!")
        
        # Display inventory
        conn = sqlite3.connect('vehicle_service.db')
        inventory_df = pd.read_sql_query("SELECT * FROM inventory", conn)
        conn.close()
        
        if not inventory_df.empty:
            st.write("Current Inventory:")
            st.dataframe(inventory_df)
    
    with tabs[2]:  # Booking Management
        st.header("Booking Management")
        st.write("Manage service bookings here")
        
        # Display current bookings
        conn = sqlite3.connect('vehicle_service.db')
        bookings_df = pd.read_sql_query("SELECT * FROM bookings", conn)
        conn.close()
        
        if not bookings_df.empty:
            st.write("Current Bookings:")
            st.dataframe(bookings_df)
            
            # Update booking status
            with st.form("update_booking_status"):
                booking_id = st.selectbox("Select Booking ID", bookings_df['booking_id'].tolist())
                new_status = st.selectbox("New Status", ["Pending", "In Progress", "Completed", "Cancelled"])
                submit_status = st.form_submit_button("Update Status")
                
                if submit_status:
                    conn = sqlite3.connect('vehicle_service.db')
                    c = conn.cursor()
                    c.execute("UPDATE bookings SET status = ? WHERE booking_id = ?",
                             (new_status, booking_id))
                    conn.commit()
                    conn.close()
                    st.success("Booking status updated successfully!")
    
    with tabs[3]:  # AI Assistant
        st.header("AI Assistant")
        st.write("Get AI-powered assistance for your tasks")
        
        # Create tabs for different AI assistance features
        ai_tabs = st.tabs(["General Assistance", "Symptom Checker", "Quick Actions"])
        
        with ai_tabs[0]:  # General Assistance
            # Task input
            task = st.text_area("Describe your task or question")
            
            if task:
                # Get context from database
                conn = sqlite3.connect('vehicle_service.db')
                staff_df = pd.read_sql_query("SELECT * FROM staff", conn)
                inventory_df = pd.read_sql_query("SELECT * FROM inventory", conn)
                bookings_df = pd.read_sql_query("SELECT * FROM bookings", conn)
                conn.close()
                
                context = {
                    "staff_count": len(staff_df),
                    "inventory_items": len(inventory_df),
                    "active_bookings": len(bookings_df[bookings_df['status'] != 'Completed']),
                    "recent_bookings": bookings_df.tail(5).to_dict('records')
                }
                
                if st.button("Get AI Assistance"):
                    with st.spinner("Getting AI assistance..."):
                        assistance = get_staff_assistance(task, context)
                        st.info("AI Assistance:")
                        st.write(assistance)
        
        with ai_tabs[1]:  # Symptom Checker
            st.subheader("Vehicle Symptom Checker")
            
            # Vehicle Type Selection
            vehicle_type = st.selectbox("Select Vehicle Type", ["Car", "Motorcycle"])
            
            # Vehicle Details
            col1, col2 = st.columns(2)
            with col1:
                vehicle_brand = st.selectbox("Select Brand", 
                    sorted(car_models.keys()) if vehicle_type == "Car" else sorted(bike_models.keys()))
            with col2:
                vehicle_model = st.selectbox("Select Model", 
                    sorted(car_models[vehicle_brand]) if vehicle_type == "Car" else sorted(bike_models[vehicle_brand]))
            
            # Vehicle Age and Usage
            col3, col4 = st.columns(2)
            with col3:
                vehicle_age = st.number_input("Vehicle Age (years)", min_value=0, max_value=50, value=0)
            with col4:
                mileage = st.number_input("Current Mileage (KM)", min_value=0, value=0)
            
            # Last Service Details
            col5, col6 = st.columns(2)
            with col5:
                last_service_date = st.date_input("Last Service Date (if any)", value=None)
            with col6:
                last_service_km = st.number_input("Last Service Mileage (KM)", min_value=0, value=0)
            
            # Symptoms Input
            st.subheader("Describe the Symptoms")
            symptoms = st.text_area(
                "Please describe any issues, sounds, or behaviors you've noticed with your vehicle. "
                "Be as detailed as possible about when and how these symptoms occur.",
                height=150
            )
            
            # Additional Context
            st.subheader("Additional Context")
            additional_context = st.text_area(
                "Any additional information that might help diagnose the issue "
                "(e.g., recent repairs, modifications, or unusual driving conditions)",
                height=100
            )
            
            if st.button("Get Diagnostic Analysis"):
                if symptoms:
                    with st.spinner("Analyzing symptoms..."):
                        vehicle_details = {
                            "type": vehicle_type,
                            "brand": vehicle_brand,
                            "model": vehicle_model,
                            "age": vehicle_age,
                            "mileage": mileage,
                            "last_service_date": last_service_date,
                            "last_service_km": last_service_km,
                            "additional_context": additional_context
                        }
                        
                        # Get diagnostic insights
                        diagnosis = get_diagnostic_insights(symptoms, vehicle_details)
                        
                        # Display results in an organized way
                        st.markdown("### Diagnostic Analysis")
                        st.write(diagnosis)
                        
                        # Add a section for preventive maintenance tips
                        st.markdown("### Preventive Maintenance Tips")
                        maintenance_prompt = f"""
                        Based on the vehicle details and symptoms:
                        Vehicle: {vehicle_brand} {vehicle_model}
                        Age: {vehicle_age} years
                        Mileage: {mileage} KM
                        Symptoms: {symptoms}
                        
                        Please provide:
                        1. Preventive maintenance recommendations
                        2. Regular maintenance schedule
                        3. Warning signs to watch for
                        4. Cost-effective maintenance tips
                        """
                        
                        maintenance_tips = get_auto_assist_response(maintenance_prompt)
                        st.write(maintenance_tips)
                else:
                    st.warning("Please describe the symptoms you're experiencing.")
        
        with ai_tabs[2]:  # Quick Actions
            st.subheader("Quick Actions")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Get Staff Performance Insights"):
                    with st.spinner("Analyzing staff performance..."):
                        context = {
                            "staff_data": staff_df.to_dict('records'),
                            "bookings_data": bookings_df.to_dict('records')
                        }
                        insights = get_auto_assist_response(
                            "Analyze staff performance and provide insights for improvement",
                            context
                        )
                        st.info("Staff Performance Insights:")
                        st.write(insights)
            
            with col2:
                if st.button("Get Inventory Optimization Suggestions"):
                    with st.spinner("Analyzing inventory..."):
                        context = {
                            "inventory_data": inventory_df.to_dict('records'),
                            "bookings_data": bookings_df.to_dict('records')
                        }
                        suggestions = get_auto_assist_response(
                            "Analyze inventory levels and provide optimization suggestions",
                            context
                        )
                        st.info("Inventory Optimization Suggestions:")
                        st.write(suggestions)

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
            },
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

# Create car_models and bike_models dictionaries
vehicle_data = get_vehicle_data()
car_models = {}
bike_models = {}

# Populate car_models
for brand in vehicle_data["Car"]["Brands"]:
    car_models[brand] = []
    for category in vehicle_data["Car"]["Categories"]:
        car_models[brand].extend(vehicle_data["Car"]["Models"][category])

# Populate bike_models
for brand in vehicle_data["Motorcycle"]["Brands"]:
    bike_models[brand] = []
    for category in vehicle_data["Motorcycle"]["Categories"]:
        bike_models[brand].extend(vehicle_data["Motorcycle"]["Models"][category])

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
    
    # Get booking details from session state
    booking_details = st.session_state.get('booking_details', {})
    
    # Vehicle Brand and Model Selection
    vehicle_brand = st.selectbox("Select Car Brand", sorted(car_models.keys()))
    vehicle_model = st.selectbox("Select Car Model", sorted(car_models[vehicle_brand]))
    
    # Service Type Selection
    service_type = st.selectbox("Service Type", ["Regular Maintenance", "Repair", "Washing"])
    
    # Auto-assist feature for service recommendations
    if st.button("Get AI Service Recommendations"):
        with st.spinner("Getting personalized recommendations..."):
            # Get service history from database
            conn = sqlite3.connect('vehicle_service.db')
            service_history = pd.read_sql_query(
                "SELECT * FROM bookings WHERE vehicle_type='Car' AND vehicle_number=?",
                conn,
                params=(booking_details.get('vehicle_number', ''),)
            ).to_dict('records')
            conn.close()
            
            recommendations = get_service_recommendations(
                "Car",
                f"{vehicle_brand} {vehicle_model}",
                service_history
            )
            st.info("AI Service Recommendations:")
            st.write(recommendations)
    
    # Service Items Selection based on service type
    service_items = []
    if service_type == "Regular Maintenance":
        service_items = st.multiselect(
            "Select Maintenance Items",
            ["Engine Oil Change", "Oil Filter Replacement", "Air Filter Cleaning", 
             "Brake Check", "Wheel Alignment", "Battery Check", "Tire Rotation"]
        )
    elif service_type == "Repair":
        # Add symptoms input for AI diagnosis
        symptoms = st.text_area("Describe the issues or symptoms you're experiencing")
        if symptoms:
            if st.button("Get AI Diagnosis"):
                with st.spinner("Analyzing symptoms..."):
                    vehicle_details = {
                        "brand": vehicle_brand,
                        "model": vehicle_model,
                        "last_service": booking_details.get('last_service_date'),
                        "last_service_km": booking_details.get('last_service_km')
                    }
                    diagnosis = get_diagnostic_insights(symptoms, vehicle_details)
                    st.info("AI Diagnostic Insights:")
                    st.write(diagnosis)
        
        service_items = st.multiselect(
            "Select Repair Items",
            ["Engine Repair", "Transmission Service", "Brake System Repair",
             "Suspension Work", "Electrical Systems", "AC Service & Repair"]
        )
    elif service_type == "Washing":
        service_items = st.multiselect(
            "Select Washing Package",
            ["Basic Wash", "Premium Wash", "Deep Cleaning"]
        )
    
    # Time Slot Selection
    time_slot = st.selectbox("Preferred Time Slot", 
                           ["09:00 AM - 11:00 AM", 
                            "11:00 AM - 01:00 PM",
                            "02:00 PM - 04:00 PM",
                            "04:00 PM - 06:00 PM"])
    
    additional_notes = st.text_area("Additional Notes (Optional)")
    
    # Auto-assist for additional notes
    if additional_notes:
        if st.button("Get AI Suggestions"):
            with st.spinner("Analyzing your notes..."):
                context = {
                    "vehicle": f"{vehicle_brand} {vehicle_model}",
                    "service_type": service_type,
                    "selected_items": service_items
                }
                suggestions = get_auto_assist_response(additional_notes, context)
                st.info("AI Suggestions:")
                st.write(suggestions)
    
    # Booking form
    with st.form("car_booking_form"):
        submit_booking = st.form_submit_button("Book Service")
        
        if submit_booking:
            try:
                # Prepare service description
                service_description = f"Vehicle: {vehicle_brand} {vehicle_model}\n"
                if booking_details.get('last_service_date'):
                    service_description += f"Last Service: {booking_details['last_service_date']}, {booking_details['last_service_km']} KM\n"
                if service_items:
                    service_description += f"Service Items: {', '.join(service_items)}\n"
                if additional_notes:
                    service_description += f"Additional Notes: {additional_notes}"
                
                conn = sqlite3.connect('vehicle_service.db')
                c = conn.cursor()
                
                # Insert booking into database
                c.execute("""
                    INSERT INTO bookings (
                        booking_id, customer_name, vehicle_type, vehicle_number,
                        service_type, booking_date, time_slot, status, description,
                        last_service_date, last_service_km, service_items, additional_notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(uuid.uuid4()),
                    booking_details['customer_name'],
                    'Car',
                    booking_details['vehicle_number'],
                    service_type,
                    datetime.now().date(),
                    time_slot,
                    'Pending',
                    service_description,
                    booking_details.get('last_service_date'),
                    booking_details.get('last_service_km'),
                    ','.join(service_items) if service_items else None,
                    additional_notes
                ))
                
                conn.commit()
                conn.close()
                
                st.success("Service booked successfully!")
                st.session_state.current_page = 'home'
                st.rerun()
                
            except Exception as e:
                st.error(f"Error booking service: {str(e)}")

def show_bike_service_form():
    st.header("Motorcycle Service Booking")
    
    # Get booking details from session state
    booking_details = st.session_state.get('booking_details', {})
    
    # Vehicle Brand and Model Selection
    vehicle_brand = st.selectbox("Select Bike Brand", sorted(bike_models.keys()))
    vehicle_model = st.selectbox("Select Bike Model", sorted(bike_models[vehicle_brand]))
    
    # Service Type Selection
    service_type = st.selectbox("Service Type", ["Regular Maintenance", "Repair", "Washing"])
    
    # Auto-assist feature for service recommendations
    if st.button("Get AI Service Recommendations"):
        with st.spinner("Getting personalized recommendations..."):
            # Get service history from database
            conn = sqlite3.connect('vehicle_service.db')
            service_history = pd.read_sql_query(
                "SELECT * FROM bookings WHERE vehicle_type='Motorcycle' AND vehicle_number=?",
                conn,
                params=(booking_details.get('vehicle_number', ''),)
            ).to_dict('records')
            conn.close()
            
            recommendations = get_service_recommendations(
                "Motorcycle",
                f"{vehicle_brand} {vehicle_model}",
                service_history
            )
            st.info("AI Service Recommendations:")
            st.write(recommendations)
    
    # Service Items Selection based on service type
    service_items = []
    if service_type == "Regular Maintenance":
        service_items = st.multiselect(
            "Select Maintenance Items",
            ["Engine Oil Change", "Oil Filter Replacement", "Air Filter Cleaning",
             "Chain Cleaning", "Brake Adjustment", "Battery Check", "Tire Pressure Check"]
        )
    elif service_type == "Repair":
        # Add symptoms input for AI diagnosis
        symptoms = st.text_area("Describe the issues or symptoms you're experiencing")
        if symptoms:
            if st.button("Get AI Diagnosis"):
                with st.spinner("Analyzing symptoms..."):
                    vehicle_details = {
                        "brand": vehicle_brand,
                        "model": vehicle_model,
                        "last_service": booking_details.get('last_service_date'),
                        "last_service_km": booking_details.get('last_service_km')
                    }
                    diagnosis = get_diagnostic_insights(symptoms, vehicle_details)
                    st.info("AI Diagnostic Insights:")
                    st.write(diagnosis)
        
        service_items = st.multiselect(
            "Select Repair Items",
            ["Engine Work", "Chain & Sprocket Replacement", "Clutch Repair",
             "Brake System Service", "Electrical Repairs", "Tire Services"]
        )
    elif service_type == "Washing":
        service_items = st.multiselect(
            "Select Washing Package",
            ["Basic Wash", "Premium Wash", "Deep Cleaning"]
        )
    
    # Time Slot Selection
    time_slot = st.selectbox("Preferred Time Slot", 
                           ["09:00 AM - 11:00 AM", 
                            "11:00 AM - 01:00 PM",
                            "02:00 PM - 04:00 PM",
                            "04:00 PM - 06:00 PM"])
    
    additional_notes = st.text_area("Additional Notes (Optional)")
    
    # Auto-assist for additional notes
    if additional_notes:
        if st.button("Get AI Suggestions"):
            with st.spinner("Analyzing your notes..."):
                context = {
                    "vehicle": f"{vehicle_brand} {vehicle_model}",
                    "service_type": service_type,
                    "selected_items": service_items
                }
                suggestions = get_auto_assist_response(additional_notes, context)
                st.info("AI Suggestions:")
                st.write(suggestions)
    
    # Booking form
    with st.form("bike_booking_form"):
        submit_booking = st.form_submit_button("Book Service")
        
        if submit_booking:
            try:
                # Prepare service description
                service_description = f"Vehicle: {vehicle_brand} {vehicle_model}\n"
                if booking_details.get('last_service_date'):
                    service_description += f"Last Service: {booking_details['last_service_date']}, {booking_details['last_service_km']} KM\n"
                if service_items:
                    service_description += f"Service Items: {', '.join(service_items)}\n"
                if additional_notes:
                    service_description += f"Additional Notes: {additional_notes}"
                
                conn = sqlite3.connect('vehicle_service.db')
                c = conn.cursor()
                
                # Insert booking into database
                c.execute("""
                    INSERT INTO bookings (
                        booking_id, customer_name, vehicle_type, vehicle_number,
                        service_type, booking_date, time_slot, status, description,
                        last_service_date, last_service_km, service_items, additional_notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(uuid.uuid4()),
                    booking_details['customer_name'],
                    'Motorcycle',
                    booking_details['vehicle_number'],
                    service_type,
                    datetime.now().date(),
                    time_slot,
                    'Pending',
                    service_description,
                    booking_details.get('last_service_date'),
                    booking_details.get('last_service_km'),
                    ','.join(service_items) if service_items else None,
                    additional_notes
                ))
                
                conn.commit()
                conn.close()
                
                st.success("Service booked successfully!")
                st.session_state.current_page = 'home'
                st.rerun()
                
            except Exception as e:
                st.error(f"Error booking service: {str(e)}")

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
        highlights_col1, highlights_col2, highlights_col3 = st.columns(3)
        
        with highlights_col1:
            st.markdown("### 🚗 Car Services")
            st.write("- Regular Maintenance")
            st.write("- Repair Services")
            st.write("- Body Work")
            st.write("- Washing Services")
            st.write("  • Basic Wash")
            st.write("  • Premium Wash")
            st.write("  • Deep Cleaning")
            st.write("  • Interior Detailing")
        
        with highlights_col2:
            st.markdown("### 🏍️ Bike Services")
            st.write("- Periodic Services")
            st.write("- Repairs & Parts")
            st.write("- Performance Tuning")
            st.write("- Washing Services")
            st.write("  • Basic Wash")
            st.write("  • Premium Wash")
            st.write("  • Deep Cleaning")
            st.write("  • Engine Cleaning")
        
        with highlights_col3:
            st.markdown("### 💧 Washing Packages")
            st.write("#### Car Packages")
            st.write("- Basic Wash: ₹500")
            st.write("  • Exterior Wash")
            st.write("  • Tire Cleaning")
            st.write("  • Basic Interior")
            st.write("- Premium Wash: ₹1,000")
            st.write("  • All Basic Services")
            st.write("  • Interior Detailing")
            st.write("  • Waxing")
            st.write("- Deep Cleaning: ₹2,000")
            st.write("  • All Premium Services")
            st.write("  • Engine Bay Cleaning")
            st.write("  • Ceramic Coating")
            st.write("#### Bike Packages")
            st.write("- Basic Wash: ₹200")
            st.write("  • Exterior Wash")
            st.write("  • Chain Cleaning")
            st.write("- Premium Wash: ₹500")
            st.write("  • All Basic Services")
            st.write("  • Deep Cleaning")
            st.write("  • Polishing")
    
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
        car_services_tab1, car_services_tab2, car_services_tab3 = st.tabs(["Regular Maintenance", "Repairs", "Washing Services"])
        
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
            
        with car_services_tab3:
            st.markdown("""
            #### Basic Wash Package (₹500)
            - Exterior Wash
            - Tire Cleaning
            - Basic Interior Cleaning
            - Window Cleaning
            
            #### Premium Wash Package (₹1,000)
            - All Basic Wash Services
            - Interior Detailing
            - Dashboard Polishing
            - Seat Cleaning
            - Carpet Cleaning
            - Waxing & Polishing
            
            #### Deep Cleaning Package (₹2,000)
            - All Premium Wash Services
            - Engine Bay Cleaning
            - Underbody Wash
            - Ceramic Coating
            - Leather Treatment
            - Odor Removal
            """)
        
        # Bike Services
        st.subheader("🏍️ Bike Services")
        bike_services_tab1, bike_services_tab2, bike_services_tab3 = st.tabs(["Regular Maintenance", "Repairs", "Washing Services"])
        
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
            
        with bike_services_tab3:
            st.markdown("""
            #### Basic Wash Package (₹200)
            - Exterior Wash
            - Chain Cleaning
            - Basic Inspection
            
            #### Premium Wash Package (₹500)
            - All Basic Wash Services
            - Deep Cleaning
            - Polishing
            - Chain Lubrication
            - Tire Dressing
            
            #### Deep Cleaning Package (₹1,000)
            - All Premium Wash Services
            - Engine Cleaning
            - Metal Polishing
            - Ceramic Coating
            - Paint Protection
            """)

def show_service_calculator():
    st.header("Service Cost Calculator")
    
    # Vehicle Type Selection
    vehicle_type = st.selectbox("Select Vehicle Type", ["Car", "Motorcycle"])
    
    # Service Type Selection
    service_type = st.selectbox("Select Service Type", ["Regular Maintenance", "Repair", "Washing", "Inspection"])
    
    # Get repair types for the selected vehicle type
    repair_types = get_repair_types()
    
    # Calculate base cost based on vehicle type and service type
    base_cost = 0
    if vehicle_type == "Car":
        if service_type == "Regular Maintenance":
            base_cost = 2000
        elif service_type == "Washing":
            base_cost = 500
        elif service_type == "Inspection":
            base_cost = 1000
    else:  # Motorcycle
        if service_type == "Regular Maintenance":
            base_cost = 1000
        elif service_type == "Washing":
            base_cost = 200
        elif service_type == "Inspection":
            base_cost = 500
    
    # Additional costs based on service type
    additional_cost = 0
    
    if service_type == "Regular Maintenance":
        st.subheader("Maintenance Items")
        col1, col2 = st.columns(2)
        
        with col1:
            if vehicle_type == "Car":
                items = [
                    ("Engine Oil Change", 500),
                    ("Oil Filter Replacement", 300),
                    ("Air Filter Cleaning", 400),
                    ("Brake Check", 600),
                    ("Wheel Alignment", 800)
                ]
            else:
                items = [
                    ("Engine Oil Change", 300),
                    ("Oil Filter Replacement", 200),
                    ("Air Filter Cleaning", 250),
                    ("Chain Cleaning", 200),
                    ("Brake Adjustment", 300)
                ]
            
            for item, cost in items:
                if st.checkbox(f"{item} (₹{cost})"):
                    additional_cost += cost
    
    elif service_type == "Repair":
        st.subheader("Repair Items")
        repair_categories = list(repair_types[vehicle_type].keys())
        selected_category = st.selectbox("Select Repair Category", repair_categories)
        
        repair_items = repair_types[vehicle_type][selected_category]
        selected_items = st.multiselect("Select Repair Items", repair_items)
        
        # Add cost for each selected repair item
        for item in selected_items:
            if "Engine" in item:
                additional_cost += 5000
            elif "Transmission" in item:
                additional_cost += 4000
            elif "Brake" in item:
                additional_cost += 2000
            elif "Suspension" in item:
                additional_cost += 3000
            elif "Electrical" in item:
                additional_cost += 1500
            elif "AC" in item:
                additional_cost += 2500
            else:
                additional_cost += 1000
    
    elif service_type == "Washing":
        st.subheader("Washing Services")
        if vehicle_type == "Car":
            packages = [
                ("Basic Wash", 500, ["Exterior Wash", "Tire Cleaning", "Basic Interior"]),
                ("Premium Wash", 1000, ["All Basic Services", "Interior Detailing", "Waxing"]),
                ("Deep Cleaning", 2000, ["All Premium Services", "Engine Bay Cleaning", "Ceramic Coating"])
            ]
        else:
            packages = [
                ("Basic Wash", 200, ["Exterior Wash", "Chain Cleaning"]),
                ("Premium Wash", 500, ["All Basic Services", "Deep Cleaning", "Polishing"]),
                ("Deep Cleaning", 1000, ["All Premium Services", "Engine Cleaning", "Ceramic Coating"])
            ]
        
        selected_package = st.radio("Select Washing Package", [p[0] for p in packages])
        for package, cost, _ in packages:
            if package == selected_package:
                additional_cost = cost
                break
    
    # Calculate total cost
    total_cost = base_cost + additional_cost
    
    # Display cost breakdown
    st.markdown("---")
    st.subheader("Cost Breakdown")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"Base Cost: ₹{base_cost}")
        st.write(f"Additional Services: ₹{additional_cost}")
    
    with col2:
        st.markdown(f"### Total Cost: ₹{total_cost}")
    
    # Disclaimer
    st.info("Note: This is an estimated cost. Final cost may vary based on actual service requirements and parts needed.")

def show_chatbot():
    st.header("Chat Support")
    
    # Initialize chat history in session state if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("How can I help you today?"):
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate response based on common queries and troubleshooting
        response = generate_chat_response(prompt)
        
        # Add assistant response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.write(response)

def generate_chat_response(prompt):
    """Generate a response based on the user's prompt"""
    prompt = prompt.lower()
    
    # Common queries and their responses
    responses = {
        "service": "We offer various services including regular maintenance, repairs, washing, and inspections. You can find detailed information in the 'Service Information' section.",
        "price": "Our service prices vary based on the type of service and vehicle. You can use the 'Cost Calculator' to get an estimate for your specific needs.",
        "booking": "To book a service, click on 'Book Service' from the home page. You'll need to provide your vehicle details and preferred service date.",
        "time": "Our service center is open from 8:00 AM to 9:00 PM, Monday through Saturday. We're closed on Sundays.",
        "location": "We are located at 123 Service Street, Auto City. You can find us easily using any map application.",
        "contact": "You can reach us at:\nPhone: 123-456-7890\nEmail: support@vehicleservice.com",
        "warranty": "We provide a 3-month warranty on all our services. For more details, please check our warranty policy in the Service Information section.",
        "payment": "We accept cash, credit/debit cards, and digital payments. Payment is due upon service completion.",
        "cancel": "You can cancel your booking up to 24 hours before the scheduled time. Please contact our support team for cancellation.",
        "status": "To check your service status, go to 'Service Status' from the home page and enter your booking ID."
    }
    
    # Check for keywords in the prompt
    for keyword, response in responses.items():
        if keyword in prompt:
            return response
    
    # If no common query matches, try to provide troubleshooting assistance
    try:
        troubleshooting_prompt = f"""
        As an automotive troubleshooting assistant, provide a simple solution for the following issue:
        
        User Query: {prompt}
        
        Please provide your response in this format:
        
        Quick Diagnosis:\n\n
        • [Brief assessment of the problem]\n\n
        
        Simple Solutions:\n\n
        • [Step 1 - Most basic solution]\n\n
        • [Step 2 - If step 1 doesn't work]\n\n
        
        When to Visit Service Center:\n\n
        • [Warning signs that indicate professional help is needed]\n\n
        
        Keep the response brief, practical, and easy to understand.
        Focus on simple solutions that can be done at home.
        """
        
        response = model.generate_content(troubleshooting_prompt)
        if response and hasattr(response, 'text'):
            return response.text
        else:
            return "I'm here to help! You can ask me about our services, prices, booking process, operating hours, location, contact information, warranty, payment methods, cancellation policy, or service status. What would you like to know?"
    except Exception as e:
        return "I'm here to help! You can ask me about our services, prices, booking process, operating hours, location, contact information, warranty, payment methods, cancellation policy, or service status. What would you like to know?"

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
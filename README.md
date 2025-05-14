# Vehicle Service Management System

A modern, AI-powered vehicle service management system built with Python and Streamlit.

## Features

### Admin Dashboard
- Staff Management (CRUD operations)
- Inventory Tracking
- Service Booking Management
- Analytics Dashboard

### Customer Portal
- AI-Powered Problem Diagnosis
- Service Booking System
- Real-time Chat Support
- Service History Tracking

## Setup Instructions

1. Clone the repository:
```bash
git clone <https://github.com/Uchiha-byte/Smart_Vehicle_Services_System.git>
cd vehicle-service-system
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

5. Initialize the database:
```bash
python init_db.py
```

6. Run the application:
```bash
streamlit run app.py
```

## Default Login Credentials

### Admin
- Username: admin
- Password: admin123

### Customer
- Username: customer
- Password: customer123

## Project Structure

```
vehicle_service_system/
├── app.py                # Main application
├── pages/               # Streamlit pages
│   ├── admin/          # Admin dashboard pages
│   └── customer/       # Customer portal pages
├── database/           # Database operations
├── utils/             # Helper functions
└── assets/           # Static files
```

## Technologies Used

- Python 3.8+
- Streamlit
- SQLite
- Google Gemini AI
- Plotly
- Pandas

## Features in Detail

### Admin Side

1. **Staff Management**
   - Add/Edit/Remove staff
   - Track attendance
   - Manage salaries
   - View performance metrics

2. **Inventory Management**
   - Track parts inventory
   - Low stock alerts
   - Purchase order generation
   - Usage analytics

3. **Service Management**
   - View all bookings
   - Update service status
   - Generate reports
   - Customer history

### Customer Side

1. **Service Booking**
   - AI-powered problem diagnosis
   - Real-time slot availability
   - Service cost estimation
   - Booking confirmation

2. **Support System**
   - 24/7 AI chatbot
   - Emergency assistance
   - Service history
   - Maintenance tips

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
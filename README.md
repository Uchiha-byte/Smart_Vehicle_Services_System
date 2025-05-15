# Vehicle Service Management System

A modern, AI-powered vehicle service management system built with Python and Streamlit. This system provides a comprehensive solution for managing vehicle services, from customer bookings to service tracking and inventory management.

## Features

### Admin Dashboard
- Staff Management (CRUD operations)
- Inventory Tracking
- Service Booking Management
- Analytics Dashboard
- Real-time Service Status Updates
- **Auto-Assist Feature**: Leverage AI to provide staff with intelligent suggestions and insights.

### Customer Portal
- AI-Powered Problem Diagnosis using Google Gemini
- Service Booking System
- Real-time Chat Support
- Service History Tracking
- Maintenance Reminders
- **Auto-Assist Feature**: Get personalized service recommendations and insights.

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Git

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/Uchiha-byte/Smart_Vehicle_Services_System.git
cd Smart_Vehicle_Services_System
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create an `api.env` file in the root directory with your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

5. Run the application:
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
├── static/             # Static files and assets
├── vehicle_service.db  # SQLite database
├── requirements.txt    # Project dependencies
├── api.env            # Environment variables
└── venv/              # Virtual environment
```

## Technologies Used

- **Python 3.8+**: Core programming language
- **Streamlit 1.45.1**: Web application framework
- **Google Gemini AI**: AI-powered problem diagnosis and auto-assist feature
- **Pandas 2.2.3**: Data manipulation and analysis
- **Plotly 5.19.0**: Interactive data visualization
- **Pillow 11.2.1**: Image processing
- **Python-dotenv 1.0.1**: Environment variable management
- **SQLite**: Database management

## Features in Detail

### Admin Side

1. **Staff Management**
   - Add/Edit/Remove staff members
   - Track staff attendance
   - Manage staff schedules
   - View performance metrics

2. **Inventory Management**
   - Real-time parts inventory tracking
   - Low stock alerts
   - Purchase order generation
   - Inventory usage analytics

3. **Service Management**
   - View and manage service bookings
   - Update service status in real-time
   - Generate detailed service reports
   - Track customer service history
   - **Auto-Assist**: Use AI to provide staff with insights and suggestions for improving service efficiency.

### Customer Side

1. **Service Booking**
   - AI-powered vehicle problem diagnosis
   - Real-time service slot availability
   - Accurate service cost estimation
   - Instant booking confirmation
   - **Auto-Assist**: Receive personalized service recommendations based on vehicle history and preferences.

2. **Support System**
   - 24/7 AI-powered chatbot support
   - Emergency assistance requests
   - Complete service history access
   - Personalized maintenance tips

## Security Features

- Secure password hashing
- Environment variable protection
- Session management
- Input validation and sanitization

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the development team. 
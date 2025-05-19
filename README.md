# AUTO ASSIST AND BOOKING SYSTEM

A comprehensive vehicle service management system built with Streamlit, featuring both customer and admin interfaces.

## Features

### Customer Features
- **Service Booking**
  - Easy booking process for cars and motorcycles
  - Multiple service types (Regular Maintenance, Repair, Washing)
  - Time slot selection
  - Service history tracking
  - Cost calculator

- **Service Information**
  - Detailed service packages
  - Pricing information
  - Service descriptions
  - Maintenance recommendations

- **Booking Management**
  - View booking history
  - Track service status
  - Cancel or modify bookings
  - Service cost estimation

- **AI-Powered Assistance**
  - Service recommendations
  - Diagnostic insights
  - Chat support
  - Maintenance tips

### Admin Features
- **Staff Management**
  - Add/remove staff members
  - Track staff duties
  - Manage staff information

- **Inventory Management**
  - Add/update/delete inventory items
  - Bulk import via CSV
  - Stock alerts
  - Inventory analytics
  - Search and filter functionality
  - Export to CSV

- **Booking Management**
  - View all bookings
  - Update booking status
  - Manage service schedules

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Vehicle_Services_System.git
cd Vehicle_Services_System
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create an `api.env` file in the root directory and add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

4. Run the application:
```bash
streamlit run app.py
```

## Database Structure

### Main Database (vehicle_service.db)
- **staff**: Staff information and management
- **bookings**: Service booking records

### Inventory Database (inventory.db)
- **inventory**: Stock items and their details
- **inventory_history**: Track changes to inventory items

## Usage

### Customer Access
1. Click "Customer Access" on the home page
2. Choose from available services:
   - Book Service
   - View Booking History
   - Check Service Status
   - Use Cost Calculator
   - Access Chat Support
   - View Service Information

### Admin Access
1. Click "Admin Access" on the home page
2. Access different management sections:
   - Staff Management
   - Inventory Management
   - Booking Management
   - AI Assistant

## Inventory Management

### Adding Items
1. Go to Admin Dashboard > Inventory Management
2. Use "Add Items" tab to:
   - Add single items manually
   - Import multiple items via CSV

### Managing Inventory
- Search and filter items
- Update quantities and prices
- View stock alerts
- Monitor inventory analytics
- Export inventory data

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Streamlit for the web framework
- Google Gemini AI for AI-powered features
- SQLite for database management 
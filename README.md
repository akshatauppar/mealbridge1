# MealBridge - Smart Food Redistribution Platform

MealBridge is a Flask-based food redistribution platform designed to reduce food waste and hunger. It connects donors, requestors, and delivery partners through a location-aware, real-time, and trackable donation system.

## 🌟 Features

- **Smart Food Donation System**: Donors can easily list surplus food with expiry validation
- **Location-Based Matching**: Requestors can find food donations near them
- **Real-Time Delivery Tracking**: Delivery partners can update delivery status in real-time
- **Digital Certificates**: Automatic PDF certificate generation for donors
- **Admin Dashboard**: Comprehensive management system for administrators
- **Responsive Design**: Modern, mobile-friendly UI with smooth animations

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd MealBridge
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (Optional)
   ```bash
   # For email functionality, set these environment variables:
   export MAIL_USERNAME="your-email@gmail.com"
   export MAIL_PASSWORD="your-app-password"
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your browser and go to `http://localhost:5000`

## 🏗️ Project Structure

```
MealBridge/
├── app.py                 # Main application entry point
├── __init__.py           # Flask app factory
├── models.py             # Database models
├── routes.py             # Application routes
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── donor/
│   ├── requestor/
│   ├── delivery/
│   └── admin/
├── static/               # Static files (CSS, JS, images)
│   └── css/
│       └── style.css
└── README.md
```

## 👥 User Roles

### 1. **Donor**
- Register and login to donate food
- Add food donations with expiry validation
- Track donation status
- Receive digital certificates

### 2. **Requestor**
- Browse available food donations
- Request food items
- Track request status
- View delivery information

### 3. **Delivery Partner**
- View assigned deliveries
- Update delivery status (Picked Up, In Transit, Delivered)
- Track delivery progress

### 4. **Admin**
- Manage users, donations, and deliveries
- View analytics and reports
- Monitor platform activity

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**: Core programming language
- **Flask 3.0**: Web framework
- **SQLAlchemy**: Database ORM
- **Flask-Login**: User authentication
- **Flask-Mail**: Email functionality
- **ReportLab**: PDF certificate generation

### Frontend
- **HTML5**: Semantic page structure
- **CSS3**: Modern styling with animations
- **JavaScript (ES6)**: Dynamic interactivity
- **Bootstrap 5.3**: Responsive UI framework
- **Font Awesome**: Icons

### Database
- **SQLite**: Development database (easily upgradeable to MySQL/PostgreSQL)

## 🔧 Configuration

### Email Setup (Optional)
To enable email functionality for certificates:

1. Create a Gmail app password
2. Set environment variables:
   ```bash
   export MAIL_USERNAME="your-email@gmail.com"
   export MAIL_PASSWORD="your-app-password"
   ```

### Database Configuration
The application uses SQLite by default. To use a different database:

1. Update the database URI in `__init__.py`:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/mealbridge'
   ```

## 📱 Features Overview

### Smart Expiry Validation
- Prevents past expiry dates
- Warns if food expires within 3 hours
- Real-time validation using JavaScript

### Location-Based Features
- Find nearby food donations
- Distance-based sorting
- Google Maps integration ready

### Real-Time Updates
- Delivery status updates
- AJAX-powered dashboards
- Auto-refresh functionality

### Security Features
- Password hashing
- Role-based access control
- Input validation and sanitization

## 🚀 Deployment

### Production Deployment

1. **Set production environment variables**
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY="your-secret-key"
   ```

2. **Use a production WSGI server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

3. **Set up a reverse proxy** (nginx recommended)

4. **Configure SSL certificate**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, email support@mealbridge.com or create an issue in the repository.

## 🔮 Future Enhancements

- [ ] Google Maps API integration
- [ ] Push notifications
- [ ] Mobile app
- [ ] Advanced analytics
- [ ] Multi-language support
- [ ] Payment integration
- [ ] SMS notifications

---

**Made with ❤️ for reducing food waste and feeding communities**

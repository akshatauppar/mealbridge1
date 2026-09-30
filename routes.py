from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import secrets
from __init__ import db, mail
from models import User, Donation, Request, Delivery, Certificate
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io
import base64

def register_routes(app):
    # Authentication routes
    @app.route('/')
    def index():
        # Get some statistics for the homepage
        total_donations = Donation.query.count()
        total_users = User.query.count()
        total_deliveries = Delivery.query.filter_by(status='delivered').count()
        
        return render_template('index.html', 
                             total_donations=total_donations,
                             total_users=total_users,
                             total_deliveries=total_deliveries)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            full_name = request.form['full_name']
            role = request.form['role']
            phone = request.form.get('phone', '')
            
            # Check if user already exists
            if User.query.filter_by(username=username).first():
                flash('Username already exists!', 'error')
                return render_template('register.html')
            
            if User.query.filter_by(email=email).first():
                flash('Email already exists!', 'error')
                return render_template('register.html')
            
            # Create new user
            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
                full_name=full_name,
                role=role,
                phone=phone
            )
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        
        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            user = User.query.filter_by(username=username).first()
            
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password!', 'error')
        
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        if current_user.role == 'donor':
            return redirect(url_for('donor_dashboard'))
        elif current_user.role == 'requestor':
            return redirect(url_for('requestor_dashboard'))
        elif current_user.role == 'delivery_partner':
            return redirect(url_for('delivery_dashboard'))
        elif current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('index'))

    # Donor routes
    @app.route('/donor/dashboard')
    @login_required
    def donor_dashboard():
        if current_user.role != 'donor':
            flash('Access denied!', 'error')
            return redirect(url_for('index'))
        
        donations = Donation.query.filter_by(donor_id=current_user.id).order_by(Donation.created_at.desc()).all()
        certificates = Certificate.query.filter_by(donor_id=current_user.id).all()
        
        return render_template('donor/dashboard.html', donations=donations, certificates=certificates, now=datetime.now(), timedelta=timedelta)

    @app.route('/donor/donate', methods=['GET', 'POST'])
    @login_required
    def donate_food():
        if current_user.role != 'donor':
            flash('Access denied!', 'error')
            return redirect(url_for('index'))
        
        if request.method == 'POST':
            food_name = request.form['food_name']
            quantity = request.form['quantity']
            food_type = request.form['food_type']
            description = request.form.get('description', '')
            location = request.form['location']
            expiry_date = request.form['expiry_date']
            expiry_time = request.form['expiry_time']
            contact_info = request.form.get('contact_info', '')
            
            # Combine date and time
            expiry_date_time = datetime.strptime(f"{expiry_date} {expiry_time}", "%Y-%m-%d %H:%M")
            
            # Check if expiry is in the past
            if expiry_date_time <= datetime.now():
                flash('Expiry date and time must be in the future!', 'error')
                return render_template('donor/donate.html')
            
            # Check if expiry is less than 3 hours from now
            if expiry_date_time <= datetime.now() + timedelta(hours=3):
                flash('Warning: This food may expire too soon to be redistributed safely.', 'warning')
            
            donation = Donation(
                food_name=food_name,
                quantity=quantity,
                food_type=food_type,
                description=description,
                location=location,
                expiry_date_time=expiry_date_time,
                contact_info=contact_info,
                donor_id=current_user.id
            )
            
            db.session.add(donation)
            db.session.commit()
            
            flash('Food donation added successfully!', 'success')
            return redirect(url_for('donor_dashboard'))
        
        return render_template('donor/donate.html')

    # Requestor routes
    @app.route('/requestor/dashboard')
    @login_required
    def requestor_dashboard():
        if current_user.role != 'requestor':
            flash('Access denied!', 'error')
            return redirect(url_for('index'))
        
        # Get available donations (not expired and not claimed)
        available_donations = Donation.query.filter(
            Donation.status == 'available',
            Donation.expiry_date_time > datetime.now(),
            Donation.donor_id != current_user.id
        ).order_by(Donation.created_at.desc()).all()
        
        # Get user's requests
        user_requests = Request.query.filter_by(requestor_id=current_user.id).order_by(Request.created_at.desc()).all()
        
        return render_template('requestor/dashboard.html', 
                             available_donations=available_donations,
                             user_requests=user_requests)

    @app.route('/requestor/request/<int:donation_id>', methods=['POST'])
    @login_required
    def request_food(donation_id):
        if current_user.role != 'requestor':
            flash('Access denied!', 'error')
            return redirect(url_for('index'))
        
        donation = Donation.query.get_or_404(donation_id)
        
        # Check if donation is still available
        if donation.status != 'available' or donation.expiry_date_time <= datetime.now():
            flash('This donation is no longer available!', 'error')
            return redirect(url_for('requestor_dashboard'))
        
        # Check if user already requested this donation
        existing_request = Request.query.filter_by(
            donation_id=donation_id,
            requestor_id=current_user.id
        ).first()
        
        if existing_request:
            flash('You have already requested this donation!', 'error')
            return redirect(url_for('requestor_dashboard'))
        
        message = request.form.get('message', '')
        
        request_obj = Request(
            donation_id=donation_id,
            requestor_id=current_user.id,
            message=message
        )
        
        db.session.add(request_obj)
        db.session.commit()
        
        flash('Food request submitted successfully!', 'success')
        return redirect(url_for('requestor_dashboard'))

    # Delivery routes
    @app.route('/delivery/dashboard')
    @login_required
    def delivery_dashboard():
        if current_user.role != 'delivery_partner':
            flash('Access denied!', 'error')
            return redirect(url_for('index'))
        
        deliveries = Delivery.query.filter_by(delivery_partner_id=current_user.id).order_by(Delivery.created_at.desc()).all()
        
        return render_template('delivery/dashboard.html', deliveries=deliveries)

    @app.route('/delivery/update_status/<int:delivery_id>', methods=['POST'])
    @login_required
    def update_delivery_status(delivery_id):
        if current_user.role != 'delivery_partner':
            flash('Access denied!', 'error')
            return redirect(url_for('index'))
        
        delivery = Delivery.query.get_or_404(delivery_id)
        new_status = request.form['status']
        
        if delivery.delivery_partner_id != current_user.id:
            flash('Access denied!', 'error')
            return redirect(url_for('delivery_dashboard'))
        
        delivery.status = new_status
        
        if new_status == 'picked_up':
            delivery.pickup_time = datetime.now()
        elif new_status == 'delivered':
            delivery.delivery_time = datetime.now()
            # Update donation status
            delivery.donation.status = 'claimed'
            # Generate and send certificate
            generate_certificate(delivery.donation)
        
        db.session.commit()
        
        flash(f'Delivery status updated to {new_status}!', 'success')
        return redirect(url_for('delivery_dashboard'))

    # Admin routes
    @app.route('/admin/dashboard')
    @login_required
    def admin_dashboard():
        if current_user.role != 'admin':
            flash('Access denied!', 'error')
            return redirect(url_for('index'))
        
        # Get statistics
        total_users = User.query.count()
        total_donations = Donation.query.count()
        total_requests = Request.query.count()
        total_deliveries = Delivery.query.count()
        completed_deliveries = Delivery.query.filter_by(status='delivered').count()
        
        # Get recent activity
        recent_donations = Donation.query.order_by(Donation.created_at.desc()).limit(10).all()
        recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
        
        return render_template('admin/dashboard.html',
                             total_users=total_users,
                             total_donations=total_donations,
                             total_requests=total_requests,
                             total_deliveries=total_deliveries,
                             completed_deliveries=completed_deliveries,
                             recent_donations=recent_donations,
                             recent_users=recent_users)

    # Utility functions
    def generate_certificate(donation):
        """Generate a PDF certificate for the donation"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title = Paragraph("Donation Certificate", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Certificate content
        content = f"""
        This certificate is presented to<br/>
        <b>{donation.donor.full_name}</b><br/><br/>
        
        For their generous donation of<br/>
        <b>{donation.quantity} of {donation.food_name}</b><br/><br/>
        
        Donated on: {donation.created_at.strftime('%B %d, %Y at %I:%M %p')}<br/>
        Location: {donation.location}<br/><br/>
        
        Thank you for bridging hunger! Your contribution helped feed people through MealBridge.<br/><br/>
        
        MealBridge Team
        """
        
        story.append(Paragraph(content, styles['Normal']))
        
        doc.build(story)
        buffer.seek(0)
        
        # Save certificate
        certificate = Certificate(
            donation_id=donation.id,
            donor_id=donation.donor_id,
            certificate_url=f"certificates/certificate_{donation.id}.pdf"
        )
        
        db.session.add(certificate)
        db.session.commit()
        
        # Send email with certificate
        send_certificate_email(donation, buffer.getvalue())

    def send_certificate_email(donation, pdf_content):
        """Send certificate via email"""
        try:
            from flask_mail import Message
            msg = Message(
                'Thank you for your donation! - MealBridge',
                sender=app.config['MAIL_USERNAME'],
                recipients=[donation.donor.email]
            )
            msg.body = f"""
            Dear {donation.donor.full_name},
            
            Thank you for your generous donation of {donation.quantity} of {donation.food_name}!
            
            Your donation has been successfully delivered and has helped feed people in need.
            
            Please find your donation certificate attached.
            
            Best regards,
            MealBridge Team
            """
            
            msg.attach(
                f"certificate_{donation.id}.pdf",
                "application/pdf",
                pdf_content
            )
            
            mail.send(msg)
        except Exception as e:
            print(f"Error sending email: {e}")

    # API routes for AJAX
    @app.route('/api/donations/nearby')
    @login_required
    def get_nearby_donations():
        """Get nearby donations for the requestor dashboard"""
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)
        radius = request.args.get('radius', 10, type=int)  # km
        
        if not lat or not lng:
            return jsonify({'error': 'Location required'}), 400
        
        # Simple distance calculation (in a real app, you'd use proper geospatial queries)
        donations = Donation.query.filter(
            Donation.status == 'available',
            Donation.expiry_date_time > datetime.now()
        ).all()
        
        nearby_donations = []
        for donation in donations:
            if donation.latitude and donation.longitude:
                # Calculate distance (simplified)
                distance = ((lat - donation.latitude) ** 2 + (lng - donation.longitude) ** 2) ** 0.5 * 111  # rough km conversion
                if distance <= radius:
                    donation_dict = {
                        'id': donation.id,
                        'food_name': donation.food_name,
                        'quantity': donation.quantity,
                        'food_type': donation.food_type,
                        'location': donation.location,
                        'expiry_date_time': donation.expiry_date_time.isoformat(),
                        'distance': round(distance, 2)
                    }
                    nearby_donations.append(donation_dict)
        
        # Sort by distance
        nearby_donations.sort(key=lambda x: x['distance'])
        
        return jsonify(nearby_donations)
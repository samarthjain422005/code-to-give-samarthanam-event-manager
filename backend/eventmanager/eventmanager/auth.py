from eventmanager.app.models import User
from eventmanager.app.models import Host
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re
from django.contrib.auth.hashers import make_password, check_password

def validate_password(password):
    """
    Validate that the password meets requirements:
    - At least 8 characters
    - Contains at least one digit
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one special character
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is valid"

def validate_name(name):
    """Validate that name is not empty and has reasonable length"""
    if not name:
        return False, "Name cannot be empty"
    
    if len(name) < 2:
        return False, "Name is too short"
    
    if len(name) > 255:
        return False, "Name is too long"
    
    return True, "Name is valid"

def validate_contact(contact):
    """Validate that contact number has proper format"""
    if not re.match(r'^\+?[0-9]{10,15}$', contact):
        return False, "Contact number must contain 10-15 digits"
    
    return True, "Contact is valid"

@csrf_exempt
def user_signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name', '')
            password = data.get('password', '')
            email = data.get('email', '')
            contact = data.get('contact', '')
            role = data.get('role', '')
            skills = data.get('skills', '')
            age = data.get('age', 0)
            location = data.get('location', '')
            organization = data.get('organization', '')
            
            name_valid, name_msg = validate_name(name)
            if not name_valid:
                return JsonResponse({'status': 'error', 'message': name_msg}, status=400)
            
            password_valid, password_msg = validate_password(password)
            if not password_valid:
                return JsonResponse({'status': 'error', 'message': password_msg}, status=400)
            
            contact_valid, contact_msg = validate_contact(contact)
            if not contact_valid:
                return JsonResponse({'status': 'error', 'message': contact_msg}, status=400)
            
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                return JsonResponse({'status': 'error', 'message': 'Email already registered'}, status=400)
            
            # Check if contact already exists
            if User.objects.filter(contact=contact).exists():
                return JsonResponse({'status': 'error', 'message': 'Contact number already registered'}, status=400)
            
            # Create user with hashed password
            hashed_password = make_password(password)
            user = User.objects.create(
                name=name,
                password=hashed_password,
                email=email,
                contact=contact,
                role=role,
                skills=skills,
                age=age,
                location=location,
                organization=organization
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'User registered successfully',
                'user_id': user.id
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

# @csrf_exempt
# def host_signup(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             name = data.get('name', '')
#             password = data.get('password', '')
#             email = data.get('email', '')
#             contact = data.get('contact', '')
            
#             # Validate inputs
#             name_valid, name_msg = validate_name(name)
#             if not name_valid:
#                 return JsonResponse({'status': 'error', 'message': name_msg}, status=400)
            
#             password_valid, password_msg = validate_password(password)
#             if not password_valid:
#                 return JsonResponse({'status': 'error', 'message': password_msg}, status=400)
            
#             contact_valid, contact_msg = validate_contact(contact)
#             if not contact_valid:
#                 return JsonResponse({'status': 'error', 'message': contact_msg}, status=400)
            
#             # Check if email already exists
#             if Host.objects.filter(email=email).exists():
#                 return JsonResponse({'status': 'error', 'message': 'Email already registered'}, status=400)
            
#             # Check if contact already exists
#             if Host.objects.filter(contact=contact).exists():
#                 return JsonResponse({'status': 'error', 'message': 'Contact number already registered'}, status=400)
            
#             # Create host with hashed password
#             hashed_password = make_password(password)
#             host = Host.objects.create(
#                 name=name,
#                 password=hashed_password,
#                 email=email,
#                 contact=contact
#             )
            
#             return JsonResponse({
#                 'status': 'success',
#                 'message': 'Host registered successfully',
#                 'host_id': host.id
#             })
            
#         except json.JSONDecodeError:
#             return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
#     return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email', '')
            password = data.get('password', '')
            
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Invalid email or password'}, status=401)
            
            if not check_password(password, user.password):
                return JsonResponse({'status': 'error', 'message': 'Invalid email or password'}, status=401)
            
            return JsonResponse({
                'status': 'success',
                'message': 'Login successful',
                'user_id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role,
                'points': user.points
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def host_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email', '')
            password = data.get('password', '')
            
            try:
                host = Host.objects.get(email=email)
            except Host.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Invalid email or password'}, status=401)
            
            # Check password
            if not check_password(password, host.password):
                return JsonResponse({'status': 'error', 'message': 'Invalid email or password'}, status=401)
            
            # Login successful
            return JsonResponse({
                'status': 'success',
                'message': 'Login successful',
                'host_id': host.id,
                'name': host.name,
                'email': host.email
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
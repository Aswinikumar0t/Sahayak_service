
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from .models import Booking  
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def home(request):
    """Single page home view"""
    return render(request, 'bookings/home.html')

def services_page(request):
    """Services listing page"""
    return render(request, 'services/services.html')

def about_page(request):
    """About page view"""
    return render(request, 'bookings/about.html')

def contact_page(request):
    """Contact page view"""
    return render(request, 'bookings/contact.html')

#sub category views
def service_subcategories(request, service_key):
    """Display subcategories for a selected service"""
    
    # Define all services and their subcategories
    services_data = {
        'electrician': {
            'name': 'Electrician',
            'icon': '⚡',
            'subcategories': [
                {
                    'key': 'wiring',
                    'name': 'Wiring & Rewiring',
                    'description': 'Complete house wiring, new connections, rewiring services',
                    'icon': '🔌',
                    'starting_price': 299,
                    'popular': True
                },
                {
                    'key': 'fan',
                    'name': 'Fan Installation',
                    'description': 'Ceiling fan, exhaust fan, wall fan installation',
                    'icon': '🌀',
                    'starting_price': 199,
                    'popular': False
                },
                {
                    'key': 'switch',
                    'name': 'Switch & Socket Repair',
                    'description': 'Switchboard repair, socket replacement, wiring fixes',
                    'icon': '🔘',
                    'starting_price': 149,
                    'popular': False
                },
                {
                    'key': 'mcb',
                    'name': 'MCB / DB Repair',
                    'description': 'Circuit breaker repair, distribution box maintenance',
                    'icon': '⚙️',
                    'starting_price': 399,
                    'popular': False
                },
                {
                    'key': 'inverter',
                    'name': 'Inverter Repair',
                    'description': 'Inverter servicing, battery check, wiring',
                    'icon': '🔋',
                    'starting_price': 349,
                    'popular': False
                },
                {
                    'key': 'ac',
                    'name': 'AC Installation',
                    'description': 'Air conditioner installation and setup',
                    'icon': '❄️',
                    'starting_price': 499,
                    'popular': False
                }
            ]
        },
        'plumber': {
            'name': 'Plumber',
            'icon': '🔧',
            'subcategories': [
                {
                    'key': 'pipe',
                    'name': 'Pipe Repair',
                    'description': 'Leakage repair, pipe replacement, PVC fixing',
                    'icon': '🪠',
                    'starting_price': 299,
                    'popular': True
                },
                {
                    'key': 'tap',
                    'name': 'Tap Installation',
                    'description': 'New tap, faucet, mixer installation',
                    'icon': '🚰',
                    'starting_price': 149,
                    'popular': False
                },
                {
                    'key': 'bathroom',
                    'name': 'Bathroom Fitting',
                    'description': 'Complete bathroom fittings, shower installation',
                    'icon': '🚽',
                    'starting_price': 399,
                    'popular': False
                },
                {
                    'key': 'drain',
                    'name': 'Drain Cleaning',
                    'description': 'Blocked drain, sink, toilet cleaning',
                    'icon': '🧹',
                    'starting_price': 249,
                    'popular': False
                },
                {
                    'key': 'motor',
                    'name': 'Water Motor Repair',
                    'description': 'Water pump repair, motor servicing',
                    'icon': '💧',
                    'starting_price': 449,
                    'popular': False
                }
            ]
        },
        'carpenter': {
            'name': 'Carpenter',
            'icon': '🪚',
            'subcategories': [
                {
                    'key': 'door',
                    'name': 'Door Repair',
                    'description': 'Door fixing, alignment, hardware replacement',
                    'icon': '🚪',
                    'starting_price': 299,
                    'popular': True
                },
                {
                    'key': 'furniture',
                    'name': 'Furniture Repair',
                    'description': 'Chair, table, cupboard, sofa repair',
                    'icon': '🪑',
                    'starting_price': 249,
                    'popular': False
                },
                {
                    'key': 'custom',
                    'name': 'Custom Woodwork',
                    'description': 'Custom furniture, cabinets, shelves making',
                    'icon': '📦',
                    'starting_price': 499,
                    'popular': False
                },
                {
                    'key': 'polish',
                    'name': 'Wood Polishing',
                    'description': 'Wood polishing, finishing, restoration',
                    'icon': '✨',
                    'starting_price': 349,
                    'popular': False
                }
            ]
        },
        'painter': {
            'name': 'Painter',
            'icon': '🎨',
            'subcategories': [
                {
                    'key': 'wall',
                    'name': 'Wall Painting',
                    'description': 'Interior & exterior wall painting',
                    'icon': '🖌️',
                    'starting_price': 399,
                    'popular': True
                },
                {
                    'key': 'texture',
                    'name': 'Texture Painting',
                    'description': 'Designer texture painting, accent walls',
                    'icon': '🎨',
                    'starting_price': 599,
                    'popular': False
                },
                {
                    'key': 'waterproof',
                    'name': 'Waterproofing',
                    'description': 'External wall waterproofing, dampness fix',
                    'icon': '💧',
                    'starting_price': 449,
                    'popular': False
                },
                {
                    'key': 'polish',
                    'name': 'Wood Polish',
                    'description': 'Furniture polishing, restoration',
                    'icon': '✨',
                    'starting_price': 299,
                    'popular': False
                }
            ]
        },
        'cleaner': {
            'name': 'Home Cleaning',
            'icon': '🧹',
            'subcategories': [
                {
                    'key': 'deep',
                    'name': 'Deep Cleaning',
                    'description': 'Complete home deep cleaning service',
                    'icon': '🧽',
                    'starting_price': 499,
                    'popular': True
                },
                {
                    'key': 'kitchen',
                    'name': 'Kitchen Cleaning',
                    'description': 'Kitchen degreasing, chimney cleaning',
                    'icon': '🍳',
                    'starting_price': 349,
                    'popular': False
                },
                {
                    'key': 'sofa',
                    'name': 'Sofa Cleaning',
                    'description': 'Upholstery cleaning, stain removal',
                    'icon': '🛋️',
                    'starting_price': 399,
                    'popular': False
                },
                {
                    'key': 'bathroom',
                    'name': 'Bathroom Cleaning',
                    'description': 'Complete bathroom sanitization',
                    'icon': '🚿',
                    'starting_price': 299,
                    'popular': False
                }
            ]
        },
        'ac-repair': {
            'name': 'AC Repair',
            'icon': '❄️',
            'subcategories': [
                {
                    'key': 'service',
                    'name': 'AC Service',
                    'description': 'Complete AC servicing and cleaning',
                    'icon': '🔧',
                    'starting_price': 399,
                    'popular': True
                },
                {
                    'key': 'gas',
                    'name': 'Gas Refill',
                    'description': 'AC gas refilling and leak check',
                    'icon': '💨',
                    'starting_price': 499,
                    'popular': False
                },
                {
                    'key': 'repair',
                    'name': 'AC Repair',
                    'description': 'Compressor, PCB, fan motor repair',
                    'icon': '🛠️',
                    'starting_price': 599,
                    'popular': False
                },
                {
                    'key': 'install',
                    'name': 'AC Installation',
                    'description': 'New AC installation and setup',
                    'icon': '🏠',
                    'starting_price': 699,
                    'popular': False
                }
            ]
        }
    }
    
    # Get the selected service data
    service = services_data.get(service_key)
    
    if not service:
        return redirect('services')
    
    context = {
        'service_key': service_key,
        'service_name': service['name'],
        'service_icon': service['icon'],
        'subcategories': service['subcategories']
    }
    
    return render(request, 'services/service_subcategories.html', context)

# Add these views:

def booking_page(request):
    """Booking page with rate plan selection"""
    # Get service from URL parameter
    service = request.GET.get('service', 'electrician')
    
    # Pass to template
    return render(request, 'bookings/booking_page.html', {
        'service': service,
        'today': datetime.now().strftime('%Y-%m-%d')
    })


def booking_confirmation(request):
    """Booking confirmation page"""
    booking_id = request.GET.get('id')
    
    # If you have a Booking model, fetch the booking details
    # booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    return render(request, 'bookings/booking_confirmation.html', {
        'booking_id': booking_id,
        'booking': None  # Replace with actual booking if you have it
    })


@login_required
def my_bookings(request):
    """View user's bookings"""
    
    # Get all bookings for logged-in user
    all_bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    
    # Separate bookings by status
    upcoming_bookings = all_bookings.filter(status__in=['pending', 'confirmed', 'assigned', 'in_progress'])
    past_bookings = all_bookings.filter(status='completed')
    cancelled_bookings = all_bookings.filter(status='cancelled')
    
    context = {
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings,
        'cancelled_bookings': cancelled_bookings,
    }
    return render(request, 'bookings/my_bookings.html', context)
    # If you have a Booking model
    # bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'bookings/my_bookings.html', {
        'bookings': []  # Replace with actual bookings
    })


@login_required
def profile_page(request):
    """User profile page"""
    return render(request, 'bookings/profile.html')


@login_required
def booking_detail(request, booking_id):
    """View single booking details"""
    # If you have a Booking model
    # booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    
    return render(request, 'bookings/booking_detail.html', {
        'booking_id': booking_id
    })

#api

@csrf_exempt
@login_required
def cancel_booking_api(request, booking_id):
    """API to cancel a booking"""
    if request.method == 'POST':
        try:
            booking = Booking.objects.get(booking_id=booking_id, user=request.user)
            if booking.status in ['pending', 'confirmed']:
                booking.status = 'cancelled'
                booking.save()
                return JsonResponse({'status': 'success', 'message': 'Booking cancelled'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Cannot cancel this booking'})
        except Booking.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Booking not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
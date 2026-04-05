from accounts.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, SubCategory, RatePlan, ServicePartner
from .serializers import CategorySerializer, SubCategorySerializer, RatePlanSerializer


@login_required
def admin_dashboard(request):
    return render(request, 'dashboard/admin_dashboard.html')


@login_required
def manager_dashboard(request):
    return render(request, 'dashboard/manager_dashboard.html')


# List all partners
def service_partner_list(request):
    corporate = ServicePartner.objects.filter(partner_type='corporate')
    solo = ServicePartner.objects.filter(partner_type='solo')
    return render(request, 'employees/service_partners.html', {
        'corporate_partners': corporate,
        'solo_partners': solo
    })


# Add new partner
def service_partner_add(request):
    if request.method == 'POST':
        # handle form
        pass
    return render(request, 'employees/add_partner.html')


def corporate_partners(request):
    partners = ServicePartner.objects.filter(partner_type='corporate')
    return render(request, 'dashboard/corporate_partners.html', {'partners': partners})


def solo_partners(request):
    partners = ServicePartner.objects.filter(partner_type='solo')
    return render(request, 'dashboard/solo_partners.html', {'partners': partners})


@login_required
def applications(request):
    return render(request, 'dashboard/applications.html')


@login_required
def bookings(request):
    return render(request, 'dashboard/bookings.html')


@login_required
def services(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_category':
            # Create new category
            name = request.POST.get('category_name')
            icon = request.POST.get('category_icon')
            is_active = request.POST.get('status') == 'active'
            
            Category.objects.create(
                name=name,
                icon=icon,
                is_active=is_active
            )
            messages.success(request, f'Category "{name}" added successfully!')
            return redirect('services')
            
        elif action == 'add_subcategory':
            # Create new sub-category
            category_id = request.POST.get('category_id')
            sub_name = request.POST.get('sub_name')
            is_active = request.POST.get('is_active') == 'true'
            
            category = get_object_or_404(Category, id=category_id)
            SubCategory.objects.create(
                category=category,
                name=sub_name,
                is_active=is_active
            )
            messages.success(request, f'Sub-category "{sub_name}" added successfully!')
            return redirect('services')
    
    # GET request - show all categories and subcategories
    categories = Category.objects.all().order_by('name')
    subcategories = SubCategory.objects.select_related('category').all().order_by('category__name', 'name')
    
    context = {
        'categories': categories,
        'subcategories': subcategories,
        'total_categories': categories.count(),
        'total_subcategories': subcategories.count(),
        'active_categories': categories.filter(is_active=True).count(),
        'active_subcategories': subcategories.filter(is_active=True).count(),
    }
    return render(request, 'dashboard/services.html', context)


@login_required
def subcategories(request, category_id):
    """View sub-categories for a specific category"""
    category = get_object_or_404(Category, id=category_id)
    subcategories = SubCategory.objects.filter(category=category, is_active=True)
    
    context = {
        'category': category,
        'subcategories': subcategories,
    }
    return render(request, 'dashboard/subcategories.html', context)


@login_required
def rate_plans(request):
    """Main rate plans view - handles both GET and POST"""
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            try:
                # Create new rate plan
                RatePlan.objects.create(
                    name=request.POST.get('plan_name'),
                    category_id=request.POST.get('category_id'),
                    sub_category_id=request.POST.get('sub_category_id'),
                    plan_type=request.POST.get('plan_type', 'hourly'),
                    price=request.POST.get('base_price'),
                    unit=request.POST.get('price_unit', 'per hour'),
                    min_hours=request.POST.get('min_hours', 1),
                    plan_for=request.POST.get('plan_for', 'both'),
                    description=request.POST.get('description', ''),
                    is_active=request.POST.get('status') == 'active',
                )
                messages.success(request, 'Rate Plan created successfully! ✅')
            except Exception as e:
                messages.error(request, f'Error creating plan: {str(e)}')

        elif action == 'edit':
            try:
                plan = RatePlan.objects.get(pk=request.POST.get('plan_id'))
                plan.name = request.POST.get('plan_name')
                plan.category_id = request.POST.get('category_id')
                plan.sub_category_id = request.POST.get('sub_category_id')
                plan.price = request.POST.get('base_price')
                plan.unit = request.POST.get('price_unit')
                plan.plan_type = request.POST.get('plan_type', 'hourly')
                plan.plan_for = request.POST.get('plan_for', 'both')
                plan.min_hours = request.POST.get('min_hours', 1)
                plan.description = request.POST.get('description', '')
                plan.is_active = request.POST.get('status') == 'active'
                plan.save()
                messages.success(request, 'Rate Plan updated successfully! ✅')
            except Exception as e:
                messages.error(request, f'Error updating plan: {str(e)}')

        return redirect('rate_plans')

    # GET request - show all rate plans
    all_plans = RatePlan.objects.select_related('category', 'sub_category').all().order_by('-created_at')
    categories = Category.objects.filter(is_active=True)

    context = {
        'plans': all_plans,
        'categories': categories,
        'total_plans': all_plans.count(),
        'b2b_plans': all_plans.filter(plan_for='b2b').count(),
        'b2c_plans': all_plans.filter(plan_for='b2c').count(),
        'active_plans': all_plans.filter(is_active=True).count(),
    }
    return render(request, 'dashboard/rate_plans.html', context)


@login_required
def edit_rate_plan(request, pk):
    """Edit a specific rate plan"""
    plan = get_object_or_404(RatePlan, pk=pk)
    categories = Category.objects.filter(is_active=True)
    
    if request.method == 'POST':
        try:
            plan.name = request.POST.get('plan_name')
            plan.category_id = request.POST.get('category_id')
            plan.sub_category_id = request.POST.get('sub_category_id')
            plan.price = request.POST.get('base_price')
            plan.unit = request.POST.get('price_unit')
            plan.plan_type = request.POST.get('plan_type', 'hourly')
            plan.plan_for = request.POST.get('plan_for', 'both')
            plan.min_hours = request.POST.get('min_hours', 1)
            plan.description = request.POST.get('description', '')
            plan.is_active = request.POST.get('status') == 'active'
            plan.save()
            messages.success(request, 'Rate Plan updated successfully! ✅')
            return redirect('rate_plans')
        except Exception as e:
            messages.error(request, f'Error updating plan: {str(e)}')
    
    return render(request, 'dashboard/rate_plans_edit.html', {
        'plan': plan,
        'categories': categories
    })


@login_required
def toggle_plan(request, pk):
    plan = get_object_or_404(RatePlan, pk=pk)
    plan.is_active = not plan.is_active
    plan.save()
    status = "activated" if plan.is_active else "deactivated"
    messages.success(request, f'Plan "{plan.name}" {status} successfully!')
    return redirect('rate_plans')


@login_required
def delete_plan(request, pk):
    plan = get_object_or_404(RatePlan, pk=pk)
    plan_name = plan.name
    plan.delete()
    messages.success(request, f'Plan "{plan_name}" deleted successfully!')
    return redirect('rate_plans')


@login_required
def toggle_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    category.is_active = not category.is_active
    category.save()
    messages.success(request, f'Category "{category.name}" status updated!')
    return redirect('services')


@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    category_name = category.name
    category.delete()
    messages.success(request, f'Category "{category_name}" deleted successfully!')
    return redirect('services')


@login_required
def toggle_subcategory(request, pk):
    subcategory = get_object_or_404(SubCategory, id=pk)
    subcategory.is_active = not subcategory.is_active
    subcategory.save()
    messages.success(request, f'Sub-category "{subcategory.name}" status updated!')
    return redirect('services')


@login_required
def delete_subcategory(request, pk):
    subcategory = get_object_or_404(SubCategory, id=pk)
    subcategory_name = subcategory.name
    subcategory.delete()
    messages.success(request, f'Sub-category "{subcategory_name}" deleted successfully!')
    return redirect('services')


@login_required
def reports(request):
    return render(request, 'dashboard/reports.html')


@login_required
def payments(request):
    return render(request, 'dashboard/payments_billing.html')


@login_required
def access_control(request):
    return render(request, 'dashboard/access_control.html')


@login_required
def booking_management(request):
    return render(request, 'dashboard/booking_management.html')


@login_required
def notifications(request):
    return render(request, 'dashboard/notifications.html')


@login_required
def profile_settings(request):
    return render(request, 'dashboard/profile_settings.html')


# ===== API ENDPOINTS =====

@api_view(['GET'])
def api_categories(request):
    """API endpoint to get all active categories"""
    categories = Category.objects.filter(is_active=True)
    serializer = CategorySerializer(categories, many=True)
    return Response({
        'status': 'success',
        'count': categories.count(),
        'categories': serializer.data
    })


@api_view(['GET'])
def api_subcategories(request):
    """API endpoint to get sub-categories for a specific category"""
    category_id = request.GET.get('category')
    
    if category_id:
        subcategories = SubCategory.objects.filter(category_id=category_id, is_active=True)
    else:
        subcategories = SubCategory.objects.filter(is_active=True)
    
    serializer = SubCategorySerializer(subcategories, many=True)
    return Response({
        'status': 'success',
        'count': subcategories.count(),
        'subcategories': serializer.data
    })


@api_view(['GET'])
def api_rate_plans(request):
    """API endpoint to get rate plans"""
    plan_id = request.GET.get('plan_id')
    sub_category_id = request.GET.get('sub_category')
    
    try:
        if plan_id:
            # Fetch single plan by ID for editing
            plan = RatePlan.objects.get(pk=plan_id)
            serializer = RatePlanSerializer(plan)
            return Response({
                'status': 'success',
                'rate_plans': [serializer.data]
            })
        elif sub_category_id:
            # Fetch plans for a specific sub-category
            rateplans = RatePlan.objects.filter(sub_category_id=sub_category_id, is_active=True)
            serializer = RatePlanSerializer(rateplans, many=True)
            return Response({
                'status': 'success',
                'count': rateplans.count(),
                'rate_plans': serializer.data
            })
        else:
            # Fetch all active plans
            rateplans = RatePlan.objects.filter(is_active=True)
            serializer = RatePlanSerializer(rateplans, many=True)
            return Response({
                'status': 'success',
                'count': rateplans.count(),
                'rate_plans': serializer.data
            })
    except RatePlan.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Plan not found'
        }, status=404)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=500)
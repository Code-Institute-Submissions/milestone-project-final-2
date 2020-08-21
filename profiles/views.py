from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm

from checkout.models import Order

@login_required
def profile(request):
    """A view that displays the profile page of a logged in user"""
    try:
        # retrieves the current user
        user = request.user.pk
        # retrieves the Profile object associated with current user
        currentprofile = Profile.objects.get(user=user)
        # renders profile.html with the Profile info of the current user
        return render(request, 'profiles/profile.html', {'profile': currentprofile})
    except Profile.DoesNotExist:
        # renders profile.html without Profile information,
        # typically because user has not yet filled in
        # their profile information
        return render(request, 'profiles/profile.html')
    
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = ProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)

def order_history(request):
    """A view that displays the orders page"""
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
# accounts/views.py
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from .forms import UserProfileForm, UserAddressForm
from .models import UserBilling

@method_decorator(login_required, name='dispatch')
class UserProfileView(View):
    template_name = 'account/profile.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        profile_form = UserProfileForm(instance=user)
        
        # Tenta buscar a instância de UserBilling
        try:
            billing_info = user.billing_info
        except UserBilling.DoesNotExist:
            billing_info = None
        
        address_form = UserAddressForm(instance=billing_info)
        return render(request, self.template_name, {
            'profile_form': profile_form,
            'address_form': address_form
        })

    def post(self, request, *args, **kwargs):
        user = request.user
        
        # Tenta buscar ou criar uma instância de UserBilling
        billing_info, created = UserBilling.objects.get_or_create(user=user)

        if 'save_profile' in request.POST:
            profile_form = UserProfileForm(request.POST, instance=user)
            address_form = UserAddressForm(instance=billing_info)
            
            if profile_form.is_valid():
                profile_form.save()
                return redirect('account_profile')

        elif 'save_address' in request.POST:
            address_form = UserAddressForm(request.POST, instance=billing_info)
            profile_form = UserProfileForm(instance=user)
            
            if address_form.is_valid():
                address_form.save()
                return redirect('account_profile')

        return render(request, self.template_name, {
            'profile_form': profile_form,
            'address_form': address_form
        })
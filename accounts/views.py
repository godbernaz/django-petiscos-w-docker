# accounts/views.py
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, View
from .forms import UserProfileForm, UserAddressForm
from .models import CustomUser

@method_decorator(login_required, name='dispatch')
class UserProfileView(View):
    template_name = 'account/profile.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        profile_form = UserProfileForm(instance=user)
        address_form = UserAddressForm(instance=user)
        return render(request, self.template_name, {
            'profile_form': profile_form,
            'address_form': address_form
        })

    def post(self, request, *args, **kwargs):
        user = request.user
        if 'save_profile' in request.POST:
            profile_form = UserProfileForm(request.POST, instance=user)
            address_form = UserAddressForm(instance=user)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('account_profile')
            
        elif 'save_address' in request.POST:
            address_form = UserAddressForm(request.POST, instance=user)
            profile_form = UserProfileForm(instance=user)
            if address_form.is_valid():
                address_form.save()
                return redirect('account_profile')

        return render(request, self.template_name, {
            'profile_form': profile_form,
            'address_form': address_form
        })
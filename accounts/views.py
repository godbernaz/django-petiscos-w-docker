# accounts/views.py
from django.contrib.auth import update_session_auth_hash
from allauth.account.utils import send_email_confirmation
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from allauth.account.models import EmailAddress

from .forms import UserProfileForm, UserAddressForm, ChangePasswordForm
from .models import UserBilling

@method_decorator(login_required, name='dispatch')
class UserProfileView(View):
    template_name = 'account/profile.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        profile_form = UserProfileForm(instance=user)

        try:
            billing_info = user.billing_info
        except UserBilling.DoesNotExist:
            billing_info = None

        address_form = UserAddressForm(instance=billing_info)
        password_form = ChangePasswordForm(user)

        # Check if the email is verified
        email_verified = EmailAddress.objects.filter(user=user, verified=True).exists()

        return render(request, self.template_name, {
            'profile_form': profile_form,
            'address_form': address_form,
            'password_form': password_form,
            'email_verified': email_verified, 
        })

    def post(self, request, *args, **kwargs):
        user = request.user
        billing_info, created = UserBilling.objects.get_or_create(user=user)

        profile_form = UserProfileForm(request.POST, instance=user)
        address_form = UserAddressForm(request.POST, instance=billing_info)
        password_form = ChangePasswordForm(user, request.POST)

        email_verified = EmailAddress.objects.filter(user=user, verified=True).exists()

        if 'save_profile' in request.POST and profile_form.is_valid():
            # Check if the e-mail has been changed
            new_email = profile_form.cleaned_data.get('email')
            if new_email and new_email != user.email:
                # Remove old e-mail
                EmailAddress.objects.filter(user=user).delete()
                # Create a new unverified e-mail
                EmailAddress.objects.create(user=user, email=new_email, verified=False)

                # Send confirmation e-mail again
                send_email_confirmation(request, user)

            # Save changes to the profile
            profile_form.save()
            messages.success(request, "Dados do perfil atualizados com sucesso!")
            return redirect('account_profile')

        elif 'save_address' in request.POST and address_form.is_valid():
            address_form.save()
            messages.success(request, "Morada atualizada com sucesso!")
            return redirect('account_profile')

        elif 'change_password' in request.POST and password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)  
            messages.success(request, "A tua password foi alterada com sucesso!")
            return redirect('account_profile')

        # Reload the page with the updated status
        return render(request, self.template_name, {
            'profile_form': profile_form,
            'address_form': address_form,
            'password_form': password_form,
            'email_verified': email_verified, 
        })
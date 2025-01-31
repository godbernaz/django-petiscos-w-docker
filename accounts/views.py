# accounts/views.py
from django.contrib.auth import update_session_auth_hash
from allauth.account.utils import send_email_confirmation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from allauth.account.models import EmailAddress
from django.shortcuts import redirect

from .forms import UserProfileForm, UserBillingForm, ChangePasswordForm
from .models import UserBilling

@method_decorator(login_required, name='dispatch')
class UserProfileView(View):
    template_name = 'account/profile.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        profile_form = UserProfileForm(instance=user)
        password_form = ChangePasswordForm(user)
        billing_profiles = UserBilling.objects.filter(user=user)

        # Form para adicionar novo perfil
        new_billing_form = UserBillingForm()

        # Form para editar um perfil (caso seja selecionado)
        billing_id = request.GET.get('edit_billing')
        edit_billing_instance = get_object_or_404(UserBilling, id=billing_id, user=user) if billing_id else None
        edit_billing_form = UserBillingForm(instance=edit_billing_instance) if edit_billing_instance else None

        email_verified = EmailAddress.objects.filter(user=user, verified=True).exists()

        return render(request, self.template_name, {
            'profile_form': profile_form,
            'password_form': password_form,
            'email_verified': email_verified,
            'billing_profiles': billing_profiles,
            'new_billing_form': new_billing_form,
            'edit_billing_form': edit_billing_form,
            'edit_billing_instance': edit_billing_instance,
        })

    def post(self, request, *args, **kwargs):
        user = request.user
        profile_form = UserProfileForm(request.POST, instance=user)
        password_form = ChangePasswordForm(user, request.POST)
        billing_profiles = UserBilling.objects.filter(user=user)

        # Form para adicionar novo perfil
        new_billing_form = UserBillingForm(request.POST)

        email_verified = EmailAddress.objects.filter(user=user, verified=True).exists()

        if 'save_profile' in request.POST and profile_form.is_valid():
            new_email = profile_form.cleaned_data.get('email')
            if new_email and new_email != user.email:
                EmailAddress.objects.filter(user=user).delete()
                EmailAddress.objects.create(user=user, email=new_email, verified=False)
                send_email_confirmation(request, user)

            profile_form.save()
            messages.success(request, "Dados do perfil atualizados com sucesso!")
            return redirect('account_profile')

        elif 'change_password' in request.POST and password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, "A tua password foi alterada com sucesso!")
            return redirect('account_profile')

        elif 'add_billing' in request.POST and new_billing_form.is_valid():
            billing = new_billing_form.save(commit=False)
            billing.user = user
            billing.save()
            messages.success(request, "Novo perfil de faturação adicionado com sucesso!")
            return redirect('account_profile')

        elif 'delete_billing' in request.POST:
            billing_id = request.POST.get('billing_id')
            billing_to_delete = get_object_or_404(UserBilling, id=billing_id, user=user)

            # Verifica se o perfil a ser deletado é o padrão
            was_default = billing_to_delete.is_default

            billing_to_delete.delete()
            
            # Se o perfil excluído era o padrão, atribuir outro como padrão
            if was_default:
                next_default = UserBilling.objects.filter(user=user).first()
                if next_default:
                    next_default.is_default = True
                    next_default.save()

            messages.success(request, "Perfil de faturação removido com sucesso!")
            return redirect('account_profile')

        elif 'edit_billing' in request.POST:
            billing_id = request.POST.get('billing_id')
            billing_to_edit = get_object_or_404(UserBilling, id=billing_id, user=user)
            edit_billing_form = UserBillingForm(request.POST, instance=billing_to_edit)
            if edit_billing_form.is_valid():
                edit_billing_form.save()
                messages.success(request, "Perfil de faturação atualizado com sucesso!")
                return redirect('account_profile')

        return render(request, self.template_name, {
            'profile_form': profile_form,
            'password_form': password_form,
            'email_verified': email_verified,
            'billing_profiles': billing_profiles,
            'new_billing_form': new_billing_form,
        })
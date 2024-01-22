from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Order
from django.shortcuts import get_object_or_404



class RightUserMixinOrder(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs['pk'])
        if not request.user.is_authenticated:
            messages.info(request, 'Необходимо войти')
            return self.handle_no_permission()
        if request.user.is_authenticated:
            if request.user.id != order.customer.id:
                messages.info(request, 'Нет прав доступа')
                return redirect(reverse_lazy('users:login'))
        return super().dispatch(request, *args, **kwargs)
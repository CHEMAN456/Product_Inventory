from django.shortcuts import render,redirect
from .models import ProdMast,StckMain,StckDetail
from .forms import ProdForm,StckMainForm,StckDetailForm
from django.forms import modelformset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from rest_framework import viewsets
from .serializers import Prod_serializer,StckDetailSerializer,StckMainSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.

@login_required
def home_view(request):
    return render(request,'inventory/home.html')

def index_view(request):
    return render(request,'inventory/index.html')

@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProdForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product created successfully!")
            return redirect('inventory:prod_list')  # Make sure this URL is defined
    else:
        form = ProdForm()
    return render(request, 'inventory/create_product.html', {'form': form})

@login_required
def product_list(request):
    products = ProdMast.objects.all().order_by('prod_name')
    return render(request, 'inventory/product_list.html', {'products': products})

@login_required
def create_transaction(request):
    StckDetailFormSet = modelformset_factory(StckDetail, form=StckDetailForm, extra=3)

    if request.method == 'POST':
        main_form = StckMainForm(request.POST)
        formset = StckDetailFormSet(request.POST, queryset=StckDetail.objects.none())

        if main_form.is_valid() and formset.is_valid():
            transaction = main_form.save(commit=False)
            transaction.created_by = request.user.username
            transaction.save()

            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                    detail = form.save(commit=False)
                    detail.transaction = transaction

                    # Only validate stock for OUT transactions
                    if transaction.transaction_type == 'Out':
                        available_stock = calculate_stock(detail.product)
                        if detail.quantity > available_stock:
                            messages.error(request, f"Not enough stock for {detail.product.prod_name}. Available: {available_stock}")
                            transaction.delete()
                            return redirect('inventory:create_transaction')

                    detail.save()

            messages.success(request, "Transaction recorded successfully.")
            return redirect('inventory:trans_list')
    else:
        main_form = StckMainForm()
        formset = StckDetailFormSet(queryset=StckDetail.objects.none())

    return render(request, 'inventory/create_transaction.html', {
        'main_form': main_form,
        'formset': formset
    })

def calculate_stock(product):
    stock_in = StckDetail.objects.filter(
        transaction__transaction_type='In', product=product
    ).aggregate(Sum('quantity'))['quantity__sum'] or 0

    stock_out = StckDetail.objects.filter(
        transaction__transaction_type='Out', product=product
    ).aggregate(Sum('quantity'))['quantity__sum'] or 0

    return stock_in - stock_out

@login_required
def transaction_list(request):
    transactions = StckMain.objects.prefetch_related('details__product').order_by('-timestamp')
    return render(request, 'inventory/transaction_list.html', {'transactions': transactions})

@login_required
def inventory_status(request):
    products = ProdMast.objects.all()
    inventory = []

    for product in products:
        stock = calculate_stock(product)
        inventory.append({
            'name': product.prod_name,
            'sku': product.sku,
            'stock': stock
        })

    return render(request, 'inventory/inventory_status.html', {'inventory': inventory})

class ProductViewSet(viewsets.ModelViewSet):
    queryset = ProdMast.objects.all()
    serializer_class = Prod_serializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = StckMain.objects.all()
    serializer_class = StckMainSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

class TransactionDetailViewSet(viewsets.ModelViewSet):
    queryset = StckDetail.objects.all()
    serializer_class = StckDetailSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
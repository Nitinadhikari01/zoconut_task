from django.shortcuts import render
from django.http import JsonResponse
from .models import Client, Appointment
from datetime import timedelta
from django.utils.timezone import now
from dashboard.models import Client
from django.db.models import Q

def dashboard(request):
    two_months_ago = now() - timedelta(days=60)
    # print(two_months_ago,'---------2_months_ago')
    new_clients = Client.objects.filter(timestamp__gte=two_months_ago).count()
    new_appointments = Appointment.objects.filter(appointment_datetime__gte=two_months_ago).count()
    context = {
        'new_clients': new_clients,
        'new_appointments': new_appointments,
    }
    return render(request, 'dashboard.html', context)



def get_clients_table(request):
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '').strip()

    order_column_index = request.GET.get('order[0][column]')
    order_dir = request.GET.get('order[0][dir]', 'asc')

    columns = ['id', 'name', 'primary_number', 'country_code', 'timestamp']

    if order_column_index:
        order_col_name = columns[int(order_column_index)]
        order_by = order_col_name if order_dir == 'asc' else f'-{order_col_name}'
    else:
        order_by = 'id'

    queryset = Client.objects.all().order_by(order_by)

    if search_value:
        queryset = queryset.filter(
            Q(name__icontains=search_value) |
            Q(primary_number__icontains=search_value) |
            Q(country_code__icontains=search_value)
        )

    total_records = Client.objects.count()

    filtered_records = queryset.count()

    queryset = queryset[start:start + length]

    data = []
    for client in queryset:
        data.append({
            "id": client.id,
            "name": client.name,
            "primary_number": client.primary_number,
            "country_code": client.country_code,
            "timestamp": client.timestamp.isoformat()
        })

    return JsonResponse({
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": data
    })



def add_client(request):
    if request.method == "POST":
        name = request.POST.get("name")
        primary_number = request.POST.get("primary_number")
        country_code = request.POST.get("country_code")
        client = Client.objects.create(name=name, primary_number=primary_number, country_code=country_code)
        return JsonResponse({"status": 'success', "client_id": client.id})
    return JsonResponse({"success": False})



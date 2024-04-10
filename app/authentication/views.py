from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from .models import Ticket, TicketIDCounter, UserProfile
from django.db import models
from django.db.models import Count
import datetime
import random



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect(reverse('super_user_home'))
            else:
                return redirect(reverse('regular_user_home'))
        else:
            error_message = 'Invalid username or password'
    else:
        error_message = None

    return render(request, 'login.html', {'error_message': error_message})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    pass

@login_required
def super_user_home_view(request):
    if request.user.is_superuser:
        tickets = Ticket.objects.all()
        ticket_count = tickets.count()
        assigned_tickets = Ticket.objects.filter(assigned_staff=request.user)
    else:
        ticket_count = 0
        assigned_tickets = []

    return render(request, 'super_user_home.html', {'ticket_count': ticket_count, 'assigned_tickets': assigned_tickets})




@login_required
def regular_user_home_view(request):
    ticket_count = Ticket.objects.filter(created_by=request.user).count()
    return render(request, 'regular_user_home.html', {'ticket_count': ticket_count})


@login_required
def create_ticket_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        created_by = request.user
        ticket = Ticket.objects.create(
            title=title,
            description=description,
            status='Open',
            priority='Low',
            created_by=created_by,
        )
        return redirect('ticket_detail', ticket_id=ticket.id)
    return render(request, 'create_ticket.html')


def generate_ticket_id():
    counter = TicketIDCounter.objects.first()
    if counter is None:
        counter = TicketIDCounter.objects.create()
    ticket_id = counter.counter
    counter.increment_counter()
    return ticket_id


@login_required
def ticket_list_view(request):
    if request.user.is_superuser:
        tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.filter(created_by=request.user)
        
    no_tickets_message = 'No hay tickets disponibles.' if not tickets.exists() else ''
    context = {
        'tickets': tickets,
        'no_tickets_message': no_tickets_message
    }
    return render(request, 'ticket_list.html', context)


@login_required
def ticket_detail_view(request, ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)
    if not request.user.is_superuser and ticket.created_by != request.user:
        editable = False
    else:
        editable = True
    return render(request, 'ticket_detail.html', {'ticket': ticket, 'editable': editable})


def update_ticket_status_view(request, ticket_id):
    if request.method == 'POST':
        new_status = request.POST.get('status')
        ticket = Ticket.objects.get(pk=ticket_id)
        ticket.status = new_status
        ticket.save()
        return redirect('ticket_detail', ticket_id=ticket_id)
    return redirect('ticket_list')

def delete_ticket_view(request, ticket_id):
    if request.method == 'POST':
        ticket = Ticket.objects.get(pk=ticket_id)
        ticket.delete()
        return redirect('ticket_list')
    return redirect('ticket_detail', ticket_id=ticket_id)

def ticket_detail_view(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    staff_members = User.objects.filter(is_superuser=True) 
    assigned_staff = random.choice(staff_members)
    appointment_date = datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 7))
    ticket.assigned_staff = assigned_staff
    ticket.appointment_date = appointment_date
    ticket.save()

    return render(request, 'ticket_detail.html', {'ticket': ticket, 'editable': True})

def about_view(request):
    return render(request, 'about.html')
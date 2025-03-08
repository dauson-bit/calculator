# views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Program, Course
from datetime import datetime
from decimal import Decimal, ROUND_DOWN
from django.shortcuts import render, redirect, get_object_or_404

def home(request):
    return render(request, 'calculator/home.html')  



def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if User.objects.filter(username=username).exists():
            return render(request, "calculator/signup.html", {"error": "User already exists. Please login."})
        else:
            User.objects.create_user(username=username, password=password)
            return redirect("login")
    return render(request, "calculator/signup.html")



def login_view(request):
    error_message = None
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("program_selection")  
        else:
            error_message = "Invalid credentials. Please try again."
    return render(request, "calculator/login.html", {"error_message": error_message})



def program_selection(request):
    programs = Program.objects.all()  # Display programs only once
    if request.method == 'POST':
        program_id = request.POST['program']
        year = request.POST['year']
        semester = request.POST['semester']
        return redirect('course_list', program_id=program_id, year=year, semester=semester)
    return render(request, 'calculator/program_selection.html', {'programs': programs})




@login_required
def course_list(request, program_id, year, semester):
    # Fetch program and courses dynamically
    program = get_object_or_404(Program, id=program_id)
    courses = Course.objects.filter(program=program, year=year, semester=semester)

    if request.method == 'POST':
        # Save grades dynamically for each course
        for course in courses:
            grade_value = request.POST.get(f'grade_{course.id}')  # Use course.id for dynamic form fields
            

        # Redirect to GPA result page
        return redirect('gpa_result', program_id=program.id, year=year, semester=semester)
    context={
        'program': program,
        'courses': courses,
        'year': year,
        'semester': semester,
    }
    return render(request, 'calculator/course_list.html', context)
        



def gpa_result(request, program_id, year, semester):
    # Fetch courses for the given program, year, and semester
    courses = Course.objects.filter(program_id=program_id, year=year, semester=semester)

    total_points = Decimal(0)
    total_credits = Decimal(0)

    # Define grade-to-GPA mappings
    grade_points = {
        'A': 5.0, 'B+': 4.0, 'B': 3.0, 'C': 2.0, 'sup': 0.0, 'CRV': 0.0
    }

    if request.method == "POST":
        grades = {}  # Store grades for each course

        for course in courses:
            grade = request.POST.get(f"grade_{course.id}")  # Get value from select field

            if grade and grade in grade_points:  # Ensure the grade is valid
                grades[course.id] = grade  # Store grade in dictionary
                total_points += Decimal(grade_points[grade]) * Decimal(course.credit_hours)
                total_credits += Decimal(course.credit_hours)

        # Calculate GPA
        gpa = total_points / total_credits if total_credits > 0 else Decimal(0.0)

        # Format GPA to 1 decimal place without rounding
        gpa = gpa.quantize(Decimal('0.0'), rounding=ROUND_DOWN)

        return render(request, 'calculator/gpa_result.html', {
            'gpa': gpa,
            'courses': courses
        })

    return render(request, 'calculator/gpa_result.html', {'courses': courses})

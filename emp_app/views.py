from django.shortcuts import render, HttpResponse
from .models import Employee, Department, Role,Attendance
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from functools import wraps


def imp_objects(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        departments = Department.objects.values_list('name', flat=True).distinct()
        roles1 = Role.objects.values_list('name', flat=True).distinct()
        emps = Employee.objects.all()
        attendance = Attendance.objects.all()


        context1 = {
            'departments': departments,
            'roles1': roles1,
            'emps': emps,
            'attendance':attendance

        }

        response = view_func(request, context1, *args, **kwargs)
        # for employee in emps:
        #     Attendance.objects.create(employee=employee)
        return response

    return wrapper


def index(request):
    return render(request, 'index.html')


@imp_objects
def allempolyee(request, context):
    return render(request, 'all_empolyee.html', context)


@imp_objects
def add_empolyee(request, context):
    success_message = None
    if request.method == 'POST':
        try:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            salary = int(request.POST['salary'])
            bonus = int(request.POST['bonus'])
            phone = int(request.POST['phone'])
            dept = request.POST['dept']
            department = Department.objects.filter(name=dept).first()
            print(str(department))
            dept_id = department.id
            role = request.POST['role']
            role = get_object_or_404(Role, name=role)
            role_id = role.id
            new_emp = Employee(
                first_name=first_name,
                last_name=last_name,
                salary=salary,
                bonus=bonus,
                phone=phone,
                dept_id=dept_id,
                role_id=role_id,
                hire_date=datetime.now()
            )
            new_emp.save()
            success_message = 'Employee added successfully'

            context['success_message'] = success_message
            return render(request, 'add_empolyee.html', context)
        except Exception as e:
            return HttpResponse(f"An Exception Occurred! Employee Has Not Been Added. Error: {e}")
    else:
        return render(request, 'add_empolyee.html', context)


@imp_objects
def del_emp(request, context):
    message = None
    if request.method == 'POST':
        try:
            emp_id = request.POST['emp_id']
            emp_del = Employee.objects.get(id=emp_id)
            emp_del.delete()
            message = "Employee removed sucessfullly"
            context['rem_message'] = message
            return render(request, 'del_emp.html', context)
        except:
            return HttpResponse("Error occured while deleting try again later!!")
    else:
        return render(request, 'del_emp.html', context)


@imp_objects
def filter_emp(request, context1):
    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST.get('dept', '')
        roles = request.POST.get('roles', '')
        emps = Employee.objects.all()
        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept:
            emps = emps.filter(dept__name__icontains=dept)
        if roles:
            emps = emps.filter(role__name__icontains=roles)
        context = {
            'emps': emps
        }
        return render(request, 'all_empolyee.html', context)

    elif request.method == 'GET':
        return render(request, 'filter_emp.html', context1)
    else:
        return HttpResponse('An Exception Occurred')

@imp_objects
def attendance(request,context1):
    if request.method == 'POST':
        try:
            emp_name = request.POST.get('names')


            return render(request, 'attendance.html', context1)
        except:
            HttpResponse("error occured")
    else:
        return  render(request, 'attendance.html', context1)





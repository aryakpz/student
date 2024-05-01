from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .models import StudentMark
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .models import StudentMark
from django.urls import reverse

class home(View):
    def get(self, request):
        return render(request, "home.html")


def student_information(request):
    if request.method == 'POST':
        student_name = request.POST.get('studentName')
        dob = request.POST.get('dob')
        subject = request.POST.get('subject')
        mark = int(request.POST.get('mark'))
        out_of = int(request.POST.get('outOf'))

        
        if out_of <= mark:
            return HttpResponse("Out of value should be greater than mark!")

       
        if StudentMark.objects.filter(student_name=student_name, subject=subject).exists():
            return HttpResponse("This subject has already been selected by this student!")

        student_mark = StudentMark(
            student_name=student_name,
            dob=dob,
            subject=subject,
            mark=mark,
            out_of=out_of
        )
        student_mark.save()
        return redirect('student_mark')

    return render(request, 'student_information.html')





def edit_student(request, pk):
    student = StudentMark.objects.get(pk=pk)
    if request.method == 'POST':
        student.student_name = request.POST.get('studentName')
        student.dob = request.POST.get('dob')
        student.subject = request.POST.get('subject')
        student.mark = int(request.POST.get('mark'))
        student.out_of = int(request.POST.get('outOf'))
       
        
        if student.out_of <= student.mark:
            return HttpResponse("Out of value should be greater than mark!")

        if StudentMark.objects.exclude(pk=pk).filter(student_name=student.student_name, subject=student.subject).exists():
            return HttpResponse("This subject has already been selected by this student!")

        student.save()
        return redirect('student_mark')


    return render(request, 'student_information.html', {'student': student})




def delete_student(request, pk):
    student = StudentMark.objects.get(pk=pk)
    student.delete()
    return redirect('student_mark')




def student_mark(request):
    all_students = StudentMark.objects.all()

    name_filter = request.GET.get('name_filter', '')
    subject_filter = request.GET.get('subject_filter', '')
    pass_fail_filter = request.GET.get('pass_fail_filter', '')

    name_filtered_students = all_students
    if name_filter:
        name_filtered_students = name_filtered_students.filter(student_name__icontains=name_filter)
              

    subject_filtered_students = name_filtered_students
    if subject_filter:
        subject_filtered_students = subject_filtered_students.filter(subject__icontains=subject_filter)

    pass_fail_filtered_students = subject_filtered_students
    if pass_fail_filter:
        pass_fail_filtered_students = pass_fail_filtered_students.filter(mark__gte=40 if pass_fail_filter.lower() == 'pass' else 0,
                                                                         mark__lt=40 if pass_fail_filter.lower() == 'fail' else 100)
        







    summary_students = all_students

    summary_data = {}
    for student in summary_students:
        if student.student_name in summary_data:
            summary_data[student.student_name]['total_mark'] += student.mark
            summary_data[student.student_name]['total_out_of'] += student.out_of
        else:
            summary_data[student.student_name] = {
                'total_mark': student.mark,
                'total_out_of': student.out_of
            }

    summary_body = []
    for student_name, data in summary_data.items():
        total_percentage = 0
        if data['total_out_of'] != 0:
            total_percentage = (data['total_mark'] / data['total_out_of']) * 100
        summary_body.append({
            'student_name': student_name,
            'total_mark': data['total_mark'],
            'total_out_of': data['total_out_of'],
            'total_percentage': total_percentage
        })

    context = {
        'all_students': all_students,
        'pass_fail_filtered_students': pass_fail_filtered_students,
        'summary_body': summary_body,
        'name_filter': name_filter,
        'subject_filter': subject_filter,
        'pass_fail_filter': pass_fail_filter,
    }


    return render(request, 'student_mark.html', context)





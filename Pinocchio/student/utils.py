from django.utils import timezone

def getStudentSemester(request):
    year = int(timezone.localdate().year)
    month = int(timezone.localdate().month)
    return (year - request.user.student.batch)*2 + 1 if month > 6 else 0

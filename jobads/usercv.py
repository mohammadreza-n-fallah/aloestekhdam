
from .models import CV
from .serializers import JobSerializer



def CheckCv(user, data,):
    cv_data = CV.objects.filter(jobad__in=data)
    cv_status_dict = {}

    for cv in cv_data:
        if cv.user == user:
            cv_status_dict[cv.jobad.id] = {
                'sended': True,
                'status': cv.status
            }
    s_data = JobSerializer(data, many=True).data
    for job_data in s_data:
        job_id = job_data['id']
        try:
            if job_id in cv_status_dict:
                job_data['cv_status'] = cv_status_dict[job_id]
            else:
                job_data['cv_status'] = {}
        except:
            pass
    return s_data
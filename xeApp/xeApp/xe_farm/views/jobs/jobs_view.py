from ...models import Jobs,Employee, JobAssignment
from ...serializers import JobsSerializer,EmployeeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

#create job
@api_view(["POST"])
def create_jobs(request):
    serializer = JobsSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "jobs created successfully"}, status = status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#edit job
@api_view(["PUT"])
def update_jobs(request, job_id):
    try:
        job = Jobs.objects.get(id = job_id)
    except Jobs.DoesNotExist:
        return Response({"message":"user not found"}, status=status.HTTP_404_NOT_FOUND)  
    serializer = JobsSerializer(job , data = request.data, partial = True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "jobs updated successfully"}, status = status.HTTP_200_OK)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
#delete job
@api_view(["DELETE"])
def delete_jobs(request, job_id):
    try:
        job = Jobs.objects.get(id = job_id)
    except Jobs.DoesNotExist:
        return Response({"message":"user not found"}, status=status.HTTP_404_NOT_FOUND)   
    job.delete()
    return Response({"message":"Jobs deleted successfully"}, status=status.HTTP_200_OK)   
#get jobs
@api_view(["GET"])
def get_jobs(request):
    try:
        job = Jobs.objects.all()
    except:
        return Response({"message":"invalid data"}, status=status.HTTP_404_NOT_FOUND)
    serializer = JobsSerializer(job, many=True)
    return Response(serializer.data)
#get jobs by id
@api_view(["GET"])
def get_jobs_by_id(request, job_id):
    try:
        job=Jobs.objects.get(id = job_id)
    except Jobs.DoesNotExist:
        return Response({"message":"user not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = JobsSerializer(job)
    return Response(serializer.data)

#assign job
@api_view(["GET"])
def job_assigning_dropdown(request):
    employees = Employee.objects.all().values('id','name')
    return Response({"options":
        [{"key": "all_employee ","label": "All Employee"},
        {"key":"individual", "label":"Individual"}
        ],
        "employee_namelist":list(employees)        
    })
    
@api_view(["POST"])
def job_assign(request):
    job_id = request.data.get('job_id')
    assign_to = request.data.get('assign_to')
    
    if not job_id or not assign_to:
        return Response({"error":"job_id and assign_to is required"}, status=status.HTTP_404_NOT_FOUND)
    try:
        job = Jobs.objects.get(id = job_id)
    except Jobs.DoesNotExist:
        return Response({"message": "job id not found"}, status = status.HTTP_404_NOT_FOUND)
    
    #all employee
    if assign_to == "all":
        employee = Employee.objects.all()
        for emp in employee:
            JobAssignment.objects.create(job = job , employee = emp)
        return Response({"message": "job assigned all employee"}, status=status.HTTP_200_OK)
    if assign_to == "individual":
        employee_id = request.data.get("employee")
        if not employee_id:
            return Response({"message":"employee id is required"}) 
        try:
            employee = Employee.objects.get(id = employee_id) 
            JobAssignment.objects.create(job = job, employee= employee)
            return Response({"message": "job assigned employee"}, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({"message":"Employee not found"}, status = status.HTTP_404_NOT_FOUND)
        
    return Response({"invalid Data"}, status = status.HTTP_400_BAD_REQUEST)
@api_view(["PUT"])
def update_status(request,job_id):
    try:
        job_status = Jobs.objects.get(id = job_id)
    except Jobs.DoesNotExist:
        return Response({"message":"job_id is not found"}, status=status.HTTP_404_NOT_FOUND)
    
    status_value = request.data.get("status")
    reason = request.data.get("incomplete_reason")
    
    if status_value not in ['completed','incompleted']:
        return Response({"give valid status"}, status=status.HTTP_400_BAD_REQUEST)
    if status_value =="incompleted" and not reason:
        return Response({"message":"if the status is incompleted then reason is required"})
    
    job_status.status = status_value
    job_status.incomplete_reason = reason if status_value == "incompleted" else None
    job_status.save()
    return Response("status were updated")

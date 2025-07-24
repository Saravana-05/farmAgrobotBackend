from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from ...models import Job, JobFarmSegment, JobEmployee, FarmSegment, Employee
from ...serializers import JobSerializer, JobSummarySerializer

@api_view(['POST'])
def create_job(request):
    """
    Create a new job with farm segments and employees
    """
    try:
        # Check if request has any data
        if not request.data:
            return Response({
                'status': 'error',
                'message': 'No data received in request'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate the job data
        serializer = JobSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Use transaction to ensure data consistency
        with transaction.atomic():
            job_record = serializer.save()
        
        # Return success response with created data
        response_serializer = JobSerializer(job_record)
        return Response({
            'status': 'success',
            'message': 'Job created successfully',
            'data': response_serializer.data
        }, status=status.HTTP_201_CREATED)
        
    except IntegrityError as e:
        return Response({
            'status': 'error',
            'message': 'Database integrity error occurred'
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_all_jobs(request):
    """
    Get all job records from the database with basic filtering options
    """
    try:
        # Get query parameters for filtering
        job_status = request.GET.get('job_status')
        employee_id = request.GET.get('employee_id')
        farm_segment_id = request.GET.get('farm_segment_id')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        job_name = request.GET.get('job_name')
        
        # Start with all jobs
        jobs = Job.objects.select_related().prefetch_related(
            'job_farm_segments__farm_segment',
            'job_employees__employee'
        )
        
        # Apply filters
        if job_status:
            jobs = jobs.filter(job_status=job_status)
        
        if employee_id:
            jobs = jobs.filter(job_employees__employee_id=employee_id)
        
        if farm_segment_id:
            jobs = jobs.filter(job_farm_segments__farm_segment_id=farm_segment_id)
        
        if start_date:
            jobs = jobs.filter(job_date__gte=start_date)
        
        if end_date:
            jobs = jobs.filter(job_date__lte=end_date)
        
        if job_name:
            jobs = jobs.filter(job_name__icontains=job_name)
        
        # Order by most recent first
        jobs = jobs.order_by('-created_at')
        
        # Use summary serializer for list view (lighter payload)
        serializer = JobSummarySerializer(jobs, many=True)
        
        return Response({
            'status': 'success',
            'message': 'Jobs retrieved successfully',
            'data': serializer.data,
            'count': jobs.count()
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_job_by_id(request, job_id):
    """
    Get a specific job record by ID with all details
    """
    try:
        job_record = Job.objects.select_related().prefetch_related(
            'job_farm_segments__farm_segment',
            'job_employees__employee'
        ).get(id=job_id)
        
        serializer = JobSerializer(job_record)
        
        return Response({
            'status': 'success',
            'message': 'Job retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Job.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Job record not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def update_job(request, job_id):
    """
    Update job data
    """
    try:
        job_record = Job.objects.get(id=job_id)
        
        # Validate the updated data
        serializer = JobSerializer(job_record, data=request.data, partial=True)
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Use transaction to ensure data consistency
        with transaction.atomic():
            job_record = serializer.save()
        
        # Return updated data
        response_serializer = JobSerializer(job_record)
        return Response({
            'status': 'success',
            'message': 'Job updated successfully',
            'data': response_serializer.data
        }, status=status.HTTP_200_OK)
        
    except Job.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Job record not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_job(request, job_id):
    """
    Delete a job record
    """
    try:
        job_record = Job.objects.get(id=job_id)
        
        # Use transaction to ensure related data is also deleted
        with transaction.atomic():
            job_record.delete()
        
        return Response({
            'status': 'success',
            'message': 'Job deleted successfully'
        }, status=status.HTTP_200_OK)
        
    except Job.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Job record not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
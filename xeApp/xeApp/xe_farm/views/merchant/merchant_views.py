from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ...models import Merchant
from ...serializers import MerchantSerializer


@api_view(['POST'])
def save_merchant_data(request):
    """
    Save merchant data to the database
    """
    try:
        # Check if request has any data
        if not request.data:
            return Response({
                'status': 'error',
                'message': 'No data received in request'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Debug logging
        print(f"Request data: {request.data}")
        
        # Validate the merchant data
        serializer = MerchantSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        
        # Check if contact number already exists
        contact = validated_data.get('contact')
        if contact:
            # Check for existing merchant with same contact number
            existing_merchant = Merchant.objects.filter(
                contact=contact
            ).first()
            
            if existing_merchant:
                return Response({
                    'status': 'error',
                    'message': 'Mobile number already exists'
                }, status=status.HTTP_400_BAD_REQUEST)
        
       
        
        # Create merchant record
        merchant = Merchant.objects.create(**validated_data)
        
        # Return success response
        response_serializer = MerchantSerializer(merchant)
        return Response({
            'status': 'success',
            'message': 'Merchant Added Successfully',
            'data': response_serializer.data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_all_merchants(request):
    """
    Get all merchants from the database
    """
    try:
        merchants = Merchant.objects.all().order_by('-created_at')
        serializer = MerchantSerializer(merchants, many=True)
        
        return Response({
            'status': 'success',
            'message': 'Merchants retrieved successfully',
            'data': serializer.data,
            'count': merchants.count()
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_merchant_by_id(request, merchant_id):
    """
    Get a specific merchant by ID
    """
    try:
        merchant = Merchant.objects.get(id=merchant_id)
        serializer = MerchantSerializer(merchant)
        
        return Response({
            'status': 'success',
            'message': 'Merchant retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Merchant.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Merchant not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_merchant_data(request, merchant_id):
    """
    Update merchant data
    """
    try:
        merchant = Merchant.objects.get(id=merchant_id)
        
        # Validate the updated data
        serializer = MerchantSerializer(merchant, data=request.data, partial=True)
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if contact number already exists (excluding current merchant)
        contact = serializer.validated_data.get('contact')
        if contact:
            existing_merchant = Merchant.objects.filter(
                contact=contact
            ).exclude(id=merchant_id).first()
            
            if existing_merchant:
                return Response({
                    'status': 'error',
                    'message': 'Mobile number already exists'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Save the updated merchant
        serializer.save()
        
        return Response({
            'status': 'success',
            'message': 'Merchant updated successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Merchant.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Merchant not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_merchant(request, merchant_id):
    """
    Delete a merchant
    """
    try:
        merchant = Merchant.objects.get(id=merchant_id)
        merchant.delete()
        
        return Response({
            'status': 'success',
            'message': 'Merchant deleted successfully'
        }, status=status.HTTP_200_OK)
        
    except Merchant.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Merchant not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

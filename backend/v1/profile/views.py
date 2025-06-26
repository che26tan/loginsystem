import os
from django.http import HttpResponse, FileResponse
from rest_framework.decorators import action, authentication_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from rest_framework.response import Response
from profile.serializers import ProfileSerializer
from profile.models import Profile
from common.utility.functions import standard_response


def demo(request):
    return HttpResponse("Profile api is working")


# only authentication person can see profile with token
# Default authentication_classes JWT
class ProfileViewSet(viewsets.ViewSet):
    @action(methods=["POST"], url_path='detail', detail=False, permission_classes=[IsAuthenticated])
    def profile_detail(self, request):
        user = request.user
        print(user.__dict__)

        try:
            profile = Profile.objects.select_related('user').get(user__user_id=user.user_id)
            print(profile.__dict__)
            serializer = ProfileSerializer(profile)
            return standard_response(True, 'profile detail successful',data=serializer.data, code=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return standard_response(False, 'profile detail failed', error= 'Profile not found', code=status.HTTP_404_NOT_FOUND)


    @action(methods=["PUT"], url_path='update', detail=False, permission_classes=[IsAuthenticated])
    def profile_update(self, request):
        user = request.user
        # print(user.__dict__)

        try:
            profile = Profile.objects.select_related('user').get(user__user_id=user.user_id)
            print("profile:",profile.city)
        except Profile.DoesNotExist:
            return standard_response(False, 'profile update failed', error= 'Profile not found', code=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        # print(serializer)
        if serializer.is_valid():
            serializer.save()
            return standard_response(True, 'profile update successful',data=serializer.data, code=status.HTTP_201_CREATED)

        return standard_response(False, 'profile detail failed', error= serializer.errors, code=status.HTTP_404_NOT_FOUND)

    # @action(methods=["POST"], url_path='profile_image', detail=False, permission_classes=[IsAuthenticated])
    # def profile_image(self, request):
    #     user = request.user
    #     if user.is_authenticated:
    #         try:
    #             profile = Profile.objects.get(user__user_id=user.user_id)
    #             image_path = profile.profile_image.path
    #
    #             print(image_path)
    #
    #             if image_path.endswith('male.svg') or image_path.endswith('female.svg') or image_path.endswith('other.svg'):
    #                 return Response({'error': 'Image not provided yet'}, status=status.HTTP_404_NOT_FOUND)
    #
    #             download_image = f"{profile.user.full_name}.jpg"
    #             print(download_image)
    #             if download_image.split('.')[0] == '':
    #                 download_image = 'profile_image.jpg'
    #
    #             print(download_image)
    #
    #             return FileResponse(open(image_path, 'rb'), as_attachment=True, filename=download_image)
    #         except Profile.DoesNotExist:
    #             return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
    #
    #     return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


    @action(methods=["POST"], url_path='upload_profile_image', detail=False,
            permission_classes=[IsAuthenticated], parser_classes=[MultiPartParser, FormParser])
    def upload_profile_image(self, request):
        user = request.user
        try:
            profile = Profile.objects.get(user__user_id=user.user_id)
        except Profile.DoesNotExist:
            return standard_response(False, 'profile image upload failed', error= 'Profile not found', code=status.HTTP_404_NOT_FOUND)

        profile_image = request.FILES.get('profile_image')
        if not profile_image:
            return standard_response(False, 'profile image upload failed', error= 'Image not Provided', code=status.HTTP_400_BAD_REQUEST)

        profile.profile_image = profile_image
        profile.save()
        return standard_response(True,'profile image upload successful',data='Profile image uploaded successfully', code=status.HTTP_200_OK)


    @action(methods=["GET"], url_path='download_profile_image', detail=False, permission_classes=[IsAuthenticated])
    def download_profile_image(self, request):
        user = request.user
        try:
            profile = Profile.objects.get(user__user_id=user.user_id)
        except Profile.DoesNotExist:
            return standard_response(False, 'Profile image load failed', error='Profile not found',
                                     code=status.HTTP_404_NOT_FOUND)

        image_path = profile.profile_image.path
        print(image_path)


        # Check if default placeholder image is being used
        if image_path.endswith(('male.svg', 'female.svg', 'other.svg')):
            return standard_response(False, 'Profile image load failed', error='Image not saved yet',
                                     code=status.HTTP_404_NOT_FOUND)

        # Check if file actually exists in the directory
        if not os.path.exists(image_path):
            return standard_response(False, 'Profile image load failed', error='Image file not found in directory',
                                     code=status.HTTP_404_NOT_FOUND)

        download_image = f"{profile.user.full_name}.jpg"
        if not download_image.split('.')[0]:
            download_image = 'profile_image.jpg'

        print(download_image)

        return FileResponse(open(image_path, 'rb'), as_attachment=True, filename=download_image)

    @action(methods=["DELETE"], url_path='delete_profile_image', detail=False, permission_classes=[IsAuthenticated])
    def delete_profile_image(self, request):
        pass
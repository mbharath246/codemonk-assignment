from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from authtoken.views import get_token_user_data
from tasks.models import Paragraph, TokenizedWords
from tasks.serializers import ParagraphSerializer, TokenizedSerializer
from users.models import CustomUser


class ParagraphsView(APIView):
    queryset = Paragraph.objects
    serializer_class = ParagraphSerializer
    data = {}
    
    def get(self, request):
        """
        API view for retrieving a list of paragraphs for the authenticated user.

        This endpoint allows authenticated users to retrieve a list of all paragraphs associated with their account.
        The API response includes the success status, a message, the list of paragraphs, and the HTTP status code.

        **Request**:
        - GET /tasks/v1/paras/

        **Responses**:
        - 200 OK:
            - Description: Successfully retrieved the list of paragraphs.
            - Response Body:
                - success: bool, indicates if the request was successful
                - message: str, confirmation message
                - data: list, a list of paragraph objects associated with the user
                - status_code: int, HTTP status code (200)
        - 401 Unauthorized:
            - Description: The token is invalid or expired.
            - Response Body:
                - success: bool, indicates if the request failed
                - message: str, error message
                - data: None
                - status_code: int, HTTP status code (401)
        """
        user_id, email, username = get_token_user_data(request)
        if not user_id or not email or not username:
            self.data['success'] = False
            self.data['message'] = "token is invalid or expired"
            self.data['data'] = None
            self.data['status_code'] = status.HTTP_401_UNAUTHORIZED
            return Response(data=self.data, status=status.HTTP_401_UNAUTHORIZED)
        
        user = CustomUser.objects.get(email=email)
        instance = self.queryset.filter(user=user)
        if not instance:
            self.data['success'] = True
            self.data['message'] = 'data is empty.'
            self.data['data'] = None
            self.data['status_code'] = status.HTTP_200_OK
            return Response(data=self.data, status=status.HTTP_200_OK)
        
        serializer = self.serializer_class(instance, many=True)
        self.data['success'] = True
        self.data['message'] = "list of all paragraph's data"
        self.data['count'] = f'{len(serializer.data)} paragraphs present'
        self.data['data'] = serializer.data
        self.data['status_code'] = status.HTTP_200_OK
        
        return Response(data=self.data, status=status.HTTP_200_OK)
    

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request):
        """
        API view for creating a new paragraphs.

        This endpoint allows authenticated users to create a new task by providing task details in the request body.
        The data is validated and saved to the database if valid. The API response includes the success status,
        a message, the created task data, and the HTTP status code.

        `the new line paragraph must be entered with 2 (back slash and n) ex: \ n\ n remove space between \ and n`

        **Request**:
        - POST /tasks/v1/paras/

        **Request Body**:
        - application/json
        - Content-Type: application/json
        - `text`: str, required.

        **Responses**:
        - 201 Created:
            - Description: The task was created successfully.
            - Response Body:
                - success: bool, indicates if the creation was successful
                - message: str, confirmation message
                - data: object, the created task details
                - status_code: int, HTTP status code (201)
        - 400 Bad Request:
            - Description: The request data was invalid or incomplete.
            - Response Body:
                - success: bool, indicates if the creation failed
                - message: str, error message
                - data: object, error details
                - status_code: int, HTTP status code (400)
        - 401 Unauthorized:
            - Description: The token is invalid or expired.
            - Response Body:
                - success: bool, indicates if the request failed
                - message: str, error message
                - data: None
                - status_code: int, HTTP status code (401)
        """
        user_id, email, username = get_token_user_data(request)
        if not user_id or not email or not username:
            self.data['success'] = False
            self.data['message'] = "token is invalid or expired"
            self.data['data'] = None
            self.data['status_code'] = status.HTTP_401_UNAUTHORIZED
            return Response(data=self.data, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            self.data['success'] = True
            self.data['message'] = "task has been created successfully"
            self.data['data'] = None
            self.data['status_code'] = status.HTTP_201_CREATED

            return Response(data=self.data, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ParagraphSearchView(APIView):
    queryset = Paragraph.objects
    serializer_class = ParagraphSerializer
    data = {}

    @swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter(
            name='word',
            in_=openapi.IN_QUERY,
            description='Word to search for in paragraphs',
            type=openapi.TYPE_STRING,
            required=True
        )
    ]
    )

    def get(self, request):
        """
        API view for searching and retrieving the top 10 paragraphs containing a specific word.

        This endpoint allows authenticated users to search for paragraphs containing a given word and returns the top 10 results.
        The API response includes the success status, a message, the list of matching paragraphs, and the HTTP status code.

        **Request**:
        - GET /tasks/v1/search/?word={word}

        **Request Parameters**:
        - `word`: str, required. The word to search for in the paragraphs.

        **Responses**:
        - 200 OK:
            - Description: Successfully retrieved the top 10 paragraphs containing the word.
            - Response Body:
                - success: bool, indicates if the retrieval was successful
                - message: str, confirmation message
                - data: list, a list of up to 10 paragraph objects containing the word
                - count: number of paragraphs found
                - status_code: int, HTTP status code (200)
        - 400 Bad Request:
            - Description: The word parameter is missing.
            - Response Body:
                - success: bool, indicates if the request failed
                - message: str, error message
                - data: None
                - status_code: int, HTTP status code (400)
        - 401 Unauthorized:
            - Description: The token is invalid or expired.
            - Response Body:
                - success: bool, indicates if the request failed
                - message: str, error message
                - data: None
                - status_code: int, HTTP status code (401)
        """
        user_id, email, username = get_token_user_data(request)
        if not user_id or not email or not username:
            self.data['success'] = False
            self.data['message'] = "Token is invalid or expired."
            self.data['data'] = None
            self.data['status_code'] = status.HTTP_401_UNAUTHORIZED
            return Response(data=self.data, status=status.HTTP_401_UNAUTHORIZED)
        
        # Get the search word from query parameters
        word :str = request.query_params.get('word')
        if not word:
            self.data['success'] = False
            self.data['message'] = "word parameter is required."
            self.data['data'] = None
            self.data['status_code'] = status.HTTP_400_BAD_REQUEST
            return Response(data=self.data, status=status.HTTP_400_BAD_REQUEST)
        
        user = CustomUser.objects.get(email=email)
        paragraphs_all = self.queryset.filter(user=user)

        matching_paragraphs = []
        for obj in paragraphs_all:
            if len(matching_paragraphs) == 10: break
            if word.lower() in obj.paragraphs.lower().split():
                matching_paragraphs.append(obj)
        
        if not matching_paragraphs:
            self.data['success'] = True
            self.data['message'] = 'No paragraphs found containing the word.'
            self.data['data'] = None
            self.data['status_code'] = status.HTTP_200_OK
            return Response(data=self.data, status=status.HTTP_200_OK)
        
        serializer = self.serializer_class(matching_paragraphs, many=True)
        self.data['success'] = True
        self.data['message'] = "List of top 10 paragraphs containing the word."
        self.data['count'] = f'{len(serializer.data)} paragraphs found'
        self.data['data'] = serializer.data
        self.data['status_code'] = status.HTTP_200_OK
        
        return Response(data=self.data, status=status.HTTP_200_OK)    

class TokenizedWordsView(APIView):
    queryset = TokenizedWords.objects
    serializer_class = TokenizedSerializer
    data = {}

    def get(self, request):
        """
        API view for retrieving a list of all tokenized data for the authenticated user.

        This endpoint allows authenticated users to retrieve a list of all tokenized data associated with their account.
        The API response includes the success status, a message, the list of tokenized data, and the HTTP status code.

        **Request**:
        - GET /api/v1/tokenized-data/

        **Responses**:
        - 200 OK:
            - Description: Successfully retrieved the list of tokenized data.
            - Response Body:
                - success: bool, indicates if the retrieval was successful
                - message: str, confirmation message
                - data: list, a list of tokenized data objects
                - status_code: int, HTTP status code (200)           
        - 401 Unauthorized:
            - Description: The token is invalid or expired.
            - Response Body:
                - success: bool, indicates if the request failed
                - message: str, error message
                - data: None
                - status_code: int, HTTP status code (401)
        """
        user_id, email, username = get_token_user_data(request)
        if not user_id or not email or not username:
            self.data['success'] = False
            self.data['message'] = "token is invalid or expired"
            self.data['data'] = None
            self.data['status_code'] = status.HTTP_401_UNAUTHORIZED
            return Response(data=self.data, status=status.HTTP_401_UNAUTHORIZED)

        user = CustomUser.objects.get(email=email)
        instance = self.queryset.filter(user=user)

        if not instance:
            self.data['success'] = True
            self.data['message'] = 'data is empty.'
            self.data['data'] = None
            self.data['status_code'] = status.HTTP_200_OK
            return Response(data=self.data, status=status.HTTP_200_OK)
        
        serializer = self.serializer_class(instance, many=True)
        
        self.data['success'] = True
        self.data['message'] = "list of all tokenized data"
        self.data['data'] = serializer.data
        self.data['status_code'] = status.HTTP_200_OK
        
        return Response(data=self.data, status=status.HTTP_200_OK)
    
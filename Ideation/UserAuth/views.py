from rest_framework.views import APIView,Response


class Index(APIView):

    def get(self,request):
        return Response({'message':'Welcome to Ideation Project'})
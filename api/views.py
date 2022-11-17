from rest_framework import viewsets
from .serializers import TestDataSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Histories

class ImgWithStartChar(APIView):
    def post(self, request, format=None):
        request_data = request.data

        base64_encoded_img = request_data['img']
        start_char = request_data['startChar']

        # 絵の検出結果の呼び出し
        # predict_word = predict(base64_encoded_img, start_char)

        # 絵の生成の呼び出し

        # モデルに保存
        Histories.objects.create(word='predict_word', img=base64_encoded_img)

        return Response(
            {"success": True, "predictedWord": "predict_word"},
            status=status.HTTP_200_OK
        )

class History(APIView):
    def get(self, request, format=None):
        histories = Histories.objects.all()

        res = []
        for history in reversed(histories):
            data = {
                'id': history.id,
                'img': history.img,
                'word': history.word,
            }

            res.append(data)

        return Response(res, status=status.HTTP_200_OK)
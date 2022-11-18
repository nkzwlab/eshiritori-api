from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from api.models import Histories
from api.generator import generate_img
from ml.inference import predict_with_first_letter
from project.settings import net, word2vec_model
from api.generator import generate_img, generate_next_word

class ImgWithStartChar(APIView):
    def post(self, request, format=None):
        request_data = request.data

        base64_encoded_img = request_data['img']
        start_char = request_data['startChar']

        # 絵の検出結果の呼び出し
        predict_word = predict_with_first_letter(base64_encoded_img, start_char, resnet_model=net, word2vec_model=word2vec_model)
        
        if predict_word[0] != start_char or predict_word[-1] == 'ん':
            return  Response({"success": False, "predictedWord": ""}, status=status.HTTP_200_OK)

        # 絵の生成の呼び出し
        next_ja, next_en = generate_next_word(predict_word[-1])
        next_encoded_img = generate_img(next_en)

        # モデルに保存
        Histories.objects.create(word=predict_word, img=base64_encoded_img)
        Histories.objects.create(word=next_ja, img=next_encoded_img)

        return Response(
            {"success": True, "predictedWord": next_ja},
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
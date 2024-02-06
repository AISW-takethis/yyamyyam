from django.shortcuts import render, redirect
from django.views import View


# Create your views here.
def index(request):
    return render(request, "user/FLW_SP_001.html")


def login(request):
    return render(request, "user/FLW_OB_001.html")


class KakaoLogin(View):
    def get(self, request):
        try:
            # kakao token 받기 / 유효성 검사를 합니다.
            token = request.headers.get("Authorization")

            if token == None:
                return JsonResponse({"messsage": "INVALID_TOKEN"}, status=401)

            # kakao token을 다시 kakao로 보내서 유저 정보를 받아옵니다.
            kakao_account = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={"Authorization": f"Bearer {token}"},
            ).json()

            # 받아온 kakao 유저정보중 id가 db에 있는지 확인합니다.
            if not User.objects.filter(kakao_id=kakao_account["id"]).exists():
                # 유저 정보가 없으면 회원가입 되도록 합니다.
                user = User.objects.create(
                    kakao_id=kakao_account["id"],
                    email=kakao_account["kakao_account"]["email"],
                )

            # kakao id를 통해 db에서 해당 유저 정보를 가져옵니다.
            user = User.objects.get(kakao_id=kakao_account["id"])

            # 유저의 id를 jwt를 통해 암호화하여 token에 실어줍니다.
            access_token = jwt.encode(
                {"user_id": user.id}, SECRET_KEY, algorithm=ALGORITHMS
            )

            return JsonResponse({"access_token": access_token}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except JSONDecodeError:
            return JsonResponse({"message": "JSON_DECODE_ERROR"}, status=400)

        except jwt.DecodeError:
            return JsonResponse({"message": "JWT_DECODE_ERROR"}, status=400)

        except ConnectionError:
            return JsonResponse({"message": "CONNECTION_ERROR"}, status=400)

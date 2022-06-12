import jwt
import requests

from django.http        import JsonResponse
from django.views       import View
from django.shortcuts   import redirect
from django.conf        import settings
from django.db          import transaction

from users.models       import SocialAccount, User

class KakaoLoginView(View):
    def get(self, request):
        try:
            code = request.GET.get("code")
            kakao_token_api = "https://kauth.kakao.com/oauth/token"
            data = {
                "grant_type"  : "authorization_code",
                "client_id"   : settings.CLIENT_ID,
                "redirect_uri": "http://localhost:3000/oauth/callback/kakao",
                "code"        : code
            }
            access_token  = requests.post(kakao_token_api, data=data, timeout=1).json()["access_token"]
            kakao_api_url = "https://kapi.kakao.com/v2/user/me"

            response = requests.get(kakao_api_url, headers={"Authorization": f"Bearer {access_token}"}, timeout=1)
            if response.status_code == 401:
                return JsonResponse({"Error":"token_error"}, status = 401)

            user_info = response.json()
            sociaaccount = SocialAccount.objects.filter(social_account_id  = user_info["id"])
            if sociaaccount.exists():
                access_token = jwt.encode({'id': sociaaccount.get().id}, settings.SECRET_KEY, settings.ALGORITHM)
                return JsonResponse({"token":access_token}, status = 200)
            
            
            with transaction.atomic():
                user=User.objects.create(
                        email        = user_info["kakao_account"]["email"],
                        name         = user_info["properties"]["nickname"],
                        thumbnail    = user_info["properties"]["profile_image"],
                        introduction = user_info["properties"]["nickname"]+"님의 BranchTime입니다"
                    )
                SocialAccount.objects.create(
                        social_account_id = user_info["id"],
                        name              = "kakao",
                        user_id           = user.id
                        )
                access_token = jwt.encode({'id':user.id}, settings.SECRET_KEY, settings.ALGORITHM)  
                return JsonResponse({"token":access_token}, status = 200)
        except KeyError:
            return JsonResponse({"message":"KEY ERROR"}, status = 400)    
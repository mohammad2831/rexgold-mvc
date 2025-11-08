from rest_framework import serializers



class RegisterVerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    referral_code =  serializers.IntegerField()
    cod_meli =  serializers.IntegerField()


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)



class VerifyLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)








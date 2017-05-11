from recaptcha import RecaptchaClient
import erpstyle

def get_context(context):
    recaptcha_client = RecaptchaClient(public_key=erpstyle.recaptcha_public , private_key=erpstyle.recaptcha_private)
    context.captcha = recaptcha_client.get_challenge_markup()

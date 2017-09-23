import requests


def recaptcha_verify(request):
	data = request.data
	captcha_rs = data.get('verified')
	url = "https://www.google.com/recaptcha/api/siteverify"
	params = {
		'secret'  : '6LervDEUAAAAAC1TIm14SMFlnKEmQTvOd2ZB9C5P',
		'response': captcha_rs
	}
	verify_rs = requests.get(url, params=params, verify=True)
	verify_rs = verify_rs.json()
	# response["status"] = verify_rs.get("success", False)
	# response['message'] = verify_rs.get('error-codes', None) or "Unspecified error."
	return verify_rs.get("success", False)

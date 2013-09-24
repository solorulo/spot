
def spot(request):
	_json = {}
	try:
		if request.user.is_authenticated():
			if request.method == "GET" :
				spot_id = request.GET['spot_id']

				fotos = Foto.objects.filter(spot__exact=int(spot_id))
				_jsonfotos = []
				for foto in fotos:
					_jsonfotos.append({
						"url":foto.foto_url,
						"id_foto":foto.foto_id
						})
				_json['status'] = {
					'code' : 200,
					'msg' : "Bien"
				}
				_json['data'] = {
					'fotos' : _jsonfotos
				}
			else:
				_json['status'] = {
					'code' : 405,
					'msg' : "Solo POST"
				}
		else:
			_json['status'] = {
				'code' : 401,
				'msg' : "Sesion no iniciada"
			}
	except:
		_json['status'] = {
			'code' : 500,
			'msg' : "Internal Error"
		}
	data = simplejson.dumps(_json)
	return HttpResponse(data)
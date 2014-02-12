
def crew(request):
	_json = {}
	try:
		if request.user.is_authenticated():
			if request.method == "GET" :
				data = {}
				crew_id = request.GET['crew_id']
				crew = Crew.objects.get(crew_id=int(crew_id))

				miembros = crew.members.select_related().all()
				fotos = Foto.objects.filter(user__in=miembros)

				_jsonfotos = []
				for foto in fotos:
					_jsonfotos.append({
						"foto_url":foto.foto_url,
						"id_foto":foto.foto_id
						})

				_jsonmembers = []
				for member in members:
					_jsonmembers.append({
						"user_id":member.user_id,
						"username":member.user.username
						})

				data['name']= crew.nombre
				data['foto_url'] = crew.foto_url
				data['fotos'] = _jsonfotos
				data['miembros'] = _jsonmembers
				_json['status'] = {
					'code' : 200,
					'msg' : "Bien"
				}
				_json['data'] = {
					'info' : data
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
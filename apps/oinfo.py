def oinfo(object):
	"""object info"""
	print ('*'*50)
	print ('*'*15,'Object','*'*15)
	print (object)
	print ('-'*15,'__doc__','-'*15)
	doc = object.__doc__
	if  doc:
		print (doc)
	print ('-'*25,'type','-'*25)
	print (type(object))
	print ('-'*25,'dir','-'*25)
	d= dir(object)
	for item in d:
		if item.startswith("__"):
			print (item, end=",")
		else:
			try:
				t = type (eval(f'object.{item}'))
			except NotImplementedError:
				t=f'-NotImplementedError-'
			except AttributeError:
				t=f'-AttributeError-'
			print (f"{item:25} {t}")
	
	print ('-'*25,'__dict__','-'*25)
	try:
		print (object.__dict__)
	except AttributeError:
		pass
	print ('*'*50)

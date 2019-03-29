# -*- coding: UTF-8 -*-

def singleton(class_):
	instances = {}
	def getinstance(*args,	**kwargs):
		if class_ not in instances:
			instances[class_] = class_(*args, **kwargs)
		return instances[class_]
	return getinstance


if __name__ == '__main__':
	@singleton
	class MyClass():
		pass

	a = MyClass()
	b = MyClass()
	assert(a == b) 
# make

RUN:
	$(info "website DEBUG=1: http://127.0.0.1:38001")
	venv/bin/python3 manage.py runserver 0.0.0.0:38001

RUN_PRODUCT:
	$(info "website DEBUG=0: http://127.0.0.1:38001")
	venv/bin/python3 manage.py runserver --settings=settings_product 0.0.0.0:38001

# 需要把静态文件集中起来以便于上生产环境
RELEASE:
	venv/bin/python3 manage.py collectstatic --no-input

SUBMIT:
	git add .
	git commit -m "$(shell date '+%Y-%m-%d %H:%M:%S')"
	git push

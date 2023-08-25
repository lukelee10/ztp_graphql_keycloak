APP_NAME = ztp-browser
NAMESPACE = ztp

reinstall: uninstall install

install:
	helm install ${APP_NAME} . -n ${NAMESPACE} --create-namespace

uninstall:
	helm uninstall -n ${NAMESPACE} ${APP_NAME} || true

purge: uninstall
	kubectl delete ns ${NAMESPACE} || true

upgrade:
	helm upgrade ${APP_NAME} . -n ${NAMESPACE}

template:
	helm template ${APP_NAME} -n ${NAMESPACE} . | less
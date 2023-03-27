
# TODO: detect version
# python3 src/pile3.py --version

docker:
	docker build . -t pile3

docker-test:
	docker run -ti pile3
# docker run -ti pile3 pile3.py --status

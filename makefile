upload:
	rsync -r  --progress  ./* tencent:~/app/wolf/
run:
	export PYTHONPATH=".:$$PYTHONPATH" ;python3 wiredwolf/server.py
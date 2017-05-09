cd ~/git/panorama-worker
source venv/bin/activate
source .env
today=`date '+%Y_%m_%d__%H_%M_%S'`;
filename="./logs/$today.log"
touch $filename
python worker.py > $filename 2>&1

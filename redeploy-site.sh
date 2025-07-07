tmux kill-server

git fetch && git reset origin/main --hard

source python3-virtualenv/bin/activate
pip install -r requirements.txt
echo "starting flask"
tmux new-session -d -s flask_server "
source python3-virtualenv &&
export FLASK_APP=app &&
flask run --host=0.0.0.0
"
echo "flask has been run"


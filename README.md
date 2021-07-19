# WatsonServer

A simple server for [watson](https://github.com/TailorDev/Watson), as the
official server, [crick](https://github.com/TailorDev/crick) no longer seems to
work.

! WARNING: this is a very crude and untested implementation, use with caution.

## Running

```sh
virtualenv -p python3 venv

. venv/bin/activate

export DATABASE_URI="sqlite:///students.sqlite3"
export WATSON_SECRET="MySuperSecretToken"

python app.py
```

Now you can set up watson with `watson config backend.token MySuperSecretToken`
and `watson config backend.url http://localhost:8080` and sync with `watson
sync`.

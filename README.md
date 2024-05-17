
Проект  Celery_Flask example
-----------------------------------------------


# активация виртуального окружения
source C:/Server/venv_flask3/Scripts/activate
#WIN#
C:\Server\venv_flask3\Scripts\activate.bat

# деактивация окружения
deactivate
#WIN#
C:\Server\venv_flask3\Scripts\deactivate.bat

# папка приложения
cd $YandexDisk/_Projects_Py/Celery_Flask/app
#WIN#
cd /d %YandexDisk%\_Projects_Py\Celery_Flask\app

# запуск приложения (обязательно с python иначе запустит глобальный)
python celery_main.py --local
# запуск сразу из папки
python $YandexDisk/_Projects_Py/Celery_Flask/app/celery_main.py --local

# запуск рабочего (worker) celery
celery -A tasks worker --loglevel=info --pool=solo


#===================================================================================================
            *** Git ***

Проект Celery_Flask
    cd "$YandexDisk/_Projects_Py/Celery_Flask"
    git remote add origin git@bitbucket.org:Vintets/celery_flask.git
    # добавить привязку ко 2 репозиторию (github)
    git remote set-url origin --add git@github.com:Vintets/Celery_Flask.git


#===================================================================================================

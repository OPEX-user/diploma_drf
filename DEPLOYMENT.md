<h1>Инструкция по локальному развёртыванию приложения</h1>

<h3>Получение исходного кода</h3>
Выберите каталог для установки приложения, перейдите в него и выполните команды GIT:<br>
git init<br>
git remote add origin git@github.com:OPEX-user/DRF.git<br>
git pull origin main<br>
<br>
<h3>Настройка окружения</h3>
Находясь в каталоге с приложением выполните команды (необходимо использовать Python 3):<br>
python -m venv venv<br>
<b>MacOs/Linux:</b> source venv/bin/activate<br>
<b>Windows:</b> /venv/Scripts/activate.bat<br> 
<br>
python -m pip install --upgrade pip<br>
cd diploma<br>
pip install -r requirements.txt<br>
<br>
<h3>Запуск приложения</h3>
Перейдите в каталог diploma<br>
Выполните следующие команды:<br>
pyton manage.py makemigrations<br>
pyton manage.py migrate<br>
pyton manage.py runserver 127.0.0.1:8000<br>
# ICOToday Backend

## Project Structure
```
DeepComp
|-- DeepComp
|   |-- apps                // Contains all models
|   |   |-- accounts        
|   |   |   |-- migrations  // Model migraitions
|   |   |   |-- admin.py    // Model admin
|   |   |   |-- apps.py
|   |   |   |-- models.py   // Model structure
|   |   |   |-- urls.py     // Model URL
|   |   |   |-- tests.py
|   |   |   `-- views.py    // Model views
|   |   |-- questions
|   |   |-- ...
|   |-- settings            // Settings folder
|   |   |-- dev.py          // Dev mode
|   |   |-- production.py   // Production mode
|   |   `-- secret.txt      // Store secret separately
|   |-- static              // Static files (img, txt, etc)
|   |-- templates           // Django templates (Only for customize Django Admin)
|   |-- urls.py             // Root URL
|   `-- wsgi.py
|-- manage.py               // Change 'DeepComp.settings.dev' to 'DeepComp.settings.production' to deploy
|-- requirements.txt        // All required python packages
`-- setup.sh                // A one step setup script

```
## Set up Script

```
> # Clone
> git clone https://github.com/C0deZLee/ICOToday-Backend.git
> # Create virtualenv and activate
> virtualenv env
> source env/bin/activate
> cd ICOToday-Backend
> # Install requirements
> pip install -r requirements.txt
> # Migrate database
> python manage.py makemigrations
> python manage.py migrate
> # Create Superuser
> python manage.py createsuperuser

sudo yum install gcc gcc-c++
sudo yum install -y libffi libffi-devel
pip install --upgrade pip 
pip install --upgrade pillow
sudo yum install libtiff-devel libjpeg-devel libzip-devel freetype-devel lcms2-devel libwebp-devel tcl-devel tk-devel

sudo yum install nginx
pip install uwsgi
sudo /etc/init.d/nginx start
touch nginx.conf
sudo mkdir /etc/nginx/sites-enabled/
sudo ln -s /home/ec2-user/ICOToday-Backend/nginx.conf /etc/nginx/sites-enabled/
sudo yum install mysql-devel
sudo yum -y install readline-devel openssl-devel gmp-devel ncurses-devel
sudo yum -y install gdbm-devel expat-devel libGL-devel libX11-devel tcl-devel tk-devel
sudo yum -y install tix-devel sqlite-devel db4-devel
pip install MySQL-python
```



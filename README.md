# DeepComp Backend

## Set up Script

```
> # Clone
> git clone https://github.com/zhxsxuan/DeepCompBackend.git
> cd DeepCompBackend
> git checkout dev
> # Create local folder for virtual env
> mkdir -p local
> cd local
> # Create virtualenv and activate
> virtualenv -p python3 env
> source env/bin/activate
> # Install requirements
> cd ../DeepComp
> pip install -r requirements.txt
> # Migrate database
> python manage.py makemigrations
> python manage.py migrate
> # Create Superuser
> python manage.py createsuperuser
> # Run local server
> python manage.py runserver
```

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

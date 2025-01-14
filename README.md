# Django Petiscos&Ariscos website with Docker

This is an example project for building a website for my mother using **Django** and **Docker**. The aim of this project is to demonstrate the integration of Django with Docker to facilitate development and implementation.
I had almost finished the backend and frontend, but as a Python developer, it's noticeable that in job positions, knowledge of Docker and databases is increasingly required, so I'm going to try to learn and make my mother's website in a professional way as if I were in a “Project” environment. 

## Technologies

- **Django** - Web Framework in Python.
- **PostgreSQL** - Database Management System.
- **Docker** - Tool for creating and managing containers.
- **Docker Compose** - Tool for defining and running multi-container Docker applications.

## Functionalities (In the future, more will be added)

- Creating users with authentication (user and superuser).
- Customized administration interface.
- Integration with PostgreSQL database.
- Configuration with Docker to facilitate the development environment.

## How to Run the Project

### Prerequisites

- **Docker** and **Docker Compose** installed on your computer.

### Passos para rodar o projeto

1. Clone the repository:
    ```bash
    git clone https://github.com/godbernaz/django-petiscos-w-docker.git

2. Navigate to the project directory:
    ```bash
    cd django-petiscos-w-docker

3. Build the containers with Docker Compose:
    ```bash
    docker-compose up -d --build
4. Access the Django container:
    ```bash
    docker-compose exec web python manage.py migrate
5. Create a superuser to access the Django admin:
    ```bash
    docker-compose exec web python manage.py createsuperuser
6. Access the site in your browser:
    * Visit http://localhost:8000 to see the application in operation.
    * Access the administration panel at http://localhost:8000/admin with the superuser credentials you created.

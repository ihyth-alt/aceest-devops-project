pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Pulling latest code from GitHub...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh 'pip install --no-cache-dir -r requirements.txt'
            }
        }

        stage('Lint') {
            steps {
                echo 'Running flake8 lint check...'
                sh 'pip install flake8'
                sh 'flake8 app.py --max-line-length=120 --ignore=E501'
            }
        }

        stage('Test') {
            steps {
                echo 'Running Pytest unit tests...'
                sh 'pytest test_app.py -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t aceest-fitness-app .'
            }
        }

    }

    post {
        success {
            echo 'BUILD SUCCESSFUL — All stages passed!'
        }
        failure {
            echo 'BUILD FAILED — Check the logs above.'
        }
    }
}

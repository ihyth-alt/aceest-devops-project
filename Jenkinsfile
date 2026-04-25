pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'ihyth32/aceest-fitness'
        IMAGE_TAG = "v4.${BUILD_NUMBER}"
        SONAR_PROJECT = 'aceest-fitness'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Lint') {
            steps {
                bat 'pip install flake8'
                bat 'flake8 app.py --max-line-length=120 --exit-zero'
            }
        }

        stage('Run Tests with Coverage') {
            steps {
                bat 'pytest test_app.py --cov=app --cov-report=xml --cov-report=term'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    bat """
                        sonar-scanner ^
                        -Dsonar.projectKey=%SONAR_PROJECT% ^
                        -Dsonar.sources=app.py ^
                        -Dsonar.tests=test_app.py ^
                        -Dsonar.python.coverage.reportPaths=coverage.xml
                    """
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: false
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                bat "docker build -t %DOCKER_IMAGE%:%IMAGE_TAG% ."
                bat "docker tag %DOCKER_IMAGE%:%IMAGE_TAG% %DOCKER_IMAGE%:latest"
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat 'echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin'
                    bat "docker push %DOCKER_IMAGE%:%IMAGE_TAG%"
                    bat "docker push %DOCKER_IMAGE%:latest"
                }
            }
        }
    }

    post {
        always {
            bat 'docker logout'
        }
        success {
            echo "Build ${BUILD_NUMBER} successful. Image: ${DOCKER_IMAGE}:${IMAGE_TAG}"
        }
        failure {
            echo "Build ${BUILD_NUMBER} failed."
        }
    }
}
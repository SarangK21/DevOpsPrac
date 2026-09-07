pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Run Tests') {z
            steps {
                sh 'python3 -m pytest'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t map_project:${BUILD_NUMBER} .'
            }
        }
    }
}
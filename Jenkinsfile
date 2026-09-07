pipeline {

    agent any

    environment {
        IMAGE_NAME = "map_project:${BUILD_NUMBER}"
        CONTAINER_NAME = "map-api-test-${BUILD_NUMBER}"
    }

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

        stage('Run Tests') {
            steps {
                sh 'python3 -m pytest'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "Jenkins PATH:"
                    echo $PATH

                    echo "Docker location:"
                    which docker || true

                    echo "Docker version:"
                    docker --version || true

                    echo "Python location:"
                    which python3
                '''
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        -p 5001:5000 \
                        ${IMAGE_NAME}
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    echo "Waiting for application..."

                    sleep 5

                    curl --fail http://localhost:5001/health

                    echo ""
                    echo "Application health check passed!"
                '''
            }
        }

        stage('Cleanup') {
            steps {
                sh '''
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                    docker rmi ${IMAGE_NAME} || true
                '''
            }
        }
    }
}
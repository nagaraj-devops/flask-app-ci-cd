pipeline {
    agent any
    environment {
        AWS_REGION = 'ap-south-1'
        ECR_REGISTRY = '412275828685.dkr.ecr.ap-south-1.amazonaws.com'
        IMAGE_NAME = 'flask-app-ci-cd'
        TARGET_IP = '15.207.11.6'
    }
    stages {
        stage('Build') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
            }
        }
        stage('Push to ECR') {
            steps {
                script {
                    // Define the explicit path
                    def awsCli = "/snap/bin/aws"
                    
                    // Perform the login, tag, and push
                    sh """
                        ${awsCli} ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                        docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${ECR_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}
                        docker push ${ECR_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}
                    """
                }
            }
        }
        stage('Deploy') {
            steps {
                sshagent(['deploy-ssh-key-nagaraj-aws']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ubuntu@${TARGET_IP} '
                            aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                            docker pull ${ECR_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}
                            docker stop flask-app || true
                            docker rm flask-app || true
                            docker run -d -p 5000:5000 --name flask-app ${ECR_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}
                        '
                    """
                }
            }
        }
    }
}
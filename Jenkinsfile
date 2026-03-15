pipeline {
    agent any
    environment {
        AWS_REGION = 'ap-south-1'
        ECR_REGISTRY = '412275828685.dkr.ecr.ap-south-1.amazonaws.com'
        IMAGE_NAME = 'flask-app-ci-cd'
    }
    stages {
        stage('Build') {
            steps {
                script {
                    // Build the image
                    sh "docker build -t ${IMAGE_NAME}:${env.BRANCH_NAME}-${env.BUILD_NUMBER} ."
                }
            }
        }
        stage('Push to ECR') {
            steps {
                script {
                    // Log in to ECR
                    sh "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}"
                    
                    // Tag and push
                    sh "docker tag ${IMAGE_NAME}:${env.BRANCH_NAME}-${env.BUILD_NUMBER} ${ECR_REGISTRY}/${IMAGE_NAME}:${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
                    sh "docker push ${ECR_REGISTRY}/${IMAGE_NAME}:${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
                }
            }
        }
        stage('Deploy to Target') {
            steps {
                sshagent(['your-ssh-credential-id']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ubuntu@<TARGET_INSTANCE_IP> '
                            aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 412275828685.dkr.ecr.ap-south-1.amazonaws.com
                            docker pull 412275828685.dkr.ecr.ap-south-1.amazonaws.com/flask-app-ci-cd:latest
                            docker stop flask-app || true
                            docker rm flask-app || true
                            docker run -d -p 5000:5000 --name flask-app 412275828685.dkr.ecr.ap-south-1.amazonaws.com/flask-app-ci-cd:latest
                        '
                    """
                }
            }
        }
    }
}
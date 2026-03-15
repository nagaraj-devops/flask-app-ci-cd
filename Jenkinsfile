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
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'ecr-cross-account-creds']]) {
                        def awsCli = "/usr/local/bin/aws"
                        
                        // 1. Login
                        sh "${awsCli} ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}"
                        
                        // 2. Build or Tag the image specifically for ECR
                        // Assuming your build stage created an image named 'flask-app-ci-cd'
                        sh "docker tag flask-app-ci-cd:${BUILD_NUMBER} ${ECR_REGISTRY}/flask-app-ci-cd:${BUILD_NUMBER}"
                        
                        // 3. Push the fully qualified image
                        sh "docker push ${ECR_REGISTRY}/flask-app-ci-cd:${BUILD_NUMBER}"
                    }
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
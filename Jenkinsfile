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
                    // Explicitly point the AWS CLI to the credentials file
                    withEnv(['AWS_SHARED_CREDENTIALS_FILE=/home/ubuntu/.aws/credentials', 'AWS_CONFIG_FILE=/home/ubuntu/.aws/config']) {
                        def awsCli = "/usr/local/bin/aws"
                        sh """
                            ${awsCli} ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                            docker push ${ECR_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}
                        """
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
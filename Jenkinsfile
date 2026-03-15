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
                withCredentials([sshUserPrivateKey(credentialsId: 'deploy-ssh-key-nagaraj-aws', keyFileVariable: 'MY_KEY')]) {
                    sh """
                        chmod 400 ${MY_KEY}
                        ssh -i ${MY_KEY} -o StrictHostKeyChecking=no ubuntu@15.207.11.6 << 'EOF'
                            # 1. Login to ECR
                            /snap/bin/aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 412275828685.dkr.ecr.ap-south-1.amazonaws.com
                            
                            # 2. Pull the specific version
                            docker pull 412275828685.dkr.ecr.ap-south-1.amazonaws.com/flask-app-ci-cd:${env.BUILD_NUMBER}
                            
                            # 3. Clean up old containers (using || true so it doesn't fail if they don't exist)
                            docker stop flask-app || true
                            docker rm flask-app || true
                            
                            # 4. Run the new container
                            docker run -d -p 5000:5000 --name flask-app 412275828685.dkr.ecr.ap-south-1.amazonaws.com/flask-app-ci-cd:${env.BUILD_NUMBER}
                            
                            # 5. Verification
                            echo "Checking running containers:"
                            docker ps | grep flask-app
        EOF
                    """
                }
            }
        }
    }
}
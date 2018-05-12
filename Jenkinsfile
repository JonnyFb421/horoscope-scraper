pipeline {
    agent any
    environment {
        IMAGE_NAME = 'jonnyfb421/horoscope-scraper'
        VERSION = sh(script:"cat ./version.txt", returnStdout: true)
        IMAGE_TAG = '$IMAGE_NAME:$VERSION'
    }
    stages {
            stage('Checkout SCM') {
                steps {
                    checkout scm
                }
            }
            stage('Running tests') {
                agent { dockerfile true }
                steps {
                    sh "pip install --user .[dev]"
                    sh "py.test --cov=horoscope_scraper --cov-report xml --junitxml=junit-results.xml tests/"
                }
            }
            stage('Push production image') {
                when { branch 'master' }
                steps {
                    script {
                        withDockerRegistry([ credentialsId: "dockerhub-creds", url: "" ]) {
                            docker.build("${IMAGE_TAG}").push()
                        }
                    }
                }
            }
            stage('Deploying the new version') {
                when { branch 'master' }
                    environment {
                        PROD_PEM = credentials('prod_pem')
                        PROD_INSTANCE = credentials('horoscope_scraper_prod')
                    }
                steps {
                    script {
                            def running_container = sh (script: "ssh -oStrictHostKeyChecking=no -i $PROD_PEM $PROD_INSTANCE sudo docker ps -qf \"label=$IMAGE_NAME\"", returnStdout: true)
                            if (running_container) {
                                sh "ssh -oStrictHostKeyChecking=no -i $PROD_PEM $PROD_INSTANCE sudo docker kill ${running_container}"
                            }
                            sh "ssh -oStrictHostKeyChecking=no -i $PROD_PEM $PROD_INSTANCE sudo docker run -d -p 80:5000 -l $IMAGE_NAME $IMAGE_TAG"
                    }
                }
            }
        }
    post {
        always {
            deleteDir()
        }
    }
}

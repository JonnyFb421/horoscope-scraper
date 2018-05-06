pipeline {
    agent any
    environment {
        IMAGE_NAME = 'jonnyfb421/horoscope-scraper'
        VERSION = sh(script:"cat ./version.txt", returnStdout: true)
        IMAGE_TAG = '$IMAGE_NAME:$VERSION'
    }
    stages {
//            stage('Running tests') {
//                agent { dockerfile true }
//                steps {
//                    sh "pip install --user .[dev]"
//                    sh "py.test --cov=horoscope_scraper --cov-report xml --junitxml=junit-results.xml tests/"
//                }
//            }
//            stage('Checkout SCM') {
//                steps {
//                    checkout scm
//                }
//            }
//            stage('Push production image') {
//                steps {
//                    script {
//                        withDockerRegistry([ credentialsId: "dockerhub-creds", url: "" ]) {
//                            docker.build("${IMAGE_TAG}").push()
//                        }
//                    }
//                }
//            }
            stage('Deploy app') {
                steps {
                    script {
                        withCredentials(bindings: [sshUserPrivateKey(credentialsId: 'ssh-ec2-horoscope-scraper', \
                                                                     keyFileVariable: 'SSH_KEY')]) {
                            sh "ssh -oStrictHostKeyChecking=no -tt -i ~/.ssh/jonny.pem ec2-user@52.14.201.238 sudo docker run -p 80:5000 $IMAGE_TAG"
                        }
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

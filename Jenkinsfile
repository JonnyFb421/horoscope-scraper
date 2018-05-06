pipeline {
    agent any
    environment {
        IMAGE_NAME = 'jonnyfb421/horoscope-scraper'
        VERSION = sh(script:"cat ./version.txt", returnStdout: true)
    }
    stages {
//            stage('Running tests') {
//                agent { dockerfile true }
//                steps {
//                    sh "pip install --user .[dev]"
//                    sh "py.test --cov=horoscope_scraper --cov-report xml --junitxml=junit-results.xml tests/"
//                }
//            }
            stage('Checkout SCM') {
                steps {
                    checkout scm
                }
            }
            stage('Push production image') {
                steps {
                    script {
                        docker.build("${env.IMAGE_NAME}:${env.VERSION}").push()
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

pipeline {
    agent { dockerfile true }

    stages {
            stage('Install Testing Dependencies') {
                steps {
                    sh "whoami"
                    sh "pip install --user .[dev]"
                }
            }
            stage('Run Tests') {
                steps {
                    sh "py.test --cov=horoscope_scraper tests/"
                    }
                }
            }
        }

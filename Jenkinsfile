pipeline {
    agent {
        node {
            label 'python-dind'
            }
      }
    triggers{
        pollSCM '*/10 * * * *'
    }
    stages {
    stage('Build') {
        steps {
            echo "Building.."
            sh '''
            cd Air_Quality
            python3 -m venv .venv
            ls -al
            .venv/bin/python --version
            . .venv/bin/activate
            pip install pytest
            cd ..
            python -m pip install -r requirements.txt
            deactivate
            '''
        }
    }
    stage('Test') {
        steps {
            echo "Testing.."
            sh '''
            cd Air_Quality
            . .venv/bin/activate
            pytest
            '''
        }
    }
    stage('Deliver') {
        steps {
            echo 'Deliver....'
            sh '''
            echo "doing delivery stuff.."
            '''
        }
    }
}
}
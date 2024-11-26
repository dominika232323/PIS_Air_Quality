pipeline {
    agent {
        node {
            label 'python-agent'
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
            .venv/bin/python -m pip install django
            . .venv/bin/activate
            pip install pytest
            pip install pytest-django
            deactivate
            . .venv/bin/activate
            '''
        }
    }
    stage('Test') {
        steps {
            echo "Testing.."
            sh '''
            cd Air_Quality
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
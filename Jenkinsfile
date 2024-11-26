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
            ls -al ./.venv
            ls -al ./.venv/venv
            .venv/venv/bin/python --version
            .venv/venv/bin/python -m pip install django
            . venv/bin/activate
            '''
        }
    }
    stage('Test') {
        steps {
            echo "Testing.."
            sh '''

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
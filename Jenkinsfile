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
            bash '''
            cd Air_Quality
            python3 -m venv .venv
            .venv/venv/bin/python --version
            .venv/venv/bin/python -m pip install django
            . venv/bin/activate
            '''
        }
    }
    stage('Test') {
        steps {
            echo "Testing.."
            bash '''

            pytest
            '''
        }
    }
    stage('Deliver') {
        steps {
            echo 'Deliver....'
            bash '''
            echo "doing delivery stuff.."
            '''
        }
    }
}
}
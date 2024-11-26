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
            . .venv/bin/activate
            pip install pytest
            pip install pytest-django
            deactivate
            pwd
            ls -al
            .venv/bin/python -m pip install -t ../requirements.txt
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
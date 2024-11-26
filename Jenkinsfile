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
            mkdir -p ~/.venvs
            python3 -m venv $HOME/.venvs/pis_env
            ~/.venvs/pis_env/bin/python --version
            ~/.venvs/pis_env/bin/python  -m pip install django
            source ~/.venvs/pis_env/bin/activate
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
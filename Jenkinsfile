pipeline {
    agent {
        node {
            label 'agent-ansible'
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
            ls
            . Air_Quality/.venv/bin/activate
            make tests
            '''
        }
    }
    stage('Deliver') {
        steps {
            echo 'Deliver....'
            sh '''
            cd deployment
            ansible-playbook -i inventory.yml playbook.yml
            '''
        }
    }
}
}
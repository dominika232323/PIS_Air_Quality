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
            pipx ensurepath
            pipx install django
            '''
        }
    }
    stage('Test') {
        steps {
            echo "Testing.."
            sh '''
            pipx install django
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
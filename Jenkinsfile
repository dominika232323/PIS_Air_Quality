pipeline {
    agent {
        node {
            label 'python-agent'
            }
      }
    triggers{
        pollSCM '*/30 * * * *',
        githubPush()
    }
    stages {
    stage('Build') {
        steps {
            echo "Building.."
            sh '''
            pip install -r requirements.txt
            '''
        }
    }
    stage('Test') {
        steps {
            echo "Testing.."
            sh '''
            echo "doing test stuff.."
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
pipeline {
  agent {
    node {
      label 'gao'
    }

  }
  stages {
    stage('Git Pull') {
      steps {
        git(url: 'ssh://git@github.com:gaokang9009/PO_WEB.git', branch: 'master')
      }
    }

    stage('Build') {
      steps {
        bat 'python run.py  demo'
      }
    }

  }
}
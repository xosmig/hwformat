pipeline {
  agent any
  stages {
    stage('build') {
      steps {
        sh './install_ubuntu.sh'
        sh 'cd example'
        sh 'hwformat bad_example.hw'
      }
    }
  }
}
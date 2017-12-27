pipeline {
  agent any
  environment {
    PATH = "$PATH:$HOME/.local/bin"
  }
  stages {
    stage('build') {
      steps {
        sh 'python3 --version'
        sh './install_ubuntu.sh'
      }
    }
    stage('test') {
      steps {
        sh '''
          cd example &&
          mv bad_example.tex bad_example_expected.tex &&
          hwformat bad_example.hw &&
          diff bad_example.tex bad_example_expected.tex
        '''
      }
    }
  }
}
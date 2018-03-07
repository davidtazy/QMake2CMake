
node {        
        stage 'Cleanup workspace'
        sh 'chmod 777 -R .'
        sh 'rm -rf dist/*'
        checkout scm
   
        
        stage 'Build .whl'     
            sh 'ls -l'
            sh 'python setup.py bdist_wheel'
           

        stage 'Archive build artifact: .whl'
            archive 'dist/*'       
}

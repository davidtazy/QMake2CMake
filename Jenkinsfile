
node {        
        stage 'Cleanup workspace'
        sh 'chmod 777 -R .'
        sh 'rm -rf dist/*'
   
        
        stage 'Build .whl'            
            sh 'python setup.py bdist_wheel'
           

        stage 'Archive build artifact: .whl'
            archive 'dist/*'       
}

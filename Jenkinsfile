
pipeline{    
        agent any
        stages{
                stage ('Cleanup workspace'){
                        steps{
                        sh 'chmod 777 -R .'
                        sh 'rm -rf dist/*'
                        checkout scm
                        }
                }
   
               
                stage ('Build .whl'){
                        steps{
                        sh 'ls -l'
                        sh 'mkdir -p dist'
                        sh 'touch dist/toto.log'
                        }
                }
           

                stage ('Archive build artifact: .whl'){
                        steps{
                        archive 'dist/*'   
                        }
                }
        }
                
}

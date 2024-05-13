### Demo app for integration with the calculator platform
After downloading the project, run `./init.sh` to install dependencies. After that you can run the app using `./nextflow run main.nf`

The application uses the input/input.json file as the input for the application. The results are saved to output and contain both JSON document and individual files. Outputs are provided in English and Latvian for demonstrating the multilingual aspects of the solutions. 

Additionally, `completed.sh` is run after successful completion of the NextFlow app, and `failed.sh` is run upon a failure.

Additionally, `runner.sh` is an example runner for starting the job using `qsub`. Project path needs to be adjusted accordingly.
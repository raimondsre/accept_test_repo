#!/usr/bin/env nextflow
project_dir = projectDir

process writeToFile {
    input:
    file 'input'

    script:
    """
    cat ${input} > ${projectDir}/output/output.txt
    """
}

process demo {
    executor = 'local'

    output:
    stdout

    script:
    """
    source ${project_dir}/venv/bin/activate && python ${projectDir}/demo.py ${project_dir}
    """
}

process completed{
    executor = 'local'

    script:
    """
    echo "ssss" > ${project_dir}/bla.txt
    """
}



workflow {
    demo | writeToFile
}

workflow.onComplete {
    def proc = "./completed.sh".execute()
    def b = new StringBuffer()
    proc.consumeProcessErrorStream(b)
    println proc.text
    println b.toString()
}

workflow.onError {
    def proc = "./failed.sh".execute()
    def b = new StringBuffer()
    proc.consumeProcessErrorStream(b)
    println proc.text
    println b.toString()
}
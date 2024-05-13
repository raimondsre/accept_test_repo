#!/usr/bin/env nextflow
project_dir = projectDir

process writeToFile {
    executor = 'local'

    input:
    file 'input'

    script:
    """
    cat ${input} > ${projectDir}/output/output.json
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
    def proc = "${project_dir}/completed.sh".execute()
    def b = new StringBuffer()
    proc.consumeProcessErrorStream(b)
    println proc.text
    println b.toString()
}

workflow.onError {
    def proc = "${project_dir}/failed.sh".execute()
    def b = new StringBuffer()
    proc.consumeProcessErrorStream(b)
    println proc.text
    println b.toString()
}
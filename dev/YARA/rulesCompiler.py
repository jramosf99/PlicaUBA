import yara
outputFile='/home/ramos/Escritorio/TFG/YARA/norma'
rule1 = '/home/ramos/Escritorio/TFG/YARA/index.yar'
rules = yara.compile(rule1)

# # guarda las normas compiladas
rules.save(outputFile)

import yara
outputFile='/home/ramos/Escritorio/tocar/YARA/norma'
rule1 = '/home/ramos/Escritorio/tocar/rules/rules/malware_index.yar'
rule2 = '/home/ramos/Escritorio/tocar/rules/rules/cve_rules_index.yar'
rules = yara.compile(filepaths={
  'rule1':rule1,
'rule2':rule2
})

# # guarda las normas compiladas
rules.save(outputFile)

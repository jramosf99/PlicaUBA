rules = yara.compile(filepaths={
  'rule1':'/home/ramos/Escritorio/tocar/YARA/norma1.yar',
'rule2':'/home/ramos/Escritorio/tocar/YARA/norma2.yar'
})

# # guarda las normas compiladas
rules.save('/home/ramos/Escritorio/tocar/YARA/norma')

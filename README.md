creare un piccolo ml project

con 2 parametri: param_1 e param_2 (devono essere tutti e 2 csv)

mettere progetto sul mio github


how to work:
- lancio il progetto passandogli 2 csv
- data_prep: elabora i 2 csv, controlla cosa sono e li unisce. Se gliene passo solo uno, lavora solo sul primo. se il file non è un csv gli faccio lanciare un errore
- model_training: NON gli faccio fare nulla
- evaluation: NON gli faccio fare nulla

come passare i parametri?
mlflow run . -P param_1="path\del\csv"

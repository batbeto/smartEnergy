with open( "teste.csv", "w" ) as arquivo:
    with open( "2018-05-12.csv", 'r' ) as db:
        for i in db.readlines( ):
            a = i.split(",")
            arquivo.write( str(f'{a[4]}, {a[7]}\n' ) )
        db.close()
    arquivo.close()

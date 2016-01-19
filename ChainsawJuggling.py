import sys

from peewee import *

def main():
    db=SqliteDatabase('jugglers.db')
    jugglers=[{'name':'Ian Stewart','country':'Canada','catches':94},
              {'name':'Aaron Gregg','country':'Canada','catches':88},
              {'name':'Chad Taylor','country':'USA','catches':78}]

    def Main_Menu():
            menuChoice = input('Please select from the following\n'
              '1) Add a juggler\n'
              '2) Delete a juggler\n'
              '3) Modify a record holders catch number\n'
              '4) Search for a record\n'
              '5) Quit Program\n')
            if menuChoice in ('1234'):
                if menuChoice=='1':
                    addNewJuggler()
                if menuChoice=='2':
                    delete_record()
                if menuChoice=='3':
                    search_and_update()
                if menuChoice=='4':
                    search_only()
                return menuChoice
            elif menuChoice == '5':
                sys.exit()
            else:
                print('That was not an option please try again.')
    # Here the program runs normally until it is force quitted by option 5


    class JugglerModel(Model):
        name=CharField(max_length=255, unique=True)
        country=CharField(max_length=255)
        catches=IntegerField()


        class Meta:
            database=db
    def search_only():
        try:
            this_record=JugglerModel.get(JugglerModel.name.startswith(input('Please input a name to change the record of.\n')))
            print ('Name: {}\tCountry: {}\tCatches: {}\t'.format(this_record.name,this_record.country,this_record.catches))
        except:
            DoesNotExist
            print('That record was not found!')
    def search_and_update():
        display_all_records()
        this_record=JugglerModel.get(JugglerModel.name.startswith(input('Please input a name to change the record of.\n')))
        catches=this_record.catches
        this_record.catches=(int(input('How many more catches than his previous record did he make?'))+catches)
        this_record.save()

    def delete_record():
        display_all_records()
        this_record=JugglerModel.get(JugglerModel.name.startswith(input('Please input the name of the record to delete.')))
        this_record.delete_instance()
        display_all_records()
    def addNewJuggler():
        name=input('Please enter the name of the new Juggler')
        country=input('Please enter the country '+name+' is from.')
        catches=int(input('What was '+name+'\'s new catch record?'))

        new_record=JugglerModel.create(name=name,country=country, catches=catches)
        new_record.save()
        display_all_records()

    def display_all_records():
        for record in JugglerModel:
            print('Name: {}\tCountry: {}\tCatches: {}\t'.format(record.name,record.country,record.catches))

    def addJugglers():
        try:
            for juggler in jugglers:
                   JugglerModel.create(name=juggler['name'],country=juggler['country'],catches=juggler['catches'])
        except IntegrityError:
            juggler_record= JugglerModel.get(name=juggler['name'])
            juggler_record.country=juggler['country']
            juggler_record.catches=juggler['catches']


    db.connect()
    db.create_tables([JugglerModel],safe=True)
    addJugglers()
    while Main_Menu():
        Main_Menu()

main()


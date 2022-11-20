DIRUSER := users/
SHADOW := .shadow
DIREXE := src/
DIRTEST := tests/
CC := python

username := prueba1
password := Seg-Red
file := frutas

all: users shadow

run:
	$(CC) $(DIREXE)/main.py

test:
	./$(DIRTEST)test_version.sh

	./$(DIRTEST)test_register_login.sh $(username) $(password)

	./$(DIRTEST)test_user_actions.sh $(username) $(password) $(file)

	./$(DIRTEST)test_all_docs.sh $(username) $(password)

clean: cleanShadow cleanUsers

users:
	mkdir -p $(DIRUSER)

shadow:
	touch $(SHADOW)

cleanShadow:
	rm $(SHADOW)
cleanUsers:
	rm -rf $(DIRUSER)
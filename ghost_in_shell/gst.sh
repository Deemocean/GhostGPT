#!/bin/bash
pip install openai
echo ' ________  ___  ___  ________  ________  _________   
|\   ____\|\  \|\  \|\   __  \|\   ____\|\___   ___\ 
\ \  \___|\ \  \\\  \ \  \|\  \ \  \___|\|___ \  \_| 
 \ \  \  __\ \   __  \ \  \\\  \ \_____  \   \ \  \  
  \ \  \|\  \ \  \ \  \ \  \\\  \|____|\  \   \ \  \ 
   \ \_______\ \__\ \__\ \_______\____\_\  \   \ \__\
    \|_______|\|__|\|__|\|_______|\_________\   \|__|
                                 \|_________|   '


if [ ! -d "IMPRINTS" ]; then
  echo "No directory for Neural Imprints exists. Automatically creating..."
  mkdir "IMPRINTS"
  read -p "Name your new imprint: " imprint_name
  touch IMPRINTS/${imprint_name}.ni
  echo -n '[]' > IMPRINTS/${imprint_name}.ni
fi

menu(){
echo "---------------------------Available imprints:-------------------------"
ls IMPRINTS/*.ni | xargs -n 1 basename | sed -e 's/\.ni$//'
echo "-----------------------------------------------------------------------"

options=("Create a clean imprints" "Inject an imprint" "Wipe an imprint" "Exit")
select opt in "${options[@]}"
do
    case $opt in
        "Create a clean imprints")
            read -p "Name your new imprint: " imprint_name
            touch IMPRINTS/${imprint_name}.ni
            echo -n '[]' > IMPRINTS/${imprint_name}.ni
            menu;;

        "Inject an imprint")
            read -p "Inject imprint: " imprint_name
            python ghost.py $imprint_name
            menu;;

        "Wipe an imprint")   
            read -p "Wipe imprint: " imprint_name
            rm IMPRINTS/${imprint_name}.ni
            menu
            ;;

        "Exit")
            break
            ;;
        *) echo "invalid option $REPLY";;
    esac
done
}

menu




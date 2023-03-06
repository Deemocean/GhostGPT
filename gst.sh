#!/bin/bash

python3 config/logo.py

if [ ! -d "IMPRINTS" ]; then
  echo "No directory for Neural Imprints exists. Automatically creating..."
  mkdir "IMPRINTS"
  read -p "Name your new imprint: " imprint_name
  touch IMPRINTS/${imprint_name}.ni
  echo -n '[]' > IMPRINTS/${imprint_name}.ni
fi

choose_platform(){
    echo "Inject to platform:"
    options=("Shell" "Telegram" "Back" )

    select opt in "${options[@]}"
do
    case $opt in
        "Shell")
            read -p "[Inject] imprint: " imprint_name
            python3 ghost/ghost_in_shell.py $imprint_name
            menu
            ;;

        "Telegram")
            read -p "[Inject] imprint: " imprint_name
            python3 ghost/ghost_in_telegram.py $imprint_name
            menu
            ;;

        "Back")
            menu
            ;;

        *) echo "invalid option $REPLY";;
    esac
done

}

config(){
    options=("[Install] Required Libs" "[Config] Keys" "[Back]" )

    select opt in "${options[@]}"
do
    case $opt in
        "[Install] Required Libs")
            pip install -r requirements.txt --upgrade
            echo -e "\033[38;5;33m done.\033[0m - if no error, you are good"
            config
            ;;

        "[Config] Keys")
            python3 config/config.py config
            config
            ;;

        "[Back]")
            menu
            ;;

        *) echo "invalid option $REPLY";;
    esac
done

}



menu(){
clear
python3 config/logo.py
echo -e "##############|First-Timer? Start with the \033[38;5;33m[Config]\033[0m option|##############"
echo "---------------------------Enviroment:---------------------------------"
python3 config/config.py print_keys
echo "---------------------------Available imprints:-------------------------"
ls IMPRINTS/*.ni | xargs -n 1 basename | sed -e 's/\.ni$//'
echo "-----------------------------------------------------------------------"

options=("[Create] an imprint" "[Inject] an imprint" "[Wipe] an imprint" "[Config]" "[Exit]" )
select opt in "${options[@]}"
do
    case $opt in
        "[Create] an imprint")
            read -p "Name your new imprint: " imprint_name
            touch IMPRINTS/${imprint_name}.ni
            echo -n '[]' > IMPRINTS/${imprint_name}.ni
            menu;;

        "[Inject] an imprint")
            choose_platform;;

        "[Wipe] an imprint")   
            read -p "Wipe imprint: " imprint_name
            rm IMPRINTS/${imprint_name}.ni
            menu
            ;;
         "[Config]")
            config
            ;;
        "[Exit]")
            clear
            exit
            ;;

        *) echo "invalid option $REPLY";;
    esac
done
}

menu



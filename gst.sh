#!/bin/bash
create_imprint(){
    read -p "Name your new imprint: " imprint_name
    if [ ${#imprint_name} != 0 ]; then
        touch IMPRINTS/${imprint_name}.ni
        echo -n '[]' > IMPRINTS/${imprint_name}.ni
    fi
}
if [ ! -d "IMPRINTS" ]; then
  echo "No directory for Neural Imprints exists. Automatically creating..."
  mkdir "IMPRINTS"
  create_imprint
fi

choose_platform(){
    SCRIPT=${DEFAULT_SCRIPT-None}
    if [ "$SCRIPT" == "None" ]; then
        echo "Inject to platform:"
        options=("Shell" "Telegram" "Back" )

        select opt in "${options[@]}"
        do
            case $opt in
                "Shell")
                    read -p "[Inject] imprint: " imprint_name
                    python3 ghost/ghost_in_shell.py $imprint_name
                    refresh
                    ;;

                "Telegram")
                    read -p "[Inject] imprint: " imprint_name
                    python3 ghost/ghost_in_telegram.py $imprint_name > /dev/null &
                    refresh
                    ;;

                "Back")
                    refresh
                    ;;
                *) echo "invalid option $REPLY";;
            esac
        done
    else case $SCRIPT in
        "Shell")
            read -p "[Inject] imprint: " imprint_name
            python3 ghost/ghost_in_shell.py $imprint_name
            refresh
            ;;

        "Telegram")
            read -p "[Inject] imprint: " imprint_name
            python3 ghost/ghost_in_telegram.py $imprint_name > /dev/null &
            refresh
            ;;

        "Back")
            refresh
            ;;

        *) echo "invalid option $REPLY";;
    esac

    fi

}
refresh(){
    python3 config/config.py set_env
    set -o allexport
    . ./config/config.env
    rm config/config.env
    clear
    if [ ! -e config/config.json ];
    then echo -e "##############|First-Timer? Start with the \033[38;5;33m[Config]\033[0m option|##############"
    fi
    python3 config/logo.py
    python3 config/config.py print_options
    menu
}
config(){
    options=("[Install] Required Libs" "[Config] Keys" "[Back]" )
    echo -e "\033[38;5;33mGhost Version Beta 3.4\033[0m"
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
                    refresh
                    ;;

                *) echo "invalid option $REPLY";;
            esac
        done
}

menu(){
options=("[Inject] an imprint" "[Train] an imprint" "[Ignore] default script" "[Wipe] an imprint" "[Config]" "[Exit]"  )
select opt in "${options[@]}"
do
    case $opt in
        "[Train] an imprint")
            FORGET=False
            choose_platform
            ;;

        "[Inject] an imprint")
            FORGET=True
            choose_platform
            ;;
        "[Ignore] default script")
            DEFAULT_SCRIPT="None"
            refresh
            ;;
        "[Wipe] an imprint")   
            read -p "Wipe imprint: " imprint_name
            rm IMPRINTS/${imprint_name}.ni
            refresh
            ;;
        "[Config]")
            config
            ;;
        "[Exit]")
            exit
            ;;
        *) echo "invalid option $REPLY";;


    esac
done
}

refresh
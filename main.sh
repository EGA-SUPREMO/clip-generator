getdescr() {
    #1 link del clip
    #2 optionel link de le fuente, sino usere el de le description
    TITLE=$(youtube-dl --skip-download --get-title --no-warnings --youtube-skip-dash-manifest $1)
    youtube-dl --skip-download --no-warnings --write-description --youtube-skip-dash-manifest -o "../Clips/desc" $1
    python3 main.py $TITLE $1 $2
}

getdescr "link de youtubu uwu"
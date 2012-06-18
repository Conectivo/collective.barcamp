#!/bin/sh
PRODUCTNAME='collective.barcamp'
I18NDOMAIN=$PRODUCTNAME

rm ./rebuild_i18n.log

i18ndude=i18ndude

[[ ! -f $i18ndude ]] && i18ndude=i18ndude
echo using $i18ndude

# List of languages
#LANGUAGES="th ko hi uk id mt fr lv gl vi hr af ru ca zh tr sk sr pt it es lt de mk be fi zh-tw sw is nl bg no da et sv ja pt-br cy hu ga cs sq ro pl"
LANGUAGES="es"

# Create locales folder structure for languages
#install -d locales
for lang in $LANGUAGES; do
    install -d ./$lang/LC_MESSAGES
    touch ./$lang/LC_MESSAGES/${PRODUCTNAME}.po
done

# Synchronise the .pot with the templates.
$i18ndude rebuild-pot --pot ./${PRODUCTNAME}.pot --create ${I18NDOMAIN} ../

# Synchronise the resulting .pot with the .po files
$i18ndude sync --pot ./${PRODUCTNAME}.pot ./*/LC_MESSAGES/${PRODUCTNAME}.po

WARNINGS=`find ../ -name "*pt" | xargs i18ndude find-untranslated | grep -e '^-WARN' | wc -l`
ERRORS=`find ../ -name "*pt" | xargs i18ndude find-untranslated | grep -e '^-ERROR' | wc -l`
FATAL=`find ../ -name "*pt"  | xargs i18ndude find-untranslated | grep -e '^-FATAL' | wc -l`

echo
echo "There are $WARNINGS warnings (possibly missing i18n markup)"
echo "There are $ERRORS errors (almost definitely missing i18n markup)"
echo "There are $FATAL fatal errors (template could not be parsed, eg. if it\'s not html)"
echo "For more details, run \'find . -name \"\*pt\" \| xargs i18ndude find-untranslated\' or" 
echo "Look the rebuild i18n log generate for this script called \'rebuild_i18n.log\' on locales dir" 

touch ./rebuild_i18n.log

find ../ -name "*pt" | xargs $i18ndude find-untranslated > ./rebuild_i18n.log

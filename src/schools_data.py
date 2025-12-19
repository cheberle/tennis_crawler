"""
NCAA Tennis Programs Database.

This is a curated list of NCAA D1 tennis programs with their athletics website URLs.
Data compiled from public sources including NCAA.com, conference websites, and athletic directories.
"""

from .models import Division

# NCAA Division 1 Men's Tennis Programs
# Approximately 250 programs
NCAA_D1_TENNIS_PROGRAMS = [
    # SEC (Southeastern Conference)
    {"school": "University of Alabama", "state": "Alabama", "athletics_url": "https://rolltide.com", "conference": "SEC"},
    {"school": "University of Arkansas", "state": "Arkansas", "athletics_url": "https://arkansasrazorbacks.com", "conference": "SEC"},
    {"school": "Auburn University", "state": "Alabama", "athletics_url": "https://auburntigers.com", "conference": "SEC"},
    {"school": "University of Florida", "state": "Florida", "athletics_url": "https://floridagators.com", "conference": "SEC"},
    {"school": "University of Georgia", "state": "Georgia", "athletics_url": "https://georgiadogs.com", "conference": "SEC"},
    {"school": "University of Kentucky", "state": "Kentucky", "athletics_url": "https://ukathletics.com", "conference": "SEC"},
    {"school": "LSU", "state": "Louisiana", "athletics_url": "https://lsusports.net", "conference": "SEC"},
    {"school": "Ole Miss", "state": "Mississippi", "athletics_url": "https://olemisssports.com", "conference": "SEC"},
    {"school": "Mississippi State", "state": "Mississippi", "athletics_url": "https://hailstate.com", "conference": "SEC"},
    {"school": "University of Missouri", "state": "Missouri", "athletics_url": "https://mutigers.com", "conference": "SEC"},
    {"school": "University of South Carolina", "state": "South Carolina", "athletics_url": "https://gamecocksonline.com", "conference": "SEC"},
    {"school": "University of Tennessee", "state": "Tennessee", "athletics_url": "https://utsports.com", "conference": "SEC"},
    {"school": "Texas A&M", "state": "Texas", "athletics_url": "https://12thman.com", "conference": "SEC"},
    {"school": "Vanderbilt University", "state": "Tennessee", "athletics_url": "https://vucommodores.com", "conference": "SEC"},

    # Big Ten
    {"school": "University of Illinois", "state": "Illinois", "athletics_url": "https://fightingillini.com", "conference": "Big Ten"},
    {"school": "Indiana University", "state": "Indiana", "athletics_url": "https://iuhoosiers.com", "conference": "Big Ten"},
    {"school": "University of Iowa", "state": "Iowa", "athletics_url": "https://hawkeyesports.com", "conference": "Big Ten"},
    {"school": "University of Michigan", "state": "Michigan", "athletics_url": "https://mgoblue.com", "conference": "Big Ten"},
    {"school": "Michigan State", "state": "Michigan", "athletics_url": "https://msuspartans.com", "conference": "Big Ten"},
    {"school": "University of Minnesota", "state": "Minnesota", "athletics_url": "https://gophersports.com", "conference": "Big Ten"},
    {"school": "University of Nebraska", "state": "Nebraska", "athletics_url": "https://huskers.com", "conference": "Big Ten"},
    {"school": "Northwestern University", "state": "Illinois", "athletics_url": "https://nusports.com", "conference": "Big Ten"},
    {"school": "Ohio State University", "state": "Ohio", "athletics_url": "https://ohiostatebuckeyes.com", "conference": "Big Ten"},
    {"school": "Penn State", "state": "Pennsylvania", "athletics_url": "https://gopsusports.com", "conference": "Big Ten"},
    {"school": "Purdue University", "state": "Indiana", "athletics_url": "https://purduesports.com", "conference": "Big Ten"},
    {"school": "University of Wisconsin", "state": "Wisconsin", "athletics_url": "https://uwbadgers.com", "conference": "Big Ten"},

    # ACC (Atlantic Coast Conference)
    {"school": "Boston College", "state": "Massachusetts", "athletics_url": "https://bceagles.com", "conference": "ACC"},
    {"school": "Clemson University", "state": "South Carolina", "athletics_url": "https://clemsontigers.com", "conference": "ACC"},
    {"school": "Duke University", "state": "North Carolina", "athletics_url": "https://goduke.com", "conference": "ACC"},
    {"school": "Florida State", "state": "Florida", "athletics_url": "https://seminoles.com", "conference": "ACC"},
    {"school": "Georgia Tech", "state": "Georgia", "athletics_url": "https://ramblinwreck.com", "conference": "ACC"},
    {"school": "University of Louisville", "state": "Kentucky", "athletics_url": "https://gocards.com", "conference": "ACC"},
    {"school": "University of Miami", "state": "Florida", "athletics_url": "https://hurricanesports.com", "conference": "ACC"},
    {"school": "University of North Carolina", "state": "North Carolina", "athletics_url": "https://goheels.com", "conference": "ACC"},
    {"school": "NC State", "state": "North Carolina", "athletics_url": "https://gopack.com", "conference": "ACC"},
    {"school": "University of Notre Dame", "state": "Indiana", "athletics_url": "https://und.com", "conference": "ACC"},
    {"school": "University of Pittsburgh", "state": "Pennsylvania", "athletics_url": "https://pittsburghpanthers.com", "conference": "ACC"},
    {"school": "Syracuse University", "state": "New York", "athletics_url": "https://cuse.com", "conference": "ACC"},
    {"school": "University of Virginia", "state": "Virginia", "athletics_url": "https://virginiasports.com", "conference": "ACC"},
    {"school": "Virginia Tech", "state": "Virginia", "athletics_url": "https://hokiesports.com", "conference": "ACC"},
    {"school": "Wake Forest", "state": "North Carolina", "athletics_url": "https://godeacs.com", "conference": "ACC"},

    # Big 12
    {"school": "Baylor University", "state": "Texas", "athletics_url": "https://baylorbears.com", "conference": "Big 12"},
    {"school": "BYU", "state": "Utah", "athletics_url": "https://byucougars.com", "conference": "Big 12"},
    {"school": "University of Kansas", "state": "Kansas", "athletics_url": "https://kuathletics.com", "conference": "Big 12"},
    {"school": "Kansas State", "state": "Kansas", "athletics_url": "https://kstatesports.com", "conference": "Big 12"},
    {"school": "Oklahoma State", "state": "Oklahoma", "athletics_url": "https://okstate.com", "conference": "Big 12"},
    {"school": "TCU", "state": "Texas", "athletics_url": "https://gofrogs.com", "conference": "Big 12"},
    {"school": "University of Texas", "state": "Texas", "athletics_url": "https://texassports.com", "conference": "Big 12"},
    {"school": "Texas Tech", "state": "Texas", "athletics_url": "https://texastech.com", "conference": "Big 12"},
    {"school": "West Virginia", "state": "West Virginia", "athletics_url": "https://wvusports.com", "conference": "Big 12"},

    # Pac-12 / Big Ten additions
    {"school": "University of Arizona", "state": "Arizona", "athletics_url": "https://arizonawildcats.com", "conference": "Big 12"},
    {"school": "Arizona State", "state": "Arizona", "athletics_url": "https://thesundevils.com", "conference": "Big 12"},
    {"school": "University of Colorado", "state": "Colorado", "athletics_url": "https://cubuffs.com", "conference": "Big 12"},
    {"school": "University of Utah", "state": "Utah", "athletics_url": "https://utahutes.com", "conference": "Big 12"},
    {"school": "UCLA", "state": "California", "athletics_url": "https://uclabruins.com", "conference": "Big Ten"},
    {"school": "USC", "state": "California", "athletics_url": "https://usctrojans.com", "conference": "Big Ten"},
    {"school": "University of Oregon", "state": "Oregon", "athletics_url": "https://goducks.com", "conference": "Big Ten"},
    {"school": "University of Washington", "state": "Washington", "athletics_url": "https://gohuskies.com", "conference": "Big Ten"},
    {"school": "Stanford University", "state": "California", "athletics_url": "https://gostanford.com", "conference": "ACC"},
    {"school": "University of California", "state": "California", "athletics_url": "https://calbears.com", "conference": "ACC"},

    # Ivy League
    {"school": "Brown University", "state": "Rhode Island", "athletics_url": "https://brownbears.com", "conference": "Ivy League"},
    {"school": "Columbia University", "state": "New York", "athletics_url": "https://gocolumbialions.com", "conference": "Ivy League"},
    {"school": "Cornell University", "state": "New York", "athletics_url": "https://cornellbigred.com", "conference": "Ivy League"},
    {"school": "Dartmouth College", "state": "New Hampshire", "athletics_url": "https://dartmouthsports.com", "conference": "Ivy League"},
    {"school": "Harvard University", "state": "Massachusetts", "athletics_url": "https://gocrimson.com", "conference": "Ivy League"},
    {"school": "University of Pennsylvania", "state": "Pennsylvania", "athletics_url": "https://pennathletics.com", "conference": "Ivy League"},
    {"school": "Princeton University", "state": "New Jersey", "athletics_url": "https://goprincetontigers.com", "conference": "Ivy League"},
    {"school": "Yale University", "state": "Connecticut", "athletics_url": "https://yalebulldogs.com", "conference": "Ivy League"},

    # American Athletic Conference
    {"school": "University of Central Florida", "state": "Florida", "athletics_url": "https://ucfknights.com", "conference": "Big 12"},
    {"school": "University of Cincinnati", "state": "Ohio", "athletics_url": "https://gobearcats.com", "conference": "Big 12"},
    {"school": "East Carolina", "state": "North Carolina", "athletics_url": "https://ecupirates.com", "conference": "American"},
    {"school": "University of Houston", "state": "Texas", "athletics_url": "https://uhcougars.com", "conference": "Big 12"},
    {"school": "University of Memphis", "state": "Tennessee", "athletics_url": "https://gotigersgo.com", "conference": "American"},
    {"school": "SMU", "state": "Texas", "athletics_url": "https://smumustangs.com", "conference": "ACC"},
    {"school": "University of South Florida", "state": "Florida", "athletics_url": "https://gousfbulls.com", "conference": "American"},
    {"school": "Temple University", "state": "Pennsylvania", "athletics_url": "https://owlsports.com", "conference": "American"},
    {"school": "Tulane University", "state": "Louisiana", "athletics_url": "https://tulanegreenwave.com", "conference": "American"},
    {"school": "Tulsa", "state": "Oklahoma", "athletics_url": "https://tulsahurricane.com", "conference": "American"},
    {"school": "Wichita State", "state": "Kansas", "athletics_url": "https://goshockers.com", "conference": "American"},

    # Mountain West
    {"school": "Air Force", "state": "Colorado", "athletics_url": "https://goairforcefalcons.com", "conference": "Mountain West"},
    {"school": "Boise State", "state": "Idaho", "athletics_url": "https://broncosports.com", "conference": "Mountain West"},
    {"school": "Fresno State", "state": "California", "athletics_url": "https://gobulldogs.com", "conference": "Mountain West"},
    {"school": "University of Nevada", "state": "Nevada", "athletics_url": "https://nevadawolfpack.com", "conference": "Mountain West"},
    {"school": "New Mexico", "state": "New Mexico", "athletics_url": "https://golobos.com", "conference": "Mountain West"},
    {"school": "San Diego State", "state": "California", "athletics_url": "https://goaztecs.com", "conference": "Mountain West"},
    {"school": "San Jose State", "state": "California", "athletics_url": "https://sjsuspartans.com", "conference": "Mountain West"},
    {"school": "UNLV", "state": "Nevada", "athletics_url": "https://unlvrebels.com", "conference": "Mountain West"},
    {"school": "Wyoming", "state": "Wyoming", "athletics_url": "https://gowyo.com", "conference": "Mountain West"},

    # Conference USA
    {"school": "Charlotte", "state": "North Carolina", "athletics_url": "https://charlotte49ers.com", "conference": "American"},
    {"school": "Florida Atlantic", "state": "Florida", "athletics_url": "https://fausports.com", "conference": "American"},
    {"school": "Florida International", "state": "Florida", "athletics_url": "https://fiusports.com", "conference": "Conference USA"},
    {"school": "Louisiana Tech", "state": "Louisiana", "athletics_url": "https://latechsports.com", "conference": "Conference USA"},
    {"school": "Marshall", "state": "West Virginia", "athletics_url": "https://herdzone.com", "conference": "Sun Belt"},
    {"school": "Middle Tennessee", "state": "Tennessee", "athletics_url": "https://goblueraiders.com", "conference": "Conference USA"},
    {"school": "North Texas", "state": "Texas", "athletics_url": "https://meangreensports.com", "conference": "American"},
    {"school": "Old Dominion", "state": "Virginia", "athletics_url": "https://odusports.com", "conference": "Sun Belt"},
    {"school": "Rice University", "state": "Texas", "athletics_url": "https://riceowls.com", "conference": "American"},
    {"school": "UAB", "state": "Alabama", "athletics_url": "https://uabsports.com", "conference": "American"},
    {"school": "UTEP", "state": "Texas", "athletics_url": "https://utepathletics.com", "conference": "Conference USA"},
    {"school": "UTSA", "state": "Texas", "athletics_url": "https://goutsa.com", "conference": "American"},
    {"school": "Western Kentucky", "state": "Kentucky", "athletics_url": "https://wkusports.com", "conference": "Conference USA"},

    # Sun Belt
    {"school": "Appalachian State", "state": "North Carolina", "athletics_url": "https://appstatesports.com", "conference": "Sun Belt"},
    {"school": "Coastal Carolina", "state": "South Carolina", "athletics_url": "https://goccusports.com", "conference": "Sun Belt"},
    {"school": "Georgia Southern", "state": "Georgia", "athletics_url": "https://gseagles.com", "conference": "Sun Belt"},
    {"school": "Georgia State", "state": "Georgia", "athletics_url": "https://georgiastatesports.com", "conference": "Sun Belt"},
    {"school": "Louisiana", "state": "Louisiana", "athletics_url": "https://ragincajuns.com", "conference": "Sun Belt"},
    {"school": "Louisiana-Monroe", "state": "Louisiana", "athletics_url": "https://ulmwarhawks.com", "conference": "Sun Belt"},
    {"school": "South Alabama", "state": "Alabama", "athletics_url": "https://usajaguars.com", "conference": "Sun Belt"},
    {"school": "Texas State", "state": "Texas", "athletics_url": "https://txstatebobcats.com", "conference": "Sun Belt"},
    {"school": "Troy", "state": "Alabama", "athletics_url": "https://troytrojans.com", "conference": "Sun Belt"},

    # West Coast Conference
    {"school": "Gonzaga", "state": "Washington", "athletics_url": "https://gozags.com", "conference": "WCC"},
    {"school": "Loyola Marymount", "state": "California", "athletics_url": "https://lmulions.com", "conference": "WCC"},
    {"school": "Pepperdine", "state": "California", "athletics_url": "https://pepperdinewaves.com", "conference": "WCC"},
    {"school": "Saint Mary's", "state": "California", "athletics_url": "https://smcgaels.com", "conference": "WCC"},
    {"school": "San Diego", "state": "California", "athletics_url": "https://usdtoreros.com", "conference": "WCC"},
    {"school": "San Francisco", "state": "California", "athletics_url": "https://usfdons.com", "conference": "WCC"},
    {"school": "Santa Clara", "state": "California", "athletics_url": "https://santaclarabroncos.com", "conference": "WCC"},

    # Big East
    {"school": "Butler", "state": "Indiana", "athletics_url": "https://butlersports.com", "conference": "Big East"},
    {"school": "Creighton", "state": "Nebraska", "athletics_url": "https://gocreighton.com", "conference": "Big East"},
    {"school": "DePaul", "state": "Illinois", "athletics_url": "https://depaulbluedemons.com", "conference": "Big East"},
    {"school": "Georgetown", "state": "Washington D.C.", "athletics_url": "https://guhoyas.com", "conference": "Big East"},
    {"school": "Marquette", "state": "Wisconsin", "athletics_url": "https://gomarquette.com", "conference": "Big East"},
    {"school": "Providence", "state": "Rhode Island", "athletics_url": "https://friars.com", "conference": "Big East"},
    {"school": "St. John's", "state": "New York", "athletics_url": "https://redstormsports.com", "conference": "Big East"},
    {"school": "Seton Hall", "state": "New Jersey", "athletics_url": "https://shupirates.com", "conference": "Big East"},
    {"school": "Villanova", "state": "Pennsylvania", "athletics_url": "https://villanova.com", "conference": "Big East"},
    {"school": "Xavier", "state": "Ohio", "athletics_url": "https://goxavier.com", "conference": "Big East"},

    # Atlantic 10
    {"school": "Davidson", "state": "North Carolina", "athletics_url": "https://davidsonwildcats.com", "conference": "Atlantic 10"},
    {"school": "Dayton", "state": "Ohio", "athletics_url": "https://daytonflyers.com", "conference": "Atlantic 10"},
    {"school": "Duquesne", "state": "Pennsylvania", "athletics_url": "https://goduquesne.com", "conference": "Atlantic 10"},
    {"school": "Fordham", "state": "New York", "athletics_url": "https://fordhamsports.com", "conference": "Atlantic 10"},
    {"school": "George Mason", "state": "Virginia", "athletics_url": "https://gomason.com", "conference": "Atlantic 10"},
    {"school": "George Washington", "state": "Washington D.C.", "athletics_url": "https://gwsports.com", "conference": "Atlantic 10"},
    {"school": "La Salle", "state": "Pennsylvania", "athletics_url": "https://goexplorers.com", "conference": "Atlantic 10"},
    {"school": "UMass", "state": "Massachusetts", "athletics_url": "https://umassathletics.com", "conference": "Atlantic 10"},
    {"school": "Rhode Island", "state": "Rhode Island", "athletics_url": "https://gorhody.com", "conference": "Atlantic 10"},
    {"school": "Richmond", "state": "Virginia", "athletics_url": "https://richmondspiders.com", "conference": "Atlantic 10"},
    {"school": "Saint Louis", "state": "Missouri", "athletics_url": "https://slubillikens.com", "conference": "Atlantic 10"},
    {"school": "VCU", "state": "Virginia", "athletics_url": "https://vcuathletics.com", "conference": "Atlantic 10"},

    # Colonial Athletic Association
    {"school": "College of Charleston", "state": "South Carolina", "athletics_url": "https://cofcsports.com", "conference": "CAA"},
    {"school": "Delaware", "state": "Delaware", "athletics_url": "https://bluehens.com", "conference": "CAA"},
    {"school": "Drexel", "state": "Pennsylvania", "athletics_url": "https://drexeldragons.com", "conference": "CAA"},
    {"school": "Elon", "state": "North Carolina", "athletics_url": "https://elonphoenix.com", "conference": "CAA"},
    {"school": "Hofstra", "state": "New York", "athletics_url": "https://gohofstra.com", "conference": "CAA"},
    {"school": "James Madison", "state": "Virginia", "athletics_url": "https://jmusports.com", "conference": "Sun Belt"},
    {"school": "Northeastern", "state": "Massachusetts", "athletics_url": "https://gonu.com", "conference": "CAA"},
    {"school": "Towson", "state": "Maryland", "athletics_url": "https://towsontigers.com", "conference": "CAA"},
    {"school": "UNC Wilmington", "state": "North Carolina", "athletics_url": "https://uncwsports.com", "conference": "CAA"},
    {"school": "William & Mary", "state": "Virginia", "athletics_url": "https://tribeathletics.com", "conference": "CAA"},

    # Other conferences
    {"school": "Army", "state": "New York", "athletics_url": "https://goarmywestpoint.com", "conference": "Patriot League"},
    {"school": "Navy", "state": "Maryland", "athletics_url": "https://navysports.com", "conference": "Patriot League"},
    {"school": "Bucknell", "state": "Pennsylvania", "athletics_url": "https://bucknellbison.com", "conference": "Patriot League"},
    {"school": "Colgate", "state": "New York", "athletics_url": "https://gocolgateraiders.com", "conference": "Patriot League"},
    {"school": "Holy Cross", "state": "Massachusetts", "athletics_url": "https://goholycross.com", "conference": "Patriot League"},
    {"school": "Lafayette", "state": "Pennsylvania", "athletics_url": "https://goleopards.com", "conference": "Patriot League"},
    {"school": "Lehigh", "state": "Pennsylvania", "athletics_url": "https://lehighsports.com", "conference": "Patriot League"},
    {"school": "Loyola Maryland", "state": "Maryland", "athletics_url": "https://loyolagreyhounds.com", "conference": "Patriot League"},

    # Southern Conference
    {"school": "The Citadel", "state": "South Carolina", "athletics_url": "https://citadelsports.com", "conference": "Southern"},
    {"school": "ETSU", "state": "Tennessee", "athletics_url": "https://etsubucs.com", "conference": "Southern"},
    {"school": "Furman", "state": "South Carolina", "athletics_url": "https://furmanpaladins.com", "conference": "Southern"},
    {"school": "Mercer", "state": "Georgia", "athletics_url": "https://mercerbears.com", "conference": "Southern"},
    {"school": "Samford", "state": "Alabama", "athletics_url": "https://samfordsports.com", "conference": "Southern"},
    {"school": "UNC Greensboro", "state": "North Carolina", "athletics_url": "https://uncgspartans.com", "conference": "Southern"},
    {"school": "Western Carolina", "state": "North Carolina", "athletics_url": "https://catamountsports.com", "conference": "Southern"},
    {"school": "Wofford", "state": "South Carolina", "athletics_url": "https://woffordterriers.com", "conference": "Southern"},

    # Missouri Valley
    {"school": "Bradley", "state": "Illinois", "athletics_url": "https://bradleybraves.com", "conference": "Missouri Valley"},
    {"school": "Drake", "state": "Iowa", "athletics_url": "https://godrakebulldogs.com", "conference": "Missouri Valley"},
    {"school": "Evansville", "state": "Indiana", "athletics_url": "https://gopurpleaces.com", "conference": "Missouri Valley"},
    {"school": "Illinois State", "state": "Illinois", "athletics_url": "https://goredbirds.com", "conference": "Missouri Valley"},
    {"school": "Indiana State", "state": "Indiana", "athletics_url": "https://gosycamores.com", "conference": "Missouri Valley"},
    {"school": "Missouri State", "state": "Missouri", "athletics_url": "https://missouristatebears.com", "conference": "Missouri Valley"},
    {"school": "Northern Iowa", "state": "Iowa", "athletics_url": "https://unipanthers.com", "conference": "Missouri Valley"},
    {"school": "Southern Illinois", "state": "Illinois", "athletics_url": "https://siusalukis.com", "conference": "Missouri Valley"},
    {"school": "Valparaiso", "state": "Indiana", "athletics_url": "https://valpoathletics.com", "conference": "Missouri Valley"},

    # Ohio Valley
    {"school": "Austin Peay", "state": "Tennessee", "athletics_url": "https://letsgopeay.com", "conference": "ASUN"},
    {"school": "Belmont", "state": "Tennessee", "athletics_url": "https://belmontbruins.com", "conference": "Missouri Valley"},
    {"school": "Eastern Kentucky", "state": "Kentucky", "athletics_url": "https://ekusports.com", "conference": "ASUN"},
    {"school": "Jacksonville State", "state": "Alabama", "athletics_url": "https://jsugamecocksports.com", "conference": "Conference USA"},
    {"school": "Morehead State", "state": "Kentucky", "athletics_url": "https://msueagles.com", "conference": "Ohio Valley"},
    {"school": "Murray State", "state": "Kentucky", "athletics_url": "https://goracers.com", "conference": "Missouri Valley"},
    {"school": "Southeast Missouri", "state": "Missouri", "athletics_url": "https://gosoutheast.com", "conference": "Ohio Valley"},
    {"school": "Tennessee State", "state": "Tennessee", "athletics_url": "https://tsutigers.com", "conference": "Ohio Valley"},
    {"school": "Tennessee Tech", "state": "Tennessee", "athletics_url": "https://ttusports.com", "conference": "Ohio Valley"},
    {"school": "UT Martin", "state": "Tennessee", "athletics_url": "https://utmsports.com", "conference": "Ohio Valley"},

    # Big South / ASUN
    {"school": "Campbell", "state": "North Carolina", "athletics_url": "https://gocamels.com", "conference": "CAA"},
    {"school": "Charleston Southern", "state": "South Carolina", "athletics_url": "https://csusports.com", "conference": "Big South"},
    {"school": "Gardner-Webb", "state": "North Carolina", "athletics_url": "https://gwusports.com", "conference": "Big South"},
    {"school": "High Point", "state": "North Carolina", "athletics_url": "https://highpointpanthers.com", "conference": "Big South"},
    {"school": "Liberty", "state": "Virginia", "athletics_url": "https://libertyflames.com", "conference": "Conference USA"},
    {"school": "Longwood", "state": "Virginia", "athletics_url": "https://longwoodlancers.com", "conference": "Big South"},
    {"school": "North Carolina A&T", "state": "North Carolina", "athletics_url": "https://ncataggies.com", "conference": "CAA"},
    {"school": "Presbyterian", "state": "South Carolina", "athletics_url": "https://gobluehose.com", "conference": "Big South"},
    {"school": "Radford", "state": "Virginia", "athletics_url": "https://radfordathletics.com", "conference": "Big South"},
    {"school": "UNC Asheville", "state": "North Carolina", "athletics_url": "https://uncabulldogs.com", "conference": "Big South"},
    {"school": "USC Upstate", "state": "South Carolina", "athletics_url": "https://upstatespartans.com", "conference": "Big South"},
    {"school": "Winthrop", "state": "South Carolina", "athletics_url": "https://winthropeagles.com", "conference": "Big South"},

    # Horizon League
    {"school": "Cleveland State", "state": "Ohio", "athletics_url": "https://csuvikings.com", "conference": "Horizon"},
    {"school": "Detroit Mercy", "state": "Michigan", "athletics_url": "https://detroittitans.com", "conference": "Horizon"},
    {"school": "Green Bay", "state": "Wisconsin", "athletics_url": "https://greenbayphoenix.com", "conference": "Horizon"},
    {"school": "IUPUI", "state": "Indiana", "athletics_url": "https://iupuijags.com", "conference": "Horizon"},
    {"school": "Milwaukee", "state": "Wisconsin", "athletics_url": "https://mkepanthers.com", "conference": "Horizon"},
    {"school": "Northern Kentucky", "state": "Kentucky", "athletics_url": "https://nkunorse.com", "conference": "Horizon"},
    {"school": "Oakland", "state": "Michigan", "athletics_url": "https://goldengrizzlies.com", "conference": "Horizon"},
    {"school": "Wright State", "state": "Ohio", "athletics_url": "https://wsuraiders.com", "conference": "Horizon"},
    {"school": "Youngstown State", "state": "Ohio", "athletics_url": "https://ysusports.com", "conference": "Horizon"},

    # MEAC / SWAC / Independents
    {"school": "Alcorn State", "state": "Mississippi", "athletics_url": "https://alcornsports.com", "conference": "SWAC"},
    {"school": "Alabama State", "state": "Alabama", "athletics_url": "https://bamastatesports.com", "conference": "SWAC"},
    {"school": "Bethune-Cookman", "state": "Florida", "athletics_url": "https://bcuathletics.com", "conference": "SWAC"},
    {"school": "Coppin State", "state": "Maryland", "athletics_url": "https://coppinstatesports.com", "conference": "MEAC"},
    {"school": "Delaware State", "state": "Delaware", "athletics_url": "https://dsuhornets.com", "conference": "MEAC"},
    {"school": "Florida A&M", "state": "Florida", "athletics_url": "https://famuathletics.com", "conference": "SWAC"},
    {"school": "Grambling State", "state": "Louisiana", "athletics_url": "https://gikigyou.com", "conference": "SWAC"},
    {"school": "Hampton", "state": "Virginia", "athletics_url": "https://hamptonpirates.com", "conference": "CAA"},
    {"school": "Howard", "state": "Washington D.C.", "athletics_url": "https://hubison.com", "conference": "CAA"},
    {"school": "Jackson State", "state": "Mississippi", "athletics_url": "https://gojsutigers.com", "conference": "SWAC"},
    {"school": "Maryland Eastern Shore", "state": "Maryland", "athletics_url": "https://umeshawks.com", "conference": "MEAC"},
    {"school": "Mississippi Valley State", "state": "Mississippi", "athletics_url": "https://mvsusports.com", "conference": "SWAC"},
    {"school": "Morgan State", "state": "Maryland", "athletics_url": "https://mabornsports.com", "conference": "MEAC"},
    {"school": "Norfolk State", "state": "Virginia", "athletics_url": "https://nsuspartans.com", "conference": "MEAC"},
    {"school": "North Carolina Central", "state": "North Carolina", "athletics_url": "https://nccueaglepride.com", "conference": "MEAC"},
    {"school": "Prairie View A&M", "state": "Texas", "athletics_url": "https://pvpanthers.com", "conference": "SWAC"},
    {"school": "Savannah State", "state": "Georgia", "athletics_url": "https://ssuathletics.com", "conference": "Independent"},
    {"school": "South Carolina State", "state": "South Carolina", "athletics_url": "https://scsubulldogs.com", "conference": "MEAC"},
    {"school": "Southern University", "state": "Louisiana", "athletics_url": "https://gojagsports.com", "conference": "SWAC"},
    {"school": "Texas Southern", "state": "Texas", "athletics_url": "https://taboronline.com", "conference": "SWAC"},

    # Additional schools
    {"school": "Abilene Christian", "state": "Texas", "athletics_url": "https://acusports.com", "conference": "WAC"},
    {"school": "Central Arkansas", "state": "Arkansas", "athletics_url": "https://ucasports.com", "conference": "ASUN"},
    {"school": "Incarnate Word", "state": "Texas", "athletics_url": "https://uiwcardinals.com", "conference": "Southland"},
    {"school": "Lamar", "state": "Texas", "athletics_url": "https://lamarcardinals.com", "conference": "Southland"},
    {"school": "McNeese", "state": "Louisiana", "athletics_url": "https://mcneesesports.com", "conference": "Southland"},
    {"school": "New Orleans", "state": "Louisiana", "athletics_url": "https://unoprivateers.com", "conference": "Southland"},
    {"school": "Nicholls State", "state": "Louisiana", "athletics_url": "https://geauxcolonels.com", "conference": "Southland"},
    {"school": "Northwestern State", "state": "Louisiana", "athletics_url": "https://nsudemons.com", "conference": "Southland"},
    {"school": "Sam Houston", "state": "Texas", "athletics_url": "https://gobearkats.com", "conference": "Conference USA"},
    {"school": "SE Louisiana", "state": "Louisiana", "athletics_url": "https://lionsports.net", "conference": "Southland"},
    {"school": "Stephen F. Austin", "state": "Texas", "athletics_url": "https://sfajacks.com", "conference": "WAC"},
    {"school": "Texas A&M-Corpus Christi", "state": "Texas", "athletics_url": "https://goislanders.com", "conference": "Southland"},
]


def get_all_schools():
    """Get all schools with Division enum."""
    schools = []
    for s in NCAA_D1_TENNIS_PROGRAMS:
        schools.append({
            **s,
            "division": Division.NCAA_D1,
        })
    return schools
